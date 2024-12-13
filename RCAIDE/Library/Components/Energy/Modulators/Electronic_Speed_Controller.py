# RCAIDE/Library/Components/Energy/Modulators/Electronic_Speed_Controller.py
# 
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller.append_esc_conditions   import append_esc_conditions 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Electronic Speed Controller Class
# ---------------------------------------------------------------------------------------------------------------------- 
class Electronic_Speed_Controller(Component):
    """
    A class for modeling electronic speed controllers (ESC) in aircraft propulsion systems.
    Inherits from the base Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'electronic_speed_controller'
    
    efficiency : float
        Efficiency of the speed controller, defaults to 0.0

    Methods
    -------
    append_operating_conditions(segment, bus, propulsor)
        Appends operating conditions for a specific flight segment, bus, and propulsor

    Notes
    -----
    The Electronic_Speed_Controller class manages the speed control of electric motors
    in aircraft propulsion systems. It regulates power delivery from the electrical
    bus to the propulsor and accounts for efficiency losses in the process.
    
    **Definitions**
    'ESC'
        Electronic Speed Controller - device that controls motor speed by regulating power
    'Operating Conditions'
        Set of parameters defining the ESC's state during operation
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

        self.tag              = 'electronic_speed_controller'  
        self.efficiency       = 0.0 

    def append_operating_conditions(self,segment,bus,propulsor): 
        propulsor_conditions =  segment.state.conditions.energy[bus.tag][propulsor.tag]
        append_esc_conditions(self,segment,propulsor_conditions)
        return 