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
    '''[1] Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    '''
    
    # Moment of inertia formula for a cuboid comes from "Simplifified Mass and Inertial Estimates for Aircraft with Components of Constant Density" by Benjamin C. Moulton and Douglas F. Hunsaker
    # Origin is defined to be the center of the cuboid
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------
    I = np.zeros((3, 3)) 
    
    V2 = length * width * height # Outer volume
    V1 = inner_length * inner_width * inner_height # Inner volume
    
    if  V2 == 0 and V1 == 0:
        temp = 0.000001 # Assigns an arbitrary value to avoid a divide by zero error. This will not affect results as V2 and V1 will be 0
        # Treats object as a point mass
    else:
        temp = (V2 - V1)
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Calculate inertia tensor
    # ----------------------------------------------------------------------------------------------------------------------    
    I[0][0] = mass / 12 * (V2 * (width ** 2 + height ** 2) - V1 * (inner_width ** 2 + inner_height ** 2)) / temp
    I[1][1] = mass / 12 * (V2 * (length ** 2 + height ** 2) - V1 * (inner_length ** 2 + inner_height ** 2)) / temp
    I[2][2] = mass / 12 * (V2 * (length ** 2 + width ** 2) - V1 * (inner_length ** 2 + inner_width ** 2)) / temp
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global 