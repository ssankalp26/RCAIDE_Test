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
import RCAIDE
from RCAIDE.Framework.Core import Data , Units 
from RCAIDE.Library.Methods.Noise.Common.background_noise     import background_noise
from RCAIDE.Library.Methods.Noise.Metrics import * 
from RCAIDE.Library.Methods.Noise.Common.generate_zero_elevation_microphone_locations import generate_zero_elevation_microphone_locations 
from RCAIDE.Library.Methods.Noise.Common.generate_terrain_microphone_locations        import generate_terrain_microphone_locations     
from RCAIDE.Library.Methods.Noise.Common.compute_relative_noise_evaluation_locations  import compute_relative_noise_evaluation_locations
from RCAIDE.Library.Methods.Geodesics.compute_point_to_point_geospacial_data          import compute_point_to_point_geospacial_data

# package imports
import numpy as np
from scipy.interpolate                                           import RegularGridInterpolator


# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Library-Plots-Geometry-Common
def post_process_noise_data(results,
                            flight_times = np.array(['06:00:00','06:30:00','07:00:00','07:30:00','08:00:00','08:30:00',
                                                     '09:00:00','09:30:00','10:00:00','10:30:00','11:00:00','11:30:00',
                                                     '12:00:00','12:30:00','13:00:00','13:30:00','14:00:00','14:30:00',
                                                     '15:00:00']),
                            time_period        = ['06:00:00','20:00:00'], 
                            compute_L_dn       = True, 
                            compute_SENEL      = True,    
                            compute_L_eq     = True,): 
    """This translates all noise data into metadata for plotting 
    
    Assumptions:
    None
    
    Source: 
 
    Inputs: results 
         
    Outputs: noise_data
    
    Properties Used:
    N/A
    """

    # Step 1: Unpack settings      
    settings   = results.segments[0].analyses.noise.settings
    N_gm_x     = settings.microphone_x_resolution
    N_gm_y     = settings.microphone_y_resolution    
    noise_data = Data()   
     
    # Step 2: Determing microhpone points where noise is to be computed
    microphone_coordinates =  None
    if settings.topography_file !=  None:
        compute_point_to_point_geospacial_data(settings)
        microphone_locations ,microphone_coordinates = generate_terrain_microphone_locations(settings) 
        noise_data.topography_file                    = settings.topography_file  
        noise_data.microphone_coordinates             = microphone_coordinates.reshape(N_gm_x,N_gm_y,3)     
        noise_data.aircraft_origin_coordinates        = settings.aircraft_origin_coordinates          
        noise_data.aircraft_destination_coordinates   = settings.aircraft_destination_coordinates         
    else:    
        microphone_locations =  generate_zero_elevation_microphone_locations(settings)   
    noise_data.microphone_y_resolution       = N_gm_y
    noise_data.microphone_x_resolution       = N_gm_x              
    noise_data.microphone_locations          = microphone_locations.reshape(N_gm_x,N_gm_y,3)         
    
    # Step 3: Create empty arrays to store noise data 
    num_fligth_segs = len(results.segments)
    num_gm_mic      = len(microphone_locations)
    num_noise_time  = settings.noise_times_steps 
    
    # Step 4: Initalize Arrays 
    N_ctrl_pts            = ( num_fligth_segs-1) * (num_noise_time -1) + num_noise_time # ensures that noise is computed continuously across segments 
    SPL_dBA               = np.ones((N_ctrl_pts,N_gm_x,N_gm_y))*background_noise()  
    Aircraft_pos          = np.zeros((N_ctrl_pts,3))  
    Time                  = np.zeros(N_ctrl_pts)   

    starting_index = 0
    ending_index   = num_noise_time
    
    # Step 5: loop through segments and store noise 
    for seg in range(num_fligth_segs):  
        segment    = results.segments[seg]
        settings   = segment.analyses.noise.settings  
        phi        = settings.noise_hemisphere_phi_angles
        theta      = settings.noise_hemisphere_theta_angles
        n          = settings.number_of_microphone_in_stencil
        conditions = segment.state.conditions  
        time       = conditions.frames.inertial.time[:,0]
        
        # Step 5.1 : Compute relative microhpone locations 
        noise_time,noise_pos,RML,PHI,THETA,num_gm_mic  = compute_relative_noise_evaluation_locations(settings, microphone_locations,segment) 
         
        # Step 5.2: Compute aircraft position and npose at interpolated hemisphere locations
        cpt   = 0 
        if seg == (num_fligth_segs - 1):
            noise_time_ = noise_time 
        else:
            noise_time_ = noise_time[:,-1] 
    
        Aircraft_pos[starting_index:ending_index] = noise_pos
        Time[starting_index:ending_index]         = noise_time  
        starting_index =+ len(noise_time_)
        ending_index   =+ len(noise_time_)
        
        for i in range(len(noise_time_)):
            # Step 5.2.1 :Noise interpolation 
            delta_t         = (noise_time[i] -time[cpt]) / (time[cpt+1] - time[cpt])
            SPL_lower       = conditions.noise.hemisphere_SPL_dBA[cpt].reshape(len(phi),len(theta))
            SPL_uppper      = conditions.noise.hemisphere_SPL_dBA[cpt+1].reshape(len(phi),len(theta))
            SPL_gradient    = SPL_uppper -  SPL_lower
            SPL_interp      = SPL_lower + SPL_gradient *delta_t
     
            #  Step 5.2.2 Create surrogate   
            SPL_dBA_surrogate = RegularGridInterpolator((phi, theta),SPL_interp  ,method = 'linear',   bounds_error=False, fill_value=None)       
            
            #  Step 5.2.3 Query surrogate
            R                 = np.linalg.norm(RML[i], axis=1) 
            locs              = np.argsort(R)[:n]
            pts               = (PHI[i][locs],THETA[i][locs]) 
            SPL_dBA_unscaled  = SPL_dBA_surrogate(pts) 
            
            #  Step 5.2.4 Scale data using radius  
            R_ref                = settings.noise_hemisphere_radius  
            SPL_dBA_scaled       = ((R_ref**2 )/ (R[locs] **2)) * SPL_dBA_unscaled  
            SPL_dBA_temp         = SPL_dBA[i].flatten()
            SPL_dBA_temp[locs]   = SPL_dBA_scaled
            SPL_dBA[i]           = SPL_dBA_temp.reshape(N_gm_x,N_gm_y)    

            if noise_time[i] >= time[cpt+1]:
                cpt += 1             
                
    # Step 6: Make any readings less that background noise equal to background noise
    SPL_dBA                             = np.nan_to_num(SPL_dBA) 
    SPL_dBA[SPL_dBA<background_noise()] = background_noise()  
     
    # Step 7: Store data 
    noise_data.SPL_dBA               = SPL_dBA
    noise_data.time                  = Time 
    noise_data.aircraft_position     = Aircraft_pos
    
    # Step 8: Perform noise metric calculations
    if compute_L_eq or compute_L_dn:
        DNL_time_period         = ['07:00:00','20:00:00']
        t_7am                   = float(DNL_time_period[0].split(':')[0])*60*60 + float(DNL_time_period[0].split(':')[1])*60 +  float(DNL_time_period[0].split(':')[2])
        t_10pm                  = float(DNL_time_period[1].split(':')[0])*60*60 + float(DNL_time_period[1].split(':')[1])*60 +  float(DNL_time_period[1].split(':')[2])            
        t_start                 = float(time_period[0].split(':')[0])*60*60 + float(time_period[0].split(':')[1])*60 +  float(time_period[0].split(':')[2])
        t_end                   = float(time_period[1].split(':')[0])*60*60 + float(time_period[1].split(':')[1])*60 +  float(time_period[1].split(':')[2])    
        SPL                     = np.zeros_like(noise_data.SPL_dBA)
        SPL[:,:,:]              = noise_data.SPL_dBA      
        N_gm_y                  = noise_data.microphone_y_resolution   
        N_gm_x                  = noise_data.microphone_x_resolution    
        time_step               = noise_data.time[1]-noise_data.time[0] 
        number_of_flights       = len(flight_times)   
        p_sq_div_p_ref_sq_L_eq  = np.zeros((N_gm_x,N_gm_y))* (10**(background_noise()/10))
        p_sq_div_p_ref_sq_L_dn  = np.zeros((N_gm_x,N_gm_y))* (10**(background_noise()/10))
          
        for i in range(number_of_flights):   
            t_flight_during_day  = float(flight_times[i].split(':')[0])*60*60 +  float(flight_times[i].split(':')[1])*60 +  float(flight_times[i].split(':')[2]) + noise_data.time
            
            # convert SPL to pressure and multiply by duration 
            p_sq_ref_flight_sq        = np.nansum(time_step * (10**(SPL/10)), axis=0)  
            
            # add to current 
            p_sq_div_p_ref_sq_L_eq    = np.nansum(np.concatenate((p_sq_ref_flight_sq[:,:,None],p_sq_div_p_ref_sq_L_eq[:,:,None]),axis = 2), axis =2)
             
            # create noise penalty 
            noise_penality          = np.zeros((len(noise_data.time),N_gm_x,N_gm_y))         
            noise_penality[t_flight_during_day<t_7am]  = 10
            noise_penality[t_flight_during_day>t_10pm] = 10 
         
            # convert SPL to pressure and multiply by duration 
            p_sq_ref_flight_sq        = np.nansum(time_step * (10**( (noise_penality + SPL)/10)), axis=0)  
        
            # add to current 
            p_sq_div_p_ref_sq_L_dn   = np.nansum(np.concatenate((p_sq_ref_flight_sq[:,:,None],p_sq_div_p_ref_sq_L_dn[:,:,None]),axis = 2), axis =2)
    
             
        noise_data.L_eq      = 10*np.log10((1/(t_end-t_start))*p_sq_div_p_ref_sq_L_eq)
        noise_data.L_eq_24hr = 10*np.log10((1/(24*Units.hours))*p_sq_div_p_ref_sq_L_eq)   
        noise_data.L_dn      = 10*np.log10((1/(24*Units.hours))*p_sq_div_p_ref_sq_L_dn)
 
    if compute_SENEL:
        SENEL_noise_metric(noise_data, flight_times,time_period)
    if compute_L_dn or compute_L_eq:
        DNL_and_Equivalent_noise_metric(noise_data, flight_times)
    
    return noise_data