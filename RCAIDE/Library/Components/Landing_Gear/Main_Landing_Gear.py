# RCAIDE/Compoments/Landing_Gear/Main_Landing_Gear.py
# 
# 
# Created:  Nov 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Landing_Gear import Landing_Gear

# ---------------------------------------------------------------------------------------------------------------------- 
#  Nose_Landing_Gear
# ---------------------------------------------------------------------------------------------------------------------- 
class Main_Landing_Gear(Landing_Gear):
    """
    A class for modeling main landing gear systems in aircraft.
    Inherits from the Landing_Gear class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'main_gear'
    units : float
        Number of main landing gear units, defaults to 0.0
    strut_length : float
        Length of the strut, defaults to 0.0
    tire_diameter : float
        Diameter of the tire, defaults to 0.0
    wheels : float
        Number of wheels on the main landing gear, defaults to 0.0

    Notes
    -----
    The Main_Gear class models the primary landing gear components that support
    the majority of the aircraft's weight during ground operations. These typically
    consist of dual or multiple wheel configurations and include braking systems.
    """
    def __defaults__(self):
        """ This sets the default values for the component attributes.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Output:
                None
                
                Properties Used:
                N/A
        """
        self.tag           = 'main_gear'
        self.units         = 0. # number of main landing gear units        
        self.strut_length  = 0.
        self.tire_diameter = 0. 
        self.wheels        = 0. # number of wheels on the main landing gear 