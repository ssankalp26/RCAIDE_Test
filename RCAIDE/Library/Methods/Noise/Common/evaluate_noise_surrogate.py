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
from RCAIDE.Library.Methods.Geodesics.compute_point_to_point_geospacial_data          import compute_point_to_point_geospacial_data

# package imports
import numpy as np
from scipy.interpolate                                           import RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Frequency_Domain_Buildup
# ---------------------------------------------------------------------------------------------------------------------- 
def  evaluate_noise_surrogate(total_SPL_dBA,total_SPL_spectra,settings,segment):

    conditions =  segment.state.conditions
    ctrl_pts   =  segment.state.numerics.number_of_control_points 

    if settings.topography_file !=  None:
        compute_point_to_point_geospacial_data(settings)
        generate_terrain_microphone_locations(settings)        
    else:    
        generate_zero_elevation_microphone_locations(settings) 
    
    RML,PHI,THETA,num_gm_mic  = compute_relative_noise_evaluation_locations(settings, segment)

    # Append microphone locations to conditions 
    conditions.noise.number_of_ground_microphones        = num_gm_mic 
    conditions.noise.microphone_locations                = RML  
    conditions.noise.microphone_directivty_phi_angle     = PHI  
    conditions.noise.microphone_directivty_theta_angle   = THETA  

    # Compute noise at hemishere locations 
    n            = settings.noise_hemisphere_microphone_resolution  
    phi_bounds   = settings.noise_hemisphere_phi_angle_bounds       
    theta_bounds = settings.noise_hemisphere_theta_angle_bounds   
    phi_data     = np.linspace(phi_bounds[0], phi_bounds[1], n)
    theta_data   = np.linspace(theta_bounds[0],theta_bounds[1], n) 
   
    # create empty arrays for results      
    SPL_dBA_scaled                = np.ones((ctrl_pts,num_gm_mic))*1E-16 
    SPL_1_3_spectrum_dBA_scaled   = np.ones((ctrl_pts,num_gm_mic,settings.harmonics[-1]))*1E-16  
          
    for i in  range(ctrl_pts):
        # Create surrogate   
        SPL_dBA_surrogate                = RegularGridInterpolator((phi_data, theta_data),total_SPL_dBA[i].reshape(n,n)     ,method = 'linear',   bounds_error=False, fill_value=None)      
        SPL_1_3_spectrum_dBA_surrogate   = RegularGridInterpolator((phi_data, theta_data),total_SPL_spectra[i].reshape(n,n,settings.harmonics[-1])   ,method = 'linear',   bounds_error=False, fill_value=None) 
        
        # Query surrogate
        pts                            =  (PHI[i],THETA[i])
        SPL_dBA_unscaled               =  SPL_dBA_surrogate(pts)
        SPL_1_3_spectrum_dBA_unscaled  =  SPL_1_3_spectrum_dBA_surrogate(pts)
        
        # Scale data using radius  
        R_ref  = settings.noise_hemisphere_radius 
        R      =  np.linalg.norm(RML[i], axis=1) 
        SPL_dBA_scaled[i]                = R_ref / R * SPL_dBA_unscaled    
        SPL_1_3_spectrum_dBA_scaled[i]   = R_ref / np.tile(R[:, None],(1,settings.harmonics[-1])) * SPL_1_3_spectrum_dBA_unscaled 
    
    # Store data        
    conditions.noise.SPL_dBA              = SPL_dBA_scaled
    conditions.noise.SPL_1_3_spectrum_dBA = SPL_1_3_spectrum_dBA_scaled

    return

