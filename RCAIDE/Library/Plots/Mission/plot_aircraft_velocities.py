## @defgroup Library-Plots-Mission  
# RCAIDE/Library/Plots/Performance/Mission/plot_aircraft_velocities.py
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
## @defgroup Library-Plots-Mission  
def plot_aircraft_velocities(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Aircraft Velocities" ,
                             file_type = ".png",
                             width = 8, height = 6): 

    """This plots true, equivalent, and calibrated airspeeds along with mach

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.condtions.freestream.
        velocity
        density
        mach_number

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
     
    fig_1   = plt.figure(save_filename+"_True_Airspeed")
    fig_2   = plt.figure(save_filename+"_Equiv._Airspeed")
    fig_3   = plt.figure(save_filename+"_Calibrated_Airspeed")
    fig_4   = plt.figure(save_filename+"_Mach_Number")
    
    fig_1.set_size_inches(width,height)
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
    fig_4.set_size_inches(width,height)

    axis_1 = fig_1.add_subplot(1,1,1) 
    axis_2 = fig_2.add_subplot(1,1,1)    
    axis_3 = fig_3.add_subplot(1,1,1)
    axis_4 = fig_4.add_subplot(1,1,1)
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        velocity = results.segments[i].conditions.freestream.velocity[:,0] / Units.kts
        density  = results.segments[i].conditions.freestream.density[:,0]
        PR       = density/1.225
        EAS      = velocity * np.sqrt(PR)
        mach     = results.segments[i].conditions.freestream.mach_number[:,0]
        CAS      = EAS * (1+((1/8)*((1-PR)*mach**2))+((3/640)*(1-10*PR+(9*PR**2)*(mach**4))))

             
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        axis_1.plot(time, velocity, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_1.set_ylabel(r'True Airspeed (kts)')
        axis_1.set_xlabel('Time (mins)')        
        set_axes(axis_1)    
        
        axis_2.plot(time, EAS, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,markersize = ps.marker_size, label = segment_name) 
        axis_2.set_ylabel(r'Equiv. Airspeed (kts)')
        axis_2.set_xlabel('Time (mins)')
        set_axes(axis_2) 
 
        axis_3.plot(time, CAS, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,markersize = ps.marker_size, label = segment_name)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Calibrated Airspeed (kts)')
        set_axes(axis_3) 
        
        axis_4.plot(time, mach, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,markersize = ps.marker_size, label = segment_name)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Mach Number')
        set_axes(axis_4) 
    
    
    if show_legend:    
        leg1 =  fig_1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4)
        leg2 =  fig_2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4)
        leg3 =  fig_3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4)
        leg4 =  fig_4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4)
        
        leg1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'}) 
    
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
        fig_1.savefig(save_filename + file_type)
        fig_2.savefig(save_filename + file_type)
        fig_3.savefig(save_filename + file_type)
        fig_4.savefig(save_filename + file_type) 
    return fig_1, fig_2, fig_3, fig_4