## @ingroup Library-Compoments-Energy-Batteries
# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Ion_LiFePO4_18650.py
# 
# 
# Created:  Mar 2024, M. Clarke
# Modified: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
from RCAIDE.Framework.Core          import Units,Data
from RCAIDE.Library.Components.Energy.Sources.Battery_Modules.Generic_Battery_Module import  Generic_Battery_Module
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Lithium_Ion_LFP  import * 

# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_LFP
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Batteries 
class Lithium_Ion_LFP(Generic_Battery_Module):
    """ 18650 lithium-iron-phosphate-oxide battery cell.  
        """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None

        Source:
            # Cell Information 
            Saw, L. H., Yonghuang Ye, and A. A. O. Tay. "Electrochemical–thermal analysis of 
            18650 Lithium Iron Phosphate cell." Energy Conversion and Management 75 (2013): 
            162-174.
            
            # Electrode Area
            Muenzel, Valentin, et al. "A comparative testing study of commercial
            18650-format lithium-ion battery cells." Journal of The Electrochemical
            Society 162.8 (2015): A1592.
            
            # Cell Thermal Conductivities 
            (radial)
            Murashko, Kirill A., Juha Pyrhönen, and Jorma Jokiniemi. "Determination of the 
            through-plane thermal conductivity and specific heat capacity of a Li-ion cylindrical 
            cell." International Journal of Heat and Mass Transfer 162 (2020): 120330.
            
            (axial)
            Saw, L. H., Yonghuang Ye, and A. A. O. Tay. "Electrochemical–thermal analysis of 
            18650 Lithium Iron Phosphate cell." Energy Conversion and Management 75 (2013): 
            162-174.
        
        """
        # ----------------------------------------------------------------------------------------------------------------------
        #  Module Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.tag                              = 'lithium_ion_lfp' 
        self.power_split_ratio                                 = None
        self.number_of_cells                                   = 1
        self.maximum_energy                                    = 0.0
        self.maximum_power                                     = 0.0
        self.maximum_voltage                                   = 0.0        
        self.electrical_configuration                          = Data()
        self.electrical_configuration.series                   = 1
        self.electrical_configuration.parallel                 = 1   
        self.electrical_configuration.total                    = 1   
        self.geometrtic_configuration                          = Data() 
        self.geometrtic_configuration.normal_count             = 1       # number of cells normal to flow
        self.geometrtic_configuration.parallel_count           = 1       # number of cells parallel to flow      
        self.geometrtic_configuration.normal_spacing           = 0.02
        self.geometrtic_configuration.parallel_spacing         = 0.02
        
        # ----------------------------------------------------------------------------------------------------------------------
        #  Cell Level Properties
        # ----------------------------------------------------------------------------------------------------------------------        
        self.cell.diameter                    = 0.0185                                                   # [m]
        self.cell.height                      = 0.0653                                                   # [m]
        self.cell.mass                        = 0.03  * Units.kg                                         # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) + (0.5*np.pi*self.cell.diameter**2)  # [m^2]
        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height       # [m^3] 
        self.cell.density                     = self.cell.mass/self.cell.volume                          # [kg/m^3]
        self.cell.electrode_area              = 0.0342                                                   # [m^2]  # estimated 
                                                        
        self.cell.maximum_voltage             = 3.6                                                      # [V]
        self.cell.nominal_capacity            = 1.5                                                      # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                      # [V]
         
        self.cell.watt_hour_rating            = self.cell.nominal_capacity  * self.cell.nominal_voltage   # [Watt-hours]      
        self.cell.specific_energy             = self.cell.watt_hour_rating*Units.Wh/self.cell.mass        # [J/kg]
        self.cell.specific_power              = self.cell.specific_energy/self.cell.nominal_capacity      # [W/kg]   
        self.cell.ragone.const_1              = 88.818  * Units.kW/Units.kg
        self.cell.ragone.const_2              = -.01533 / (Units.Wh/Units.kg)
        self.cell.ragone.lower_bound          = 60.     * Units.Wh/Units.kg
        self.cell.ragone.upper_bound          = 225.    * Units.Wh/Units.kg         
        self.cell.resistance                  = 0.022                                                    # [Ohms]
                                                                                                            
        self.cell.specific_heat_capacity      = 1115                                                     # [J/kgK]                                                     
        self.cell.radial_thermal_conductivity = 0.475                                                    # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 37.6    
                                                 
        
        return
    

    def energy_calc(self,state,bus,coolant_lines, t_idx, delta_t, discharge= True): 
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
        stored_results_flag, stored_battery_tag =  compute_lfp_cell_performance(self,state,bus,coolant_lines, t_idx,delta_t,discharge) 
                        
        return stored_results_flag, stored_battery_tag
    
    def reuse_stored_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag,discharge= True):
        reuse_stored_lfp_cell_data(self,state,bus,coolant_lines, t_idx, delta_t,stored_results_flag, stored_battery_tag, discharge)
        return    
    
    def compute_voltage(self,battery_conditions):
        """ Computes the voltage of a single LFP cell  
    
        Assumptions:
            None
        
        Source:
            None
    
        Args:
            self               : battery          [unitless] 
            battery_conditions : state of battery [unitless]
            
        Returns: 
            None
        """              

        return battery_conditions.pack.voltage_under_load 
    
    def update_battery_age(self,segment,increment_battery_age_by_one_day = False):   
        """ This does nothing. """
        pass 
        return  
 
  
      