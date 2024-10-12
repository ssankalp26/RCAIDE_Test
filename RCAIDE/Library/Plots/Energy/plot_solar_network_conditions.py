## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_solar_network_conditions.py
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
def plot_solar_network_conditions(results,
                    save_figure   = False,
                    show_legend   = True,
                    save_filename = "Solar_Flux",
                    file_type     = ".png",
                    width = 8, height = 6):
    """This plots the solar flux and power train performance of an solar powered aircraft

    Assumptions:
    None
     
    Source:
    None
    
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
    
    for network in results.segments[0].analyses.energy.vehicle.networks: 
        busses  = network.busses
        for bus in busses:     
            for battery in bus.battery_modules:  
                fig_1 = plt.figure('Solar_Flux_' + battery.tag)
                fig_2 = plt.figure('Charing_Power_' + battery.tag)
                fig_3 = plt.figure('Battery_Current_' + battery.tag)
                fig_4 = plt.figure('Battery_Energy_' + battery.tag)
                fig_1.set_size_inches(width,height)    
                fig_2.set_size_inches(width,height)    
                fig_3.set_size_inches(width,height)    
                fig_4.set_size_inches(width,height)    
                for i in range(len(results.segments)):   
                    bus_results         = results.segments[i].conditions.energy[bus.tag] 
                    time                = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
                    flux                = results.segments[i].conditions.energy.solar_flux[:,0]
                    charge              = bus_results.power_draw[:,0]
                    current             = bus_results.current_draw[:,0]
                    energy              = bus_results.energy[:,0] / Units.MJ 
                
                    segment_tag  =  results.segments[i].tag
                    segment_name = segment_tag.replace('_', ' ')
                    axis_1 = fig_1.add_subplot(1,1,1)
                    axis_2 = fig_2.add_subplot(1,1,1)
                    axis_3 = fig_3.add_subplot(1,1,1)
                    axis_4 = fig_4.add_subplot(1,1,1)
                    
                    axis_1.plot(time, flux, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
                    axis_1.set_ylabel(r'Solar Flux (W/m^2)')
                    axis_1.set_xlabel('Time (mins)')
                    set_axes(axis_1)    
                
                    axis_2.plot(time, charge, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
                    axis_2.set_ylabel(r'Charging Power (W)')
                    axis_2.set_xlabel('Time (mins)')
                    set_axes(axis_2) 
                
                    axis_3.plot(time, current, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
                    axis_3.set_xlabel('Time (mins)')
                    axis_3.set_ylabel(r'Battery Current (A)')
                    set_axes(axis_3) 
                
                    axis_4.plot(time, energy, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
                    axis_4.set_xlabel('Time (mins)')
                    axis_4.set_ylabel(r'Battery Energy (MJ)')
                    set_axes(axis_4)   
                            
    if show_legend:        
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_4 =  fig_4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        leg_4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
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
        fig_1.savefig('Solar_Flux_' + battery.tag + file_type)   
        fig_2.savefig('Charing_Power_' + battery.tag + file_type)  
        fig_3.savefig('Battery_Current_' + battery.tag + file_type)  
        fig_4.savefig('Battery_Energy_' + battery.tag + file_type)   

    return fig_1, fig_2, fig_3 , fig_4