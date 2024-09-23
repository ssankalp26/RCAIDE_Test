# RCAIDE/Methods/Energy/Distributors/Electrical_Bus.py
# 
# 
# Created: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Methods-Energy-Sources-Battery 
def compute_bus_conditions(bus,state): 
    """  
    """
    
    bus_conditions                         = state.conditions.energy[bus.tag]
    
    for battery_module in  bus.battery_modules:
        bm_conditions                          =  bus_conditions[battery_module]
        bus_conditions.current                 += bm_conditions.current
        bus_conditions.energy                  += bm_conditions.current_energy
        bus_conditions.voltage_open_circuit    = battery.pack.voltage_open_circuit
        bus_conditions.voltage_under_load      = battery.pack.voltage_under_load 
        bus_conditions.heat_energy_generated   = battery.pack.heat_energy_generated
        bus_conditions.efficiency              = (bus_conditions.power_draw+bus_conditions.heat_energy_generated)/bus_conditions.power_draw        
    
    return 