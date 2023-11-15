## @ingroup Methods-Noise-Certification
# RCAIDE/Methods/Noise/Certification/turbofan_approach_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
from RCAIDE.Methods.Noise.Correlation_Buildup.Turbofan import compute_turbofan_aircraft_noise

# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Turbofan Approach Noise
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Methods-Noise-Certification
def turbofan_approach_noise(approach_mission,noise_configs):  
    """This method calculates approach noise of a turbofan aircraft
            
    Assumptions:
        N/A

    Source:
        N/A 

    Inputs:
        analyses        - data structure of RCAIDE analyses                [None]
        noise_configs   - data structure for RCAIDE vehicle configurations [None]

    Outputs: 
        SPL             - sound pressure level                            [dB]

    Properties Used:
        N/A 
        
    """ 
    # Update number of control points for noise      
    mission                                                       = approach_mission
    approach_initialization                                       = mission.evaluate()   
    n_points                                                      = np.ceil(approach_initialization.segments.descent.conditions.frames.inertial.time[-1] /0.5 +1)
    mission.npoints_takeoff_sign                                  = np.sign(n_points) 
    mission.segments.descent.state.numerics.number_of_control_points = int(np.minimum(200, np.abs(n_points))[0])

    # Set up analysis 
    noise_segment                                  = mission.segments.descent 
    noise_segment.analyses.noise.settings.approach = True
    noise_analyses                                 = noise_segment.analyses 
    noise_settings                                 = noise_segment.analyses.noise.settings
    noise_config                                   = noise_configs.landing  
    noise_config.engine_flag                       = True
    noise_config.print_output                      = 0
    noise_config.output_file                       = 'Noise_Approach.dat'
    noise_config.output_file_engine                = 'Noise_Approach_Engine.dat'    

    noise_result_approach = compute_turbofan_aircraft_noise(noise_config,noise_analyses,noise_segment,noise_settings)   
        
    return noise_result_approach