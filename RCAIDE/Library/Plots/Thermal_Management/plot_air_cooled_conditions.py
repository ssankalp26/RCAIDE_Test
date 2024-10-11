# RCAIDE/Library/Plots/Thermal_Management/plot_air_cooled_conditions.py
# 
# 
# Created:  Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#   plot_air_cooled_conditions
# ----------------------------------------------------------------------------------------------------------------------   
def plot_air_cooled_conditions(air_cooled, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the Air Cooled Heat Acqusition conditions throughout flight.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results.segments.conditions.energy[coolant_line.tag][air_cooled.tag].
                                                                       effectiveness
                                                                       total_heat_removed
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
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     

    fig_1 = plt.figure(save_filename + '_Effectivess')
    fig_2 = plt.figure(save_filename + '_Heat_Removed')
    fig_1.set_size_inches(width,height)  
    fig_2.set_size_inches(width,height)  
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1)        
    b_i = 0  
   
    for i in range(len(results.segments)):  
        time                       = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
        air_cooled_conditions      = results.segments[i].conditions.energy[coolant_line.tag][air_cooled.tag]   
        effectiveness              = air_cooled_conditions.effectiveness[:,0]
        total_heat_removed         = air_cooled_conditions.total_heat_removed[:,0]
        segment_tag                = results.segments[i].tag
        segment_name               = segment_tag.replace('_', ' ') 

                         
        axis_1.plot(time, effectiveness, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_1.set_ylabel(r'Effectiveness') 
        axis_1.set_xlabel(r'Time (mins)')
        set_axes(axis_1)     
         
        axis_2.plot(time, total_heat_removed, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_2.set_ylabel(r'Heat Removed (W)')
        axis_2.set_xlabel(r'Time (mins)')
        set_axes(axis_2) 
              
        b_i += 1 
            
    if show_legend:    
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})  
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})   
    
    fig_1.tight_layout()    
    fig_2.tight_layout()     
    
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8) 
    fig_2.subplots_adjust(top=0.8)  

    if save_figure:
        fig_1.savefig(save_filename + air_cooled.tag + file_type)    
        fig_2.savefig(save_filename + air_cooled.tag + file_type)    
    return fig_1,fig_2    