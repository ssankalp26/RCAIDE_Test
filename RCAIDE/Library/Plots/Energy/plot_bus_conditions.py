## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_bus_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Energy
def plot_bus_conditions(results,
                                 save_figure=False,
                                 show_legend = True,
                                 save_filename="Bus_Conditions",
                                 file_type=".png",
                                 width = 8, height = 6):
    """Plots the pack-level conditions of the battery throughout flight.

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
        freestream.altitude
        weights.total_mass
        weights.vehicle_mass_rate
        frames.body.thrust_force_vector

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


    fig_1 = plt.figure(save_filename + '_SOC')
    fig_2 = plt.figure(save_filename + '_Energy')
    fig_3 = plt.figure(save_filename + '_Current')
    fig_4 = plt.figure(save_filename + '_Power')
    fig_5 = plt.figure(save_filename + '_Voltage')
    fig_6 = plt.figure(save_filename + '_Temperature')
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
    b_i = 0 
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses
        for bus in busses:  
           
            for i in range(len(results.segments)): 
                time                = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
                bus_results         = results.segments[i].conditions.energy[bus.tag] 
                pack_energy         = bus_results.energy[:,0] 
                pack_power          = bus_results.power_draw[:,0]
                pack_volts          = bus_results.voltage_under_load [:,0] 
                pack_current        = bus_results.current_draw[:,0]
                pack_SOC            = bus_results.SOC[:,0] 
                pack_temperature    = bus_results.temperature[:,0]  
        
                segment_tag  =  results.segments[i].tag
                segment_name = segment_tag.replace('_', ' ')   
                axis_1.plot(time, pack_SOC, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                axis_1.set_ylabel(r'SOC')
                axis_1.set_xlabel('Time (mins)')
                axis_1.set_ylim([0,1.1])
                set_axes(axis_1)     
                
                axis_2.plot(time, (pack_energy/1000)/Units.Wh, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                axis_2.set_ylabel(r'Energy (kW-hr)')
                axis_2.set_xlabel('Time (mins)')
                set_axes(axis_2)
                
                axis_3.plot(time, pack_current, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                axis_3.set_ylabel(r'Current (A)')
                axis_3.set_xlabel('Time (mins)')
                set_axes(axis_3)  
         
                axis_4.plot(time, pack_power/1000, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
                axis_4.set_ylabel(r'Power (kW)')
                axis_4.set_xlabel('Time (mins)')
                set_axes(axis_4)     
                 
                axis_5.plot(time, pack_volts, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                axis_5.set_ylabel(r'Voltage (V)')
                axis_5.set_xlabel('Time (mins)')
                set_axes(axis_5) 
         
                axis_6.plot(time, pack_temperature, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                axis_6.set_ylabel(r'Temperature, $\degree$C')
                axis_6.set_xlabel('Time (mins)')
                set_axes(axis_6)   

            b_i += 1 
            
    if show_legend:      
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_4 =  fig_4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_5 =  fig_5.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_6 =  fig_6.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
        leg_4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
        leg_5.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
        leg_6.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})      
    
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8) 
    fig_2.subplots_adjust(top=0.8) 
    fig_3.subplots_adjust(top=0.8) 
    fig_4.subplots_adjust(top=0.8) 
    fig_5.subplots_adjust(top=0.8) 
    fig_6.subplots_adjust(top=0.8)   
    
    if save_figure:
        fig_1.savefig(bus.tag + 'Conditions_SOC' + file_type)
        fig_2.savefig(bus.tag + 'Conditions_Energy' + file_type)
        fig_3.savefig(bus.tag + 'Conditions_Current' + file_type)
        fig_4.savefig(bus.tag + 'Conditions_Power'  + file_type)
        fig_5.savefig(bus.tag + 'Conditions_Voltage' + file_type)
        fig_6.savefig(bus.tag + 'Conditions_Temperature' + file_type)
   
    return fig_1,fig_2, fig_3, fig_4, fig_5, fig_6


