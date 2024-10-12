# RCAIDE/Library/Plots/Thermal_Management/plot_wavy_channel_conditions.py
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
#   plot_wavy_channel_conditions
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Thermal_Management
def plot_wavy_channel_conditions(wavy_channel, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the Wavy Channel Heat Acqusition conditions throughout flight.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results.segments.conditions.energy[coolant_line.tag][wavy_channel.tag].
                                                                       outlet_coolant_temperature
                                                                       coolant_mass_flow_rate
                                                                       power
                                                                
                                                                       
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
    
    fig_1 = plt.figure(save_filename + '_Coolant_Temp' )
    fig_2 = plt.figure(save_filename + '_Coolant_Flowrate')
    fig_3 = plt.figure(save_filename + '_Power')
    fig_1.set_size_inches(width,height)
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
     
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1) 
    axis_3 = fig_3.add_subplot(1,1,1)
    
    b_i = 0  
    
    for i in range(len(results.segments)):  
        time                            = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
        wavy_channel_conditions         = results.segments[i].conditions.energy[coolant_line.tag][wavy_channel.tag]   
        outlet_coolant_temperature      = wavy_channel_conditions.outlet_coolant_temperature[:,0]
        coolant_mass_flow_rate          = wavy_channel_conditions.coolant_mass_flow_rate[:,0]
        power                           = wavy_channel_conditions.power[:,0]         
        segment_tag                     = results.segments[i].tag
        segment_name                    = segment_tag.replace('_', ' ') 
 
        axis_1.plot(time, outlet_coolant_temperature, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        axis_1.set_ylabel(r'Coolant Temp. (K)') 
        axis_1.set_xlabel(r'Time (mins)')
        set_axes(axis_1)     
         
        axis_2.plot(time, coolant_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_2.set_ylabel(r'Coolant $\dot{m}$ (kg/s)')
        axis_2.set_xlabel(r'Time (mins)')
        set_axes(axis_2) 
 
        axis_3.plot(time, power, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_3.set_ylabel(r'Power (W)')
        axis_3.set_xlabel(r'Time (mins)')
        set_axes(axis_3)   
                          
    b_i += 1 
            
    if show_legend:          
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})   
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        leg_3 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})      
    
    fig_1.tight_layout()    
    fig_2.tight_layout()    
    fig_3.tight_layout()
        
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8) 
    fig_2.subplots_adjust(top=0.8) 
    fig_3.subplots_adjust(top=0.8)
    
    
    if save_figure:
        fig_1.savefig(wavy_channel.tag + 'Coolant_Temp' + file_type) 
        fig_2.savefig(wavy_channel.tag + 'Coolant_Flowrate' + file_type) 
        fig_3.savefig(wavy_channel.tag + 'Power' + file_type)    
    return fig_1,  fig_2, fig_3