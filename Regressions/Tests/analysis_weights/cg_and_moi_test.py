# cg_and_moi_test.py   
from RCAIDE.Framework.Core import Units,  Data ,  Container 

from RCAIDE.load import load as load_results
from RCAIDE.save import save as save_results 

import numpy as  np 
import sys

sys.path.append('../../Vehicles')
# the analysis functions

from Boeing_737             import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup

def main(): 
    Transport_Aircraft_Test()
    BWB_Aircraft_Test()
    return

def General_Aviation_Test(): 

    vehicle                = general_aviation_setup()	
    weight                 = General_Aviation.compute_operating_empty_weight(vehicle)	  
 
    return  

def EVTOL_Aircraft_Test(): 
    vehicle = evtol_setup()
    weight  = Electric.compute_operating_empty_weight(vehicle)
    
    return 
 

if __name__ == '__main__':
    main()
