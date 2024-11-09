## @ingroup Methods-Energy-Sources-Battery-Common
# RCAIDE/Methods/Energy/Sources/Battery/Common/initialize_from_geometric_configuration.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Units

import  numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Common
def initialize_from_geometric_configuration(battery_module):
    
    normal_count       = battery_module.electrical_configuration.series 
    parallel_count     = battery_module.electrical_configuration.parallel
    normal_spacing     = battery_module.geometrtic_configuration.normal_spacing   
    parallel_spacing   = battery_module.geometrtic_configuration.parallel_spacing
    packing_factor     = battery_module.packing_factor
    cell_diameter      = battery_module.cell.diameter
    cell_height        = battery_module.cell.height 
        
    euler_angles   = battery_module.orientation_euler_angles
    
    
    x1 =  normal_count * (cell_diameter + normal_spacing) * packing_factor # distance in the module-level normal direction
    x2 =  parallel_count * (cell_diameter + parallel_spacing) * packing_factor # distance in the module-level parallel direction
    x3 =  cell_height * packing_factor # distance in the module-level height direction
    
    if  euler_angles[0] == (np.pi / 2):
        x1prime      = x2
        x2prime      = -x1
        x3prime      = x3
    
    if euler_angles[1] == (np.pi / 2):
        x1primeprime = -x3prime
        x2primeprime = x2prime
        x3primeprime = x1prime
    if euler_angles[2] == (np.pi / 2):
        length       = x1primeprime
        width        = x3primeprime
        height       = -x2primeprime

    # store length, width and height
    battery_module.length = length
    battery_module.width = width
    battery_module.height = height
    
    return 