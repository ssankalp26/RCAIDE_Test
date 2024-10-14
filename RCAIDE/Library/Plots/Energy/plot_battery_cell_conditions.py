## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_battery_cell_conditions.py
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
## @ingroup Library-Plots-Energy
def plot_battery_cell_conditions(results,
                                  save_figure = False,
                                  show_legend = True,
                                  save_filename = "Battery_Cell_Conditions",
                                  file_type = ".png",
                                  width = 8, height = 6):
    """Plots the cell-level conditions of the battery throughout flight.

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
    
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))    
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1) 
    axis_3 = fig_3.add_subplot(1,1,1) 
    axis_4 = fig_4.add_subplot(1,1,1)
    axis_5 = fig_5.add_subplot(1,1,1) 
    axis_6 = fig_6.add_subplot(1,1,1)                              
           
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses
        for bus in busses: 
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_batteries == False: 
                    for i in range(len(results.segments)):  
                        time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
                        battery_conditions  = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]    
                        cell_power          = battery_conditions.cell.power[:,0]
                        cell_energy         = battery_conditions.cell.energy[:,0]
                        cell_volts          = battery_conditions.cell.voltage_under_load[:,0] 
                        cell_current        = battery_conditions.cell.current[:,0]
                        cell_SOC            = battery_conditions.cell.state_of_charge[:,0]   
                        cell_temperature    = battery_conditions.cell.temperature[:,0]   
                        
                        if i == 0: 
                            axis_1.plot(time, cell_SOC, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag) 
                        else:
                            axis_1.plot(time, cell_SOC, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width) 
                        axis_1.set_ylabel(r'SOC')
                        axis_1.set_xlabel('Time (mins)') 
                        axis_1.set_ylim([0,1.1])
                        set_axes(axis_1)     
                       
                        if i == 0: 
                            axis_2.plot(time, cell_energy/Units.Wh, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_2.plot(time, cell_energy/Units.Wh, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )
                        axis_2.set_ylabel(r'Energy (W-hr)')
                        axis_2.set_xlabel('Time (mins)') 
                        set_axes(axis_2) 
                 
                        if i == 0: 
                            axis_3.plot(time, cell_current, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_3.plot(time, cell_current, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )
                        axis_3.set_ylabel(r'Current (A)')
                        axis_3.set_xlabel('Time (mins)') 
                        set_axes(axis_3)
                        
                        if i == 0: 
                            axis_4.plot(time, cell_power, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_4.plot(time, cell_power, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )
                        axis_4.set_ylabel(r'Power (W)')
                        axis_4.set_xlabel('Time (mins)') 
                        set_axes(axis_4)     
                         
                        if i == 0: 
                            axis_5.plot(time, cell_volts, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag) 
                        else:
                            axis_5.plot(time, cell_volts, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width ) 
                        axis_5.set_ylabel(r'Voltage (V)')
                        axis_5.set_xlabel('Time (mins)') 
                        set_axes(axis_5) 
                 
                        if i == 0: 
                            axis_6.plot(time, cell_temperature, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_6.plot(time, cell_temperature, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )
                        axis_6.set_ylabel(r'Temperature, $\degree$C')
                        axis_6.set_xlabel('Time (mins)') 
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
 
    
    # Adjusting the sub-plots for legend 
    fig_1.tight_layout()    
    fig_2.tight_layout()    
    fig_3.tight_layout()    
    fig_4.tight_layout()    
    fig_5.tight_layout()    
    fig_6.tight_layout()   
    
    fig_1.subplots_adjust(top=0.8)  
    fig_2.subplots_adjust(top=0.8)  
    fig_3.subplots_adjust(top=0.8)  
    fig_4.subplots_adjust(top=0.8)  
    fig_5.subplots_adjust(top=0.8)  
    fig_6.subplots_adjust(top=0.8)
    
    if save_figure:
        fig_1.savefig(battery.tag + '_' + save_filename + '_SOC' + file_type)
        fig_2.savefig(battery.tag + '_' + save_filename + '_Energy'  + file_type)
        fig_3.savefig(battery.tag + '_' + save_filename + '_Current'  + file_type)
        fig_4.savefig(battery.tag + '_' + save_filename + '_Power'  + file_type)
        fig_5.savefig(battery.tag + '_' + save_filename + '_Voltage'  + file_type)
        fig_6.savefig(battery.tag + '_' + save_filename + '_Temperature'  + file_type)
    return fig_1,fig_2,fig_2,fig_3,fig_4,fig_5,fig_6