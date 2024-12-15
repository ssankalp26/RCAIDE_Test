# RCAIDE/Methods/Energy/Sources/Battery/Lithium_Ion_LFP/compute_lfp_cell_performance.py
# 
# 
# Created: Nov 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Units
from RCAIDE.Framework.Mission.Common     import   Conditions
import numpy as np  
from copy import deepcopy

# ----------------------------------------------------------------------------------------------------------------------
# compute_lfp_cell_performance
# ----------------------------------------------------------------------------------------------------------------------  
def append_fuel_cell_conditions(fuel_cell_stack,segment,bus): 
 
    ones_row                                                                = segment.state.ones_row    
                        
    bus_results                                                             = segment.state.conditions.energy[bus.tag]        
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag]                       = Conditions() 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem                   = Conditions()
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem                   = Conditions()

    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].fuel_to_air_ratio     = fuel_cell_stack.fuel_cell.fuel_to_air_ratio* ones_row(1)      
         
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.i                 = 0 * ones_row(1)  
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.p_drop_fc         = fuel_cell_stack.fuel_cell.rated_p_drop_fc * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.p_drop_hum        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.lambda_O2         = 0 * ones_row(1) 
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.T_fc              = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.P_H2_input        = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.P_air             = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.RH                = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.degradation       = 0 * ones_row(1)


    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.FC_air_p          = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].pem.p_air_out         = 0 * ones_row(1)
    
    
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.p_in_comp         = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.pi_comp           = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.mdot_in_comp      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.mdot_out_exp      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.p_in_exp          = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.pi_exp            = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.P_comp            = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.P_motor_comp      = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.P_exp             = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.P_generator_exp   = 0 * ones_row(1)
    bus_results.fuel_cell_stacks[fuel_cell_stack.tag].cem.P_CEM             = 0 * ones_row(1)
           
    
    return

def append_fuel_cell_segment_conditions(fuel_cell_stack, bus, conditions, segment):
    
    
    return


def reuse_stored_fuel_cell_data():
    
    
    return 