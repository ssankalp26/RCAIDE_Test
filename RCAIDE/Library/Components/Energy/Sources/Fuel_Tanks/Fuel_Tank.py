# RCAIDE/Library/Components/Energy/Sources/Fuel_Tanks/Fuel_Tank.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Library.Components          import Component
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Tanks.append_fuel_tank_conditions import append_fuel_tank_conditions 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------   
class Fuel_Tank(Component):
    """
    A base class for modeling fuel tanks in aircraft energy systems.
    Inherits from the Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'fuel_tank'
    
    fuel_selector_ratio : float
        Ratio determining fuel selection priority, defaults to 1.0
    
    mass_properties : Data
        Collection of mass-related properties
        - empty_mass : float
            Mass of empty tank structure, defaults to 0.0
    
    secondary_fuel_flow : float
        Secondary fuel flow rate, defaults to 0.0
    
    fuel : None
        Fuel type stored in tank, defaults to None

    Methods
    -------
    append_operating_conditions(segment, fuel_line)
        Appends operating conditions for a flight segment and fuel line

    Notes
    -----
    The Fuel_Tank class serves as a base class for all fuel tank types,
    providing common attributes and methods for fuel tank modeling. It includes
    basic properties needed for fuel management and tank characteristics.
    This class is meant to be inherited by specific fuel tank implementations
    like Central_Fuel_Tank and Wing_Fuel_Tank.
    
    **Definitions**
    'Fuel Selector Ratio'
        Ratio that determines the priority of fuel usage from this tank
    'Secondary Fuel Flow'
        Additional fuel flow rate beyond primary flow
    'Empty Mass'
        Structural mass of the tank without fuel
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None
         

    def append_operating_conditions(self,segment,fuel_line):  
        append_fuel_tank_conditions(self,segment, fuel_line)  
        return                                          