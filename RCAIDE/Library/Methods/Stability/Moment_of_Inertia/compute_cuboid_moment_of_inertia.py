# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cubiod_moment_of_inertia.py 
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
def compute_cubiod_moment_of_inertia(origin,mass,length,width,height,inner_length=0,inner_width=0,inner_height=0,center_of_gravity=[[0,0,0]]):  
    # Moment of inertia formula for a cuboid comes from "Simplifified Mass and Inertial Estimates for Aircraft with Components of Constant Density" by Benjamin C. Moulton and Douglas F. Hunsaker
    I = np.zeros((3, 3)) 
    
    V2 = length * width * height
    V1 = inner_length * inner_width * inner_height
    
    I[0][0] = mass / 12 * (V2 * (width ** 2 + height ** 2) - V1 * (inner_width ** 2 + inner_height ** 2)) / (V2 - V1)
    I[1][1] = mass / 12 * (V2 * (length ** 2 + height ** 2) - V1 * (inner_length ** 2 + inner_height ** 2)) / (V2 - V1)
    I[2][2] = mass / 12 * (V2 * (length ** 2 + width ** 2) - V1 * (inner_length ** 2 + inner_width ** 2)) / (V2 - V1)
    
    
    return I 