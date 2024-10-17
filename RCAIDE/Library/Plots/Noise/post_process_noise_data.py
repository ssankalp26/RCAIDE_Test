## @ingroup Library-Plots-Geometry-Common
# RCAIDE/Library/Plots/Noise/post_process_noise_dat.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Framework.Core import Data , Units 
from RCAIDE.Library.Methods.Noise.Common.background_noise     import background_noise
from RCAIDE.Library.Methods.Noise.Metrics import * 

import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Library-Plots-Geometry-Common
def post_process_noise_data(results,
                            flight_times = np.array(['06:00:00','06:30:00','07:00:00','07:30:00','08:00:00','08:30:00',
                                                     '09:00:00','09:30:00','10:00:00','10:30:00','11:00:00','11:30:00',
                                                     '12:00:00','12:30:00','13:00:00','13:30:00','14:00:00','14:30:00',
                                                     '15:00:00']), 
                            DNL_time_period    = 24*Units.hours,
                            LAeqt_time_period  = 15*Units.hours,
                            SENEL_time_period  = 24*Units.hours): 
    """This translates all noise data into metadata for plotting 
    
    Assumptions:
    None
    
    Source: 
 
    Inputs: results 
         
    Outputs: noise_data
    
    Properties Used:
    N/A
    """

    # unpack 
    background_noise_dbA = background_noise() 
    N_ctrl_pts = 1
    for j in range(len(results.segments)): 
        N_ctrl_pts  += len(results.segments[j].conditions.frames.inertial.time[:,0]) - 1 
    N_gm_x                = results.segments[0].analyses.noise.settings.microphone_x_resolution
    N_gm_y                = results.segments[0].analyses.noise.settings.microphone_y_resolution     
    SPL_dBA_old           = np.zeros((N_ctrl_pts ,N_gm_x,N_gm_y)) 
    time_old              = np.zeros(N_ctrl_pts)
    Aircraft_pos          = np.zeros((N_ctrl_pts,3)) 
    Mic_pos_gm            = results.segments[0].analyses.noise.settings.microphone_locations.reshape(N_gm_x,N_gm_y,3) 
    x0                    = results.segments[0].analyses.noise.settings.aircraft_origin_location[0]
    y0                    = results.segments[0].analyses.noise.settings.aircraft_origin_location[1]

    # Step 1: Merge data from all segments 
    idx = 0 
    for i in range(len(results.segments)): 
        if  type(results.segments[i]) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge:
            pass
        else:  
            if i == 0:  start = 0 
            else: start = 1                    
            seg_cpts  = len(results.segments[i].conditions.frames.inertial.time[:,0])  
            for j in range(start,seg_cpts): 
                time_old[idx]          = results.segments[i].conditions.frames.inertial.time[j,0]
                Aircraft_pos[idx,0]    = results.segments[i].conditions.frames.inertial.position_vector[j,0]  + x0
                Aircraft_pos[idx,1]    = results.segments[i].conditions.frames.inertial.position_vector[j,1]  + y0 
                x_idx                  = abs(Mic_pos_gm[:,0,0] - Aircraft_pos[idx,0]).argmin()
                y_idx                  = abs(Mic_pos_gm[0,:,1] - Aircraft_pos[idx,1]).argmin() 
                Aircraft_pos[idx,2]    = -results.segments[i].conditions.frames.inertial.position_vector[j,2] + Mic_pos_gm[x_idx,y_idx,2] 
                SPL_dBA_old[idx]       = results.segments[i].conditions.noise.SPL_dBA[j].reshape(N_gm_x,N_gm_y)
                idx  += 1
                
    # Step 2: Make any readings less that background noise equal to background noise
    SPL_dBA                               = np.nan_to_num(SPL_dBA_old) 
    SPL_dBA[SPL_dBA<background_noise_dbA] = background_noise_dbA  
     
    # store data 
    noise_data                           = Data() 
    noise_data.SPL_dBA                   = SPL_dBA_old # SPL_dBA_new  
    noise_data.time                      = time_old # t_new  
    noise_data.microphone_locations      = Mic_pos_gm
    if results.segments[0].analyses.noise.settings.topography_file  == None:
        noise_data.topography_file                  =  None
    else:
        noise_data.topography_file                  = results.segments[0].analyses.noise.settings.topography_file  
        noise_data.microphone_coordinates           = results.segments[0].analyses.noise.settings.microphone_coordinates.reshape(N_gm_x,N_gm_y,3)     
        noise_data.aircraft_origin_coordinates      = results.segments[0].analyses.noise.settings.aircraft_origin_coordinates          
        noise_data.aircraft_destination_coordinates = results.segments[0].analyses.noise.settings.aircraft_destination_coordinates    
    
    noise_data.microphone_y_resolution       = N_gm_y
    noise_data.microphone_x_resolution       = N_gm_x   
    noise_data.aircraft_position             = Aircraft_pos # Aircraft_pos_new              
    noise_data.aircraft_origin_location      = results.segments[0].analyses.noise.settings.aircraft_origin_location             
    noise_data.aircraft_destination_location = results.segments[0].analyses.noise.settings.aircraft_destination_location        
 
 
    noise_data  = Equivalent_noise_metric(noise_data, flight_times,LAeqt_time_period)
    noise_data  = SENEL_noise_metric(noise_data, flight_times,SENEL_time_period)
    noise_data  = DNL_noise_metric(noise_data, flight_times,DNL_time_period)
    
    return noise_data