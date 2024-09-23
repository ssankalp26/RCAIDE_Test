# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cylinder_moment_of_inertia.py 
# 
# Created:  Sept. 2024, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cylinder Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cylinder_moment_of_inertia(origin,mass,length,radius,inner_length=0,inner_radius=0,center_of_gravity=[[0,0,0]]):  
    '''[1] Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    '''
    
    # Moment of inertia formula is modifed from "Simplifified Mass and Inertial Estimates for Aircraft with Components of Constant Density" by Benjamin C. Moulton and Douglas F. Hunsaker
    # Of note, this tensor includes the ability to have closed ends... something not included in the paper. 
    # 
    # origin is defined to be the center of the cylinder. 
           
    I =  np.zeros((3, 3))
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Moment of inertia in local system. cylinder axis is along the X-direction.
    # ----------------------------------------------------------------------------------------------------------------------
    
    if  (radius == 0 or length == 0):
        temp = 1
    else:
        temp = (np.pi * radius ** 2 * length - np.pi * inner_radius ** 2 * inner_length) 
    
    rho = mass / temp
    I[0][0] =  rho * (1 / 2 * np.pi * (radius ** 4 * length) - 1 / 2 * np.pi * (inner_radius ** 4 * inner_length)) # Ixx
    I[1][1] =  rho * (1 / 12 * (3 *np.pi*(radius ** 4)*length + np.pi * radius ** 2 * length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Iyy
    I[2][2] =  rho * (1 / 12 * (3 *np.pi*(radius ** 4)*length + np.pi * radius ** 2 * length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Izz
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG    
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global 