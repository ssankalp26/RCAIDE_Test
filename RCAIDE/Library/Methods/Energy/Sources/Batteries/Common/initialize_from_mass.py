# RCAIDE/Methods/Energy/Sources/Battery/Common/initialize_from_mass.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  initialize_from_mass
# ----------------------------------------------------------------------------------------------------------------------  
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
    """     
    useful_mass                            = battery_module.mass_properties.mass/module_weight_factor 
    battery_module.maximum_energy          = useful_mass*battery_module.cell.specific_energy  
    battery_module.maximum_power           = useful_mass*battery_module.cell.specific_power
    battery_module.initial_maximum_energy  = battery_module.maximum_energy         
