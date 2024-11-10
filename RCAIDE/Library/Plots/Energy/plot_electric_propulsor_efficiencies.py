## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_electric_propulsor_efficiencies.py
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
def plot_electric_propulsor_efficiencies(results,
                                  save_figure = False,
                                  show_legend=True,
                                  save_filename = "Electric_Efficiencies",
                                  file_type = ".png",
                                  width = 8, height = 6):
    """This plots the electric driven network propeller efficiencies 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion. 
         etap
         etam
         fom
        
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
    
    fig_1 = plt.figure('Rotor_Efficiencies')
    fig_2 = plt.figure('Figure_of_Merit_Efficiencies')
    fig_3 = plt.figure('Motor_Efficiencies')
    fig_1.set_size_inches(width,height) 
    fig_2.set_size_inches(width,height) 
    fig_3.set_size_inches(width,height)  
    axis_1 = fig_1.add_subplot(1,1,1)
    axis_2 = fig_2.add_subplot(1,1,1) 
    axis_3 = fig_3.add_subplot(1,1,1)   
    pi     = 0 
    for network in results.segments[0].analyses.energy.vehicle.networks:  
        if 'busses' in network: 
            for bus in network.busses:    
                for p_i, propulsor in enumerate(bus.propulsors): 
                    if p_i == 0: 
                        plot_propulsor_data(results,bus,propulsor,axis_1,axis_2,axis_3,line_colors,ps,pi)
                    elif (bus.identical_propulsors == False) and p_i !=0:  
                        plot_propulsor_data(results,bus,propulsor,axis_1,axis_2,axis_3,line_colors,ps,pi)  
                    pi += 1
               
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
        fig_1.savefig(save_filename + file_type) 
        fig_2.savefig(save_filename + file_type) 
        fig_3.savefig(save_filename + file_type) 
     
    return fig_1,fig_2, fig_3

def plot_propulsor_data(results,bus,propulsor,axis_1,axis_2,axis_3,line_colors,ps,pi):
    
    if 'rotor' in propulsor: 
        thrustor =  propulsor.rotor
        axis_1.set_ylabel(r'$\eta_{rotor}$')
    elif 'ducted_fan' in propulsor:
        thrustor =  propulsor.ducted_fan
        axis_1.set_ylabel(r'$\eta_{ducted fan}$')
    motor =  propulsor.motor
    
    for i in range(len(results.segments)): 
        bus_results  = results.segments[i].conditions.energy[bus.tag] 
        time         = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min      
        effp         = bus_results[propulsor.tag][thrustor.tag].efficiency[:,0]
        fom          = bus_results[propulsor.tag][thrustor.tag].figure_of_merit[:,0]
        effm         = bus_results[propulsor.tag][motor.tag].efficiency[:,0]        
        segment_tag  = results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
         
        axis_1.plot(time, effp, color = line_colors[i], marker = ps.markers[pi], markersize= ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        
        axis_1.set_xlabel('Time (mins)')
        axis_1.set_ylim([0,1.1])
        set_axes(axis_1)         
         
        axis_2.plot(time, fom, color = line_colors[i], marker = ps.markers[pi], markersize= ps.marker_size , linewidth = ps.line_width, label = segment_name) 
        axis_2.set_xlabel('Time (mins)')
        axis_2.set_ylabel(r'FoM')
        axis_2.set_ylim([0,1.1])
        set_axes(axis_2) 
 
        axis_3.plot(time, effm, color = line_colors[i], marker = ps.markers[pi], markersize= ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'$\eta_{motor}$')
        axis_3.set_ylim([0,1.1])
        set_axes(axis_3)   
    return 