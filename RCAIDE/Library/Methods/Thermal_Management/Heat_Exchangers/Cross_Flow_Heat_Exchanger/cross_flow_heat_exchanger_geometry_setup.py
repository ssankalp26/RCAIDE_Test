# RCAIDE/Library/Methods/Thermal_Management/Heat_Exchangers/Cross_Flow_Heat_Exchanger/cross_flow_heat_exchanger_geometry_setup.py
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE     

# ----------------------------------------------------------------------------------------------------------------------  
#  Cross Flow Heat Exchanger Geometry Setup 
# ----------------------------------------------------------------------------------------------------------------------   
def cross_flow_heat_exchanger_geometry_setup(HEX, battery): 
    """ Modifies geometry of Cross Flow Heat Exchanger  
          
          Inputs:  
             nexus     - RCAIDE optmization framework with Wavy Channel geometry data structure [None]
              
          Outputs:   
             procedure - optimization methodology                                       
              
          Assumptions: 
             N/A 
        
          Source:
             None
    """            
    vehicle                                                                  = RCAIDE.Vehicle()  
    net                                                                      = RCAIDE.Framework.Networks.Electric()
    bus                                                                      = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus()
    bus.battery_modules.append(battery)                
    coolant_line                                                             = RCAIDE.Library.Components.Energy.Distributors.Coolant_Line(bus)     
    # Just to create an empty container for the Heat Exchanger
    RCAIDE.Library.Components.Thermal_Management.Batteries.Liquid_Cooled_Wavy_Channel(coolant_line)
    
    HEX.coolant_temperature_of_hot_fluid                  = 313 # Temperature from reservior
    coolant_line.heat_exchangers.cross_flow_hex           = HEX     
    
    net.busses.append(bus)
    net.coolant_lines.append(coolant_line) 
    vehicle.append_energy_network(net) 
    

    
    configs                             = RCAIDE.Library.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Library.Components.Configs.Config(vehicle)  
    config                              = RCAIDE.Library.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 