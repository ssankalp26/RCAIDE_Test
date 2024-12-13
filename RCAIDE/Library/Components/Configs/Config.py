# RCAIDE/Library/Compoments/Configs/Config.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Framework.Core    import Diffed_Data
from RCAIDE.Vehicle          import Vehicle  

# ----------------------------------------------------------------------------------------------------------------------
#  Config
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Components-Configs
class Config(Diffed_Data,Vehicle):
    """
    A class for managing aircraft configurations, inheriting from both Diffed_Data and Vehicle classes.
    Provides functionality to store and manage different configurations of an aircraft.

    Attributes
    ----------
    tag : str
        Identifier for the configuration, defaults to 'config'
    
    _base : Vehicle
        Base vehicle configuration object
    
    _diff : Vehicle
        Differential vehicle configuration object for tracking changes

    Methods
    -------
    __defaults__()
        Sets the default values for the configuration attributes

    Notes
    -----
    The Config class serves as a top-level configuration manager that combines
    the functionality of differential data tracking (Diffed_Data) with vehicle
    properties (Vehicle). This allows for efficient management and comparison
    of different aircraft configurations.
    
    **Definitions**
    'Base Configuration'
        The reference configuration from which variations are derived
    'Differential Configuration'
        A configuration that tracks changes relative to the base configuration
    
    References
    ----------
    .. [1] None currently listed
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """     
        self.tag    = 'config'
        self._base  = Vehicle()
        self._diff  = Vehicle()
