## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Frequency_Domain_Buildup.py
# 
# 
# Created:  Oct 2024, A. Mollow
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# noise imports
from RCAIDE.Library.Methods.Noise.Common.generate_zero_elevation_microphone_locations import generate_zero_elevation_microphone_locations 
from RCAIDE.Library.Methods.Noise.Common.generate_terrain_microphone_locations        import generate_terrain_microphone_locations     
from RCAIDE.Library.Methods.Noise.Common.compute_relative_noise_evaluation_locations  import compute_relative_noise_evaluation_locations   

# package imports
import numpy as np
from scipy.interpolate                                           import RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Frequency_Domain_Buildup
# ---------------------------------------------------------------------------------------------------------------------- 
def  evaluate_noise_surrogate(total_SPL_dBA,total_SPL_spectra,settings,segment):

    conditions =  segment.state.conditions

    if settings.topography_file !=  None:
        microhpone_locations =  generate_terrain_microphone_locations(settings)        
    else:    
        microhpone_locations =  generate_zero_elevation_microphone_locations(settings)
        
    
    RML,PHI,THETA,num_gm_mic  = compute_relative_noise_evaluation_locations(settings,microhpone_locations, segment)

    # Append microphone locations to conditions   
    conditions.noise.number_of_ground_microphones        = num_gm_mic 
    conditions.noise.microphone_locations                = RML  
    conditions.noise.microphone_directivty_phi_angle     = PHI  
    conditions.noise.microphone_directivty_theta_angle   = THETA  

    # Compute noise at hemishere locations  
    phi_data = settings.noise_hemisphere_phi_angle_bounds     
    theta_data = settings.noise_hemisphere_theta_angle_bounds   

    # Create surrogate   
    SPL_dBA_surrogate                = RegularGridInterpolator((phi_data, theta_data),total_SPL_dBA       ,method = 'linear',   bounds_error=False, fill_value=None)      
    SPL_1_3_spectrum_dBA_surrogate   = RegularGridInterpolator((phi_data, theta_data),total_SPL_spectra   ,method = 'linear',   bounds_error=False, fill_value=None) 

    # Query surrogate
    pts                            =  (PHI,THETA)
    SPL_dBA_unscaled               =  SPL_dBA_surrogate(pts)
    SPL_1_3_spectrum_dBA_unscaled  =  SPL_1_3_spectrum_dBA_surrogate(pts)
    
    # Scale data using radius  
    R_ref  = settings.noise_hemisphere_radius 
    R      =  np.linalg.norm(num_gm_mic, axis=2) 
    SPL_dBA_scaled                = SPL_dBA_unscaled     # AIDAN TO CORRECT 
    SPL_1_3_spectrum_dBA_scaled   = SPL_1_3_spectrum_dBA_unscaled # AIDAN TO CORRECT
    
    # Store data        
    conditions.noise.SPL_dBA              = SPL_dBA_scaled
    conditions.noise.SPL_1_3_spectrum_dBA = SPL_1_3_spectrum_dBA_scaled

    return

