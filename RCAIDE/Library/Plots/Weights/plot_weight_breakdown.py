## @ingroup Library-Plots-Weights
# RCAIDE/Library/Plots/Weights/plot_weight_breakdown.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
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
                            width = 7.5, height = 7.2): 
  

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

    group_name         =  []
    group_weight       =  []
    group_color        =  []
    subgroup_name      =  []
    subgroup_weight    =  []
    sub_subgroup_name  =  []
    sub_subgroup_weight=  []
    subgroup_color     =  []
    sub_subgroup_color =  []
                

    structural_colors =  0*len(group_name)
    propulsion_colors =  0*len(subgroup_name) 
    payload_colors    =  0*len(sub_subgroup_name) 
    systems_colors    =  0*len(sub_subgroup_name) 
    opt_itels_colors  =  0*len(sub_subgroup_name)
     
    i = 0           
    for item , tag in  breakdown.items():
        if tag == 'total':
            pass
        else:
            if item is Dict():
                group_name.append(tag)
                group_weight.append(item.total)
                group_color.append( ) 
                for sub_item , sub_tag in item():
                    if sub_item is Dict():
                        if sub_tag == 'structural': 
                            colormap       = structural_colors 
                        if sub_tag == 'propulsion': 
                            colormap       = propulsion_colors 
                        if sub_tag == 'payload': 
                            colormap       = payload_colors 
                        if sub_tag == 'systems': 
                            colormap       = systems_colors 
                        if sub_tag == 'operational_items': 
                            colormap       = opt_itels_colors 
                        subgroup_color.append(colormap[0])
                        subgroup_name.append(sub_tag)
                        subgroup_weight.append(sub_item.total)
                        k = 1
                        for sub_sub_item , sub_sub_tag in sub_item():  
                            sub_subgroup_color.append(colormap[k])
                            sub_subgroup_name.append(sub_sub_tag)
                            sub_subgroup_weight.append(sub_sub_item)
                            k += 1 
            elif tag == 'fuel': 
                group_name.append(tag)
                group_weight.append(item)
                
            i += 1
                
      
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['legend.fontsize'] = 14
      
    labels  = group_name + subgroup_name
    pie_1_dummy_labels = ['']*len(group_name)
    pie_2_dummy_labels = ['']*len(subgroup_name)
    pie_3_dummy_labels = ['']*len(sub_subgroup_name)  
     
    fig, ax = plt.subplots()
    ax.axis('equal')  
    
    pie_chart_width  = 0.3
    pie_chart_radius = 1.6
    pie_1_radius = pie_chart_radius - 2 * pie_chart_width
    pie_2_radius = pie_chart_radius -  pie_chart_width

    pie_1, _ = ax.pie(group_weight, radius = pie_1_radius, labels = pie_1_dummy_labels,  colors=group_color )
    plt.setp(pie_1, width=pie_chart_width, edgecolor = 'white')
         
    
    pie_2, _ = ax.pie(subgroup_weight, radius=pie_2_radius, labels = pie_2_dummy_labels,   colors=subgroup_color)
    plt.setp(pie_2, width=pie_chart_width, edgecolor='white')
    

    pie_3, _ = ax.pie(sub_subgroup_weight, radius=pie_chart_radius, labels = pie_3_dummy_labels,   colors=sub_subgroup_color)
    plt.setp(pie_3, width=pie_chart_width, edgecolor='white')
    
    ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart 
    
    # Add legend 
    plt.margins(0, 0)
    
    plt.tight_layout() 
    plt.show() 
     
    # Add weight of aircraft 
    weight_text = str((round(weight,2))) + ' kg'
    if not SI_Units:    
        weight = weight/Units.lbs
        weight_text = str((round(weight,1))) + ' lbs.' 
    ax.annotate('MTOW', (np.pi*3/4,0.2), size= 20) 
    ax.annotate(weight_text, (np.pi,0.2), size= 20)   
    
    if show_legend: 
        ax.legend(labels, loc='lower center', ncol = 3, prop={'size': 14}  ,bbox_to_anchor= (0,-.25, 1, 0.3)  )
    ax.set_axis_off()  
    
    fig.tight_layout()
    
    if save_figure:
        plt.savefig(save_filename + '.pdf')    
        
    return  fig 
