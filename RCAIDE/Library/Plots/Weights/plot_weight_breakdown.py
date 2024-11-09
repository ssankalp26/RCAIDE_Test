## @ingroup Library-Plots-Weights
# RCAIDE/Library/Plots/Weights/plot_weight_breakdown.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from  RCAIDE.Framework.Core import Units   
import numpy as np    
import matplotlib.pyplot as plt  
import matplotlib.cm as cm   

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Weights
def plot_weight_breakdown(vehicle,
                            save_figure = True,
                            show_legend=True,
                            SI_Units   = True,
                            save_filename = "Weight_Breakdown",
                            aircraft_name  = None,
                            file_type = ".png",
                            width = 10, height = 7.2): 
  

    """This plots the weight breakdown of an evtol aircraft

    Assumptions:
    None

    Source:
    None

    Inputs:
    vehicle

    Outputs:
    Plots

    Properties Used:
    N/A
    """

    breakdown =  vehicle.weight_breakdown    
    weight    =  vehicle.mass_properties.max_takeoff

    group_names         =  []
    group_weights       =  []
    group_colors        =  []
    subgroup_names      =  []
    subgroup_weights    =  []
    sub_subgroup_names  =  []
    sub_subgroup_weights=  []
    subgroup_colors     =  []
    sub_subgroup_colors =  []
            
    tab10  = cm.tab10(np.linspace(0,1,10))
    Pastel = cm.Pastel1(np.linspace(0,1,10))
    i = 0           
    for tag ,  item in  breakdown.items():
        if tag == 'zero_fuel_weight' or   tag == 'max_takeoff':
            pass
        else:
            if type(item)  == RCAIDE.Framework.Core.Data:
                group_names.append(tag)
                group_weights.append(item.total/weight)
                group_colors.append(Pastel[i]) 
                for  sub_tag  , sub_item in item.items():
                    if type(sub_item) == RCAIDE.Framework.Core.Data:
                        if sub_tag == 'structural': 
                            color  = tab10[0]
                            colors = cm.Blues(np.linspace(0.1,1,10))
                        if sub_tag == 'propulsion': 
                            color        = tab10[1] 
                            colors = cm.Oranges(np.linspace(0.1,1,10))
                        if sub_tag == 'payload': 
                            color  = tab10[2]
                            colors = cm.Greens(np.linspace(0.1,1,10))
                        if sub_tag == 'systems': 
                            color  = tab10[3] 
                            colors = cm.Reds(np.linspace(0.1,1,10)) 
                        if sub_tag == 'operational_items': 
                            color  = tab10[4]
                            colors = cm.Purples(np.linspace(0.1,1,10)) 
                        subgroup_colors.append(color)
                        subgroup_names.append(sub_tag)
                        subgroup_weights.append(sub_item.total/weight)
                        k = 1
                        for sub_sub_tag ,  sub_sub_item in sub_item.items():  
                            sub_subgroup_colors.append(colors[k])
                            sub_subgroup_names.append(sub_sub_tag)
                            sub_subgroup_weights.append(sub_sub_item)
                            k += 1
                    else: 
                        subgroup_colors.append('white')
                        subgroup_names.append(tag)
                        subgroup_weights.append(item.total/weight)                            
            elif tag == 'fuel': 
                group_names.append(tag)
                group_weights.append(item/breakdown.total)
                group_colors.append('black' ) 
                subgroup_colors.append('white')
                subgroup_names.append(tag)
                subgroup_weights.append(item/breakdown.total)                
                
        i += 1
                
      
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['legend.fontsize'] = 14
      
    labels  = group_names + subgroup_names
    pie_1_dummy_labels = ['']*len(group_names)
    pie_2_dummy_labels = ['']*len(subgroup_names)
    pie_3_dummy_labels = ['']*len(sub_subgroup_names)  
     
    fig, ax = plt.subplots()
    ax.axis('equal')  
    
    pie_chart_width  = 0.3
    pie_chart_radius = 1.6
    pie_1_radius = pie_chart_radius - 2 * pie_chart_width
    pie_2_radius = pie_chart_radius -  pie_chart_width

    pie_1, _ = ax.pie(group_weights, radius = pie_1_radius, labels = pie_1_dummy_labels,  colors=group_colors )
    plt.setp(pie_1, width=pie_chart_width, edgecolor = 'white')
         
    
    pie_2, _ = ax.pie(subgroup_weights, radius=pie_2_radius, labels = pie_2_dummy_labels,   colors=subgroup_colors)
    plt.setp(pie_2, width=pie_chart_width, edgecolor='white')
    

    #pie_3, _ = ax.pie(sub_subgroup_weights, radius=pie_chart_radius, labels = pie_3_dummy_labels,   colors=sub_subgroup_colors)
    #plt.setp(pie_3, width=pie_chart_width, edgecolor='white')
    
    ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart 
    
    # Add legend 
    #plt.margins(0, 0)
     
    # Add weight of aircraft 
    weight_text = str((round(weight,2))) + ' kg'
    if not SI_Units:    
        weight = weight/Units.lbs
        weight_text = str((round(weight,1))) + ' lbs.' 
    ax.annotate('MTOW', (np.pi*3/4,0.2), size= 20) 
    ax.annotate(weight_text, (np.pi,0.2), size= 20)   
    
    if show_legend: 
        fig.legend(labels, loc='center left', prop={'size': 14})
    ax.set_axis_off()
     
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(left=0.5) 
        
    
    if save_figure:
        plt.savefig(save_filename + '.pdf')    
        
    return  fig 
