# RCAIDE/Library/Components/Energy/Distributors/Fuel_Line.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ---------------------------------------------------------------------------------------------------------------------- 
class Fuel_Line(Component):
    """
    A class for modeling fuel distribution lines in aircraft fuel systems.
    Inherits from the base Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'fuel_line'
    
    fuel_tanks : Container
        Collection of fuel tanks connected to this fuel line
    
    propulsors : Container
        Collection of propulsion systems supplied by this fuel line
    
    identical_propulsors : bool
        Flag indicating if all propulsors are identical, defaults to True
    
    active : bool
        Flag indicating if the fuel line is operational, defaults to True
    
    efficiency : float
        Efficiency of fuel distribution, defaults to 1.0

    Methods
    -------
    __defaults__()
        Sets the default values for the fuel line attributes

    Notes
    -----
    The Fuel_Line class manages the distribution of fuel between tanks and
    propulsion systems in the aircraft. It handles fuel routing and monitors
    the distribution efficiency.
    
    **Definitions**
    'Fuel Distribution'
        System for routing fuel from tanks to propulsion systems
    'Distribution Efficiency'
        Measure of effectiveness in fuel transfer through the line
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'fuel_line'  
        self.fuel_tanks                    = Container()
        self.propulsors                    = Container()
        self.identical_propulsors          = True 
        self.active                        = True 
        self.efficiency                    = 1.0 