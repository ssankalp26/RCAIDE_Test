## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Correlation_Buildup.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE Imports 
from RCAIDE.Library.Methods.Noise.Correlation_Buildup.Airframe.airframe_noise         import airframe_noise
from RCAIDE.Library.Methods.Noise.Correlation_Buildup.Turbofan.turbofan_engine_noise  import turbofan_engine_noise   
from RCAIDE.Library.Methods.Noise.Common.decibel_arithmetic                           import SPL_arithmetic 
from RCAIDE.Library.Methods.Noise.Common.evaluate_noise_surrogate                     import evaluate_noise_surrogate
from RCAIDE.Library.Methods.Noise.Common.generate_hemisphere_microphone_locations     import generate_hemisphere_microphone_locations 
from RCAIDE.Library.Methods.Noise.Common.generate_zero_elevation_microphone_locations import generate_zero_elevation_microphone_locations 
from RCAIDE.Library.Methods.Noise.Common.generate_terrain_microphone_locations        import generate_terrain_microphone_locations     
from RCAIDE.Library.Methods.Noise.Common.compute_relative_noise_evaluation_locations  import compute_relative_noise_evaluation_locations
from RCAIDE.Library.Methods.Geodesics.compute_point_to_point_geospacial_data          import compute_point_to_point_geospacial_data
from .Noise      import Noise   

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Noise
class Correlation_Buildup(Noise): 
    """This is an acoustic analysis based on a collection of correlative modes

     Assumptions: 
 
     Source:
     N/A
 
     Inputs:
     None
 
     Outputs:
     None
 
     Properties Used:
     N/A 
    """    
    
    def __defaults__(self):
        
        """ This sets the default values for the analysis.
        
            Assumptions:
            Ground microphone angles start in front of the aircraft (0 deg) and sweep in a lateral direction 
            to the starboard wing and around to the tail (180 deg)
            
            Source:
            N/A
            
            Inputs:
            None
            
            Output:
            None
            
            Properties Used:
            N/A
        """
        
        # Initialize quantities
        self.tag =  "Correlation_Buildup"
        return
            
    def evaluate_noise(self,segment):
        """ Process vehicle to setup geometry, condititon and configuration
    
        Assumptions:
        None
    
        Source:
        N/4
    
        Inputs:
        self.settings.
            center_frequencies  - 1/3 octave band frequencies   [unitless]
    
        Outputs:
        None
    
        Properties Used: 
        """         
    
        # unpack 
        config        = segment.analyses.noise.vehicle 
        settings      = self.settings     
        conditions    = segment.state.conditions  
        dim_cf        = len(settings.center_frequencies ) 
        ctrl_pts      = int(segment.state.numerics.number_of_control_points) 
         
        microphone_locations =  generate_hemisphere_microphone_locations(settings)     
        N_hemisphere_mics    =  len(microphone_locations)
        
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
        
        # create empty arrays for results      
        total_SPL_dBA          = np.ones((ctrl_pts,num_gm_mic))*1E-16 
        total_SPL_spectra      = np.ones((ctrl_pts,num_gm_mic,dim_cf))*1E-16  
    
        # flap noise - only applicable for turbofan aircraft
        if 'flap' in config.wings.main_wing.control_surfaces:    
            airframe_noise_res        = airframe_noise(segment,config,settings) 
            total_SPL_dBA             = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],airframe_noise_res.SPL_dBA[:,None,:]),axis =1),sum_axis=1)
            total_SPL_spectra[:,:,5:] = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,5:],airframe_noise_res.SPL_1_3_spectrum[:,None,:,:]),axis =1),sum_axis=1)
             
            
          # iterate through sources  
        for network in config.networks: 
            if 'fuel_lines' in network:
                for fuel_line in network.fuel_lines:  
                    for propulsor in fuel_line.propulsors:        
                        engine_noise                = turbofan_engine_noise(propulsor,conditions.noise[fuel_line.tag][propulsor.tag].turbofan,segment,settings)    
                        total_SPL_dBA               = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],engine_noise.SPL_dBA[:,None,:]),axis =1),sum_axis=1)
                        total_SPL_spectra[:,:,5:]   = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,5:],engine_noise.SPL_1_3_spectrum[:,None,:,:]),axis =1),sum_axis=1)
                    
        conditions.noise.SPL_dBA              = total_SPL_dBA
        conditions.noise.SPL_1_3_spectrum_dBA = total_SPL_spectra                                                      
        return   

