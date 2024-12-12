## @ingroup Library-Plots-Weights
# RCAIDE/Library/Plots/Weights/plot_weight_breakdown.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE 
import numpy as np    
import matplotlib.pyplot as plt   
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Weights
def plot_weight_breakdown(vehicle,
                            save_figure    = False,
                            show_figure    = True, 
                            show_legend    = True,
                            SI_Units       = True,
                            save_filename  = "Weight_Breakdown",
                            aircraft_name  = None,
                            file_type      = ".png",
                            width          = 10, height = 7.2): 
  

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
    
    level_1 = []
    level_2 = []
    level_3 = []
    values  = []
      
    for tag ,  item in  breakdown.items():
        if tag == 'zero_fuel_weight' or   tag == 'max_takeoff':
            pass
        else:
            if type(item)  == RCAIDE.Framework.Core.Data: 
                for  sub_tag  , sub_item in item.items():
                    if type(sub_item) == RCAIDE.Framework.Core.Data: 
                        for sub_sub_tag ,  sub_sub_item in sub_item.items():
                            if sub_sub_tag != 'total':
                                level_1.append(tag.replace("_", " "))
                                level_2.append(sub_tag.replace("_", " "))
                                level_3.append(sub_sub_tag.replace("_", " "))
                                values.append(sub_sub_item )
                    elif sub_tag != 'total':
                        level_1.append(tag.replace("_", " "))
                        level_2.append(sub_tag.replace("_", " "))
                        level_3.append(np.nan)
                        values.append(sub_item) 
            elif tag == 'fuel':
                level_1.append(tag.replace("_", " "))
                level_2.append(np.nan)
                level_3.append(np.nan)
                values.append(sub_item) 
                  
    df = pd.DataFrame(
        dict(level_1=level_1, level_2=level_2, level_3=level_3, values=values)
    ) 
    fig = px.sunburst(df,
                      path=['level_1', 'level_2', 'level_3'], 
                      values='values',  
                      color_discrete_sequence=px.colors.qualitative.G10)
    
    # Add a dummy inner layer for the hole
    fig.update_traces(
        textfont=dict(size=20), 
        insidetextorientation='horizontal', 
        textinfo='label+percent entry', 
        marker=dict(colors=['rgba(0,0,0,0)'] + px.colors.qualitative.G10)
    )
    fig.update_layout( 
    uniformtext=dict(minsize=12, mode='hide'),
    )
 
    if save_figure:
        fig.write_image(save_filename + file_type)
    
    if show_figure:
        fig.write_html( save_filename + '.html', auto_open=True)        
    return  fig 
