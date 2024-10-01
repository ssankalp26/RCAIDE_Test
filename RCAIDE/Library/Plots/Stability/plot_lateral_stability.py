## @ingroup Library-Plots-Performance-Stability  
# RCAIDE/Library/Plots/Performance/Stability/plot_lateral_stability.py
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
def plot_lateral_stability(results,
                             save_figure = False,
                             show_legend=True,
                             save_filename = "Lateral_Stability",
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
     
    fig1   = plt.figure(save_filename+"_Bank_Angle")
    fig2   = plt.figure(save_filename+"_Aileron_Deflection")
    fig3   = plt.figure(save_filename+"_Rudder_Deflection")
    
    fig1.set_size_inches(width,height)
    fig2.set_size_inches(width,height)
    fig3.set_size_inches(width,height)
    
    axis_1 = plt.subplot(1,1,1) 
    axis_2 = plt.subplot(1,1,1)  
    axis_3 = plt.subplot(1,1,1)    
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min  
        phi      = results.segments[i].conditions.aerodynamics.angles.phi[:,0] / Units.deg          
        delta_a  = results.segments[i].conditions.control_surfaces.aileron.deflection[:,0] / Units.deg  
        delta_r  = results.segments[i].conditions.control_surfaces.rudder.deflection[:,0] / Units.deg   
          
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        axis_1.plot(time, phi, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name, markersize = ps.marker_size)
        axis_1.set_ylabel(r'$Bank Angle \phi$')
        axis_2.set_xlabel('Time (mins)')
        set_axes(axis_1)     

        axis_2.plot(time,delta_a , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name, markersize = ps.marker_size)
        axis_2.set_xlabel('Time (mins)')
        axis_2.set_ylabel(r'Aileron Defl. (deg)')
        set_axes(axis_2)  

        axis_3.plot(time,delta_r , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,  markersize = ps.marker_size)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Rudder Defl. (deg)')
        set_axes(axis_3)         
         
    if show_legend:
        leg1 =  fig1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg2 =  fig2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg3 =  fig3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        
        leg1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
    
    # Adjusting the sub-plots for legend
    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()
    
    fig1.subplots_adjust(top=0.8)
    fig2.subplots_adjust(top=0.8)
    fig3.subplots_adjust(top=0.8) 
 
    if save_figure:
        fig1.savefig(save_filename +"_Bank_Angle"+ file_type)
        fig2.savefig(save_filename +"_Aileron_Deflection"+ file_type)
        fig3.savefig(save_filename +"_Rudder_Deflection"+ file_type) 
    return fig1,fig2,fig3 