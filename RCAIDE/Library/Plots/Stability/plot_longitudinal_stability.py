## @ingroup Library-Plots-Performance-Stability  
# RCAIDE/Library/Plots/Performance/Stability/plot_longitudinal_stability.py
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
## @ingroup Library-Plots-Performance-Stability
def plot_longitudinal_stability(results,
                             save_figure = False,
                             show_legend=True,
                             save_filename = "Longitudinal_Stability",
                             file_type = ".png",
                             width = 8, height = 6):
    """This plots the static stability characteristics of an aircraft 
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
     
    fig1   = plt.figure(save_filename+"_Cm")
    fig2   = plt.figure(save_filename+"CM/alpha")
    fig3   = plt.figure(save_filename+"_Static_Margin")
    fig4   = plt.figure(save_filename+"_Elevator_Deflection")
    fig5   = plt.figure(save_filename+"_Cm/Delta")
    fig6   = plt.figure(save_filename+"_Cl/Alpha")
    
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
        time       = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        c_m        = results.segments[i].conditions.static_stability.coefficients.M[:,0]   
        SM         = results.segments[i].conditions.static_stability.static_margin[:,0]  
        delta_e    = results.segments[i].conditions.control_surfaces.elevator.deflection[:,0] / Units.deg
        CM_delta_e = results.segments[i].conditions.static_stability.derivatives.CM_delta_e[:,0]
        Cm_alpha   = results.segments[i].conditions.static_stability.derivatives.CM_alpha[:,0]
        CL_alpha   = results.segments[i].conditions.static_stability.derivatives.Clift_alpha[:,0] 
          
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')  
        
        axis_1.plot(time, c_m, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_1.set_ylabel(r'$C_M$')
        axis_1.set_xlabel('Time (mins)')
        axis_1.set_ylim([-1, 1])  
        set_axes(axis_1) 

        axis_2.plot(time, Cm_alpha, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        axis_2.set_ylabel(r'$C_M\alpha$')
        axis_2.set_xlabel('Time (mins)')
        axis_2.set_ylim([-1, 1]) 
        set_axes(axis_2) 
        
        axis_3.plot(time,SM , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Static Margin (%)')
        set_axes(axis_3)  

        axis_4.plot(time,delta_e , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Elevator Defl.n') 
        axis_4.set_ylim([-15, 15]) 
        set_axes(axis_4) 
        
        axis_5.plot(time,CM_delta_e , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_5.set_xlabel('Time (mins)')
        axis_5.set_ylabel(r'$C_M\delta_e$')
        axis_5.set_ylim([-1, 1]) 
        set_axes(axis_5)
        
        axis_6.plot(time,CL_alpha, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_6.set_xlabel('Time (mins)')
        axis_6.set_ylabel(r'$C_L\alpha$')
        axis_6.set_ylim([-5, 5]) 
        set_axes(axis_6)    
        
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
    
          
    # Adjusting the sub-plots for legend 
    fig1.subplots_adjust(top=0.8)
    fig2.subplots_adjust(top=0.8)
    fig3.subplots_adjust(top=0.8)
    fig4.subplots_adjust(top=0.8)
    fig5.subplots_adjust(top=0.8)
    fig6.subplots_adjust(top=0.8)
    

 
    if save_figure:
        fig1.savefig(save_filename +"_Cm"+ file_type)
        fig2.savefig(save_filename +"CM/alpha"+ file_type)
        fig3.savefig(save_filename +"_Static_Margin"+ file_type)
        fig4.savefig(save_filename +"_Elevator_Deflection"+ file_type)
        fig5.savefig(save_filename +"_Cm/Delta"+ file_type)
        fig6.savefig(save_filename +"_Cl/Alpha"+ file_type)   
    return fig1,  fig2,  fig3,  fig4,  fig5,  fig6
 