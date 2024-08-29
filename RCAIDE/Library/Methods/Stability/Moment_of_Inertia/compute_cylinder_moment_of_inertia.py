# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cylinder_moment_of_inertia.py 
# 
# Created:  Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE
from RCAIDE.Framework.Core import Units 

# package imports 
import numpy as np 


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cuboid Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cylinder_moment_of_inertia(origin,mass,length,radius,inner_length=0,inner_radius=0,center_of_gravity=[[0,0,0]]):  
    # Moment of inertia formula is modifed from "Simplifified Mass and Inertial Estimates for Aircraft with Components of Constant Density" by Benjamin C. Moulton and Douglas F. Hunsaker
    
    # origin is defined to be the center of the cylinder. 
    I_total = np.zeros((3, 3))
       
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    I[0][0] =  mass / (np.pi * radius ** 2 * length - np.pi * inner_radius ** 2 * inner_length) * (1 / 2 * np.pi * (radius ** 4 * length) - 1 / 2 * np.pi * (inner_radius ** 4 * inner_length)) # Ixx
    I[1][1] =  mass / (np.pi * radius ** 2 * length - np.pi * inner_radius ** 2 * inner_length) * (1 / 12 * (3 *np.pi*(radius ** 4)*length + np.pi * radius ** 2 * length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Iyy
    I[2][2] =  mass / (np.pi * radius ** 2 * length - np.pi * inner_radius ** 2 * inner_length) * (1 / 12 * (3 *np.pi*(radius ** 4)*length + np.pi * radius ** 2 * length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Izz
    
    # transform moment of inertia to global system
    s = np.array(origin) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    I_total = np.array(I_total) + np.array(I_global)
    
    return I_total 