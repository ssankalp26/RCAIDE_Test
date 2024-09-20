# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cubiod_moment_of_inertia.py 
# 
# Created:  August 2024, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE

# package imports 
import numpy as np 


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cuboid Moment of Intertia: Equations from Simplified Mass and Inertial Estimates for Aircraft by Moulton and Hunsaker
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cubiod_moment_of_inertia(origin,mass,length,width,height,inner_length=0,inner_width=0,inner_height=0,center_of_gravity=[[0,0,0]]):  
    # Moment of inertia formula for a cuboid comes from "Simplifified Mass and Inertial Estimates for Aircraft with Components of Constant Density" by Benjamin C. Moulton and Douglas F. Hunsaker
    # Origin is defined to be the center of the cuboid
    I = np.zeros((3, 3)) 
    
    V2 = length * width * height # Outer volume
    V1 = inner_length * inner_width * inner_height # Inner volume
    
    # Calculate inertia tensor. X is defined to be forward, Y is Port (left) of aircraft, and Z is up.
    I[0][0] = mass / 12 * (V2 * (width ** 2 + height ** 2) - V1 * (inner_width ** 2 + inner_height ** 2)) / (V2 - V1)
    I[1][1] = mass / 12 * (V2 * (length ** 2 + height ** 2) - V1 * (inner_length ** 2 + inner_height ** 2)) / (V2 - V1)
    I[2][2] = mass / 12 * (V2 * (length ** 2 + width ** 2) - V1 * (inner_length ** 2 + inner_width ** 2)) / (V2 - V1)
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s = np.array(origin) - np.array(center_of_gravity) # Vector between component and the CG
        
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global 