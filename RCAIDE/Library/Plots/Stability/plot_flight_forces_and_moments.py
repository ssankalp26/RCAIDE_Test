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
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Intertial_Forces_and_Moments",
                             file_type = ".png",
                             width = 12, height = 8):
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
  
    
    fig1   = plt.figure(save_filename+ "_X_Force")
    fig2   = plt.figure(save_filename+"_Roll_Moment")
    fig3   = plt.figure(save_filename+"_Y_Force")
    fig4   = plt.figure(save_filename+"_Pitch_Moment")
    fig5   = plt.figure(save_filename+"_Z_Force")
    fig6   = plt.figure(save_filename+"_Yaw_Moment")
    
    fig1.set_size_inches(width,height)
    fig2.set_size_inches(width,height)
    fig3.set_size_inches(width,height)
    fig4.set_size_inches(width,height)
    fig5.set_size_inches(width,height)
    fig6.set_size_inches(width,height) 

    axis_1 = plt.subplot(1,1,1)
    axis_2 = plt.subplot(1,1,1)
    axis_3 = plt.subplot(1,1,1)
    axis_4 = plt.subplot(1,1,1)
    axis_5 = plt.subplot(1,1,1)  
    axis_6 = plt.subplot(1,1,1)    
    
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
        axis_1.plot(time,X, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_1.set_ylabel(r'X Moment (N)')
        axis_1.set_xlabel('Time (mins)')
        axis_1.set_ylim([-1000, 1000]) 
        set_axes(axis_1)                
        
        axis_2.set_ylabel(r'Roll Moment (Nm)')
        axis_2.set_xlabel('Time (mins)')
        axis_2.plot(time,L, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_2.set_ylim([-1000, 1000]) 
        set_axes(axis_2)     
        
        axis_3.plot(time,Y, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_3.set_ylabel(r'Y force (N)')
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylim([-1000, 1000]) 
        set_axes(axis_3)  
        
        axis_4.plot(time,M, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_4.set_ylabel(r'Pitch Moment (Nm)')
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylim([-1000, 1000]) 
        set_axes(axis_4) 

        axis_5.plot(time, Z, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_5.set_xlabel('Time (mins)')
        axis_5.set_ylabel(r'Z Force (m)')
        axis_5.set_ylim([-1000, 1000]) 
        set_axes(axis_5)    

        axis_6.plot(time, N, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_6.set_xlabel('Time (mins)')
        axis_6.set_ylabel(r'Yaw Moment (Nm)')
        axis_6.set_ylim([-1000, 1000]) 
        set_axes(axis_6)   
 
    if show_legend:    
        leg1 =  fig1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg2 =  fig2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg3 =  fig3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg4 =  fig4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg5 =  fig5.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg6 =  fig6.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        
        leg1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg5.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg6.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()
    fig4.tight_layout()
    fig5.tight_layout()
    fig6.tight_layout()
    
    fig1.subplots_adjust(top=0.8)
    fig2.subplots_adjust(top=0.8)
    fig3.subplots_adjust(top=0.8)
    fig4.subplots_adjust(top=0.8)
    fig5.subplots_adjust(top=0.8)
    fig6.subplots_adjust(top=0.8) 
    
    if save_figure:
        fig1.savefig(save_filename + "_X_Force"+ file_type)
        fig2.savefig(save_filename +"_Roll_Moment"+ file_type)
        fig3.savefig(save_filename +"_Y_Force"+ file_type)
        fig4.savefig(save_filename +"_Pitch_Moment"+ file_type)
        fig5.savefig(save_filename +"_Z_Force"+ file_type)
        fig6.savefig(save_filename +"_Yaw_Moment"+ file_type)  
    return fig1,  fig2,  fig3,  fig4,  fig5,  fig6
