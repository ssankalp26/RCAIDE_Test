# weights.py   
from RCAIDE.Framework.Core import Units,  Data ,  Container
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion       as Propulsion
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Transport        as Transport
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Common           as Common
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import General_Aviation as General_Aviation
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import BWB              as BWB
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Human_Powered    as HP
 
from Legacy.trunk.S.Input_Output.SUAVE.load    import load as load_results
from Legacy.trunk.S.Input_Output.SUAVE.archive import archive as save_results 

import numpy as  np 
import sys

sys.path.append('../../Vehicles')
# the analysis functions

from Boeing_737             import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup
from Boeing_BWB_450         import vehicle_setup as bwb_setup
#from Solar_UAV              import vehicle_setup  as uav_setup
#from Human_Powered_Glider   import vehicle_setup  as hp_setup
#from Solar_UAV              import vehicle_setup  as uav_setupp 



def main(): 
    Transport_Aircraft_Test()
    BWB_Aircraft_Test()
    General_Aviation_Test()
    #Human_Powered_Aircraft_Test()
    EVTOL_Aircraft_Test()
    #UAV_Test()
    return


def Transport_Aircraft_Test():
    # Transport Weights
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
    
        save_results(weight, 'weights_'+method_type.replace(' ','_')+'.res')
        #old_weight = load_results('weights_'+method_type.replace(' ','_')+'.res')
    
        check_list = [
            'payload_breakdown.total',        
            'payload_breakdown.passengers',             
            'payload_breakdown.baggage',                                   
            'structures.wing',            
            'structures.fuselage',        
            'propulsion_breakdown.total',      
            'structures.nose_landing_gear',    
            'structures.main_landing_gear',                   
            'systems_breakdown.total',         
            'systems_breakdown.furnish',      
            'structures.horizontal_tail', 
            'structures.vertical_tail',
            'empty', 
            'fuel'
        ]
    
        ## do the check
        #for k in check_list:
            #print(k)
    
            #old_val = old_weight.deep_get(k)
            #new_val = weight.deep_get(k)
            #err = (new_val-old_val)/old_val
            #print('Error:' , err)
            #assert np.abs(err) < 1e-6 , 'Check Failed : %s' % k     
    
            #print('')
            
    return 

def General_Aviation_Test():
    
    #General Aviation weights; note that values are taken from Raymer,	
    #but there is a huge spread among the GA designs, so individual components	
    #differ a good deal from the actual design	

    vehicle        = general_aviation_setup()	
    weight         = General_Aviation.compute_operating_empty_weight(vehicle)	
    weight.fuel    = vehicle.fuel.mass_properties.mass	
    actual         = Data()	
    actual.bag     = 0.	
    actual.empty   = 694.7649585502986
    actual.fuel    = 53.66245194970156

    actual.wing            = 147.65984323497554
    actual.fuselage        = 126.85012177631337
    actual.propulsion      = 224.40728553408732	
    actual.landing_gear    = 67.81320006645151	
    actual.furnishing      = 37.8341395817	
    actual.electrical      = 41.28649399649684	
    actual.control_systems = 20.51671046011007	
    actual.fuel_systems    = 20.173688786768366	
    actual.systems         = 102.62736387596043	

    error                 = Data()	
    error.fuel            = (actual.fuel - weight.fuel)/actual.fuel	
    error.empty           = (actual.empty - weight.empty)/actual.empty	
    error.wing            = (actual.wing - weight.structures.wing)/actual.wing	
    error.fuselage        = (actual.fuselage - weight.structures.fuselage)/actual.fuselage	
    error.propulsion      = (actual.propulsion - weight.propulsion_breakdown.total)/actual.propulsion	
    error.landing_gear    = (actual.landing_gear - (weight.structures.main_landing_gear+weight.structures.nose_landing_gear))/actual.landing_gear	
    error.furnishing      = (actual.furnishing-weight.systems_breakdown.furnish)/actual.furnishing	
    error.electrical      = (actual.electrical-weight.systems_breakdown.electrical)/actual.electrical	
    error.control_systems = (actual.control_systems-weight.systems_breakdown.control_systems)/actual.control_systems	
    error.fuel_systems    = (actual.fuel_systems-weight.propulsion_breakdown.fuel_system)/actual.fuel_systems	
    error.systems         = (actual.systems - weight.systems_breakdown.total)/actual.systems	

    print('Results (kg)')	
    print(weight)	

    print('Relative Errors')	
    print(error)	

    for k, v in error.items():	
        assert (np.abs(v) < 1E-6)
        
def BWB_Aircraft_Test():
    # BWB WEIGHTS
    vehicle = bwb_setup()
    weight  = BWB.compute_operating_empty_weight(vehicle)

    # regression values
    actual = Data()
    actual.payload         = 27349.9081525 #includes cargo #17349.9081525 #without cargo
    actual.pax             = 15036.587065500002
    actual.bag             = 2313.3210870000003
    actual.fuel            = 23361.42500371662
    actual.empty           = 24417.180232883387
    actual.wing            = 7272.740220314861
    actual.fuselage        = 1.0
    actual.propulsion      = 1413.8593105126783
    actual.landing_gear    = 3160.632
    actual.systems         = 12569.948702055846
    actual.wt_furnish      = 8205.349895589

    # error calculations
    error                 = Data()
    error.payload         = (actual.payload - weight.payload_breakdown.total)/actual.payload
    error.pax             = (actual.pax - weight.payload_breakdown.passengers)/actual.pax
    error.bag             = (actual.bag - weight.payload_breakdown.baggage)/actual.bag
    error.fuel            = (actual.fuel - weight.fuel)/actual.fuel
    error.empty           = (actual.empty - weight.empty)/actual.empty
    error.wing            = (actual.wing - weight.structures.wing)/actual.wing
    error.fuselage        = (actual.fuselage - (weight.structures.fuselage+1.0))/actual.fuselage
    error.propulsion      = (actual.propulsion - weight.propulsion_breakdown.total)/actual.propulsion
    error.systems         = (actual.systems - weight.systems_breakdown.total)/actual.systems
    error.wt_furnish      = (actual.wt_furnish - weight.systems_breakdown.furnish)/actual.wt_furnish

    print('Results (kg)')
    print(weight)

    print('Relative Errors')
    print(error)

    for k, v in error.items():
        assert (np.abs(v) < 1E-6)

def Human_Powered_Aircraft_Test():
    # Human Powered Aircraft
    vehicle = hp_setup()
    weight = HP.compute_operating_empty_weight(vehicle)

    # regression values
    actual = Data()
    actual.empty           = 143.59737768459374
    actual.wing            = 95.43286881794776
    actual.fuselage        = 1.0
    actual.horizontal_tail = 31.749272074174737
    actual.vertical_tail   = 16.415236792471237

    # error calculations
    error                 = Data()
    error.empty           = (actual.empty - weight.empty) / actual.empty
    error.wing            = (actual.wing - weight.wing) / actual.wing
    error.fuselage        = (actual.fuselage - (weight.fuselage + 1.0)) / actual.fuselage
    error.horizontal_tail = (actual.horizontal_tail - weight.horizontal_tail) / actual.horizontal_tail
    error.vertical_tail   = (actual.vertical_tail - weight.vertical_tail) / actual.vertical_tail
    print('Results (kg)')
    print(weight)

    print('Relative Errors')
    print(error)

    for k, v in error.items():
        assert (np.abs(v) < 1E-6)

        
    return


def EVTOL_Aircraft_Test():
     
    return

def UAV_Test():
    
    return


if __name__ == '__main__':
    main()
