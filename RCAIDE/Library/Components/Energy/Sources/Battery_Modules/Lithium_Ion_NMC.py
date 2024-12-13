# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Lithium_Ion_LFP.py
# 
# 
# Created:  Mar 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                                            import Units , Data
from .Generic_Battery_Module                                          import Generic_Battery_Module   
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Lithium_Ion_NMC  import *
# package imports 
import numpy as np
import os 
from scipy.interpolate  import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_NMC
# ---------------------------------------------------------------------------------------------------------------------- 
class Lithium_Ion_NMC(Generic_Battery_Module):
    """
    A class for modeling lithium nickel manganese cobalt oxide (NMC) battery cells in aircraft energy systems.
    Inherits from the Generic_Battery_Module class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'lithium_ion_nmc'
    
    maximum_energy : float
        Maximum energy capacity, defaults to 0.0
    
    maximum_power : float
        Maximum power output, defaults to 0.0
    
    maximum_voltage : float
        Maximum voltage output, defaults to 0.0
    
    cell : Data
        Collection of cell-specific properties
        - chemistry : str
            Battery chemistry type, set to 'LiNiMnCoO2'
        - diameter : float
            Cell diameter in meters, defaults to 0.0185
        - height : float
            Cell height in meters, defaults to 0.0653
        - mass : float
            Cell mass in kg, defaults to 0.048
        - surface_area : float
            Cell surface area in m^2, calculated from dimensions
        - volume : float
            Cell volume in m^3, calculated from dimensions
        - density : float
            Cell density in kg/m^3, calculated from mass and volume
        - electrode_area : float
            Area of electrode in m^2, defaults to 0.0342
        - maximum_voltage : float
            Maximum cell voltage in V, defaults to 4.2
        - nominal_capacity : float
            Nominal capacity in Amp-hrs, defaults to 3.8
        - nominal_voltage : float
            Nominal voltage in V, defaults to 3.6
        - charging_voltage : float
            Charging voltage in V, defaults to nominal_voltage
        - specific_energy : float
            Energy per unit mass in J/kg, calculated
        - specific_power : float
            Power per unit mass in W/kg, calculated
        - resistance : float
            Internal resistance in Ohms, defaults to 0.025
        - specific_heat_capacity : float
            Specific heat in J/kgK, defaults to 1108
        - radial_thermal_conductivity : float
            Thermal conductivity in radial direction in J/kgK, defaults to 0.4
        - axial_thermal_conductivity : float
            Thermal conductivity in axial direction in J/kgK, defaults to 32.2

    Methods
    -------
    energy_calc(state, bus, coolant_lines, t_idx, delta_t)
        Computes the state of the NMC battery cell
    
    reuse_stored_data(state, bus, coolant_lines, t_idx, delta_t, stored_results_flag, stored_battery_tag)
        Reuses previously stored battery data
    
    update_battery_age(segment, battery_conditions, increment_battery_age_by_one_day)
        Updates the battery age based on usage conditions

    Notes
    -----
    The Lithium_Ion_NMC class models 18650 lithium nickel manganese cobalt oxide cells,
    providing detailed thermal and electrical characteristics. These cells offer a good
    balance of energy density, power capability, and cycle life.
    
    **Definitions**
    'NMC'
        Lithium Nickel Manganese Cobalt Oxide (LiNiMnCoO2) - a type of lithium-ion battery chemistry
    'Thermal Conductivity'
        Measure of the material's ability to conduct heat
    'Specific Heat Capacity'
        Amount of heat needed to raise temperature by one degree per unit mass
    
    References
    ----------
    ..  [1] Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical 
            lithium ion battery during discharge cycle." Energy Conversion and Management
            52.8-9 (2011): 2973-2981.
            
        [2] Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
        [3] Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
        [4] Muenzel, Valentin, et al. "A comparative testing study of commercial
            18650-format lithium-ion battery cells." Journal of The Electrochemical
            Society 162.8 (2015): A1592.
    """
    def __defaults__(self):   
        """This sets the default values.
    
        Assumptions:
            Convective Thermal Conductivity Coefficient corresponds to forced
            air cooling in 35 m/s air 
        
        Source: 
            convective  heat transfer coefficient, h 
            Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical 
            lithium ion battery during discharge cycle." Energy Conversion and Management
            52.8-9 (2011): 2973-2981.
            
            thermal conductivity, k 
            Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
            specific heat capacity, Cp
            (axial and radial)
            Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
            System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
            (2019): 6077-6107.
            
            # Electrode Area
            Muenzel, Valentin, et al. "A comparative testing study of commercial
            18650-format lithium-ion battery cells." Journal of The Electrochemical
            Society 162.8 (2015): A1592.
        
        """
        # ----------------------------------------------------------------------------------------------------------------------
        #  Module Level Properties
        # ----------------------------------------------------------------------------------------------------------------------
        
        self.tag                                         = 'lithium_ion_nmc'
        self.maximum_energy                              = 0.0
        self.maximum_power                               = 0.0
        self.maximum_voltage                             = 0.0  
         
        # ----------------------------------------------------------------------------------------------------------------------
        #  Cell Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.cell.chemistry                   = 'LiNiMnCoO2'
        self.cell.diameter                    = 0.0185                                                                            # [m]
        self.cell.height                      = 0.0653                                                                            # [m]
        self.cell.mass                        = 0.048 * Units.kg                                                                  # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) + (0.5*np.pi*self.cell.diameter**2)  # [m^2]
        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height 
        self.cell.density                     = self.cell.mass/self.cell.volume                                                  # [kg/m^3]  
        self.cell.electrode_area              = 0.0342                                                                           # [m^2] 
                                                                                                                           
        self.cell.maximum_voltage             = 4.2                                                                              # [V]
        self.cell.nominal_capacity            = 3.8                                                                             # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                                              # [V] 
        self.cell.charging_voltage            = self.cell.nominal_voltage                                                        # [V] 
        
        self.cell.watt_hour_rating            = self.cell.nominal_capacity  * self.cell.nominal_voltage                          # [Watt-hours]      
        self.cell.specific_energy             = self.cell.watt_hour_rating*Units.Wh/self.cell.mass                               # [J/kg]
        self.cell.specific_power              = self.cell.specific_energy/self.cell.nominal_capacity                             # [W/kg]   
        self.cell.resistance                  = 0.025                                                                            # [Ohms] 
                                                            
        self.cell.specific_heat_capacity      = 1108                                                                             # [J/kgK]    
        self.cell.radial_thermal_conductivity = 0.4                                                                              # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 32.2                                                                             # [J/kgK] # estimated
    
                                              
        battery_raw_data                      = load_battery_results()                                                   
        self.cell.discharge_performance_map   = create_discharge_performance_map(battery_raw_data)  

        return  
    
    def energy_calc(self,state,bus,coolant_lines, t_idx, delta_t): 
        """Computes the state of the NMC battery cell.
           
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
        stored_results_flag, stored_battery_tag =  compute_nmc_cell_performance(self,state,bus,coolant_lines, t_idx,delta_t) 
        
        return stored_results_flag, stored_battery_tag
    
    def reuse_stored_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag):
        reuse_stored_nmc_cell_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag)
        return 
    
    def update_battery_age(self,segment,battery_conditions,increment_battery_age_by_one_day = False):  
        """ This is an aging model for 18650 lithium-nickel-manganese-cobalt-oxide batteries.   
        
        Assumptions:
            None
        
        Source:
            None
    
        Args:
            self                                      : battery            [unitless] 
            battery_conditions                        : state of battery   [unitless]
            increment_battery_age_by_one_day (boolean): day increment flag [unitless]  
            
        Returns: 
            None
        """        
        update_nmc_cell_age(self,segment,battery_conditions,increment_battery_age_by_one_day) 
        
        return  

def create_discharge_performance_map(raw_data):
    """
    Creates discharge and charge response surface for a LiNiMnCoO2 battery cell.

    Parameters
    ----------
    raw_data : Data
        Data object containing battery discharge curves
        - Voltage : array
            4D array of voltage data [current, operating temperature, state_of_charge, value]
        - Temperature : array
            4D array of temperature data [current, operating temperature, state_of_charge, value]

    Returns
    -------
    battery_data : Data
        Response surface of battery properties
        - Voltage : RegularGridInterpolator
            Interpolator for voltage based on current, temperature, and state of charge
        - Temperature : RegularGridInterpolator
            Interpolator for temperature based on current, temperature, and state of charge

    Notes
    -----
    The function processes raw battery data to create interpolation surfaces for both
    voltage and temperature characteristics. It uses regular grid interpolation to
    create a model that can predict battery behavior under various operating conditions.
    """   
    # Process raw data   
    processed_data = Data() 
    processed_data.Voltage        = np.zeros((5,6,15,2)) # current , operating temperature , state_of_charge vs voltage      
    processed_data.Temperature    = np.zeros((5,6,15,2)) # current , operating temperature , state_of_charge vs temperature 

    # Reshape  Data          
    raw_data.Voltage 
    for i, Amps in enumerate(raw_data.Voltage):
        for j , Deg in enumerate(Amps):
            min_x    = 0 
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Voltage[i,j,:,:]= vec   

    for i, Amps in enumerate(raw_data.Temperature):
        for j , Deg in enumerate(Amps):
            min_x    = 0   
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Temperature[i,j,:,:]= vec  
    
    # Create performance maps  
    battery_data             = Data() 
    amps                    = np.linspace(0, 8, 5)
    temp                    = np.linspace(0, 50, 6) +  272.65
    SOC                     = np.linspace(0, 1, 15)
    battery_data.Voltage     = RegularGridInterpolator((amps, temp, SOC), processed_data.Voltage,bounds_error=False,fill_value=None)
    battery_data.Temperature = RegularGridInterpolator((amps, temp, SOC), processed_data.Temperature,bounds_error=False,fill_value=None) 
     
    return battery_data  

def load_battery_results(): 
    '''Load experimental raw data of NMC cells 
        
       Assumptions:
           Ideal gas
           
       Source:
           Automotive Industrial Systems Company of Panasonic Group, Technical Information of 
           NCR18650G, URL https://www.imrbatteries.com/content/panasonic_ncr18650g.pdf
    
       Args: 
           None
           
       Returns:
           battery_data: raw data from battery   [unitless]
    '''    
    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator     
    return RCAIDE.load(rel_path+ 'NMC_Raw_Data.res')