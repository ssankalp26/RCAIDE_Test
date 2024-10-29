## @ingroup Methods-Noise-Metrics 
# RCAIDE/Methods/Noise/Metrics/Equivalent_noise_metric.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
from RCAIDE.Framework.Core import Units 
from RCAIDE.Library.Methods.Noise.Common.background_noise     import background_noise

# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Equivalent_noise_metric
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Methods-Noise-Metrics  
def DNL_and_Equivalent_noise_metric(noise_data, flight_times = ['12:00:00'],time_period = ['06:00:00','20:00:00']):   
    """This method calculates the Average A-weighted Sound Level, LAeqT,
    also known as the equivalent continuous noise level and the Day-Night Average Sound Level 
    
    Assumptions:  
        Flights occure between 6:00 and 9:00 pm (i.e. a 15 hour window)

    Source:
        None

    Inputs:
       noise_data  - post-processed noise data structure 

    Outputs: [dB]
       noise_data  - post-processed noise data structure 

    Properties Used:
        N/A  
    """
    
    # determine start and end of time period

    DNL_time_period           = ['07:00:00','20:00:00']
    t_7am                     = float(DNL_time_period[0].split(':')[0])*60*60 + float(DNL_time_period[0].split(':')[1])*60 +  float(DNL_time_period[0].split(':')[2])
    t_10pm                    = float(DNL_time_period[1].split(':')[0])*60*60 + float(DNL_time_period[1].split(':')[1])*60 +  float(DNL_time_period[1].split(':')[2])            
    t_start                   = float(time_period[0].split(':')[0])*60*60 + float(time_period[0].split(':')[1])*60 +  float(time_period[0].split(':')[2])
    t_end                     = float(time_period[1].split(':')[0])*60*60 + float(time_period[1].split(':')[1])*60 +  float(time_period[1].split(':')[2])     
    SPL                       = noise_data.SPL_dBA    
    N_gm_y                    = noise_data.microphone_y_resolution   
    N_gm_x                    = noise_data.microphone_x_resolution    
    time_step                 = noise_data.time[1]-noise_data.time[0] 
    number_of_flights         = len(flight_times)   
    p_div_p_ref_sq_L_eq    = np.zeros((N_gm_x,N_gm_y)) 
    p_div_p_ref_sq_L_24hr  = np.zeros((N_gm_x,N_gm_y))
    p_div_p_ref_sq_L_dn    = np.zeros((N_gm_x,N_gm_y)) 
      
    ambient_noise_duration      = t_end - t_start  
    ambient_noise_duration_24hr = 24 * Units.hrs 
    for i in range(number_of_flights):   
        t_flight_during_day  = float(flight_times[i].split(':')[0])*60*60 +  float(flight_times[i].split(':')[1])*60 +  float(flight_times[i].split(':')[2]) + noise_data.time
        
        # compute ambient noise duration 
        ambient_noise_duration  -= noise_data.time[-1]
        ambient_noise_duration_24hr -= noise_data.time[-1]

        # create noise penalty 
        noise_penality          = np.zeros((len(noise_data.time),N_gm_x,N_gm_y))         
        noise_penality[t_flight_during_day<t_7am]  = 10
        noise_penality[t_flight_during_day>t_10pm] = 10         
        
        # convert SPL to pressure and multiply by duration 
        p_sq_ref_flight_sq     = np.nansum(time_step * (10**(SPL/10)), axis=0)   
        p_sq_ref_flight_sq_dn  = np.nansum(time_step * (10**( (noise_penality + SPL)/10)), axis=0)  
    
        # add to current  
        p_div_p_ref_sq_L_eq    = np.nansum(np.concatenate((p_sq_ref_flight_sq[:,:,None],p_div_p_ref_sq_L_eq[:,:,None]),axis = 2), axis =2)
        p_div_p_ref_sq_L_24hr  = np.nansum(np.concatenate((p_sq_ref_flight_sq[:,:,None],p_div_p_ref_sq_L_24hr[:,:,None]),axis = 2), axis =2)
        p_div_p_ref_sq_L_dn    = np.nansum(np.concatenate((p_sq_ref_flight_sq_dn[:,:,None],p_div_p_ref_sq_L_dn[:,:,None]),axis = 2), axis =2)
 
    
    # add on background noise for remainder of time
    ambient_noise_duration      =  np.maximum(ambient_noise_duration,0)
    ambient_noise_duration_24hr =  np.maximum(ambient_noise_duration_24hr,0)
    p_div_p_ref_sq_L_eq   += ambient_noise_duration *  (10**(background_noise()/10))
    p_div_p_ref_sq_L_24hr += ambient_noise_duration_24hr *  (10**(background_noise()/10))
    p_div_p_ref_sq_L_dn   += ambient_noise_duration *  (10**(background_noise()/10))
    
    noise_data.L_eq      = 10*np.log10((1/(t_end-t_start))*p_div_p_ref_sq_L_eq)
    noise_data.L_eq_24hr = 10*np.log10((1/(24*Units.hours))*p_div_p_ref_sq_L_24hr)   
    noise_data.L_dn      = 10*np.log10((1/(t_end-t_start))*p_div_p_ref_sq_L_dn)
      
    return  
