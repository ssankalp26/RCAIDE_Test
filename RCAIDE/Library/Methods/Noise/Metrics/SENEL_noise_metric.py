## @ingroup Methods-Noise-Metrics
# RCAIDE/Methods/Noise/Metrics/SENEL_noise_metric.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
from RCAIDE.Framework.Core import Units 
from RCAIDE.Library.Methods.Noise.Common.decibel_arithmetic   import SPL_arithmetic
from RCAIDE.Library.Methods.Noise.Common.background_noise     import background_noise

# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
# SENEL_noise_metric
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Methods-Noise-Metrics 
def SENEL_noise_metric(noise_data, flight_times = ['12:00:00'],time_period  = ['06:00:00','20:00:00']):
    """This method calculates the Single Event Noise Exposure Level at all points in the computational domain

    Assumptions:
        None

    Source:
        None  
    
    Inputs: 
        SPL      - Noise level 
        
    Outputs: 
        SENEL    - Single Event Noise Exposure Level            [SENEL]
        
    Properties Used:
        N/A     
    """       
    t_start   = float(time_period[0].split(':')[0])*60*60 + float(time_period[0].split(':')[1])*60 +  float(time_period[0].split(':')[2])
    t_end     = float(time_period[1].split(':')[0])*60*60 + float(time_period[1].split(':')[1])*60 +  float(time_period[1].split(':')[2])    
     
 
    SPL        = np.zeros_like(noise_data.SPL_dBA)
    SPL[:,:,:] = noise_data.SPL_dBA       
    t          = noise_data.time  
    N_gm_y     = noise_data.microphone_y_resolution   
    N_gm_x     = noise_data.microphone_x_resolution    
    time_step  = t[1]-t[0]
    
    # Compute Day-Night Sound Level and Noise Equivalent Noise   
    number_of_flights       = len(flight_times) 
    T                       = t_end - t_start
    number_of_timesteps     = int(T/time_step) 
 
    TNE = np.zeros((number_of_timesteps,N_gm_x,N_gm_y))* (10**(background_noise()/10))  # cumulative noise exposure 
    for i in range(number_of_flights): 
        # get start time of flight
        t0                      = int((float(flight_times[i].split(':')[0])*60*60 +  float(flight_times[i].split(':')[1])*60 +   float(flight_times[i].split(':')[2]) - 6*Units.hours)/time_step)    
        p_prefs_A               = time_step *  (10**(TNE[t0:t0+len(t)][:,:,:,None]/10))
        p_prefs_B               = time_step *  (10**(SPL[:,:,:,None]/10))
        C                       = np.concatenate((p_prefs_A,p_prefs_B),axis = 3)
        TNE[t0:t0+len(t)]       = 10*np.log10(np.nansum(C,axis=3))  
        TNE[t0:t0+len(t)]       = SPL_arithmetic(np.concatenate((TNE[t0:t0+len(t)][:,:,:,None] , SPL[:,:,:,None]), axis=3), sum_axis=3) 
             
    # get matrix of maximum noise levels 
    SPL_max = np.max(TNE,axis = 0)
    
    # subtract 10 db to get bounds 
    SPL_max_min10 = SPL_max - 10
    
    # mask all noise values that are lower than L-10 level
    SPL_valid  = np.ma.masked_array(TNE, TNE >SPL_max_min10)
    SENEL      = SPL_arithmetic(SPL_valid,sum_axis=0)   
    
    # sum the noise 
    noise_data.SENEL                   = SENEL  
     
    return  