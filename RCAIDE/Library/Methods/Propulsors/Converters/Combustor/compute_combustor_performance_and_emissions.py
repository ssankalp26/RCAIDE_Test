## @ingroup Library-Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Methods/Energy/Propulsors/Converters/Combustor/compute_combustor_performance_and_emissions.py
# 
# 
# Created:  Jul 2024, M. Guidotti

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
    gamma  = conditions.freestream.isentropic_expansion_factor 
    Cp     = conditions.freestream.specific_heat_at_constant_pressure
    To     = conditions.freestream.temperature
    Tto    = conditions.freestream.stagnation_temperature
    stoichiometric_f = propellant.stoichiometric_f
    
    # unpacking the values form inputs
    Tt_in    = combustor.inputs.stagnation_temperature
    Pt_in    = combustor.inputs.stagnation_pressure
    Tt4      = combustor.turbine_inlet_temperature
    pib      = combustor.pressure_ratio
    eta_b    = combustor.efficiency
    nondim_r = combustor.inputs.nondim_mass_ratio
    P_0      = combustor.inputs.static_pressure
    
    # unpacking values from combustor
    htf    = combustor.fuel_data.specific_energy
    ar     = combustor.area_ratio
    
    # compute pressure
    Pt_out = Pt_in*pib

    # method to compute combustor properties

    # method - computing the stagnation enthalpies from stagnation temperatures
    ht4     = Cp*Tt4*nondim_r
    ht_in   = Cp*Tt_in*nondim_r
    ho      = Cp*To
    
    # Using the Turbine exit temperature, the fuel properties and freestream temperature to compute the fuel to air ratio f
    f       = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out  = Cp*Tt4
    
    # Primary zone input variables
    Phi_PZ_des    = combustor.Phi_PZ_des     # Primary zone design equivalence ratio                 [-]
    N_PZ          = combustor.N_PZ           # Number of primary zone reactors                       [-]
    S_PZ          = combustor.S_PZ           # Primary zone mixing parameter                         [-]
    V_PZ          = combustor.V_PZ           # Primary zone volume                                   [m^3]
                                                                                                     
    # Secondary zone input variables                                                                 
    A_SZ          = combustor.A_SZ           # Secondary zone cross-sectional area                   [m^2]   
    L_SZ          = combustor.L_SZ           # Secondary zone length                                 [m]   
    Phi_SZ_des    = combustor.Phi_SZ_des     # Secondary zone design equivalence ratio               [-]   
    l_SA_SM       = combustor.l_SA_SM        # Secondary air length fraction (of L_SZ) in slow mode  [-]  
    l_SA_FM       = combustor.l_SA_FM        # Secondary air length fraction (of L_SZ) in fast mode  [-]  
    l_DA_start    = combustor.l_DA_start     # Dilution air start length fraction (of L_SZ)          [-]  
    l_DA_end      = combustor.l_DA_end       # Dilution air end length fraction (of L_SZ)            [-]  
    f_SM          = combustor.f_SM           # Fraction of PZ mixture that enters the slow mode      [-] 
    
    m_dot_out     = m_dot_in + K_v*(P - P0)
    
    

    
    # pack computed quantities into outputs
    combustor.outputs.stagnation_temperature  = Tt4
    combustor.outputs.stagnation_pressure     = Pt_out
    combustor.outputs.stagnation_enthalpy     = ht_out
    combustor.outputs.fuel_to_air_ratio       = f 
    return 
