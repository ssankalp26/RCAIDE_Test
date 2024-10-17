## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_battery_health_conditions.py
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
def plot_battery_temperature(results,
                                  save_figure = False,
                                  show_legend = True,
                                  save_filename = "Battery_Temperature",
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
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     

    fig_1 = plt.figure(save_filename)
    fig_2 = plt.figure(save_filename)
    fig_3 = plt.figure(save_filename)
    fig_1.set_size_inches(width,height)  
    fig_2.set_size_inches(width,height)  
    fig_3.set_size_inches(width,height)  
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1) 
    axis_3 = fig_3.add_subplot(1,1,1)
    
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses
        for bus in busses: 
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_batteries == False:                
                    for i in range(len(results.segments)):
                        bus_results         = results.segments[i].conditions.energy[bus.tag]
                        time                = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min                      
                        battery_conditions  = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]  
                        cell_temp           = battery_conditions.cell.temperature[:,0]
                        cell_charge         = battery_conditions.cell.charge_throughput[:,0]
                        pack_Q              = bus_results.heat_energy_generated[:,0]
                        
                        if i == 0: 
                            axis_1.plot(time,cell_temp, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag) 
                        else:
                            axis_1.plot(time,cell_temp, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width) 
                        axis_1.set_ylabel(r'Temperature (K)') 
                        axis_1.set_xlabel('Time (mins)')
                        set_axes(axis_1)
                        
                        if i == 0: 
                            axis_2.plot(time, cell_charge, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_2.plot(time, cell_charge, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )
                        axis_2.set_xlabel('Time (mins)')
                        axis_2.set_ylabel(r'Charge Throughput (Ah)')
                        set_axes(axis_2)
                        
                        if i == 0: 
                            axis_3.plot(time, pack_Q/1000, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_3.plot(time, pack_Q/1000, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width )   
                        axis_3.set_xlabel('Time (mins)')
                        axis_3.set_ylabel(r'$\dot{Q}_{heat}$ (kW)')
                        set_axes(axis_3) 
    
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
    
    fig_1.subplots_adjust(top=0.8) 
    fig_2.subplots_adjust(top=0.8) 
    fig_3.subplots_adjust(top=0.8)
    
    if save_figure:
        fig_1.savefig(save_filename  + file_type)   
        fig_2.savefig(save_filename  + file_type)   
        fig_3.savefig(save_filename  + file_type)   
    return fig_1, fig_2, fig_3