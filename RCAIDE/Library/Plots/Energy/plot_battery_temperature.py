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
                                  width = 11, height = 7):
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

    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height)  
    axis_1 = plt.subplot(2,2,1)
    axis_2 = plt.subplot(2,2,2) 
    axis_3 = plt.subplot(2,2,3)     
 
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses 
        for  bus_i, bus in enumerate(busses):
            for b_i, battery in enumerate(bus.battery_modules):
                if b_i == 0 or bus.identical_battery_modules == False:
                    for i in range(len(results.segments)): 
                        bus_results         = results.segments[i].conditions.energy[bus.tag]
                        time                = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min                      
                        battery_conditions  = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]  
                        cell_temp           = battery_conditions.cell.temperature[:,0]
                        cell_charge         = battery_conditions.cell.charge_throughput[:,0]
                        pack_Q              = bus_results.heat_energy_generated[:,0]
                        
                        if b_i == 0 and i == 0:
                            axis_1.plot(time,cell_temp, color = line_colors[i], marker = ps.markers[bus_i], linewidth = ps.line_width, label = battery.tag)
                        else:
                            axis_1.plot(time,cell_temp, color = line_colors[i], marker = ps.markers[bus_i], linewidth = ps.line_width)
                        axis_1.set_ylabel(r'Temperature (K)') 
                        set_axes(axis_1)        
                        
                        axis_2.plot(time, cell_charge, color = line_colors[i], marker = ps.markers[bus_i], linewidth = ps.line_width)
                        axis_2.set_xlabel('Time (mins)')
                        axis_2.set_ylabel(r'Charge Throughput (Ah)')
                        set_axes(axis_2)   
                        
                        axis_3.plot(time, pack_Q/1000, color = line_colors[i], marker = ps.markers[bus_i], linewidth = ps.line_width)
                        axis_3.set_xlabel('Time (mins)')
                        axis_3.set_ylabel(r'$\dot{Q}_{heat}$ (kW)')
                        set_axes(axis_3) 
    
    if show_legend:         
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
    
    # Adjusting the sub-plots for legend
    fig.tight_layout() 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Battery Temperature'   
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename  + file_type)   
    return fig 