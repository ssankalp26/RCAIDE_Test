# RCAIDE/Library/Plots/Thermal_Management/plot_cross_flow_heat_exchanger_conditions.py
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
#   plot_heat_exchanger_system_conditions
# ----------------------------------------------------------------------------------------------------------------------   
def plot_cross_flow_heat_exchanger_conditions(cross_flow_hex, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the Cross Flow Heat Exchanger conditions throughout flight.
    
     Assumptions:
     None
    
     Source:
     None
    
     Inputs:
     results.segments.conditions.energy[coolant_line.tag][cross_flow_hex.tag].
                                                                             coolant_mass_flow_rate
                                                                             effectiveness_HEX   
                                                                             power          
                                                                             air_inlet_pressure
                                                                             inlet_air_temperature 
                                                                             air_mass_flow_rate    
                                                                       
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

    fig_1 = plt.figure(save_filename + '_Effectiveness' )
    fig_2 = plt.figure(save_filename + '_Inlet_Air_Temp' )
    fig_3 = plt.figure(save_filename + '_Coolant_Flowrate' )
    fig_4 = plt.figure(save_filename + '_Air_Flowrate' )
    fig_5 = plt.figure(save_filename + '_Power' )
    fig_6 = plt.figure(save_filename + '_Inlet_Air_Pressure' )
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
   
    for i in range(len(results.segments)):  
        time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
        cross_flow_hex_conditions  = results.segments[i].conditions.energy[coolant_line.tag][cross_flow_hex.tag]  

        coolant_mass_flow_rate     = cross_flow_hex_conditions.coolant_mass_flow_rate[:,0]        
        effectiveness_HEX          = cross_flow_hex_conditions.effectiveness_HEX[:,0]   
        power                      = cross_flow_hex_conditions.power[:,0]                       
        inlet_air_pressure         = cross_flow_hex_conditions.air_inlet_pressure[:,0]          
        inlet_air_temperature      = cross_flow_hex_conditions.inlet_air_temperature[:,0]          
        air_mass_flow_rate         = cross_flow_hex_conditions.air_mass_flow_rate[:,0]     
                            

        segment_tag  = results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
 
        axis_1.plot(time, effectiveness_HEX, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name) 
        axis_1.set_ylabel(r'Effectiveness') 
        axis_1.set_xlabel(r'Time (mins)')
        set_axes(axis_1)      

        axis_2.plot(time,  inlet_air_temperature, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_2.set_ylabel(r'Air Temp. (K)') 
        axis_2.set_xlabel(r'Time (mins)')
        set_axes(axis_2)    
        
        axis_3.plot(time, coolant_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_3.set_ylabel(r'Coolant $\dot{m}$ (kg/s)')
        axis_3.set_xlabel(r'Time (mins)')
        set_axes(axis_3) 

        axis_4.plot(time, air_mass_flow_rate, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_4.set_ylabel(r'Air $\dot{m}$ (kg/s)')
        axis_4.set_xlabel(r'Time (mins)')
        set_axes(axis_4)                               
 
        axis_5.plot(time, power/1000, color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_5.set_ylabel(r'Power (KW)')
        axis_5.set_xlabel(r'Time (mins)')
        set_axes(axis_5)    

        axis_6.plot(time, inlet_air_pressure/10e6 , color = line_colors[i], marker = ps.markers[b_i],markersize = ps.marker_size, linewidth = ps.line_width, label = segment_name)
        axis_6.set_ylabel(r'Air Pres. (MPa)')
        axis_6.set_xlabel(r'Time (mins)')
        set_axes(axis_6) 
 
       
        b_i += 1 
            
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
    
    fig_1.tight_layout()    
    fig_2.tight_layout()    
    fig_3.tight_layout()    
    fig_4.tight_layout()
    fig_5.tight_layout()    
    fig_6.tight_layout()    
    
    # Adjusting the sub-plots for legend 
    fig_1.subplots_adjust(top=0.8)  
    fig_2.subplots_adjust(top=0.8)  
    fig_3.subplots_adjust(top=0.8)  
    fig_4.subplots_adjust(top=0.8)  
    fig_5.subplots_adjust(top=0.8)  
    fig_6.subplots_adjust(top=0.8)  
    
    if save_figure:
        fig_1.savefig(save_filename + cross_flow_hex.tag + file_type)  
        fig_2.savefig(save_filename + cross_flow_hex.tag + file_type)  
        fig_3.savefig(save_filename + cross_flow_hex.tag + file_type)  
        fig_4.savefig(save_filename + cross_flow_hex.tag + file_type)  
        fig_5.savefig(save_filename + cross_flow_hex.tag + file_type)  
        fig_6.savefig(save_filename + cross_flow_hex.tag + file_type)    
    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6