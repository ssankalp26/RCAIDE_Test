# RCAIDE/Library/Components/Energy/Sources/Fuel_Tanks/Wing_Fuel_Tank.py
# 
# 
# Created:  Sep 2024, A. Molloy and M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from .Fuel_Tank  import Fuel_Tank 
from RCAIDE.Library.Methods.Energy.Sources.Fuel_Tanks.append_fuel_tank_conditions import append_fuel_tank_conditions 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------   
class Wing_Fuel_Tank(Fuel_Tank):
    """
    A class for modeling wing-integrated fuel tanks in aircraft energy systems.
    Inherits from the Fuel_Tank class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'wing_fuel_tank'
    
    fuel_selector_ratio : float
        Ratio determining fuel selection priority, defaults to 1.0
    
    mass_properties : Data
        Collection of mass-related properties
        - empty_mass : float
            Mass of empty tank structure, defaults to 0.0
    
    secondary_fuel_flow : float
        Secondary fuel flow rate, defaults to 0.0
    
    length : float
        Physical length of the fuel tank, defaults to 0.0
    
    width : float
        Physical width of the fuel tank, defaults to 0.0
    
    height : float
        Physical height of the fuel tank, defaults to 0.0
    
    fuel : None
        Fuel type stored in tank, defaults to None

    Methods
    -------
    append_operating_conditions(segment, fuel_line)
        Appends operating conditions for a flight segment and fuel line

    Notes
    -----
    The Wing_Fuel_Tank class models fuel tanks integrated into the aircraft wings.
    These tanks utilize the wing structure for fuel storage, which can improve
    aircraft efficiency by reducing the need for dedicated fuel storage space
    in the fuselage. The class provides functionality for managing fuel storage,
    flow rates, and physical dimensions specific to wing-integrated tanks.
    
    **Definitions**
    'Fuel Selector Ratio'
        Ratio that determines the priority of fuel usage from this tank
    'Secondary Fuel Flow'
        Additional fuel flow rate beyond primary flow
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'wing_fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.length                      = 0.0
        self.width                       = 0.0
        self.height                      = 0.0
        self.fuel                        = None
         

    def append_operating_conditions(self,segment,fuel_line):  
        append_fuel_tank_conditions(self,segment, fuel_line)  
        return                                          