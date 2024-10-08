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
def compute_motor_weight(torque, kwt2=.3928, xwt=.8587):
    """ Calculate the weight of motor using NASA correlations 
            
    Source: NDARC Theory Manual, Page 213
    https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20170011656.pdf
    
    Inputs:
            torque- maximum torque the motor can deliver safely      [N-m]
            kwt2
            xwt
            
    Outputs:
            mass- mass of the motor                                [kilograms]
        
    Properties Used:
            N/A
    """   
    trq  = torque/(Units.ft*Units.lbf)
    mass = kwt2*(trq**xwt) * Units.pounds # mass in kg
     
    return mass 