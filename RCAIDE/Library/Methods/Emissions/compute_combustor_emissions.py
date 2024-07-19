## @ingroup Library-Methods-Emissions
# RCAIDE/Library/Methods/Emissions/compute_combustor_emissions.py
# 
# Created:  Jul 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_combustor_emissions
# ----------------------------------------------------------------------------------------------------------------------   

def compute_combustor_emissions(combustor,conditions, propellant):
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

    # unpacking the values form combustor
    Tt_in              = combustor.inputs.stagnation_temperature
    Pt_in              = combustor.inputs.stagnation_pressure
    Tt4                = combustor.turbine_inlet_temperature
    pib                = combustor.pressure_ratio
    eta_b              = combustor.efficiency
    nondim_r           = combustor.inputs.nondim_mass_ratio
    P_0                = combustor.inputs.static_pressure
    htf                = combustor.fuel_data.specific_energy
    ar                 = combustor.area_ratio
    
    # unpacking the values from conditions
    gamma              = conditions.freestream.isentropic_expansion_factor 
    Cp                 = conditions.freestream.specific_heat_at_constant_pressure
    To                 = conditions.freestream.temperature
    Tto                = conditions.freestream.stagnation_temperature
    stoichiometric_f   = propellant.stoichiometric_f
    
    # additional input variables
    nuc_fac            = 1
    coag_fac           = 1  
    ox_num_fac         = 1
    ox_fac             = 1
    sg_fac             = 1
    eps                = 2.2
    C_N                = 1.48*(10**(-11))
    rho_soot           = 2000
    C_coag             = 1                                                                                            # 1-9    
    
    # -----------------------------------------------------------------------------------------------------
    # Soot Model (two-equation model) -> 4 steps: nucleation, surface growth, coagulation and oxidation.
    # -----------------------------------------------------------------------------------------------------    
    
    beta_ij            = Ni*Nj*np.pi*((ri + rj)**2)*np.sqrt(8*kB*T/(np.pi*mu_ij))
    gamma_i            = C_N*m_i**4
    dNdt_nuc_ij        = ((gamma_i + gamma_j)/2)*eps*np.sqrt(8*np.pi*kB*T/mu_ij)*(N_A**2)*((ri + rj)**2)*PAH_i*PAH_j
    dNdt_nuc           = np.sum(dNdt_ij)
    dNdt_mech          = nuc_fac*dNdt_nuc + coag_fac*dNdt_coag + ox_num_fac*(N/M)*ox_fac*dMdt_ox                      # equations for soot number density (N) [particles/m**3]
    dNdt_coag          = -C_coag*np.sqrt((24*R_u*T)/(rho_soot*N_A))*(d_p**(0.5))*N**2
    dMdt_nuc           = np.sum(((n_Cij*W_c)/(N_A))*dNdt_ij)
    d_p                = (6*M/(np.pi*rho_soot*N))**(1/3)
    A_S                = N*np.pi*d_p**2
    A_kG               = 7.5*10**2
    Ea_Ru              = 12100
    k_G_T              = A_kG*np.exp(Ea_Ru/T)
    dMdt_sg            = 2*W_c*k_G_T*(C2H2)*f_A_S
    gamma_soot         = 0.3
    dMdt_sg_i          = n_C_i*W_C*((gamma_soot + gamma_i)/2)*eps*np.sqrt(8*np.pi*kB*T/m_soot_i)*(d_p/2 + r_i)**2*N*PAH_i
    dMdt_sg_PAH        = np.sum(dMdt_sg_i)
    dMdt_mech          = nuc_fac*dMdt_nuc + sg_fac*dMdt_sg + ox_fac*dMdt_ox                                           # equations for mass density
    dMdt_ox_i          = -0.25*W_c*eta_i*i*np.sqrt(8*R_u*T/(np.pi*W_i))*np.exp(-E_A_i/(R_u*T))*A_s
    eta_OH             = 0.13
    dMdt_ox_OH         = -8.82*eta_OH*W_c*(T**0.5)*OH*A_S
    eta_OH             = 1
    k_O_2_T            = 745.88*(T**0.5)*np.exp(-19680/T)
    dMdt_ox_OH         = -eta_O_2*W_c*k_O_2_T*O_2*A_S
    eta_O              = 1
    k_O_2              = 1.82*np.sqrt(T)
    dMdt_ox_O          = -eta_O*W_c*k_O_T*O*A_S
        
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
    
    # no soot
    K_v                = 0.001                                                                                      # [kg/(s*Pa)]
    m_dot_in           = combustor.m_dot_in                                                                         # mass flow entering the reactor
    m_dot_out          = m_dot_in + K_v*(P - P_0)                                                                   # Conservation of mass 𝑚 -> dmdt = m_dot_in - m_dot_out
    omega_dot_k        = combustor.omega_dot_k                                                                      # formation rate of species 𝑘 [kmol/(m**3·s)]
    W_k                = combustor.W_k                                                                              # Molecular weight of species 𝑘 [kg/kmol]
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
    
    # with soot
    M                  = combustor.M                                                                                # mass density of soot [kg/m3]
    m_soot             = M*V_PZ                                                                                     # soot mass 
    m_tot              = combustor.m_tot                                                                            # total reactor mass
    m_gas              = m_tot − m_soot                                                                             # mass of the gas
    dYkdt_soot         = combustor.dYkdt_soot                                                                       # change in mass fractions in the gas due to species transitioning from the gas phase to the solid soot phase (and vice versa)
    dYkdt              = omega_dot_k*W_k/rho_gas + m_dot_in*(Y_k_in - Y_k)/m_gas 
    + dYkdt_soot - Y_k*np.sum(dYkdt_soot)                                                                           # Conservation of species
    c_p_soot           = 840                                                                                        # [J/kg*K]
    T_ref              = 298                                                                                        # [K]
    h_soot_ref         = combustor.h_soot_ref                                                                       # assumed to be equal to the specific enthalpy of graphite at 𝑇ref (= 298 K)
    h_soot             = h_soot_ref + c_p_soot*(T - T_ref)                                                          # specific enthalpy of soot
    dHdt_1             = m_dot_in*h_in - h_gas*m_dot_gas_out - h_soot*m_dot_soot_out                                # equation for the change in total enthalpy - step 1
    m_dot_gas_soot     = m_gas*np.sum(dYkdt_soot)                                                                   # total mass (in kg) of soot turning into gas on a per second basis
    m_dot_soot_soot    = - m_dot_gas_soot                                                                           # amount of gas turning into soot [kg/s]
    dm_gas_dt          = m_dot_gas_in - m_dot_gas_out + m_dot_gas_soot                                              # time derivates of m_gas
    dm_soot_dt         = - m_dot_soot_out + m_dot_soot_soot                                                         # time derivates of m_soot
    dHdt_2             = h_gas*dm_gas_dt + h_soot*dm_soot_dt + (m_gas*c_p_gas + m_soot*c_p_soot)*dTdt 
    + m_gas*np.sum(h_k*dYkdt)                                                                                       # equation for the change in total enthalpy - step 2
    dTdt               = (1/(m_gas*c_p_gas + m_soot*c_p_soot))*((-h_soot*m_dot_soot_soot 
    - np.sum(h_k*m_dot_k_gen) + m_dot_gas_in*(h_gas_in - np.sum(h_k*Y_k)) - np.sum(h_k*m_gas*dYkdt_soot)))
    dNdt_m_dot         = - m_dot_out*N/(rho_out*V_PZ)                                                               # general term accounting for the decrease in N due to soot leaving the reactor with the outgoing massflow
    dNdt               = dNdt_mech + dNdt_m_dot                                                                     # equation for N
    dMdt_m_dot         = - m_dot_out*M/(rho_out*V_PZ)                                                               # general term 
    dMdt               = dMdt_mech + dMdt_m_dot                                                                     # equation for M    
                                                                                           
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
        
    # no soot
    dm_dot_gas_dz      = beta_air_in                                                                                # Mass (flow) conservation equation
    u                  = combustor.u                                                                                # Axial velocity [m/s]
    dYkdz              = (beta_air_in*(Y_k_in - Y_k))/(rho_gas*u*A_SZ) + (omega_dot*W_k)/(rho_gas*u)                # Species conservation equation for the secondary zone without soot
    dTdz               = (1/(m_dot_gas*c_p_gas))*(-A_SZ*np.sum(h_k*omega_dot_k*W_k) + 
                                                  beta_air_in*(h_air_in - np.sum(h_k*Y_k_in)))                      # Equation for the temperature
    # with soot
    dm_dot_tot_dz      = beta_air_in                                                                                # conservation of total mass (flow)
    dMdt               = dMdt_mech 
    dm_dot_soot_dz     = dMdt*A_SZ                                                                                  # change of the mass flow of soot
    m_dot_gas          = m_dot_tot - m_dot_soot                                                                     # mass flow of gas
    dNdt               = dNdt_mech
    dn_dot_soot_dz     = dNdt*A_SZ                                                                                  # soot number flow 
    V_dot              = m_dot_gas/rho_gas                                                                          # volume flow
    M                  = m_dot_soot/V_dot
    N                  = n_dot_soot/V_dot
    u                  = m_dot_gas/(rho_gas*A_SZ)                                                                   # velocity
    dYkdz              = (beta_air_in*(Y_k_in - Y_k))/(rho_gas*u*A_SZ) + (omega_dot*W_k)/(rho_gas*u) 
    + (1/u)*dYkdt_soot - (Y_k/u)*np.sum(dYkdt_soot)                                                                 # Species conservation equation for the secondary zone with soot                                                      
    dTdz               = (1/(m_dot_gas*c_p_gas + m_dot_soot*c_p_soot))*(-A_SZ*np.sum(h_k*omega_dot_k*W_k) 
    - A_SZ*rho_gas*np.sum(h_k*dYkdt_soot) - A_SZ*h_soot*dMdt + beta_air_in*(h_air_in - np.sum(h_k*Y_k_in)))         # energy equation
     
    W_c                = combustor.W_c                                                                              # atomic weight of carbon [kg/kmol]
    dMdt_k             = combustor.dMdt_k                                                                           # rate of change in soot mass density due to reactions with species 𝑘 of the soot formation process
    k_f                = combustor.k_f                                                                              # molar ratio in which species 𝑘 reacts to form or destroy soot (0.5 for surface growth through C2H2)
    dYkdt_soot         = - dMdt_k*(W_k*k_f)/(rho_gas*W_c)                                                           # rates of change of mass fractions of the reacting gas species (dYkdt) are adjusted according to the rate of soot formation

    L                  = combustor.L                                                                                # enthalpy of vaporization [J/kg] at standard conditions
    Delta_h            = combustor.Delta_h                                                                          # change in specific enthalpy going from standard conditions to 𝑇3 and 𝑃3
    h_mix              = (1/m_dot_mix)*(m_dot_air*h_air_P3_T3 + m_dot_fuel*h_fuel_P3_T3 - m_dot_fuel*(L + Delta_h)) # specific enthalpy of the gas-fuel mixture
    
    # pack computed quantities into outputs
    combustor.outputs.stagnation_temperature  = Tt4
    
    return 
