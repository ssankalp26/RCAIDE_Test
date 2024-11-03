# RCAIDE/Methods/Energy/Distributors/Electrical_Bus.py
# 
# 
# Created: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
def compute_bus_conditions(bus,state,t_idx, delta_t): 
    """ Computes the conditions of the bus based on the response of the battery modules
        
        Assumptions:
        N/A
    
        Source:
        N/A
    
        Inputs:
               bus
               state  
       
        Outputs:
        None
           
        Properties Used:
        None
        """  
    
    bus_conditions                         = state.conditions.energy[bus.tag]
    if t_idx != state.numerics.number_of_control_points-1:  
         # If the battery is fully charged, set the charging current to 0 to accomodate for the cooling time
        if state.conditions.energy.recharging and bus_conditions.state_of_charge[t_idx+1] == 1:
            bus_conditions.charging_current[t_idx+1]    = 0
            bus_conditions.power_draw[t_idx+1]          = 0
            bus_conditions.current_draw[t_idx+1]        = 0
       
        bus_conditions.energy[t_idx+1,0]    = 0
        if bus.battery_module_electric_configuration is  'Series':
            for battery_module in  bus.battery_modules:
                bm_conditions                                    =  bus_conditions.battery_modules[battery_module.tag]
                bus_conditions.voltage_open_circuit[t_idx+1]    += bm_conditions.voltage_open_circuit[t_idx+1]
                bus_conditions.voltage_under_load[t_idx+1]      += bm_conditions.voltage_under_load[t_idx+1]
                bus_conditions.heat_energy_generated[t_idx+1]   += bm_conditions.heat_energy_generated[t_idx+1]
                bus_conditions.temperature[t_idx+1]             += bm_conditions.temperature[t_idx+1]
                bus_conditions.energy[t_idx+1,0]                += bm_conditions.energy[t_idx+1]
            bus_conditions.temperature[t_idx+1]          = bus_conditions.temperature[t_idx+1] / len(bus.battery_modules)
            bus_conditions.state_of_charge[t_idx+1]      = bm_conditions.state_of_charge[t_idx+1]  
            bus_conditions.efficiency[t_idx+1]           = (bus_conditions.power_draw[t_idx+1]+bus_conditions.heat_energy_generated[t_idx+1])/bus_conditions.power_draw[t_idx+1]
           
        elif bus.battery_module_electric_configuration is 'Parallel':
            for battery_module in  bus.battery_modules:
                bm_conditions                                    = bus_conditions.battery_modules[battery_module.tag]
                bus_conditions.heat_energy_generated[t_idx+1]   += bm_conditions.heat_energy_generated[t_idx+1]
                bus_conditions.temperature[t_idx+1]             += bm_conditions.temperature[t_idx+1]
                bus_conditions.energy[t_idx+1]                  += bm_conditions.energy[t_idx+1]
            bus_conditions.voltage_open_circuit[t_idx+1]     = bm_conditions.voltage_open_circuit[t_idx+1]
            bus_conditions.voltage_under_load[t_idx+1]       = bm_conditions.voltage_under_load[t_idx+1]             
            bus_conditions.temperature[t_idx+1]              = bus_conditions.temperature[t_idx+1] / len(bus.battery_modules)
            bus_conditions.state_of_charge[t_idx+1]          = bm_conditions.cell.state_of_charge[t_idx+1]  
            bus_conditions.efficiency[t_idx+1]               = (bus_conditions.power_draw[t_idx+1]+bus_conditions.heat_energy_generated[t_idx+1])/bus_conditions.power_draw[t_idx+1]
            
    return 