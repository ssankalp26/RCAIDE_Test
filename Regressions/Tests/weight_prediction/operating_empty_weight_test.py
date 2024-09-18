# weights.py   
from RCAIDE.Framework.Core import Units,  Data ,  Container
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion       as Propulsion
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Transport        as Transport
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Common           as Common
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import General_Aviation as General_Aviation
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import BWB              as BWB
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Human_Powered    as HP
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import UAV              as UAV
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups import Electric       as Electric
 
from Legacy.trunk.S.Input_Output.SUAVE.load    import load as load_results
from Legacy.trunk.S.Input_Output.SUAVE.archive import archive as save_results 

import numpy as  np 
import sys

sys.path.append('../../Vehicles')
# the analysis functions

from Boeing_737             import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup
from Boeing_BWB_450         import vehicle_setup as bwb_setup
from Tiltwing_EVTOL         import vehicle_setup as evtol_setup
#from Solar_UAV              import vehicle_setup as uav_setup
#from Human_Powered_Glider   import vehicle_setup  as hp_setup

def main(): 
    Transport_Aircraft_Test()
    BWB_Aircraft_Test()
    General_Aviation_Test()
    #Human_Powered_Aircraft_Test()
    EVTOL_Aircraft_Test()
    #UAV_Test()
    return


def Transport_Aircraft_Test(): 
    vehicle = transport_setup() 
    method_types = ['RCAIDE', 'FLOPS Simple', 'FLOPS Complex', 'Raymer']
    
    for method_type in method_types:
        print('Testing Method: '+method_type)
        if 'FLOPS' in method_type:
            settings = Data()
            settings.FLOPS = Data()
            settings.FLOPS.aeroelastic_tailoring_factor = 0.
            settings.FLOPS.strut_braced_wing_factor     = 0.
            settings.FLOPS.composite_utilization_factor = 0.5
            settings.FLOPS.variable_sweep_factor = 1.
        elif 'Raymer' in method_type:
            settings = Data()
            settings.Raymer = Data()
            settings.Raymer.fuselage_mounted_landing_gear_factor = 1.
        else:
            settings = None
            
        weight = Common.compute_operating_empty_weight(vehicle, settings = settings, method_type = method_type)
    
        #save_results(weight, 'weights_'+method_type.replace(' ','_')+'.res')
        old_weight = load_results('weights_'+method_type.replace(' ','_')+'.res')
    
        check_list = [
            'payload_breakdown.total',        
            'payload_breakdown.passengers',             
            'payload_breakdown.baggage',                                   
            'structural_breakdown.wing',            
            'structural_breakdown.fuselage',        
            'propulsion_breakdown.total',      
            'structural_breakdown.nose_landing_gear',    
            'structural_breakdown.main_landing_gear',                   
            'systems_breakdown.total',         
            'systems_breakdown.furnish',      
            'structural_breakdown.horizontal_tail', 
            'structural_breakdown.vertical_tail',
            'empty',  
        ]
    
        # do the check
        for k in check_list:
            print(k) 
            old_val = old_weight.deep_get(k)
            new_val = weight.deep_get(k)
            err = (new_val-old_val)/old_val
            print('Error:' , err)
            assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     
    
            print('')
            
    return 

def General_Aviation_Test():
    
    #General Aviation weights; note that values are taken from Raymer,	
    #but there is a huge spread among the GA designs, so individual components	
    #differ a good deal from the actual design	

    vehicle                = general_aviation_setup()	
    weight                 = General_Aviation.compute_operating_empty_weight(vehicle)	  

    #save_results(weight, 'weights_General_Aviation.res')
    old_weight = load_results('weights_General_Aviation.res')

    check_list = [
        'empty',
        'structural_breakdown.wing',
        'structural_breakdown.fuselage',
        'structural_breakdown.total',
        'propulsion_breakdown.total',   
        'systems_breakdown.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
    return 
        
def BWB_Aircraft_Test():
    # BWB WEIGHTS
    vehicle = bwb_setup()
    weight  = BWB.compute_operating_empty_weight(vehicle)

    #save_results(weight, 'weights_BWB.res')
    old_weight = load_results('weights_BWB.res')
    
    check_list = [
        'empty',
        'structural_breakdown.wing', 
        'structural_breakdown.total',
        'propulsion_breakdown.total',   
        'systems_breakdown.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
        
    return

def EVTOL_Aircraft_Test(): 
    vehicle = evtol_setup()
    weight  = Electric.compute_operating_empty_weight(vehicle)

    #save_results(weight, 'weights_EVTOL.res')
    old_weight = load_results('weights_EVTOL.res')
    
    check_list = [
        'empty', 
        'structural_breakdown.total',
        'propulsion_breakdown.total',   
        'systems_breakdown.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = old_weight.deep_get(k)
        new_val = weight.deep_get(k)
        err = (new_val-old_val)/old_val
        print('Error:' , err)
        assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        print('')
     
    return

        
#def Human_Powered_Aircraft_Test():
    ## Human Powered Aircraft
    #vehicle = hp_setup()
    #weight  = HP.compute_operating_empty_weight(vehicle) 

    #save_results(weight, 'weights_Human_Powered.res')
    #old_weight = load_results('weights_Human_Powered.res')
    
    #check_list = [
        #'empty',
        #'structural_breakdown.wing', 
        #'structural_breakdown.total', 
    #]

    ## do the check
    #for k in check_list:
        #print(k)

        #old_val = old_weight.deep_get(k)
        #new_val = weight.deep_get(k)
        #err = (new_val-old_val)/old_val
        #print('Error:' , err)
        #assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        #print('')
        
    #return       


#def UAV_Test():

    #vehicle = uav_setup()
    #weight  = UAV.compute_operating_empty_weight(vehicle)

    #save_results(weight, 'weights_UAV.res')
    #old_weight = load_results('weights_UAV.res')
    
    #check_list = [
        #'empty', 
    #]

    ## do the check
    #for k in check_list:
        #print(k) 
        #old_val = old_weight.deep_get(k)
        #new_val = weight.deep_get(k)
        #err = (new_val-old_val)/old_val
        #print('Error:' , err)
        #assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     

        #print('') 
    
    #return


if __name__ == '__main__':
    main()
