# RCAIDE/Library/Compoments/Energy/Sources/Fuel_Cells/Generic_Fuel_Cell.py
# 
# 
# Created:  Dec 2024, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                                     import Units, Data
from RCAIDE.Library.Components                                 import Component    
from RCAIDE.Library.Attributes.Gases                           import Air  
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Cell_Stacks.Generic.compute_fuel_cell_performance import *
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Cell_Stacks.Generic.append_fuel_cell_conditions import *

# ----------------------------------------------------------------------------------------------------------------------
#  Generic_Fuel_Cell
# ----------------------------------------------------------------------------------------------------------------------    
class Generic_Fuel_Cell_Stack(Component):
    """This is a fuel cell component.
    
    Assumptions:
    None

    Source:
    None
    """    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        Some default values come from a Nissan 2011 fuel cell

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """           

        self.energy_density                                    = 0.0
        self.current_energy                                    = 0.0
        self.current_capacitor_charge                          = 0.0
        self.capacity                                          = 0.0
            
        self.length                                            = 0.0
        self.width                                             = 0.0
        self.height                                            = 0.0
        self.volume_packaging_factor                           = 1.05
        self.BMS_additional_weight_factor                      = 1.42
                 
        self.orientation_euler_angles                          = [0.,0.,0.]  # vector of angles defining default orientation of rotor        
                     
        self.fuel_cell                                         = Data() 
        self.fuel_cell.propellant                              = RCAIDE.Library.Attributes.Propellants.Gaseous_Hydrogen()
        self.fuel_cell.oxidizer                                = Air()
        self.fuel_cell.efficiency                              = .65                                 # normal fuel cell operating efficiency at sea level
        self.fuel_cell.specific_power                          = 2.08        *Units.kW/Units.kg      # specific power of fuel cell [kW/kg]; default is Nissan 2011 level
        self.fuel_cell.mass_density                            = 1203.208556 *Units.kg/Units.m**3.   # take default as specs from Nissan 2011 fuel cell            
        self.fuel_cell.volume                                  = 0.0
        self.fuel_cell.max_power                               = 0.0 

        self.electrical_configuration                          = Data()
        self.electrical_configuration.series                   = 1
        self.electrical_configuration.parallel                 = 1   
        
        self.geometrtic_configuration                          = Data() 
        self.geometrtic_configuration.normal_count             = 1
        self.geometrtic_configuration.parallel_count           = 1
        self.geometrtic_configuration.normal_spacing           = 0.02
        self.geometrtic_configuration.stacking_rows            = 3
        self.geometrtic_configuration.parallel_spacing         = 0.02           
        
    def energy_calc(self,state):
        """This call the assigned discharge method.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        see properties used

        Outputs:
        mdot     [kg/s] (units may change depending on selected model)

        Properties Used:
        self.discharge_model(self, conditions, numerics)
        """
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
        
        stored_results_flag, stored_battery_tag = compute_fuel_cell_performance(self,state,bus,coolant_lines, t_idx,delta_t) 
        
        return stored_results_flag, stored_battery_tag 

    def append_operating_conditions(self,segment,bus):  
        append_fuel_cell_conditions(self,segment,bus)  
        return
    
    def append_fuel_cell_segment_conditions(self,bus, conditions, segment):
        append_fuel_cell_segment_conditions(self,bus, conditions, segment)
        return 

    def reuse_stored_data(self,state,bus,stored_results_flag, stored_fuel_cell_tag):
        reuse_stored_fuel_cell_data(self,state,bus,stored_results_flag, stored_fuel_cell_tag)
        return     
    