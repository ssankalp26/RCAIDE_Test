# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Electrical_Bus.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Components                                 import Component
from RCAIDE.Library.Components.Component                       import Container
from RCAIDE.Library.Methods.Energy.Distributors.Electrical_Bus import *


# ----------------------------------------------------------------------------------------------------------------------
#  Electrical_Bus
# ---------------------------------------------------------------------------------------------------------------------- 
class Electrical_Bus(Component):
    """
    A class for modeling electrical power distribution buses in aircraft systems.
    Inherits from the base Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'bus'
    
    battery_modules : Container
        Collection of battery modules connected to this bus
    
    propulsors : Container
        Collection of propulsion systems connected to this bus
    
    solar_panel : None
        Reference to connected solar panel system
    
    avionics : Avionics
        Aircraft avionics system connected to this bus
    
    payload : Payload
        Aircraft payload system connected to this bus
    
    identical_propulsors : bool
        Flag indicating if all propulsors are identical, defaults to True
    
    identical_battery_modules : bool
        Flag indicating if all battery modules are identical, defaults to True
    
    active : bool
        Flag indicating if the bus is operational, defaults to True
    
    efficiency : float
        Efficiency of power distribution, defaults to 1.0
    
    voltage : float
        Bus voltage, defaults to 0.0
    
    power_split_ratio : float
        Ratio for power distribution, defaults to 1.0
    
    nominal_capacity : float
        Nominal power capacity of the bus, defaults to 0.0
    
    charging_c_rate : float
        Battery charging C-rate, defaults to 1.0
    
    number_of_battery_modules : int
        Number of battery modules connected, defaults to 1
    
    battery_module_electric_configuration : str
        Configuration of battery modules, defaults to "Series"

    Methods
    -------
    append_operating_conditions(segment)
        Appends operating conditions for a flight segment
    
    append_segment_conditions(conditions, segment)
        Appends conditions for a specific segment
    
    initialize_bus_properties()
        Initializes the electrical bus properties
    
    compute_distributor_conditions(state, t_idx, delta_t)
        Computes conditions for the distributor

    Notes
    -----
    The Electrical_Bus class manages power distribution between various
    aircraft components including batteries, propulsors, avionics, and payloads.
    It handles power routing and electrical system configuration.
    
    **Definitions**
    'C-rate'
        Rate at which a battery is charged/discharged relative to its capacity
    'Power Split Ratio'
        Ratio determining power distribution between connected components
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """                
        self.tag                                   = 'bus' 
        self.battery_modules                       = Container()
        self.propulsors                            = Container() 
        self.solar_panel                           = None 
        self.avionics                              = RCAIDE.Library.Components.Systems.Avionics()
        self.payload                               = RCAIDE.Library.Components.Payloads.Payload()        
        self.identical_propulsors                  = True
        self.identical_battery_modules             = True  
        self.active                                = True
        self.efficiency                            = 1.0
        self.voltage                               = 0.0 
        self.power_split_ratio                     = 1.0
        self.nominal_capacity                      = 0.0
        self.charging_c_rate                       = 1.0
        self.number_of_battery_modules             = 1
        self.battery_module_electric_configuration = "Series" 
        
    def append_operating_conditions(self, segment):
        append_bus_conditions(self, segment)
        return
    def append_segment_conditions(self, conditions, segment):
        append_bus_segment_conditions(self, conditions, segment)
        return    
    
    def initialize_bus_properties(self):
        initialize_bus_properties(self)
        return
    def compute_distributor_conditions(self,state,t_idx, delta_t):
        compute_bus_conditions(self,state,t_idx, delta_t)
        return    