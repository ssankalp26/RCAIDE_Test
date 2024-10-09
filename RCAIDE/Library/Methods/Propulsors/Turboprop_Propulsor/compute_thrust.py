## @ingroup Methods-Energy-Propulsors-Turboprop_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turboprop_Propulsor/compute_thrust.py
# 
# 
# Created:  Sep 2024, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Units 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_thrust
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turboprop_Propulsor
def compute_thrust(turboprop,turboprop_conditions,conditions):
    """Computes thrust and other properties as below.

    Assumptions:
    Perfect gas

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor        [-] (gamma)
      specific_heat_at_constant_pressure [J/(kg K)]
      velocity                           [m/s]
      speed_of_sound                     [m/s]
      mach_number                        [-]
      pressure                           [Pa]
      gravity                            [m/s^2]
    conditions.throttle                  [-] (.1 is 10%)
    Turboprop_conditions.
      fuel_to_air_ratio                  [-]
      total_temperature_reference        [K]
      total_pressure_reference           [Pa]
      core_nozzle.
        velocity                         [m/s]
        static_pressure                  [Pa]
        area_ratio                       [-]
      fan_nozzle.
        velocity                         [m/s]
        static_pressure                  [Pa]
        area_ratio                       [-]
      number_of_engines                  [-]
      bypass_ratio                       [-]
      flow_through_core                  [-] percentage of total flow (.1 is 10%)
      flow_through_fan                   [-] percentage of total flow (.1 is 10%)

    Outputs:
    Turboprop_conditions.
      thrust                             [N]
      thrust_specific_fuel_consumption   [N/N-s]
      non_dimensional_thrust             [-]
      core_mass_flow_rate                [kg/s]
      fuel_flow_rate                     [kg/s]
      power                              [W]
      Specific Impulse                   [s]

    Properties Used:
    Turboprop.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      compressor_nondimensional_massflow [-]
      SFC_adjustment                     [-]
    """       
    
    #compute dimensional mass flow rates
    throttle                                       = 1.0    
    g                                              = conditions.freestream.gravity 
    Tref                                           = turboprop.reference_temperature
    Pref                                           = turboprop.reference_pressure  
    total_temperature_reference                    = turboprop_conditions.total_temperature_reference
    total_pressure_reference                       = turboprop_conditions.total_pressure_reference     
    
    #unpack from turboprop
    f                                              = turboprop_conditions.fuel_to_air_ratio 
    cp_t                                           = turboprop_conditions.cpt
    cp_c                                           = turboprop_conditions.cpc
    R_t                                            = turboprop_conditions.R_t
    R_c                                            = turboprop_conditions.R_c
    T9                                             = turboprop_conditions.T9
    P9                                             = turboprop_conditions.P9  
    gamma_c                                        = turboprop_conditions.gamma_c
    V9                                             = turboprop_conditions.core_exit_velocity
    T0                                             = conditions.freestream.temperature
    P0                                             = conditions.freestream.pressure      
    M0                                             = conditions.freestream.mach_number
    V0                                             = conditions.freestream.velocity
    a0                                             = conditions.freestream.speed_of_sound  
    Tt4                                            = turboprop.combustor.turbine_inlet_temperature
    eta_prop                                       = turboprop.design_propeller_efficiency
    eta_g                                          = turboprop.design_gearbox_efficiency
    eta_mL                                         = turboprop.low_pressure_turbine.mechanical_efficiency
    h_PR                                           = turboprop.combustor.fuel_data.lower_heating_value
    tau_tH                                         = (turboprop_conditions.stag_temp_hpt_out/turboprop_conditions.stag_temp_hpt_in)
    tau_tL                                         = (turboprop_conditions.stag_temp_lpt_out/turboprop_conditions.stag_temp_lpt_in)

    C_prop                                         = eta_prop*eta_g*eta_mL*(1 + f)*(cp_t*Tt4)/(cp_c*T0)*tau_tH*(1 - tau_tL)
    Cc                                             = (gamma_c - 1)*M0*((1 + f)*(V9/a0) - M0 + (1 + f)*(R_t/R_c)*((T9/T0)/((V9/a0)))*((1 - (P0/P9))/gamma_c))
    C_tot                                          = Cc + C_prop
    Fsp                                            = (C_tot*cp_c*T0)/(V0)   #Computing Specifc Thrust
    TSFC                                           = (f/(Fsp)) * Units.hour # 1/s is converted to 1/hr here
    Isp                                            = Fsp*a0/(f*g)           #Computing the specific impulse
    W_dot_mdot0                                    = C_tot*cp_c*T0
    PSFC                                           = (f/(C_tot*cp_c*T0))
    eta_T                                          = C_tot/((f*h_PR)/(cp_c*T0))
    eta_P                                          = C_tot/((C_prop/eta_prop) + ((gamma_c - 1)/2)*((1 + f)*((V9/a0))**2 - M0**2))    
    
    mdot_core                                      = turboprop.design_thrust/(Fsp*throttle)  
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))
    
    #computing the dimensional thrust
    FD2              = Fsp*mdot_core*throttle

    #fuel flow rate
    a = np.array([0.])        
    fuel_flow_rate   = np.fmax(FD2*TSFC/g,a)*1./Units.hour

    #computing the power 
    power            = FD2*V0

    # pack outputs 
    turboprop_conditions.thrust                            = FD2 
    turboprop_conditions.thrust_specific_fuel_consumption  = TSFC
    turboprop_conditions.non_dimensional_thrust            = Fsp 
    turboprop_conditions.core_mass_flow_rate               = mdot_core
    turboprop_conditions.fuel_flow_rate                    = fuel_flow_rate    
    turboprop_conditions.power                             = power  
    turboprop_conditions.specific_impulse                  = Isp
    turboprop_conditions.specific_power                    = W_dot_mdot0  
    turboprop_conditions.power_specific_fuel_consumption   = PSFC 
    turboprop_conditions.thermal_efficiency                = eta_T
    turboprop_conditions.propulsive_efficiency             = eta_P

    return 