# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/compute_motor_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
from RCAIDE.Framework.Core import  Units 
 
# ----------------------------------------------------------------------------------------------------------------------
#  Motor Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_motor_weight(torque):
    """ Calculate the weight of motor using NASA correlations 
             
    
    Inputs:
            torque- maximum torque the motor can deliver safely      [N-m]
            kwt2
            xwt
            
    Outputs:
            mass- mass of the motor                                [kilograms]
        
    Properties Used:
            N/A
    """   
    mass  = -2E-7 * (torque ** 2) +  0.0117 * torque +  34.124
     
    return mass 