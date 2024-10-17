## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Frequency_Domain_Buildup.py
# 
# 
# Created:   Jul 2023, M. Clarke
# Modified:  Oct 2024, A. Molloy

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE Imports 
from RCAIDE.Library.Methods.Noise.Common.decibel_arithmetic                           import SPL_arithmetic 
from RCAIDE.Library.Methods.Noise.Common.evaluate_noise_surrogate                     import evaluate_noise_surrogate
from RCAIDE.Library.Methods.Noise.Common.generate_hemisphere_microphone_locations     import generate_hemisphere_microphone_locations  
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.compute_rotor_noise  import compute_rotor_noise 
from .Noise      import Noise

# package imports
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Frequency_Domain_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Noise
class Frequency_Domain_Buildup(Noise):
    """This is an acoustic analysis based on a collection of frequency domain methods 

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
        self.tag =  "Frequency_Domain_Buildup"        
            
    def evaluate_noise(self,segment):
        """ Process vehicle to setup vehicle, condititon and configuration
    
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
        self.vehicle
        """         
    
        # unpack 
        config        = segment.analyses.noise.vehicle 
        settings      = self.settings  
        conditions    = segment.state.conditions  
        dim_cf        = len(settings.center_frequencies ) 
        ctrl_pts      = int(segment.state.numerics.number_of_control_points) 
         
        microphone_locations =  generate_hemisphere_microphone_locations(settings)     
        N_hemisphere_mics    =  len(microphone_locations)
        
        # create empty arrays for results      
        total_SPL_dBA          = np.ones((ctrl_pts,N_hemisphere_mics))*1E-16 
        total_SPL_spectra      = np.ones((ctrl_pts,N_hemisphere_mics,dim_cf))*1E-16  
         
        # iterate through sources and iteratively add rotor noise 
        for network in config.networks:
            for tag , item in  network.items():
                if (tag == 'busses') or (tag == 'fuel_line'): 
                    for distributor in item: 
                        for propulsor in distributor.propulsors:
                            for sub_tag , sub_item in  propulsor.items():
                                if (sub_tag == 'rotor') or (sub_tag == 'propeller'): 
                                    compute_rotor_noise(microphone_locations,distributor,propulsor,segment,settings) 
                                    total_SPL_dBA     = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_dBA[:,None,:]),axis =1),sum_axis=1)
                                    total_SPL_spectra = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,:],conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_1_3_spectrum[:,None,:,:]),axis =1),sum_axis=1) 
                             
        evaluate_noise_surrogate(total_SPL_dBA,total_SPL_spectra,settings,segment)
        return
    
    