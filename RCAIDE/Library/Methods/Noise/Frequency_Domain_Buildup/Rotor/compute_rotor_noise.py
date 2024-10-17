## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor
# RCAIDE/Methods/Noise/Frequency_Domain_Buildup/Rotor/compute_rotor_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports 
from RCAIDE.Framework.Core import  Data   
from RCAIDE.Library.Methods.Noise.Common.decibel_arithmetic                             import SPL_arithmetic  
from RCAIDE.Library.Methods.Noise.Common.compute_noise_source_coordinates               import compute_rotor_point_source_coordinates  
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.harmonic_noise_point   import harmonic_noise_point
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.harmonic_noise_line    import harmonic_noise_line
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.harmonic_noise_plane   import harmonic_noise_plane
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.broadband_noise        import broadband_noise
from RCAIDE.Library.Methods.Noise.Frequency_Domain_Buildup.Rotor.broadband_noise_unsteady        import broadband_noise_unsteady
from RCAIDE.Library.Methods.Noise.Common                                                import atmospheric_attenuation
from RCAIDE.Library.Methods.Noise.Metrics.A_weighting_metric                            import A_weighting_metric  

# Python package imports   
import numpy as np    

# ----------------------------------------------------------------------------------------------------------------------    
#  Rotor Noise 
# ----------------------------------------------------------------------------------------------------------------------    
## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor
def compute_rotor_noise(microphone_locations,distributor,propulsor,segment,settings):
    ''' This is a collection medium-fidelity frequency domain methods for rotor acoustic noise prediction which 
    computes the acoustic signature (sound pressure level, weighted sound pressure levels,
    and frequency spectrums of a system of rotating blades           
        
    Assumptions:
    None

    Source:
    None
    
    Inputs:
        rotors                  - data structure of rotors                            [None]
        segment                 - flight segment data structure                       [None] 
        results                 - data structure containing of acoustic data          [None]
        settings                - accoustic settings                                  [None]
                               
    Outputs:
        Results.    
            blade_passing_frequencies      - blade passing frequencies                           [Hz]
            SPL                            - total SPL                                           [dB]
            SPL_dBA                        - dbA-Weighted SPL                                    [dBA]
            SPL_1_3_spectrum               - 1/3 octave band spectrum of SPL                     [dB]
            SPL_1_3_spectrum_dBA           - 1/3 octave band spectrum of A-weighted SPL          [dBA]
            SPL_broadband_1_3_spectrum     - 1/3 octave band broadband contribution to total SPL [dB] 
            SPL_harmonic_1_3_spectrum      - 1/3 octave band harmonic contribution to total SPL  [dB]
            SPL_harmonic_bpf_spectrum_dBA  - A-weighted blade passing freqency spectrum of 
                                             harmonic compoment of SPL                           [dB]
            SPL_harmonic_bpf_spectrum      - blade passing freqency spectrum of harmonic
                                             compoment of SPL                                    [dB] 
     
    Properties Used:
        N/A   
    '''
 
    # unpack
    rotor                = propulsor.rotor
    conditions           = segment.state.conditions
    energy_conditions    = conditions.energy[distributor.tag][propulsor.tag][rotor.tag]
    harmonics_blade      = settings.harmonics
    harmonics_load       = np.linspace(0,5,6).astype(int)  
      
    # create data structures for computation
    Noise   = Data()  
    Results = Data()
                     
    # compute position vector from point source (or should it be origin) at rotor hub to microphones 
    coordinates = compute_rotor_point_source_coordinates(distributor,propulsor,rotor,conditions,microphone_locations,settings)  

    # ----------------------------------------------------------------------------------
    # Harmonic Noise
    # ---------------------------------------------------------------------------------- 
    # harmonic noise with planar load distribution
    if settings.fidelity == 'plane_source':
        harmonic_noise_plane(harmonics_blade,harmonics_load,conditions,energy_conditions,coordinates,rotor,settings,Noise)
    elif settings.fidelity == 'line_source': 
        harmonic_noise_line(harmonics_blade,harmonics_load,conditions,energy_conditions,coordinates,rotor,settings,Noise)
    else:
        harmonic_noise_point(harmonics_blade,harmonics_load,conditions,energy_conditions,coordinates,rotor,settings,Noise) 

    # ----------------------------------------------------------------------------------    
    # Broadband Noise
    # ----------------------------------------------------------------------------------
    # broadband_noise(harmonics_blade,harmonics_load,conditions,energy_conditions,coordinates,rotor,settings,Noise)  
    broadband_noise_unsteady(conditions,energy_conditions,coordinates,rotor,settings,Noise)  

    # ----------------------------------------------------------------------------------    
    # Atmospheric attenuation 
    # ----------------------------------------------------------------------------------
    delta_atmo = atmospheric_attenuation(np.linalg.norm(coordinates.X_r[:,0,0,0,:],axis=1),settings.center_frequencies)

    # ----------------------------------------------------------------------------------    
    # Combine Harmonic (periodic/tonal) and Broadband Noise
    # ----------------------------------------------------------------------------------
    num_mic      = len(coordinates.X_hub[0,:,0,0])
    Noise.SPL_total_1_3_spectrum      = 10*np.log10( 10**(Noise.SPL_prop_harmonic_1_3_spectrum/10) + 10**(Noise.SPL_prop_broadband_1_3_spectrum/10)) - np.tile(delta_atmo[:,None,:],(1,num_mic,1))
    Noise.SPL_total_1_3_spectrum[np.isnan(Noise.SPL_total_1_3_spectrum)] = 0 

    # ----------------------------------------------------------------------------------
    # Summation of spectra from propellers into one SPL and store results
    # ----------------------------------------------------------------------------------
    Results.SPL                                           = SPL_arithmetic(Noise.SPL_total_1_3_spectrum, sum_axis=2)
    Results.SPL_dBA                                       = SPL_arithmetic(A_weighting_metric(Noise.SPL_total_1_3_spectrum,settings.center_frequencies), sum_axis=2)
    Results.SPL_harmonic                                  = SPL_arithmetic(Noise.SPL_prop_harmonic_1_3_spectrum, sum_axis=2) 
    Results.SPL_broadband                                 = SPL_arithmetic(Noise.SPL_prop_broadband_1_3_spectrum, sum_axis=2)
    
    # blade passing frequency 
    Results.blade_passing_frequencies                     = Noise.f          
    Results.SPL_harmonic_bpf_spectrum                     = Noise.SPL_prop_harmonic_bpf_spectrum
    Results.SPL_harmonic_bpf_spectrum_dBA                 = A_weighting_metric(Results.SPL_harmonic_bpf_spectrum,Noise.f) 
    
    # 1/3 octave band
    Results.one_third_frequency_spectrum                  = settings.center_frequencies 
    Results.SPL_1_3_spectrum                              = Noise.SPL_total_1_3_spectrum     
    Results.SPL_1_3_spectrum_dBA                          = A_weighting_metric(Results.SPL_1_3_spectrum,settings.center_frequencies)      
    Results.SPL_harmonic_1_3_spectrum                     = Noise.SPL_prop_harmonic_1_3_spectrum    
    Results.SPL_harmonic_1_3_spectrum_dBA                 = A_weighting_metric(Results.SPL_harmonic_1_3_spectrum,settings.center_frequencies) 
    Results.SPL_broadband_1_3_spectrum                    = Noise.SPL_prop_broadband_1_3_spectrum 
    Results.SPL_broadband_1_3_spectrum_dBA                = A_weighting_metric(Results.SPL_broadband_1_3_spectrum,settings.center_frequencies)
    
    # A-weighted
    conditions.noise[distributor.tag][propulsor.tag][rotor.tag] = Results 
    return  
