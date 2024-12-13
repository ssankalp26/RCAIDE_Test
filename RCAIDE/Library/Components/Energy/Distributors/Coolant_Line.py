# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Coolant_Line.py 
# 
# Created:  Aug 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Coolant Line
# ---------------------------------------------------------------------------------------------------------------------- 
class Coolant_Line(Component):
    """
    A class for modeling coolant distribution lines in aircraft thermal management systems.
    Inherits from the base Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'coolant_line'
    
    active : bool
        Flag indicating if the coolant line is operational, defaults to True
    
    efficiency : float
        Efficiency of the coolant distribution, defaults to 1.0
    
    identical_battery_modules : Data
        Information about identical battery modules in the system
    
    battery_modules : Container
        Collection of battery modules connected to this coolant line
        - module_tag : Container
            Container for each battery module's cooling system data

    Methods
    -------
    __defaults__()
        Sets the default values for the coolant line attributes
    
    __init__(distributor)
        Initializes the coolant line with battery module containers

    Notes
    -----
    The Coolant_Line class manages the distribution of coolant to various
    battery modules in the aircraft's thermal management system. It tracks
    the connection to battery modules and maintains their cooling requirements.
    
    **Definitions**
    'Thermal Management System'
        System responsible for maintaining optimal temperature in battery modules
    'Battery Module'
        Individual battery unit requiring thermal management
    """
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'coolant_line'  

                    
    def __init__ (self, distributor=None):
        
        """This initializes empty containers to add heat acqusition systems
           for battery modules that are present on a particular bus.
    
        Assumptions:
            None
        
        Source:
            None
        """               
        self.active                        = True 
        self.efficiency                    = 1.0
 
            
        for tag, item in  distributor.items():
            self.identical_battery_modules  =  distributor.identical_battery_modules
            if tag == 'battery_modules':
                self.battery_modules  = Container()
                for battery in item:
                    self.battery_modules[battery.tag] = Container()