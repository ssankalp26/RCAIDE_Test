## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_rotor_disc_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units

# python imports   
import matplotlib.pyplot as plt 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Library-Plots-Performance-Aerodynamics
def plot_rotor_disc_performance(prop,outputs,i=0,title=None,
                                save_figure=False,
                                save_filename = "Rotor_Disc_Perfomrance",
                                file_type = ".png",
                                width = 8, height = 6):  
    """Plots rotor disc performance

    Assumptions:
    None

    Source: 
    None
    
    Inputs
    outputs    - rotor outputs data structure 

    Outputs:
    Plots

    Properties Used:
    N/A 
    """
     
    # Now plotting:
    psi  = outputs.disc_azimuthal_distribution[i,:,:]
    r    = outputs.disc_radial_distribution[i,:,:]
    psi  = np.append(psi,np.atleast_2d(np.ones_like(psi[:,0])).T*2*np.pi,axis=1)
    r    = np.append(r,np.atleast_2d(r[:,0]).T,axis=1) 
    T    = outputs.disc_thrust_distribution[i]
    Q    = outputs.disc_torque_distribution[i]
    alf  = (outputs.disc_effective_angle_of_attack[i])/Units.deg
    va   = outputs.disc_axial_induced_velocity[i]
    vt   = outputs.disc_tangential_induced_velocity[i]  
    T    = np.append(T,np.atleast_2d(T[:,0]).T,axis=1)
    Q    = np.append(Q,np.atleast_2d(Q[:,0]).T,axis=1)
    alf  = np.append(alf,np.atleast_2d(alf[:,0]).T,axis=1) 
    va   = np.append(va, np.atleast_2d(va[:,0]).T, axis=1)
    vt   = np.append(vt, np.atleast_2d(vt[:,0]).T, axis=1)
    
    lev = 101
    cm  = 'jet'
    
    # plot the grid point velocities
    fig_1   = plt.figure(save_filename + '_Thrust_Distribution' )
    fig_2   = plt.figure(save_filename + '_Torque_Distribution' )
    fig_3   = plt.figure(save_filename + '_Blade_Angle' )
    fig_4   = plt.figure(save_filename + '_Axial_Velocity' )
    fig_5   = plt.figure(save_filename + '_Tangential_Velocity' ) 
    
    fig_1.set_size_inches(width,height)
    fig_2.set_size_inches(width,height)
    fig_3.set_size_inches(width,height)
    fig_4.set_size_inches(width,height) 
    fig_5.set_size_inches(width,height)  
     
    axis_1    = fig_1.add_subplot(111, polar=True)
    axis_2    = fig_2.add_subplot(111, polar=True) 
    axis_3    = fig_3.add_subplot(111, polar=True)  
    axis_4    = fig_4.add_subplot(111, polar=True) 
    axis_5    = fig_5.add_subplot(111, polar=True)   
    
    p_1   = axis_1.contourf(psi, r, T,lev,cmap=cm)
    axis_1.set_title('Thrust Distribution',pad=15)      
    axis_1.set_rorigin(0)
    axis_1.set_yticklabels([])
    plt.colorbar(p_1, ax=axis_1)
       
    p_2   = axis_2.contourf(psi, r, Q,lev,cmap=cm) 
    axis_2.set_title('Torque Distribution',pad=15) 
    axis_2.set_rorigin(0)
    axis_2.set_yticklabels([])    
    plt.colorbar(p_2, ax=axis_2)
       
    p_3   = axis_3.contourf(psi, r, alf,lev,cmap=cm) 
    axis_3.set_title('Local Blade Angle (deg)',pad=15) 
    axis_3.set_rorigin(0)
    axis_3.set_yticklabels([])
    plt.colorbar(p_3, ax=axis_3)
       
    p_4   = axis_4.contourf(psi, r, va,lev,cmap=cm) 
    axis_4.set_title('Va',pad=15) 
    axis_4.set_rorigin(0)
    axis_4.set_yticklabels([])
    plt.colorbar(p_4, ax=axis_4)    
            
    p_5   = axis_5.contourf(psi, r, vt,lev,cmap=cm) 
    axis_5.set_title('Vt',pad=15) 
    axis_5.set_rorigin(0)
    axis_5.set_yticklabels([])
    plt.colorbar(p_5, ax=axis_5)    

    if save_figure:
        fig_1.savefig(save_filename + file_type)
        fig_2.savefig(save_filename + file_type)
        fig_3.savefig(save_filename + file_type)
        fig_4.savefig(save_filename + file_type)
        fig_5.savefig(save_filename + file_type)
        
    return fig_1,fig_2, fig_3, fig_4,fig_5