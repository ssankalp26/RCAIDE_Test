## @ingroup  Library-Methods-Emissions-Chemical_Reactor_Network 
# RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network/build_CRN_EI_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import  Data 

# package imports 
from scipy.interpolate       import RegularGridInterpolator
from scipy import interpolate
import cantera              as ct 
import pandas               as pd

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Stability   
def build_CRN_EI_surrogates(emissions):
     
    surrogates =  emissions.surrogates
    training   =  emissions.training  
    
    # unpack data
    surrogates     = Data()
    mach_data      = training.Mach
    geometry       = emissions.geometry
    AoA_data       = emissions.training.angle_of_attack           
    Beta_data      = emissions.training.sideslip_angle  
    u_data         = emissions.training.u
    v_data         = emissions.training.v
    w_data         = emissions.training.w
    p_data         = emissions.training.roll_rate 

   
    surrogates.Clift_wing_alpha = Data()
    surrogates.Cdrag_wing_alpha = Data()  
    surrogates.Clift_wing_alpha[wing.tag] = RegularGridInterpolator((AoA_data ,mach_data),training.Clift_wing_alpha[wing.tag]        ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.Cdrag_wing_alpha[wing.tag] = RegularGridInterpolator((AoA_data ,mach_data),training.Cdrag_wing_alpha[wing.tag]        ,method = 'linear',   bounds_error=False, fill_value=None) 
        
    