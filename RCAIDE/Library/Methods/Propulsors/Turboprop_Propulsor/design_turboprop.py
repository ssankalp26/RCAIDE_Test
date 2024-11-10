## @ingroup Library-Methods-Energy-Propulsors-Turboshaft_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turboshaft_Propulsor/design_turboprop.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports     
import RCAIDE
from RCAIDE.Framework.Core                                           import Data
from RCAIDE.Framework.Mission.Common                                 import Conditions
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor         import compute_compressor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turboprop_Propulsor           import size_core 
from RCAIDE.Library.Methods.Propulsors.Common                        import compute_static_sea_level_performance 

# Python package imports   
import numpy                                                                as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Design Turboshaft
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor
def design_turboprop(turboprop):  
    #check if mach number and temperature are passed
    if(turboprop.design_mach_number==None or turboprop.design_altitude==None):
        
        #raise an error
        raise NameError('The sizing conditions require an altitude and a Mach number')
    
    else:
        #call the atmospheric model to get the conditions at the specified altitude
        atmosphere                                        = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data                                         = atmosphere.compute_values(turboprop.design_altitude,turboprop.design_isa_deviation)
        planet                                            = RCAIDE.Library.Attributes.Planets.Earth()
                                                          
        p                                                 = atmo_data.pressure          
        T                                                 = atmo_data.temperature       
        rho                                               = atmo_data.density          
        a                                                 = atmo_data.speed_of_sound    
        mu                                                = atmo_data.dynamic_viscosity   
    
        # setup conditions
        conditions                                        = RCAIDE.Framework.Mission.Common.Results()
    
        # freestream conditions    
        conditions.freestream.altitude                    = np.atleast_1d(turboprop.design_altitude)
        conditions.freestream.mach_number                 = np.atleast_1d(turboprop.design_mach_number)
        conditions.freestream.pressure                    = np.atleast_1d(p)
        conditions.freestream.temperature                 = np.atleast_1d(T)
        conditions.freestream.density                     = np.atleast_1d(rho)
        conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
        conditions.freestream.gravity                     = np.atleast_1d(planet.compute_gravity(turboprop.design_altitude))
        conditions.freestream.isentropic_expansion_factor = np.atleast_1d(turboprop.working_fluid.compute_gamma(T,p))
        conditions.freestream.Cp                          = np.atleast_1d(turboprop.working_fluid.compute_cp(T,p))
        conditions.freestream.R                           = np.atleast_1d(turboprop.working_fluid.gas_specific_constant)
        conditions.freestream.speed_of_sound              = np.atleast_1d(a)
        conditions.freestream.velocity                    = np.atleast_1d(a*turboprop.design_mach_number)
         
         
    fuel_line                                             = RCAIDE.Library.Components.Energy.Distributors.Fuel_Line()
    segment                                               = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions                              = conditions
    segment.state.conditions.energy[fuel_line.tag]        = Conditions()
    segment.state.conditions.noise[fuel_line.tag]         = Conditions()
    turboprop.append_operating_conditions(segment,fuel_line) 
    for tag, item in  turboprop.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,fuel_line,turboprop) 
         
    ram                                                   = turboprop.ram
    inlet_nozzle                                          = turboprop.inlet_nozzle
    compressor                                            = turboprop.compressor
    combustor                                             = turboprop.combustor
    high_pressure_turbine                                 = turboprop.high_pressure_turbine
    low_pressure_turbine                                  = turboprop.low_pressure_turbine
    core_nozzle                                           = turboprop.core_nozzle  

    # unpack component conditions
    turboprop_conditions                                  = conditions.energy[fuel_line.tag][turboprop.tag]
    ram_conditions                                        = turboprop_conditions[ram.tag]     
    inlet_nozzle_conditions                               = turboprop_conditions[inlet_nozzle.tag]
    core_nozzle_conditions                                = turboprop_conditions[core_nozzle.tag] 
    compressor_conditions                                 = turboprop_conditions[compressor.tag]  
    combustor_conditions                                  = turboprop_conditions[combustor.tag]
    lpt_conditions                                        = turboprop_conditions[low_pressure_turbine.tag]
    hpt_conditions                                        = turboprop_conditions[high_pressure_turbine.tag] 
     
    # Step 1: Set the working fluid to determine the fluid properties
    ram.working_fluid                                     = turboprop.working_fluid

    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions,conditions)

    # Step 3: link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature = ram_conditions.outputs.stagnation_temperature
    inlet_nozzle_conditions.inputs.stagnation_pressure    = ram_conditions.outputs.stagnation_pressure
    inlet_nozzle_conditions.inputs.static_temperature     = ram_conditions.outputs.static_temperature
    inlet_nozzle_conditions.inputs.static_pressure        = ram_conditions.outputs.static_pressure
    inlet_nozzle_conditions.inputs.mach_number            = ram_conditions.outputs.mach_number
    inlet_nozzle.working_fluid                            = ram.working_fluid

    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions,conditions)      

    # Step 5: Link low pressure compressor to the inlet nozzle 
    compressor_conditions.inputs.stagnation_temperature   = inlet_nozzle_conditions.outputs.stagnation_temperature
    compressor_conditions.inputs.stagnation_pressure      = inlet_nozzle_conditions.outputs.stagnation_pressure
    compressor_conditions.inputs.static_temperature       = inlet_nozzle_conditions.outputs.static_temperature
    compressor_conditions.inputs.static_pressure          = inlet_nozzle_conditions.outputs.static_pressure
    compressor_conditions.inputs.mach_number              = inlet_nozzle_conditions.outputs.mach_number  
    compressor.working_fluid                              = inlet_nozzle.working_fluid 

    # Step 6: Compute flow through the low pressure compressor
    compute_compressor_performance(compressor,compressor_conditions,conditions)
    
    # Step 7: Link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature    = compressor_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure       = compressor_conditions.outputs.stagnation_pressure
    combustor_conditions.inputs.static_temperature        = compressor_conditions.outputs.static_temperature
    combustor_conditions.inputs.static_pressure           = compressor_conditions.outputs.static_pressure
    combustor_conditions.inputs.mach_number               = compressor_conditions.outputs.mach_number  
    combustor.working_fluid                               = compressor.working_fluid 
    
    # Step 8: Compute flow through the high pressor compressor 
    compute_combustor_performance(combustor,combustor_conditions,conditions)

    #link the high pressure turbione to the combustor 
    hpt_conditions.inputs.stagnation_temperature          = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure             = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio               = combustor_conditions.outputs.fuel_to_air_ratio 
    hpt_conditions.inputs.static_temperature              = combustor_conditions.outputs.static_temperature
    hpt_conditions.inputs.static_pressure                 = combustor_conditions.outputs.static_pressure
    hpt_conditions.inputs.mach_number                     = combustor_conditions.outputs.mach_number 
    hpt_conditions.inputs.compressor                      = compressor_conditions.outputs 
    high_pressure_turbine.working_fluid                   = combustor.working_fluid
    hpt_conditions.inputs.bypass_ratio                    = 0.0
    
    compute_turbine_performance(high_pressure_turbine,hpt_conditions,conditions)
            
    #link the low pressure turbine to the high pressure turbine 
    lpt_conditions.inputs.stagnation_temperature          = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure             = hpt_conditions.outputs.stagnation_pressure 
    lpt_conditions.inputs.static_temperature              = hpt_conditions.outputs.static_temperature
    lpt_conditions.inputs.static_pressure                 = hpt_conditions.outputs.static_pressure 
    lpt_conditions.inputs.mach_number                     = hpt_conditions.outputs.mach_number     
    lpt_conditions.inputs.compressor                      = Data()
    lpt_conditions.inputs.compressor.work_done            = 0.0     
    lpt_conditions.inputs.bypass_ratio                    = 0.0    
    lpt_conditions.inputs.fuel_to_air_ratio               = combustor_conditions.outputs.fuel_to_air_ratio 
    low_pressure_turbine.working_fluid                    = high_pressure_turbine.working_fluid    
     
    compute_turbine_performance(low_pressure_turbine,lpt_conditions,conditions)
    
    #link the core nozzle to the low pressure turbine
    core_nozzle_conditions.inputs.stagnation_temperature  = lpt_conditions.outputs.stagnation_temperature
    core_nozzle_conditions.inputs.stagnation_pressure     = lpt_conditions.outputs.stagnation_pressure
    core_nozzle_conditions.inputs.static_temperature      = lpt_conditions.outputs.static_temperature
    core_nozzle_conditions.inputs.static_pressure         = lpt_conditions.outputs.static_pressure  
    core_nozzle_conditions.inputs.mach_number             = lpt_conditions.outputs.mach_number   
    core_nozzle.working_fluid                             = low_pressure_turbine.working_fluid 
    
    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,core_nozzle_conditions,conditions)

    # compute the thrust using the thrust component

    turboprop_conditions.cpt                              = lpt_conditions.outputs.cp
    turboprop_conditions.R_t                              = lpt_conditions.outputs.gas_constant
    turboprop_conditions.stag_temp_lpt_out                = lpt_conditions.inputs.stagnation_temperature
    turboprop_conditions.stag_temp_lpt_in                 = lpt_conditions.outputs.stagnation_temperature
    turboprop_conditions.stag_temp_hpt_out                = hpt_conditions.inputs.stagnation_temperature
    turboprop_conditions.stag_temp_hpt_in                 = hpt_conditions.outputs.stagnation_temperature
    turboprop_conditions.stag_press_lpt_exit              = lpt_conditions.outputs.stagnation_pressure 
    turboprop_conditions.core_exit_velocity               = core_nozzle_conditions.outputs.velocity
    turboprop_conditions.core_area_ratio                  = core_nozzle_conditions.outputs.area_ratio
    turboprop_conditions.core_nozzle                      = core_nozzle_conditions.outputs
    turboprop_conditions.P9                               = core_nozzle_conditions.outputs.static_pressure    
    turboprop_conditions.T9                               = core_nozzle_conditions.outputs.static_temperature
    turboprop_conditions.cpc                              = compressor_conditions.outputs.cp
    turboprop_conditions.gamma_c                          = compressor_conditions.outputs.gamma
    turboprop_conditions.R_c                              = compressor_conditions.outputs.gas_constant 
    turboprop_conditions.total_temperature_reference      = compressor_conditions.inputs.stagnation_temperature
    turboprop_conditions.total_pressure_reference         = compressor_conditions.inputs.stagnation_pressure 
    turboprop_conditions.fuel_to_air_ratio                = combustor_conditions.outputs.fuel_to_air_ratio
    turboprop_conditions.combustor_stagnation_temperature = combustor_conditions.outputs.stagnation_temperature 
    
    # Step 25: Size the core of the turboprop  
    size_core(turboprop,turboprop_conditions,conditions)
    
    # Step 26: Static Sea Level Thrust 
    compute_static_sea_level_performance(turboprop)

    turboprop.design_thrust_specific_fuel_consumption = turboprop_conditions.thrust_specific_fuel_consumption  
    turboprop.design_non_dimensional_thrust           = turboprop_conditions.non_dimensional_thrust            
    turboprop.design_core_mass_flow_rate              = turboprop_conditions.core_mass_flow_rate               
    turboprop.design_fuel_flow_rate                   = turboprop_conditions.fuel_flow_rate                     
    turboprop.design_power                            = turboprop_conditions.power                             
    turboprop.design_specific_power                   = turboprop_conditions.specific_power                    
    turboprop.design_power_specific_fuel_consumption  = turboprop_conditions.power_specific_fuel_consumption   
    turboprop.design_thermal_efficiency               = turboprop_conditions.thermal_efficiency                
    turboprop.design_propulsive_efficiency            = turboprop_conditions.propulsive_efficiency             
    return      
  