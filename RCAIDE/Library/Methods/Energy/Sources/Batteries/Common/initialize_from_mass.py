## @ingroup Methods-Energy-Sources-Battery-Common
# RCAIDE/Methods/Energy/Sources/Battery/Common/initialize_from_mass.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Common
def initialize_from_mass(battery_module,module_weight_factor = 1.42 ):
    """
    Calculate the max energy and power based of the mass
    Assumptions:
    A constant value of specific energy and power

    Inputs:
    mass              [kilograms]
    battery_module.
      specific_energy [J/kg]               
      specific_power  [W/kg]

    Outputs:
     battery_module.
       maximum_energy
       maximum_power
       mass_properties.
        mass


    """     
    mass = battery_module.mass_properties.mass/module_weight_factor
    
    if battery_module.cell.mass == None: 
        n_series   = 1
        n_parallel = 1 
    else:
        n_cells    = int(mass/battery_module.cell.mass)
        n_series   = int(battery_module.maximum_voltage/battery_module.cell.maximum_voltage)
        n_parallel = int(n_cells/n_series)
        
    battery_module.maximum_energy                    = mass*battery_module.cell.specific_energy  
    battery_module.maximum_power                     = mass*battery_module.cell.specific_power
    battery_module.initial_maximum_energy            = battery_module.maximum_energy    
    battery_module.electrical_configuration.series   = n_series
    battery_module.electrical_configuration.parallel = n_parallel 
    battery_module.electrical_configuration.total    = n_parallel*n_series      
