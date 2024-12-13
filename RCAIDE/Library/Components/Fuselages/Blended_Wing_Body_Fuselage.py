# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Fuselage import Fuselage
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
class Blended_Wing_Body_Fuselage(Fuselage):
    """
    A specialized fuselage class for blended wing body aircraft configurations.

    Attributes
    ----------
    tag : str
        Identifier for the fuselage component, defaults to 'bwb_fuselage'
        
    aft_centerbody_area : float
        Area of the aft centerbody section, defaults to 0.0
        
    aft_centerbody_taper : float
        Taper ratio of the aft centerbody section, defaults to 0.0
        
    cabin_area : float
        Area of the cabin section, defaults to 0.0

    Methods
    -------
    compute_moment_of_inertia(center_of_gravity)
        Computes the moment of inertia matrix for the blended wing body fuselage about the given center of gravity

    Notes
    -----
    The Blended Wing Body Fuselage class extends the base Fuselage class to provide
    specialized functionality for BWB aircraft configurations. This design integrates
    the wing and fuselage into a single lifting body.
    
    **Definitions**
    'Blended Wing Body'
        An aircraft configuration that smoothly integrates the wings and fuselage
        into a single aerodynamic surface
    'Centerbody'
        The central section of a BWB aircraft that houses the passenger cabin
        and cargo hold
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
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
          
        self.tag                   = 'bwb_fuselage'
        self.aft_centerbody_area   = 0.0
        self.aft_centerbody_taper  = 0.0
        self.cabin_area            = 0.0
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        I =  np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) 
        return I        