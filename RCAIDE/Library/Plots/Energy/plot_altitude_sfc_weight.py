## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_altitude_sfc_weight.py
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
## @ingroup Library-Plots-Performance-Energy-Fuel
def plot_altitude_sfc_weight(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Altitude_SFC_Weight" ,
                             file_type = ".png",
                             width = 8, height = 6):
    """This plots the altitude, specific fuel consumption and vehicle weight.

    Assumptions:
    None

    Source: 

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
     
    fig_1   = plt.figure(save_filename + '_Throttle' )
    fig_2   = plt.figure(save_filename + '_Weight' )
    fig_3   = plt.figure(save_filename + '_SFC' )
    fig_4   = plt.figure(save_filename + '_Fuel_Flow_Rate' )
    fig_1.set_size_inches(width,height) 
    fig_2.set_size_inches(width,height) 
    fig_3.set_size_inches(width,height) 
    fig_4.set_size_inches(width,height) 
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1)
    axis_3 = fig_3.add_subplot(1,1,1)
    axis_4 = fig_4.add_subplot(1,1,1)
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:, 0] / Units.min
        Weight   = results.segments[i].conditions.weights.total_mass[:, 0] * 9.81   
        mdot     = results.segments[i].conditions.weights.vehicle_mass_rate[:, 0]
        thrust   = results.segments[i].conditions.frames.body.thrust_force_vector[:, 0]
        sfc      = (mdot / Units.lb) / (thrust / Units.lbf) * Units.hr       
            
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        
        axis_1.set_ylabel(r'Throttle')
        set_axes(axis_1)               
        for network in results.segments[i].analyses.energy.vehicle.networks: 
            busses      = network.busses
            fuel_lines  = network.fuel_lines 
            for network in results.segments[i].analyses.energy.vehicle.networks: 
                busses      = network.busses
                fuel_lines  = network.fuel_lines 
                for bus in busses:
                    for j ,  propulsor in enumerate(bus.propulsors):
                        eta = results.segments[i].conditions.energy[bus.tag][propulsor.tag].throttle[:,0]   
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)  
                for fuel_line in fuel_lines:  
                    for j ,  propulsor in enumerate(fuel_line.propulsors): 
                        eta = results.segments[i].conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0]   
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name  )  
         
        axis_2.plot(time, Weight/1000 , color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        axis_2.set_ylabel(r'Weight (kN)')
        axis_2.set_xlabel('Time (mins)')
        set_axes(axis_2) 

        axis_3.plot(time, sfc, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'SFC (lb/lbf-hr)')
        set_axes(axis_3) 

        axis_4.plot(time, mdot, color = line_colors[i], marker = ps.markers[0],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Fuel Rate (kg/s)')
        set_axes(axis_4)     
    
    if show_legend:
        leg_1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_4 =  fig_4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg_1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg_3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
        leg_4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})   
    
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8)
    fig_2.subplots_adjust(top=0.8)
    fig_3.subplots_adjust(top=0.8)
    fig_4.subplots_adjust(top=0.8)  
        
    fig_1.tight_layout()    
    fig_2.tight_layout()    
    fig_3.tight_layout()    
    fig_4.tight_layout()     
    
    if save_figure:
        fig_1.savefig(save_filename + file_type)   
        fig_2.savefig(save_filename + file_type)   
        fig_3.savefig(save_filename + file_type)   
        fig_4.savefig(save_filename + file_type)    
    return fig_1,fig_2,fig_3,fig_4 