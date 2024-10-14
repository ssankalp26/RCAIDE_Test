## @ingroup Analyses-Geodesics
# RCAIDE/Framework/Analyses/Geodesics/Geodesics.py
# 
# Created:  Oct. 2024, A. Molloy 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports
from  RCAIDE.Library.Methods.Geodesics.Geodesics import Geodesic_Calculate

# ----------------------------------------------------------------------------------------------------------------------
#  Calculate Distance between two coordinate locations
# ----------------------------------------------------------------------------------------------------------------------  
def Calculate_Distance(coord1, coord2):
    distance = Geodesic_Calculate(coord1, coord2).kilometers
    return(distance)

if __name__ == '__main__': 
    Calculate_Distance()