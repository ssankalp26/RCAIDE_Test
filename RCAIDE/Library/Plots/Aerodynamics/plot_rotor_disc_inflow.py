## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_rotor_disc_inflow.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   

# python imports 
import matplotlib.patches as patches 
import matplotlib.pyplot as plt 
import numpy as np


# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Library-Plots-Performance-Aerodynamics  
def plot_rotor_disc_inflow(prop,velocities, grid_points, 
                           save_filename = "Rotor_Disc_Inflow",
                           file_type = ".png",
                           width = 8, height = 6):

    """Plots rotor disc inflow velocities

    Assumptions:
    None

    Source: 
    None
    
    Inputs
    velocites  - velocites at rotor plane  [m/s]

    Outputs:
    Plots

    Properties Used:
    N/A
    """    
    
    u = velocities.u_velocities
    v = velocities.v_velocities
    w = velocities.w_velocities
    vtot = np.sqrt(u**2 + v**2 + w**2)
    
    # plot the velocities at rotor
    y = grid_points.ymesh
    z = grid_points.zmesh

    R  = prop.tip_radius
    Rh = prop.hub_radius
    psi_360 = np.linspace(0,2*np.pi,40)
    
    vmin = round(np.min([u,v,w,vtot]),3)
    vmax = round(np.max([u,v,w,vtot]),3)
    levels = np.linspace(vmin,vmax, 21)
    
    # plot the grid point velocities 
    # plot the grid point velocities
    fig_1   = plt.figure(save_filename + '_Axial_Velocity' )
    fig_2   = plt.figure(save_filename + '_Spanwise_Velocity' )
    fig_3   = plt.figure(save_filename + '_Downwash_Velocity' )
    fig_4   = plt.figure(save_filename + '_Total_Velocity' ) 
    
    fig_1.set_size_inches(width,height)
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
    fig_4.set_size_inches(width,height)  
     
    axis_1    = fig_1.add_subplot(111)
    axis_2    = fig_2.add_subplot(111) 
    axis_3    = fig_3.add_subplot(111)  
    axis_4    = fig_4.add_subplot(111)   
    
    c1 = axis_1.tricontourf(y,z, u, levels=levels, vmax=vmax, vmin=vmin, cmap='seismic')
    plt.colorbar(c1, ax=axis_1)#, orientation="horizontal")           
                               
    c2 = axis_2.tricontourf(y,z, v, levels=levels, vmax=vmax, vmin=vmin, cmap='seismic')
    plt.colorbar(c2, ax=axis_2)#, orientation="horizontal")           
                               
    c3 = axis_3.tricontourf(y,z, w, levels=levels, vmax=vmax, vmin=vmin, cmap='seismic')
    plt.colorbar(c3, ax=axis_3)#, orientation="horizontal")
    
    c4 = axis_4.tricontourf(y,z, vtot, levels=levels, vmax=vmax, vmin=vmin, cmap='seismic')
    plt.colorbar(c4, ax=axis_4)#, orientation="horizontal")    
    
    # plot the rotor radius
    axis_1.plot(R*np.cos(psi_360), R*np.sin(psi_360), 'k')
    axis_2.plot(R*np.cos(psi_360), R*np.sin(psi_360), 'k')
    axis_3.plot(R*np.cos(psi_360), R*np.sin(psi_360), 'k')
    axis_4.plot(R*np.cos(psi_360), R*np.sin(psi_360), 'k')
    
    # plot the rotor hub
    axis_1.plot(Rh*np.cos(psi_360), Rh*np.sin(psi_360), 'k')
    axis_2.plot(Rh*np.cos(psi_360), Rh*np.sin(psi_360), 'k')
    axis_3.plot(Rh*np.cos(psi_360), Rh*np.sin(psi_360), 'k')
    axis_4.plot(Rh*np.cos(psi_360), Rh*np.sin(psi_360), 'k')
    
    # plot rotation direction
    style = "Simple, tail_width=0.5, head_width=4, head_length=8"
    kw    = dict(arrowstyle=style,color="k")
    
    if prop.rotation==1:
        # Rotation direction is ccw
        arrow1 = patches.FancyArrowPatch((-0.8*R,-0.8*R),(0.8*R,-0.8*R), connectionstyle="arc3,rad=0.4", **kw)
        arrow2 = patches.FancyArrowPatch((-0.8*R,-0.8*R),(0.8*R,-0.8*R), connectionstyle="arc3,rad=0.4", **kw)
        arrow3 = patches.FancyArrowPatch((-0.8*R,-0.8*R),(0.8*R,-0.8*R), connectionstyle="arc3,rad=0.4", **kw)
        arrow4 = patches.FancyArrowPatch((-0.8*R,-0.8*R),(0.8*R,-0.8*R), connectionstyle="arc3,rad=0.4", **kw)
    elif prop.rotation==-1:
        # Rotation direction is cw
        arrow1 = patches.FancyArrowPatch((0.8*R,-0.8*R),(-0.8*R,-0.8*R), connectionstyle="arc3,rad=-0.4", **kw)
        arrow2 = patches.FancyArrowPatch((0.8*R,-0.8*R),(-0.8*R,-0.8*R), connectionstyle="arc3,rad=-0.4", **kw)
        arrow3 = patches.FancyArrowPatch((0.8*R,-0.8*R),(-0.8*R,-0.8*R), connectionstyle="arc3,rad=-0.4", **kw)
        arrow4 = patches.FancyArrowPatch((0.8*R,-0.8*R),(-0.8*R,-0.8*R), connectionstyle="arc3,rad=-0.4", **kw) 
    
    axis_1.add_patch(arrow1)
    axis_2.add_patch(arrow2)
    axis_3.add_patch(arrow3)
    axis_4.add_patch(arrow4)
    
    axis_1.set_aspect('equal', 'box')
    axis_2.set_aspect('equal', 'box')
    axis_3.set_aspect('equal', 'box')
    axis_4.set_aspect('equal', 'box')
    axis_1.set_xlabel('y')
    axis_1.set_ylabel("z")
    axis_2.set_xlabel('y')
    axis_2.set_ylabel("z")
    axis_3.set_xlabel('y')
    axis_3.set_ylabel("z")
    axis_4.set_xlabel('y')
    axis_4.set_ylabel("z")
    axis_1.set_title("Axial Velocity, u")        
    axis_2.set_title("Spanwise Velocity, v")
    axis_3.set_title("Downwash Velocity, w")
    axis_4.set_title("Total Velocity") 
    
    return fig_1,fig_2,fig_3, fig_4