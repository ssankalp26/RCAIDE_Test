# Regressions/Vehicles/Isolated_Battery_Cell.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Core                                    import Units 
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Common   import initialize_from_circuit_configuration  
 
# ----------------------------------------------------------------------------------------------------------------------
#  Build the Vehicle
# ----------------------------------------------------------------------------------------------------------------------   

def vehicle_setup(current,C_rat,cell_chemistry,fixed_bus_voltage): 

    vehicle                       = RCAIDE.Vehicle() 
    vehicle.tag                   = 'battery'   
    vehicle.reference_area        = 1
 
    # ################################################# Vehicle-level Properties #####################################################   
    # mass properties
    vehicle.mass_properties.takeoff         = 1 * Units.kg 
    vehicle.mass_properties.max_takeoff     = 1 * Units.kg 
         
    net                              = RCAIDE.Framework.Networks.Electric() 
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                              = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus() 
 
    # Battery    
    if cell_chemistry == 'lithium_ion_nmc': 
        battery = RCAIDE.Library.Components.Energy.Sources.Battery_Modules.Lithium_Ion_NMC()
    elif cell_chemistry == 'lithium_ion_lfp': 
        battery = RCAIDE.Library.Components.Energy.Sources.Battery_Modules.Lithium_Ion_LFP()   
    initialize_from_circuit_configuration(battery)  
    battery.voltage = battery.maximum_voltage 
    bus.battery_modules.append(battery)
    bus.battery_module_electric_configuration = 'Series'
    bus.charging_c_rate                       = 1
    bus.initialize_bus_electrical_properties()    
    #------------------------------------------------------------------------------------------------------------------------------------           
    # Payload 
    #------------------------------------------------------------------------------------------------------------------------------------  
    payload                      = RCAIDE.Library.Components.Payloads.Payload()
    payload.power_draw           = current * bus.voltage  
    payload.mass_properties.mass = 1.0 * Units.kg
    bus.payload                  = payload 
    bus.charging_c_rate          = C_rat
      
    # append bus   
    net.busses.append(bus) 
    
    # append network 
    vehicle.append_energy_network(net) 
 
    # ##################################   Determine Vehicle Mass Properties Using Physic Based Methods  ################################       
    vehicle.mass_properties.takeoff = battery.mass_properties.mass 
    return vehicle


def configs_setup(vehicle): 
    configs         = RCAIDE.Library.Components.Configs.Config.Container()  
    discharge_config     = RCAIDE.Library.Components.Configs.Config(vehicle)
    discharge_config.tag = 'discharge' 
    configs.append(discharge_config)
    
    charge_config     = RCAIDE.Library.Components.Configs.Config(vehicle)
    charge_config.tag = 'charge'
    charge_config.networks.electric.busses.bus.payload.power_draw =  0
    configs.append(charge_config)
   
    
    return configs 