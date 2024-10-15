## @ingroup Methods-Noise-Common 
# RCAIDE/Methods/Noise/Common/compute_relative_noise_evaluation_locations.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Relative Noise Evaluatation Locations
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Methods-Noise-Common 
def compute_relative_noise_evaluation_locations(settings,microphone_locations,segment):
    """This computes the relative locations on the surface in the computational domain where the 
    propogated sound is computed. Vectors point from observer/microphone to aircraft/source  
            
    Assumptions: 
        Acoustic scattering is not modeled

    Source:
        N/A  

    Inputs:  
        settings.ground_microphone_locations                - array of microphone locations on the ground  [meters] 
        segment.conditions.frames.inertial.position_vector  - position of aircraft                         [boolean]                                          

    Outputs: 
    GM_THETA   - angle measured from ground microphone in the x-z plane from microphone to aircraft 
    GM_PHI     - angle measured from ground microphone in the y-z plane from microphone to aircraft 
    RML        - relative microphone locations  
    num_gm_mic - number of ground microphones
 
    Properties Used:
        N/A       
    """       
  
    MSL_altitude      = settings.mean_sea_level_altitude  
    pos               = segment.state.conditions.frames.inertial.position_vector  
    num_gm_mic        = len(microphone_locations)  
    RML               = np.zeros((len(pos),num_gm_mic,3)) 
    PHI               = np.zeros((len(pos),num_gm_mic))
    THETA             = np.zeros((len(pos),num_gm_mic))
        
    
    for cpt in range(len(pos)):  
        relative_locations           = np.zeros((num_gm_mic,3,1))
        relative_locations[:,0,0]    = microphone_locations[:,0,0] -  (pos[cpt,0] + settings.aircraft_departure_location[0])
        relative_locations[:,1,0]    = microphone_locations[:,1,0] -  (pos[cpt,1] + settings.aircraft_departure_location[1]) 
        if MSL_altitude:
            relative_locations[:,2,0]    = -(pos[cpt,2])  - microphone_locations[:,2,0] 
        else:
            relative_locations[:,2,0]    = -(pos[cpt,2])    
        
        RML[cpt,:,:]   = relative_locations[:,:,0] 
    
        PHI[cpt,:]     =  np.arctan(np.sqrt(np.square(relative_locations[:, 0, 0]) + np.square(relative_locations[:, 1, 0]))/relative_locations[:, 2, 0]) # AIDAN TO COMPUTE !!
        THETA[cpt,:]   =  np.arctan(relative_locations[:, 1, 0]/relative_locations[:, 1, 0]) # AIDAN TO COMPUTE !! 
    
    return RML,PHI,THETA,num_gm_mic 
 