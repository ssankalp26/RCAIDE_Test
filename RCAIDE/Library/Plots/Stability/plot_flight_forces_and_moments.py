## @ingroup Library-Plots-Stability
# RCAIDE/Library/Plots/Stability/plot_stability_forces_and_moments.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Stability
def plot_flight_forces_and_moments(results,
                             save_figure   = False,
                             show_legend   = True,
                             save_filename = "Intertial_Forces_and_Moments",
                             file_type     = ".png",
                             width         = 8,
                             height        = 6):
    """This plots the aerodynamic forces 
    """ 

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     
  
    
    fig_1   = plt.figure(save_filename + '_X_Force')
    fig_2   = plt.figure(save_filename + '_Roll_Moment')
    fig_3   = plt.figure(save_filename + '_Y_Force')
    fig_4   = plt.figure(save_filename + '_Pitch_Moment')
    fig_5   = plt.figure(save_filename + '_Z_Force')
    fig_6   = plt.figure(save_filename + '_Yaw_Moment')
    fig_1.set_size_inches(width,height) 
    fig_2.set_size_inches(width,height) 
    fig_3.set_size_inches(width,height) 
    fig_4.set_size_inches(width,height) 
    fig_5.set_size_inches(width,height) 
    fig_6.set_size_inches(width,height)  

    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1)
    axis_3 = fig_3.add_subplot(1,1,1)
    axis_4 = fig_4.add_subplot(1,1,1)
    axis_5 = fig_5.add_subplot(1,1,1)  
    axis_6 = fig_6.add_subplot(1,1,1)    
    
    for i in range(len(results.segments)): 
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
        X = results.segments[i].conditions.frames.inertial.total_force_vector[:,0]
        Y = results.segments[i].conditions.frames.inertial.total_force_vector[:,1]
        Z = results.segments[i].conditions.frames.inertial.total_force_vector[:,2]
        L = results.segments[i].conditions.frames.inertial.total_moment_vector[:,0]
        M = results.segments[i].conditions.frames.inertial.total_moment_vector[:,1]
        N = results.segments[i].conditions.frames.inertial.total_moment_vector[:,2]
        
                       
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        axis_1.plot(time,X, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_1.set_ylabel(r'X Force (N)') 
        axis_1.set_xlabel('Time (mins)')        
        axis_1.set_ylim([-1000, 1000]) 
        set_axes(axis_1)                
        
        axis_2.set_ylabel(r'Roll Moment (Nm)')
        axis_2.set_xlabel('Time (mins)')
        axis_2.plot(time,L, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_2.set_ylim([-1000, 1000]) 
        set_axes(axis_2)     
        
        axis_3.plot(time,Y, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_3.set_ylabel(r'Y force (N)') 
        axis_3.set_xlabel('Time (mins)')        
        axis_3.set_ylim([-1000, 1000]) 
        set_axes(axis_3)  
        
        axis_4.plot(time,M, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_4.set_ylabel(r'Pitch Moment (Nm)')
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylim([-1000, 1000]) 
        set_axes(axis_4) 

        axis_5.plot(time, Z, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_5.set_xlabel('Time (mins)')
        axis_5.set_ylabel(r'Z Force (m)')
        axis_5.set_ylim([-1000, 1000]) 
        set_axes(axis_5)    

        axis_6.plot(time, N, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
        axis_6.set_xlabel('Time (mins)')
        axis_6.set_ylabel(r'Yaw Moment (Nm)')
        axis_6.set_ylim([-1000, 1000]) 
        set_axes(axis_6)   
 
    if show_legend:    
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_4 =  fig_4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_5 =  fig_5.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_6 =  fig_6.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_5.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_6.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    fig_1.tight_layout()
    fig_2.tight_layout()
    fig_3.tight_layout()
    fig_4.tight_layout()
    fig_5.tight_layout()
    fig_6.tight_layout()
        
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8)  
    fig_2.subplots_adjust(top=0.8) 
    fig_3.subplots_adjust(top=0.8) 
    fig_4.subplots_adjust(top=0.8) 
    fig_5.subplots_adjust(top=0.8) 
    fig_6.subplots_adjust(top=0.8)        
    
    if save_figure:
        fig_1.savefig(save_filename + '_X_Force' + file_type)  
        fig_2.savefig(save_filename + '_Roll_Moment' + file_type)   
        fig_3.savefig(save_filename + '_Y_Force' + file_type)   
        fig_4.savefig(save_filename + '_Pitch_Moment' + file_type)   
        fig_5.savefig(save_filename + '_Z_Force' + file_type)   
        fig_6.savefig(save_filename + '_Yaw_Moment'+ file_type)    
    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6
