## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_battery_degradation.py
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
def plot_battery_degradation(results,
                            save_figure = False,
                            line_color = 'bo-',
                            line_color2 = 'rs--',
                            save_filename = "Battery_Degradation",
                            file_type = ".png",
                            width = 8, height = 6):
    """This plots the solar flux and power train performance of an solar powered aircraft

    Assumptions:
    None
    
    Source:
    None    
    
    Inputs:
    results.segments.conditions.propulsion
        solar_flux
        battery_power_draw
        battery_energy
    
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

    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses
        for bus in busses:
            if bus.identical_batteries:
                for i, battery in enumerate(bus.battery_modules):
                    if i == 0:
                        num_segs          = len(results.segments)
                        time_hrs          = np.zeros(num_segs)  
                        capacity_fade     = np.zeros_like(time_hrs)
                        resistance_growth = np.zeros_like(time_hrs)
                        cycle_day         = np.zeros_like(time_hrs)
                        charge_throughput = np.zeros_like(time_hrs)    
                             
                        for i in range(len(results.segments)): 
                            time_hrs[i]           = results.segments[i].conditions.frames.inertial.time[-1,0]  / Units.hour   
                            battery_conditions    = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]    
                            cycle_day[i]          = battery_conditions.cell.cycle_in_day
                            capacity_fade[i]      = battery_conditions.cell.capacity_fade_factor
                            resistance_growth[i]  = battery_conditions.cell.resistance_growth_factor
                            charge_throughput[i]  = battery_conditions.cell.charge_throughput[-1,0]  
    
                        fig_1 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_1')
                        fig_2 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_2')
                        fig_3 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_3')
                        fig_4 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_1')
                        fig_5 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_2')
                        fig_6 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_3')
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
                        
                        axis_1.plot(charge_throughput, capacity_fade, color = ps.color , marker = ps.markers[0], linewidth = ps.line_width ) 
                        axis_1.set_ylabel('$E/E_0$')
                        axis_1.set_xlabel('Ah')
                        set_axes(axis_1)      
                    
                        axis_2.plot(time_hrs, capacity_fade, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width ) 
                        axis_2.set_ylabel('$E/E_0$')
                        axis_2.set_xlabel('Time (hrs)')
                        set_axes(axis_2)     
                    
                        axis_3.plot(cycle_day, capacity_fade, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width ) 
                        axis_3.set_ylabel('$E/E_0$')
                        axis_3.set_xlabel('Time (days)')
                        set_axes(axis_3)
                        
                        axis_4.plot(charge_throughput, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                        axis_4.set_ylabel('$R/R_0$')
                        axis_4.set_xlabel('Ah')
                        set_axes(axis_4)      
                    
                        axis_5.plot(time_hrs, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                        axis_5.set_ylabel('$R/R_0$')
                        axis_5.set_xlabel('Time (hrs)')
                        set_axes(axis_5)     
                    
                        axis_6.plot(cycle_day, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                        axis_6.set_ylabel('$R/R_0$')
                        axis_6.set_xlabel('Time (days)')
                        set_axes(axis_6)             
                             
                        fig_1.tight_layout()    
                        fig_2.tight_layout()    
                        fig_3.tight_layout()    
                        fig_4.tight_layout()    
                        fig_5.tight_layout()    
                        fig_6.tight_layout()    
                        if save_figure:    
                            fig_1.savefig(save_filename + '_'+ battery.tag + file_type) 
                            fig_2.savefig(save_filename + '_'+ battery.tag + file_type) 
                            fig_3.savefig(save_filename + '_'+ battery.tag + file_type) 
                            fig_4.savefig(save_filename + '_'+ battery.tag + file_type) 
                            fig_5.savefig(save_filename + '_'+ battery.tag + file_type) 
                            fig_6.savefig(save_filename + '_'+ battery.tag + file_type)  
                
            else: 
                for battery in bus.battery_modules:

                    fig_1 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_1')
                    fig_2 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_2')
                    fig_3 = plt.figure(battery.tag  + save_filename + '_' + 'Energy_3')
                    fig_4 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_1')
                    fig_5 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_2')
                    fig_6 = plt.figure(battery.tag  + save_filename + '_' + 'Resistance_3')
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
                    
                    num_segs          = len(results.segments)
                    time_hrs          = np.zeros(num_segs)  
                    capacity_fade     = np.zeros_like(time_hrs)
                    resistance_growth = np.zeros_like(time_hrs)
                    cycle_day         = np.zeros_like(time_hrs)
                    charge_throughput = np.zeros_like(time_hrs)    
                         
                    for i in range(len(results.segments)): 
                        time_hrs[i]    = results.segments[i].conditions.frames.inertial.time[-1,0]  / Units.hour   
                        battery_conditions  = results.segments[i].conditions.energy[bus.tag].battery_modules[battery.tag]    
                        cycle_day[i]          = battery_conditions.cell.cycle_in_day
                        capacity_fade[i]      = battery_conditions.cell.capacity_fade_factor
                        resistance_growth[i]  = battery_conditions.cell.resistance_growth_factor
                        charge_throughput[i]  = battery_conditions.cell.charge_throughput[-1,0]  
              
                    axis_1.plot(charge_throughput, capacity_fade, color = ps.color , marker = ps.markers[0], linewidth = ps.line_width ) 
                    axis_1.set_ylabel('$E/E_0$')
                    axis_1.set_xlabel('Ah')
                    set_axes(axis_1)      
                 
                    axis_2.plot(time_hrs, capacity_fade, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width ) 
                    axis_2.set_ylabel('$E/E_0$')
                    axis_2.set_xlabel('Time (hrs)')
                    set_axes(axis_2)     
                 
                    axis_3.plot(cycle_day, capacity_fade, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width ) 
                    axis_3.set_ylabel('$E/E_0$')
                    axis_3.set_xlabel('Time (days)')
                    set_axes(axis_3)     
                 
                    axis_4.plot(charge_throughput, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                    axis_4.set_ylabel('$R/R_0$')
                    axis_4.set_xlabel('Ah')
                    set_axes(axis_4)      
                 
                    axis_5.plot(time_hrs, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                    axis_5.set_ylabel('$R/R_0$')
                    axis_5.set_xlabel('Time (hrs)')
                    set_axes(axis_5)     
                
                    axis_6 = plt.subplot(3,2,6) 
                    axis_6.plot(cycle_day, resistance_growth, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width )
                    axis_6.set_ylabel('$R/R_0$')
                    axis_6.set_xlabel('Time (days)')
                    set_axes(axis_6)       
                    
                    fig_1.tight_layout()    
                    fig_2.tight_layout()    
                    fig_3.tight_layout()    
                    fig_4.tight_layout()    
                    fig_5.tight_layout()    
                    fig_6.tight_layout()    
                    if save_figure:    
                        fig_1.savefig(save_filename + '_'+ battery.tag + file_type) 
                        fig_2.savefig(save_filename + '_'+ battery.tag + file_type) 
                        fig_3.savefig(save_filename + '_'+ battery.tag + file_type) 
                        fig_4.savefig(save_filename + '_'+ battery.tag + file_type) 
                        fig_5.savefig(save_filename + '_'+ battery.tag + file_type) 
                        fig_6.savefig(save_filename + '_'+ battery.tag + file_type)  
        
    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6

