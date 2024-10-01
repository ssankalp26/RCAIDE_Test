## @ingroup Library-Plots-Performance-Aerodynamics   
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_polar_files.py
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

## @ingroup Library-Plots-Performance-Aerodynamics   
def plot_airfoil_polar_files(polar_data,
                             save_figure = False,
                             save_filename = "Airfoil_Polars",
                             file_type = ".png",
                             width = 8, height = 6):
    """This plots all airfoil polars in the list "airfoil_polar_paths" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_polar_paths   [list of strings]

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
    
    
    # Get raw data polars
    CL           = polar_data.lift_coefficients
    CD           = polar_data.drag_coefficients
    alpha        = polar_data.angle_of_attacks/Units.degrees
    Re_raw       = polar_data.reynolds_numbers
    n_Re         = len(polar_data.re_from_polar) 
        
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,n_Re))     
     
    fig_1   = plt.figure(save_filename + "_Cl_vs_Alpha")
    fig_2   = plt.figure(save_filename + "_Cd_vs_Alpha")
    fig_3   = plt.figure(save_filename + "_Cl_vs_Cd")
    fig_4   = plt.figure(save_filename + "_Cl/Cd_vs_Alpha")
    
    fig_1.set_size_inches(width,height) 
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
    fig_4.set_size_inches(width,height)
    
    axis_1 = plt.subplot(1,1,1)
    axis_2 = plt.subplot(1,1,1)
    axis_3 = plt.subplot(1,1,1)
    axis_4 = plt.subplot(1,1,1)    
    
    for j in range(n_Re):
        
        Re_val = str(round(Re_raw[j])/1e6)+'e6'  
                
        axis_1.plot(alpha, CL[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val,markersize = ps.marker_size)
        axis_1.set_ylabel(r'$C_l$')
        axis_1.set_xlabel(r'$\alpha$')
        set_axes(axis_1)    
        
        axis_2.plot(alpha,CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val,markersize = ps.marker_size) 
        axis_2.set_ylabel(r'$C_d$')
        axis_2.set_xlabel(r'$\alpha$')
        set_axes(axis_2)  
        
        axis_3.plot(CL[j,:],CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val,markersize = ps.marker_size)
        axis_3.set_xlabel('$C_l$')
        axis_3.set_ylabel(r'$C_d$')
        set_axes(axis_3) 
    
        axis_4.plot(alpha, CL[j,:]/CD[j,:], color = line_colors[j], marker = ps.markers[0], linewidth = ps.line_width, label ='Re='+Re_val,markersize = ps.marker_size) 
        axis_4.set_ylabel(r'$Cl/Cd$')
        axis_4.set_xlabel(r'$\alpha$')
        set_axes(axis_4)   
    
    if save_figure:
        fig_1.savefig(save_filename + "_Cl_vs_Alpha"+ file_type)
        fig_2.savefig(save_filename + "_Cd_vs_Alpha"+ file_type)
        fig_3.savefig(save_filename + "_Cl_vs_Cd"+ file_type)
        fig_4.savefig(save_filename + "_Cl/Cd_vs_Alpha"+ file_type)   
    return fig_1, fig_2, fig_3, fig_4