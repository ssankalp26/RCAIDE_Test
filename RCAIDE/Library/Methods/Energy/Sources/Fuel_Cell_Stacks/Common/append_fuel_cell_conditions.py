# RCAIDE/Methods/Energy/Sources/fuel_cell/Lithium_Ion_LFP/compute_lfp_cell_performance.py
# 
# 
# Created: Nov 2024, M. Clarke
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
# compute_lfp_cell_performance
# ----------------------------------------------------------------------------------------------------------------------  
def append_fuel_cell_conditions(fuel_cell,segment,bus):
    ones_row                                               = segment.state.ones_row

    # compute ambient conditions
    atmosphere    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    alt           = -segment.conditions.frames.inertial.position_vector[:,2] 
    if segment.temperature_deviation != None:
        temp_dev = segment.temperature_deviation    
    atmo_data    = atmosphere.compute_values(altitude = alt,temperature_deviation=temp_dev)  

    bus_results                                       = segment.state.conditions.energy[bus.tag]        
    bus_results.fuel_cell_stacks[fuel_cell.tag]          = Conditions() 
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell     = Conditions()


    bus_results.fuel_cell_stacks[fuel_cell.tag].voltage_open_circuit      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.voltage_open_circuit = 0 * ones_row(1)

    bus_results.fuel_cell_stacks[fuel_cell.tag].internal_resistance       = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.internal_resistance  = 0 * ones_row(1)

    bus_results.fuel_cell_stacks[fuel_cell.tag].voltage_under_load         = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.voltage_under_load    = 0 * ones_row(1)

    bus_results.fuel_cell_stacks[fuel_cell.tag].power                      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.power                 = 0 * ones_row(1)   

    bus_results.fuel_cell_stacks[fuel_cell.tag].power_draw                 = 0 * ones_row(1)    
    bus_results.fuel_cell_stacks[fuel_cell.tag].current_draw               = 0 * ones_row(1)

    bus_results.fuel_cell_stacks[fuel_cell.tag].current                    = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.current               = 0 * ones_row(1)  

    bus_results.fuel_cell_stacks[fuel_cell.tag].heat_energy_generated      = 0 * ones_row(1)   
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.heat_energy_generated = 0 * ones_row(1)    

    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.energy                = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell.tag].energy                     = 0 * ones_row(1)      

    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.cycle_in_day               = 0
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.resistance_growth_factor   = 1.
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.capacity_fade_factor       = 1. 

    # Conditions for recharging fuel_cell 
    if isinstance(segment,RCAIDE.Framework.Mission.Segments.Ground.Recharge):
        segment.state.conditions.energy.recharging  = True 
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1)
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Discharge:
        segment.state.conditions.energy.recharging   = False 
        segment.state.unknowns['discharge']          =  0* ones_row(1)  
        segment.state.residuals.network['discharge'] =  0* ones_row(1)     
    else:
        segment.state.conditions.energy.recharging  = False 

    # first segment 
    if 'initial_fuel_cell_state_of_charge' in segment:  
        initial_fuel_cell_energy                                            = segment.initial_fuel_cell_state_of_charge*fuel_cell.maximum_energy   
        bus_results.fuel_cell_stacks[fuel_cell.tag].maximum_initial_energy   = initial_fuel_cell_energy
        bus_results.fuel_cell_stacks[fuel_cell.tag].energy                   = initial_fuel_cell_energy* ones_row(1) 
        bus_results.fuel_cell_stacks[fuel_cell.tag].state_of_charge          = segment.initial_fuel_cell_state_of_charge* ones_row(1) 
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.state_of_charge     = segment.initial_fuel_cell_state_of_charge* ones_row(1) 
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.depth_of_discharge  = 1 - segment.initial_fuel_cell_state_of_charge* ones_row(1)
    else:  
        bus_results.fuel_cell_stacks[fuel_cell.tag].energy                    = 0 * ones_row(1)
        bus_results.fuel_cell_stacks[fuel_cell.tag].state_of_charge           = 0 * ones_row(1)
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.state_of_charge      = 0 * ones_row(1)       
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.depth_of_discharge   = 0 * ones_row(1)   

    # temperature 
    if 'fuel_cell_cell_temperature' in segment:
        cell_temperature  = segment.fuel_cell_cell_temperature  
    else:
        cell_temperature                                      = atmo_data.temperature[0,0] 
    bus_results.fuel_cell_stacks[fuel_cell.tag].temperature      = cell_temperature * ones_row(1)         
    bus_results.fuel_cell_stacks[fuel_cell.tag].cell.temperature = cell_temperature * ones_row(1) 

    # charge thoughput 
    if 'charge_throughput' in segment: 
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.charge_throughput          = segment.charge_throughput * ones_row(1)  
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.resistance_growth_factor   = segment.resistance_growth
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.capacity_fade_factor       = segment.capacity_fade
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.cycle_in_day               = segment.cycle_day
    else:
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.charge_throughput          = 0 * ones_row(1)
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.resistance_growth_factor   = 1 
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.capacity_fade_factor       = 1 
        bus_results.fuel_cell_stacks[fuel_cell.tag].cell.cycle_in_day               = 0 
    # This is the only one besides energy and discharge flag that should be moduleed into the segment top level
    if 'increment_fuel_cell_age_by_one_day' not in segment:
        segment.increment_fuel_cell_age_by_one_day   = False    
    
    
    return
 
def append_fuel_cell_segment_conditions(fuel_cell, bus, conditions, segment):
    
    
    return


def reuse_stored_fuel_cell_data():
    
    
    return 