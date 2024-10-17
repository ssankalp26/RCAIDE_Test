## @ingroup Library-Plots-Energy
# RCAIDE/Library/Plots/Energy/plot_fuel_consumption.py
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
def plot_fuel_consumption(results,
                    save_figure = False,
                    show_legend=True,
                    save_filename = "Aircraft_Fuel_Burnt",
                    file_type = ".png",
                    width = 8, height = 6): 

    """This plots aircraft fuel usage
    
    
    Assumptions:
    None

    Source: 
  
    Inputs:
    results.segments.condtions.
        frames.inertial.time
        weights.fuel_mass
        weights.additional_fuel_mass
        weights.total_mass
        
    Outputs:
    Plots
    Properties Used:
    N/A	"""

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axis_1.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axis_1.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))       
  
    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height)

    prev_seg_fuel       = 0
    prev_seg_extra_fuel = 0
    total_fuel          = 0

    axis_1 = fig.add_subplot(1,1,1)
            
    for i in range(len(results.segments)):

        segment  = results.segments[i]
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min  
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')        

        if "has_additional_fuel" in segment.conditions.weights and segment.conditions.weights.has_additional_fuel == True: 
            fuel     = segment.conditions.weights.fuel_mass[:,0]
            alt_fuel = segment.conditions.weights.additional_fuel_mass[:,0]

            if i == 0: 
                plot_fuel     = np.negative(fuel)
                plot_alt_fuel = np.negative(alt_fuel) 
                axis_1.plot( time , plot_fuel , 'ro-', marker = ps.markers[0], linewidth = ps.line_width , label = 'fuel')
                axis_1.plot( time , plot_alt_fuel , 'bo-', marker = ps.markers[0], linewidth = ps.line_width, label = 'additional fuel' )
                axis_1.plot( time , np.add(plot_fuel, plot_alt_fuel), 'go-', marker = ps.markers[0], linewidth = ps.line_width, label = 'total fuel' ) 
                axis_1.legend(loc='center right')   

            else:
                prev_seg_fuel       += results.segments[i-1].conditions.weights.fuel_mass[-1]
                prev_seg_extra_fuel += results.segments[i-1].conditions.weights.additional_fuel_mass[-1] 
                current_fuel         = np.add(fuel, prev_seg_fuel)
                current_alt_fuel     = np.add(alt_fuel, prev_seg_extra_fuel) 
                axis_1.plot( time , np.negative(current_fuel)  , 'ro-' , marker = ps.markers[0], linewidth = ps.line_width)
                axis_1.plot( time , np.negative(current_alt_fuel ), 'bo-', marker = ps.markers[0], linewidth = ps.line_width)
                axis_1.plot( time , np.negative(current_fuel + current_alt_fuel), 'go-', marker = ps.markers[0], linewidth = ps.line_width)

        else: 
            initial_weight  = results.segments[0].conditions.weights.total_mass[:,0][0] 
            fuel            = results.segments[i].conditions.weights.total_mass[:,0]
            time            = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
            total_fuel      = np.negative(results.segments[i].conditions.weights.total_mass[:,0] - initial_weight )
            axis_1.plot( time, total_fuel, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name)

    axis_1.set_ylabel('Fuel (kg)')
    axis_1.set_xlabel('Time (min)') 
    set_axes(axis_1)  

    if show_legend:    
        leg =  fig.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()     
    fig.subplots_adjust(top=0.8) 

    if save_figure:
        plt.savefig(save_filename + file_type)  
        
    return fig 