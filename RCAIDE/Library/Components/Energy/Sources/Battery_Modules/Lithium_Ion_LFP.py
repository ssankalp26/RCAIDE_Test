# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Lithium_Ion_LFP.py
# 
# 
# Created: Nov 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core          import Units,Data
from .Generic_Battery_Module import  Generic_Battery_Module
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Lithium_Ion_LFP  import * 

# package imports 
import numpy as np  
import os
from scipy.interpolate  import NearestNDInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_LFP
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Batteries 
class Lithium_Ion_LFP(Generic_Battery_Module):
    """
    A class for modeling lithium iron phosphate (LFP) battery cells in aircraft energy systems.
    Inherits from the Generic_Battery_Module class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'lithium_ion_lfp'
    
    power_split_ratio : float
        Power distribution ratio, defaults to None
    
    number_of_cells : int
        Number of cells in the module, defaults to 1
    
    maximum_energy : float
        Maximum energy capacity, defaults to 0.0
    
    maximum_power : float
        Maximum power output, defaults to 0.0
    
    maximum_voltage : float
        Maximum voltage output, defaults to 0.0
    
    cell : Data
        Collection of cell-specific properties
        - chemistry : str
            Battery chemistry type, set to 'LiFePO4'
        - diameter : float
            Cell diameter in meters, defaults to 0.0185
        - height : float
            Cell height in meters, defaults to 0.0653
        - mass : float
            Cell mass in kg, defaults to 0.03
        - surface_area : float
            Cell surface area in m^2, calculated from dimensions
        - volume : float
            Cell volume in m^3, calculated from dimensions
        - density : float
            Cell density in kg/m^3, calculated from mass and volume
        - electrode_area : float
            Area of electrode in m^2, defaults to 0.0342
        - maximum_voltage : float
            Maximum cell voltage in V, defaults to 3.6
        - nominal_capacity : float
            Nominal capacity in Amp-hrs, defaults to 2.6
        - nominal_voltage : float
            Nominal voltage in V, defaults to 3.6
        - watt_hour_rating : float
            Energy capacity in Watt-hours, calculated
        - specific_energy : float
            Energy per unit mass in J/kg, calculated
        - specific_power : float
            Power per unit mass in W/kg, calculated
        - resistance : float
            Internal resistance in Ohms, defaults to 0.022
        - specific_heat_capacity : float
            Specific heat in J/kgK, defaults to 1115
        - radial_thermal_conductivity : float
            Thermal conductivity in radial direction in J/kgK, defaults to 0.475
        - axial_thermal_conductivity : float
            Thermal conductivity in axial direction in J/kgK, defaults to 37.6

    Methods
    -------
    energy_calc(state, bus, coolant_lines, t_idx, delta_t)
        Computes the state of the LFP battery cell
    
    reuse_stored_data(state, bus, coolant_lines, t_idx, delta_t, stored_results_flag, stored_battery_tag)
        Reuses previously stored battery data
    
    update_battery_age(segment, battery_conditions, increment_battery_age_by_one_day)
        Updates the battery age based on usage conditions

    Notes
    -----
    The Lithium_Ion_LFP class models 26650 A123 lithium iron phosphate cells,
    providing detailed thermal and electrical characteristics. These cells are known
    for their stability, safety, and good cycle life.
    
    **Definitions**
    'LFP'
        Lithium Iron Phosphate (LiFePO4) - a type of lithium-ion battery chemistry
    'Thermal Conductivity'
        Measure of the material's ability to conduct heat
    'Specific Heat Capacity'
        Amount of heat needed to raise temperature by one degree per unit mass
    
    References
    ----------
    .. [1] LithiumWerks, "A123 26650 Cell Datasheet." A123 Batteries, Jan 2019, URL: https://a123batteries.com/product_images/uploaded_images/26650.pdf.
    .. [2] Arora, Shashank, and Ajay Kapoor. “Experimental Study of Heat Generation 
        Rate during Discharge of LiFePO4 Pouch Cells of Different Nominal Capacities
        and Thickness.” Batteries 5, no. 4 (November 11, 2019): 70. 
        https://doi.org/10.3390/batteries5040070.   
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None

        Source:
         # Cell Information 
           Datasheet: https://a123batteries.com/product_images/uploaded_images/26650.pdf
            
            Arora, Shashank, and Ajay Kapoor. “Experimental Study of Heat Generation 
            Rate during Discharge of LiFePO4 Pouch Cells of Different Nominal Capacities
            and Thickness.” Batteries 5, no. 4 (November 11, 2019): 70. 
            https://doi.org/10.3390/batteries5040070.        
        """
        # ----------------------------------------------------------------------------------------------------------------------
        #  Module Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.tag                                               = 'lithium_ion_lfp' 
        self.power_split_ratio                                 = None
        self.number_of_cells                                   = 1
        self.maximum_energy                                    = 0.0
        self.maximum_power                                     = 0.0
        self.maximum_voltage                                   = 0.0       
        
        # ----------------------------------------------------------------------------------------------------------------------
        #  Cell Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.cell.chemistry                   = 'LiFePO4'
        self.cell.diameter                    = 0.0185                                                    # [m]
        self.cell.height                      = 0.0653                                                    # [m]
        self.cell.mass                        = 0.03  * Units.kg                                          # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) \
                                                + (0.5*np.pi*self.cell.diameter**2)                       # [m^2]

        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height        # [m^3] 
        self.cell.density                     = self.cell.mass/self.cell.volume                           # [kg/m^3]
        self.cell.electrode_area              = 0.0342                                                    # [m^2]  # estimated 
                                                        
        self.cell.maximum_voltage             = 3.6                                                       # [V]
        self.cell.nominal_capacity            = 2.6                                                       # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                       # [V]
         
        self.cell.watt_hour_rating            = self.cell.nominal_capacity  * self.cell.nominal_voltage   # [Watt-hours]      
        self.cell.specific_energy             = self.cell.watt_hour_rating*Units.Wh/self.cell.mass        # [J/kg]
        self.cell.specific_power              = self.cell.specific_energy/self.cell.nominal_capacity      # [W/kg]   
        self.cell.resistance                  = 0.022                                                     # [Ohms]
                                                                                                            
        self.cell.specific_heat_capacity      = 1115                                                      # [J/kgK]                                                     
        self.cell.radial_thermal_conductivity = 0.475                                                     # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 37.6                                                      # [J/kgK]  

        battery_raw_data                      = load_battery_results()                                                   
        self.cell.discharge_performance_map   = create_discharge_performance_map(battery_raw_data)

        return                                     

    def energy_calc(self,state,bus,coolant_lines, t_idx, delta_t): 
        """Computes the state of the LFP battery cell.
           
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self               : battery        [unitless]
            state              : temperature    [K]
            bus                : pressure       [Pa]
            discharge (boolean): discharge flag [unitless]
            
        Returns: 
            None
        """      
        stored_results_flag, stored_battery_tag =  compute_lfp_cell_performance(self,state,bus,coolant_lines, t_idx,delta_t) 
                        
        return stored_results_flag, stored_battery_tag
    
    def reuse_stored_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag):
        reuse_stored_lfp_cell_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag)
        return    
      
    def update_battery_age(self,segment, battery_conditions,increment_battery_age_by_one_day): 
        update_lfp_cell_age(self,segment, battery_conditions,increment_battery_age_by_one_day)
        return 
    
def create_discharge_performance_map(raw_data):
    """
    Creates an interpolation surface for battery discharge performance based on raw data.

    Parameters
    ----------
    raw_data : dict
        Dictionary containing battery discharge performance data
        - c_rate_key : dict
            Nested dictionary for each C-rate
            - temp_key : dict
                Nested dictionary for each temperature
                - discharge : list
                    Discharge capacity values
                - voltage : list
                    Voltage values

    Returns
    -------
    battery_data : NearestNDInterpolator
        Interpolator object that can predict voltage based on:
        - C-rate
        - Temperature
        - Discharge capacity

    Notes
    -----
    The function processes raw battery data to create a 3D interpolation surface
    that relates voltage to C-rate, temperature, and discharge capacity. This allows
    for prediction of battery voltage under various operating conditions.

    References
    ----------
    .. [1] Lin, Xinfan, Hector Perez, Jason B. Siegel, and Anna G. Stefanopoulou.
           "An Electro-Thermal Model for the A123 26650 LiFePO4 Battery." 
           University of Michigan. Accessed November 11, 2024. 
           https://hdl.handle.net/2027.42/97341.
    """
    
    # Prepare lists for the data needed for interpolation
    c_rates = []
    temperatures = []
    discharge_capacities = []
    voltages = []

    # Iterate through the data structure to populate the lists
    for c_rate_key, temp_data in raw_data.items():
        c_rate = float(c_rate_key)  # Convert C-rate to float

        for temp_key, data in temp_data.items():
            initial_temp = int(temp_key.split()[-1])  # Extract temperature as an integer

            # Extend lists with the discharge, voltage, and other data
            discharge_capacities.extend(data['discharge'])
            voltages.extend(data['voltage'])
            c_rates.extend([c_rate] * len(data['discharge']))
            temperatures.extend([initial_temp] * len(data['discharge']))

    # Convert lists to numpy arrays
    points = np.array([c_rates, temperatures, discharge_capacities]).T
    values = np.array(voltages)

    # Create the interpolant
    battery_data = NearestNDInterpolator(points, values) # Can be replaced by a Linear Interpolator for a better fit but computation time increases by 30 times. 

    return battery_data  

def load_battery_results(): 
    """
    Loads experimental raw data for LFP battery cells from a resource file.

    Parameters
    ----------
    None

    Returns
    -------
    raw_data : dict
        Dictionary containing battery discharge performance data
        - c_rate_key : dict
            Nested dictionary for each C-rate
            - temp_key : dict
                Nested dictionary for each temperature
                - discharge : list
                    Discharge capacity values
                - voltage : list
                    Voltage values

    Notes
    -----
    The function loads pre-recorded experimental data for LFP battery cells from
    a resource file named 'lfp_raw_data.res'. This data is used to create
    discharge performance maps for battery simulation.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, 'lfp_raw_data.res')

    # Load the raw_data using RCAIDE.load()
    raw_data = RCAIDE.load(full_path)

    return raw_data