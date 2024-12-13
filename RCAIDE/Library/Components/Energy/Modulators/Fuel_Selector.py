# RCAIDE/Library/Components/Energy/Modulators/Fuel_Selector.py
#  
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Fuel_Selector
# ----------------------------------------------------------------------------------------------------------------------  
class Fuel_Selector(Component):
    """
    A class for managing fuel source selection in aircraft fuel systems.
    Inherits from the base Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'fuel_selector'
    
    efficiency : float
        Efficiency of the fuel selection system, defaults to 0.0

    Notes
    -----
    The Fuel_Selector class manages the routing and selection of fuel sources
    in aircraft fuel systems. It controls which fuel tanks or sources are
    active and handles the switching between different fuel sources.
    
    **Definitions**
    'Fuel Selection'
        Process of choosing and routing fuel from different available sources
    'Selection Efficiency'
        Measure of effectiveness in fuel source switching and routing
    """
    
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
            """         

        self.tag              = 'fuel_selector'  
        self.efficiency       = 0.0       
     