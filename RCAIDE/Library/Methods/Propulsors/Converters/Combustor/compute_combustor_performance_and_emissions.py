## @ingroup Library-Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Methods/Energy/Propulsors/Converters/Combustor/compute_combustor_performance_and_emissions.py
# 
# 
# Created:  Jul 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_combustor_performance_and_emissions
# ----------------------------------------------------------------------------------------------------------------------   

## @ingroup Energy-Propulsors-Converters-Combustor  
def compute_combustor_performance_and_emissions(combustor,conditions, propellant):
    """ This computes the output values from the input values according to
    equations from the source and the combustor emissions.

    Assumptions:
    Constant efficiency and pressure ratio

    Source: Lukas Frederik Jakob Brink, (2020), 'Modeling the Impact of Fuel Composition on Aircraft Engine NO𝑥, CO and Soot Emissions', Master's Thesis, MIT
    
    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      temperature                         [K]
      stagnation_temperature              [K]
    combustor.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      nondim_mass_ratio                   [-]

    Outputs:
    combustor.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      fuel_to_air_ratio                   [-]

    Properties Used:
    combustor.
      turbine_inlet_temperature           [K]
      pressure_ratio                      [-]
      efficiency                          [-]
      area_ratio                          [-]
      fuel_data.specific_energy           [J/kg]
    """         
    # unpack the values

    # unpacking the values from conditions
    gamma            = conditions.freestream.isentropic_expansion_factor 
    Cp               = conditions.freestream.specific_heat_at_constant_pressure
    To               = conditions.freestream.temperature
    Tto              = conditions.freestream.stagnation_temperature
    stoichiometric_f = propellant.stoichiometric_f
    
    # unpacking the values form inputs
    Tt_in            = combustor.inputs.stagnation_temperature
    Pt_in            = combustor.inputs.stagnation_pressure
    Tt4              = combustor.turbine_inlet_temperature
    pib              = combustor.pressure_ratio
    eta_b            = combustor.efficiency
    nondim_r         = combustor.inputs.nondim_mass_ratio
    P_0              = combustor.inputs.static_pressure
    
    # unpacking values from combustor
    htf              = combustor.fuel_data.specific_energy
    ar               = combustor.area_ratio
    
    # compute pressure
    Pt_out           = Pt_in*pib

    # method to compute combustor properties

    # method - computing the stagnation enthalpies from stagnation temperatures
    ht4              = Cp*Tt4*nondim_r
    ht_in            = Cp*Tt_in*nondim_r
    ho               = Cp*To
    
    # Using the Turbine exit temperature, the fuel properties and freestream temperature to compute the fuel to air ratio f
    f                = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out           = Cp*Tt4
    
    # -----------------------------------------------------------------------------------------------------
    # Combustor Model
    # -----------------------------------------------------------------------------------------------------
    
    # Primary zone input variables
    Phi_PZ_des         = combustor.Phi_PZ_des                                                                       # Primary zone design equivalence ratio                 [-]
    N_PZ               = combustor.N_PZ                                                                             # Number of primary zone reactors                       [-]
    S_PZ               = combustor.S_PZ                                                                             # Primary zone mixing parameter                         [-]
    V_PZ               = combustor.V_PZ                                                                             # Primary zone volume                                   [m^3]
    
    # Primary zone model
    Phi_sign           = combustor.Phi_sign                                                                         # mean equivalence ratio
    sigma_Phi          = S_PZ*Phi_sign                                                                              # standard deviation of the equivalence ratio
    Phi_i              = combustor.Phi_i                                                                            # equivalence ratio 𝜑𝑖
    Delta_Phi          = combustor.Delta_Phi                                                                        # Delta equivalence ratio
    f_Phi_i            = (1/(sigma_Phi*np.sqrt(2*np.pi)))*np.exp(-(Phi_i - Phi_sign)**2/(2*sigma_Phi**2))*Delta_Phi # fraction of mass flow entering reactor 𝑖 at equivalence ratio 𝜑𝑖
    LHV_input_fuel     = combustor.LHV_input_fuel                                                                   # Lower heating value [MJ/kg] used in the engine model to generate the input conditions        
    LHV_model_fuel     = combustor.LHV_model_fuel                                                                   # Lower heating value of the fuel used in the combustor model
    F_SC               = LHV_input_fuel/LHV_model_fuel                                                              # fuel scaler
    m_dot_fuel_takeoff = conditions.m_dot_fuel_takeoff                                                              # mass flow of fuel entering the combustor at takeoff
    m_dot_air_takeoff  = conditions.m_dot_air_takeoff                                                               # mass flow of air at takeoff
    FAR_st             = combustor.FAR_st                                                                           # stoichiometric fuel-to-air ratio
    f_air_PZ           = (m_dot_fuel_takeoff*F_SC)/(Phi_PZ_des*m_dot_air_takeoff*FAR_st)                            # fraction of total air present in the combustor that enters the primary zone
    m_dot_fuel_j       = combustor.m_dot_fuel_j                                                                     # mass flow of fuel at thrust level 𝑗 
    m_dot_air_j        = combustor.m_dot_air_j                                                                      # mass flow of air at thrust level 𝑗
    Phi_j_sign         = m_dot_fuel_j*F_SC/(f_air_PZ*m_dot_air_j*FAR_st)                                            # mean equivalence ratio at thrust level 𝑗
    V_PZ_i             = combustor.V_PZ_i                                                                           # volume of PZ reactor 𝑖
    rho_i              = combustor.rho_i                                                                            # density of the mixture in reactor 𝑖
    m_dot_fuel_i       = combustor.m_dot_fuel_i                                                                     # mass flow of fuel in reactor 𝑖
    m_dot_air_i        = combustor.m_dot_air_i                                                                      # mass flow of air in reactor 𝑖
    t_res_i            = V_PZ_i/(rho_i*(m_dot_fuel_i + m_dot_air_i))                                                # residence time in reactor 𝑖
    
    K_v                = 0.001                                                                                      # [kg/(s*Pa)]
    m_dot_in           = combustor.m_dot_in                                                                         # mass flow entering the reactor
    m_dot_out          = m_dot_in + K_v*(P - P_0)                                                                   # Conservation of mass 𝑚 -> dmdt = m_dot_in - m_dot_out
    omega_dot_k        = combustor.omega_dot_k                                                                      # formation rate of species 𝑘 [kmol/(m**3·s)]
    W_k                = combustor.W_k                                                                              # Molecular weight [kg/kmol]
    Y_k                = combustor.Y_k                                                                              # Mass fraction of species 𝑘 in the gas
    Y_k_in             = combustor.Y_k_in                                                                           # Mass fraction of species 𝑘 in the gas entering the reactor
    rho_gas            = combustor.rho_gas                                                                          # Density of the gas inside the primary zone reactor [kg/m**3]
    m                  = combustor.m                                                                                # Mass
    dYkdt              = omega_dot_k*W_k/rho_gas + m_dot_in*(Y_k_in - Y_k)/m                                        # Conservation of species
    K                  = combustor.K                                                                                # total number of species in the gas
    c_p                = combustor.c_p                                                                              # specific heat capacity of the gas at constant pressure [J/(kg·K)]
    h_k                = combustor.h_k                                                                              # specific enthalpy of species 𝑘 [J/kg]
    m_dot_k_gen        = V_PZ*omega_dot_k*W_k                                                                       # generated mass per second of species 𝑘 [kg/s]
    h_in               = combustor.h_in                                                                             # specific enthalpy entering the reactor
    dTdt               = (1/(m*c_p))*(m_dot_in*(h_in - np.sum(h_k*Y_k_in)) - np.sum(h_k*m_dot_k_gen))               # energy equation for the ideal gas constant pressure reactor
    
    M                  = combustor.M                                                                                # mass density of soot [kg/m3]
    m_soot             = M*V_PZ                                                                                     # soot mass 
    m_tot              = combustor.m_tot                                                                            # total reactor mass
    m_gas              = m_tot − m_soot                                                                             # mass of the gas
    dYkdt_soot         = combustor.dYkdt_soot                                                                       # change in mass fractions in the gas due to species transitioning from the gas phase to the solid soot phase (and vice versa)
    dYkdt              = omega_dot_k*W_k/rho_gas + m_dot_in*(Y_k_in - Y_k)/m_gas + dYkdt_soot - Y_k*np.sum(dYkdt_soot) # Conservation of species
    c_p_soot           = 840                                                                                        # [J/kg*K]
    T_ref              = 298                                                                                        # [K]
    h_soot_ref         = combustor.h_soot_ref                                                                       # assumed to be equal to the specific enthalpy of graphite at 𝑇ref (= 298 K)
    h_soot             = h_soot_ref + c_p_soot*(T - T_ref)
    dHdt               = m_dot_in*h_in - h_gas*m_dot_gas_out - h_soot*m_dot_soot_out
    dTdt               = (1/(m_gas*c_p_gas + m_soot*c_p_soot))*(-h_soot*m_dot_soot - np.sum(h_k*m_dot_k_gen) + m_dot_gas_in*(h_gas_in - np.sum(h_k*Y_k)) - np.sum(h_k*m_gas*dYkdt_soot))
    
                                                                                           
    # Secondary zone input variables                                                                 
    A_SZ               = combustor.A_SZ                                                                             # Secondary zone cross-sectional area                   [m^2]   
    L_SZ               = combustor.L_SZ                                                                             # Secondary zone length                                 [m]   
    Phi_SZ_des         = combustor.Phi_SZ_des                                                                       # Secondary zone design equivalence ratio               [-]   
    l_SA_SM            = combustor.l_SA_SM                                                                          # Secondary air length fraction (of L_SZ) in slow mode  [-]  
    l_SA_FM            = combustor.l_SA_FM                                                                          # Secondary air length fraction (of L_SZ) in fast mode  [-]  
    l_DA_start         = combustor.l_DA_start                                                                       # Dilution air start length fraction (of L_SZ)          [-]  
    l_DA_end           = combustor.l_DA_end                                                                         # Dilution air end length fraction (of L_SZ)            [-]  
    f_SM               = combustor.f_SM                                                                             # Fraction of PZ mixture that enters the slow mode      [-] 
                       
    # Secondary zone model
    m_dot_air          = combustor.m_dot_air                                                                        # mass flow of air 
    f_air_SA           = m_dot_fuel_takeoff/(Phi_SZ_des*FAR_st*m_dot_air_takeoff)                                   # Fraction of total air entering the secondary zone as secondary air 
    f_air_DA           = 1 - f_air_PZ - f_air_SA                                                                    # Dilution air fraction
    f_FM               = 1 - f_SM                                                                                   # Fraction of PZ mixture that enters the fast mode
    beta_SA_SM         = (f_air_SA*f_SM*m_dot_air)/(l_SA_SM*L_SZ)
    beta_SA_FM         = (f_air_SA*f_FM*m_dot_air)/(l_SA_FM*L_SZ)
    beta_DA            = (f_air_DA*m_dot_air)/(l_SA_FM*L_SZ)
    z                  = combustor.z
    if z >= 0 and z <= l_SA_SM*L_SZ:
        beta_air_in    = beta_SA_SM                                                                                 # Magnitude of incoming airflow at any point in the secondary zone
    elif z >= 0 and z <= l_SA_FM*L_SZ:
        beta_air_in    = beta_SA_FM
    elif z >= l_DA_start*L_SZ and z <= l_DA_end*L_SZ:
        beta_air_in    = beta_DA
    else:
        beta_air_in    = 0
        

    
    

    
    # pack computed quantities into outputs
    combustor.outputs.stagnation_temperature  = Tt4
    combustor.outputs.stagnation_pressure     = Pt_out
    combustor.outputs.stagnation_enthalpy     = ht_out
    combustor.outputs.fuel_to_air_ratio       = f 
    return 
