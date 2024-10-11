## @defgroup Library-Plots-Mission  
# RCAIDE/Library/Plots/Performance/Mission/plot_flight_trajectory.py
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
## @ingroup Library-Plots-Mission           
def plot_flight_trajectory(results,
                           line_color = 'bo-',
                           line_color2 = 'rs--',
                           save_figure = False,
                           show_legend   = True,
                           save_filename = "Flight_Trajectory",
                           file_type = ".png",
                           width = 8, height = 6):
    """This plots the 3D flight trajectory of the aircraft.

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
         frames 
             body.inertial_rotations
             inertial.position_vector 
         freestream.velocity
         aerodynamics.
             lift_coefficient
             drag_coefficient
             angle_of_attack
        
    Outputs: 
    Plots

    Properties Used:
    N/A	
    """	     

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters) 
        
    fig_1 = plt.figure(save_filename+"_Distance")
    fig_2 = plt.figure(save_filename + "_x_vs_y")
    fig_3 = plt.figure(save_filename+"_z_vs_time")
    fig_4 = plt.figure(save_filename+"_3D")
    
    fig_1.set_size_inches(width,height)
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
    fig_4.set_size_inches(width,height) 
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))    
     

    axis_1 = fig_1.add_subplot(1,1,1) 
    axis_2 = fig_2.add_subplot(1,1,1)    
    axis_3 = fig_3.add_subplot(1,1,1)
    axis_4 = fig_4.add_subplot(111, projection='3d')
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        Range    = results.segments[i].conditions.frames.inertial.aircraft_range[:,0]/Units.nmi
        x        = results.segments[i].conditions.frames.inertial.position_vector[:,0]  
        y        = results.segments[i].conditions.frames.inertial.position_vector[:,1] 
        z        = -results.segments[i].conditions.frames.inertial.position_vector[:,2] 

        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
         
        axis_1.plot( time , Range, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width , label = segment_name, markersize = ps.marker_size)
        axis_1.set_ylabel('Distance (nmi)')
        axis_1.set_xlabel('Time (min)')
        set_axes(axis_1)            
 
        axis_2.plot(x, y , line_color, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name , markersize = ps.marker_size)
        axis_2.set_xlabel('x (m)')
        axis_2.set_ylabel('y (m)')
        set_axes(axis_2)
 
        axis_3.plot( time , z, line_color , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name , markersize = ps.marker_size)
        axis_3.set_ylabel('z (m)')
        axis_3.set_xlabel('Time (min)')
        set_axes(axis_3)
        
        axis_4.scatter(x, y, z, marker='o',c=  line_colors[i],s = ps.marker_size)
        axis_4.set_xlabel('x')
        axis_4.set_ylabel('y')
        axis_4.set_zlabel('z')
        axis_4.set_box_aspect([1,1,1])
        set_axes(axis_4)         
        
    if show_legend:        
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4)  
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})  
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})  
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig_1.tight_layout()    
    fig_2.tight_layout()    
    fig_3.tight_layout()    
    fig_4.tight_layout()
    
    fig_1.subplots_adjust(top=0.8)
    fig_2.subplots_adjust(top=0.8)
    fig_3.subplots_adjust(top=0.8)
    fig_4.subplots_adjust(top=0.8)
    
    if save_figure:
        fig_1.savefig(save_filename + file_type)
        fig_2.savefig(save_filename + file_type)
        fig_3.savefig(save_filename + file_type)
        fig_4.savefig(save_filename + file_type)  
             
    return fig_1,fig_2,fig_3,fig_4         