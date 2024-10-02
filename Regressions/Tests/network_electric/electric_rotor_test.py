# Regression/scripts/Tests/network_electric/electric_network_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Plots  import *       

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from Stopped_Rotor_EVTOL    import vehicle_setup, configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():           
    vehicle = vehicle_setup()
    # lift Coefficient Check During Cruise
    lift_coefficient_true   = 0
    lift_coefficient        = 0
    print('CL: ' + str(lift_coefficient)) 
    diff_CL                 = np.abs(lift_coefficient  - lift_coefficient_true) 
    print('CL difference: ' +  str(diff_CL)) 
    assert np.abs((lift_coefficient  - lift_coefficient_true)/lift_coefficient_true) < 1e-6 
              
if __name__ == '__main__': 
    main()    
    plt.show()
