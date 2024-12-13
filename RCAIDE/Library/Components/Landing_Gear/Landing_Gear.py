# RCAIDE/Compoments/Landing_Gear/Landing_Gear.py
# 
# 
# Created:  Nov 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components import Component    
# ---------------------------------------------------------------------------------------------------------------------- 
#  Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------  
class Landing_Gear(Component):
    """
    A base class for modeling aircraft landing gear systems.
    Inherits from the Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'landing_gear'
    tire_diameter : float
        Diameter of the tire, defaults to 0.0
    strut_length : float
        Length of the strut, defaults to 0.0
    units : float
        Units of the gear, defaults to 0.0
    gear_extended : bool
        Whether the gear is extended, defaults to False
    wheels : float
        Number of wheels, defaults to 0.0
    
    Notes
    -----
    The Landing_Gear class serves as a base class for all landing gear types,
    providing common attributes and methods for landing gear modeling. It includes
    properties needed for structural, dynamic, and kinematic analysis.
    
    **Definitions**
    'Strut'
        Main structural member of the landing gear
    """

    def __defaults__(self):
        """ This sets the default values for the component attributes.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
        """
       
        self.tag            = 'landing_gear'   
        self.tire_diameter  = 0 
        self.strut_length   = 0 
        self.units          = 0 
        self.gear_extended  = False
        self.wheels         = 0     