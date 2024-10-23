## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Frequency_Domain_Buildup.py
# 
# 
# Created:  Oct 2024, A. Molloy
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# noise imports
from RCAIDE.Library.Methods.Noise.Common.generate_zero_elevation_microphone_locations import generate_zero_elevation_microphone_locations 
from RCAIDE.Library.Methods.Noise.Common.generate_terrain_microphone_locations        import generate_terrain_microphone_locations     
from RCAIDE.Library.Methods.Noise.Common.compute_relative_noise_evaluation_locations  import compute_relative_noise_evaluation_locations
from RCAIDE.Library.Methods.Geodesics.compute_point_to_point_geospacial_data          import compute_point_to_point_geospacial_data

# package imports
import numpy as np
from scipy.interpolate                                           import RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Frequency_Domain_Buildup
# ---------------------------------------------------------------------------------------------------------------------- 
def  evaluate_noise_surrogate(total_SPL_dBA,total_SPL_spectra,settings,segment):
    '''
    NIRANJAN
    
    '''

    conditions =  segment.state.conditions

    if settings.topography_file !=  None:
        compute_point_to_point_geospacial_data(settings)
        generate_terrain_microphone_locations(settings)        
    else:    
        generate_zero_elevation_microphone_locations(settings) 
    
    noise_time,noise_pos,RML,PHI,THETA,num_gm_mic  = compute_relative_noise_evaluation_locations(settings, segment)
    ctrl_pts   =  len(noise_time)  

    # Append microphone locations to conditions 
    conditions.noise.number_of_ground_microphones        = num_gm_mic 
    conditions.noise.microphone_locations                = RML  
    conditions.noise.microphone_directivty_phi_angle     = PHI  
    conditions.noise.microphone_directivty_theta_angle   = THETA  

    # Compute noise at hemishere locations      
    phi     = settings.noise_hemisphere_phi_angles
    theta   = settings.noise_hemisphere_theta_angles
   
    # create empty arrays for results      
    SPL_dBA_scaled                = np.ones((ctrl_pts,num_gm_mic))*1E-16  
          
    cpt   =  0
    time  = segment.state.conditions.frames.inertial.time[:,0]
    for i in  range(ctrl_pts):
        SPL_lower       = total_SPL_dBA[cpt].reshape(len(phi),len(theta))
        SPL_uppper      = total_SPL_dBA[cpt+1].reshape(len(phi),len(theta))
        SPL_gradient    = SPL_uppper -  SPL_lower
        x               = (noise_time[i] -time[cpt,0]) / (time[cpt+1,0] - time[cpt,0])
        SPL_interp      = SPL_lower + SPL_gradient * x 
 
        # Create surrogate   
        SPL_dBA_surrogate                = RegularGridInterpolator((phi, theta),SPL_interp  ,method = 'linear',   bounds_error=False, fill_value=None)       
        
        # Query surrogate
        pts                            =  (PHI[i],THETA[i])
        SPL_dBA_unscaled               =  SPL_dBA_surrogate(pts) 
        
        # Scale data using radius  
        R_ref  = settings.noise_hemisphere_radius 
        R      =  np.linalg.norm(RML[i], axis=1) 
        SPL_dBA_scaled[i]                = R_ref / R * SPL_dBA_unscaled
        
        if noise_time[i] >= time[cpt]:
            cpt += 1
    
    # Store data        
    conditions.noise.SPL_dBA  = SPL_dBA_scaled 

    return

