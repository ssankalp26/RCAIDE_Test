## @ingroup Methods-Energy-Sources-Battery-Common
# RCAIDE/Methods/Energy/Sources/Battery/Common/initialize_from_circuit_configuration.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Units 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Common
def initialize_from_circuit_configuration(battery_module,module_weight_factor = 1.42):  
    """Calculate module level properties of battery_module using cell 
    properties and module configuraton
    
    Assumptions:
    Total battery_module pack mass contains build-up factor (1.42) for battery_module casing,
    internal wires, thermal management system and battery_module management system 
    Factor computed using information of battery_module properties for X-57 Maxwell 
    Aircraft
    
    Source:
    Cell Charge: Chin, J. C., Schnulo, S. L., Miller, T. B., Prokopius, K., and Gray, 
    J., Battery Performance Modeling on Maxwell X-57",AIAA Scitech, San Diego, CA,
    2019. URLhttp://openmdao.org/pubs/chin_battery_performance_x57_2019.pdf.     

    Inputs:
    mass              
    battery_module.cell
      nominal_capacity        [amp-hours]            
      nominal_voltage         [volts]
      pack_config             [unitless]
      mass                    [kilograms]
                          
    Outputs:              
     battery_module.             
       maximum_energy         [watt-hours]
       maximum_power              [watts]
       initial_maximum_energy [watt-hours]
       specific_energy        [watt-hours/kilogram]
       charging_voltage       [volts]
       charging_current       [amps]
       mass_properties.    
        mass                  [kilograms] 
    """    
    amp_hour_rating                               = battery_module.cell.nominal_capacity    
    nominal_voltage                               = battery_module.cell.nominal_voltage
    maximum_voltage                               = battery_module.cell.maximum_voltage   
    total_battery_assemply_mass                   = battery_module.cell.mass * battery_module.electrical_configuration.series * battery_module.electrical_configuration.parallel   
    battery_module.mass_properties.mass           = total_battery_assemply_mass*module_weight_factor  
    battery_module.specific_energy                = (amp_hour_rating*maximum_voltage)/battery_module.cell.mass  * Units.Wh/Units.kg
    battery_module.maximum_energy                 = total_battery_assemply_mass*battery_module.specific_energy    
    battery_module.specific_power                 = battery_module.specific_energy/battery_module.cell.nominal_capacity 
    battery_module.maximum_power                  = battery_module.specific_power*battery_module.mass_properties.mass  
    battery_module.maximum_voltage                = battery_module.cell.maximum_voltage  * battery_module.electrical_configuration.series   
    battery_module.initial_maximum_energy         = battery_module.maximum_energy      
    battery_module.electrical_configuration.total = battery_module.electrical_configuration.series * battery_module.electrical_configuration.parallel        
