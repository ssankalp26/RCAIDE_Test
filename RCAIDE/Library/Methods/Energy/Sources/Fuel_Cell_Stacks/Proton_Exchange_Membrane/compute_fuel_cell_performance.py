import  numpy as  np
from scipy.optimize import minimize_scalar

def compute_fuel_cell_performance(fuel_cell_stack,state,bus,coolant_lines,t_idx,delta_t): 

    # ---------------------------------------------------------------------------------    
    # fuel cell properties
    # ---------------------------------------------------------------------------------  
    fuel_cell       = fuel_cell_stack.fuel_cell
    fuel_cell_mass  = fuel_cell_stack.mass_properties.mass
    
    # ---------------------------------------------------------------------------------
    # Compute Bus electrical properties 
    # ---------------------------------------------------------------------------------    
    bus_conditions              = state.conditions.energy[bus.tag]
    bus_config                  = bus.fuel_cell_stack_electric_configuration
    E_bus                       = bus_conditions.energy
    P_bus                       = bus_conditions.power_draw
    I_bus                       = bus_conditions.current_draw
    
    # ---------------------------------------------------------------------------------
    # Compute fuel_cell_stack Conditions
    # -------------------------------------------------------------------------    
    fuel_cell_stack_conditions = state.conditions.energy[bus.tag].fuel_cell_stacks[fuel_cell_stack.tag]
    
    V_oc_stack         = fuel_cell_stack_conditions.voltage_open_circuit
    V_oc_fuel_cell     = fuel_cell_stack_conditions.fuel_cell.voltage_open_circuit   
    P_cell             = fuel_cell_stack_conditions.fuel_cell.power   
    V_ul_fuel_cell     = fuel_cell_stack_conditions.fuel_cell.voltage_under_load 
    I_cell             = fuel_cell_stack_conditions.fuel_cell.current_density       
    P_stack            = fuel_cell_stack_conditions.power 
    V_ul_stack         = fuel_cell_stack_conditions.voltage_under_load
    I_stack            = fuel_cell_stack_conditions.current      
     
    # ---------------------------------------------------------------------------------
    # Compute fuel_cell_stack electrical properties 
    # -------------------------------------------------------------------------    
    # Calculate the current going into one cell  
    n_series          = fuel_cell_stack.electrical_configuration.series
    n_parallel        = fuel_cell_stack.electrical_configuration.parallel 
    n_total           = n_series*n_parallel 
    no_stacks         = bus.number_of_fuel_cell_stacks
    
    # ---------------------------------------------------------------------------------
    # Examine Thermal Management System
    # ---------------------------------------------------------------------------------
    HAS = None  
    for coolant_line in coolant_lines:
        for tag, item in  coolant_line.items():
            if tag == 'fuel_cell_stacks':
                for sub_tag, sub_item in item.items():
                    if sub_tag == fuel_cell_stack.tag:
                        for btms in  sub_item:
                            HAS = btms     
    # ---------------------------------------------------------------------------------------------------
    # Current State 
    # ---------------------------------------------------------------------------------------------------
    if bus_config == 'Series':
        I_stack[t_idx]      = I_bus[t_idx]
    elif bus_config  == 'Parallel':
        I_stack[t_idx]      = I_bus[t_idx] / bus.number_of_fuel_cell_stacks

    I_cell[t_idx] = I_stack[t_idx] / n_parallel
    V_ul_fuel_cell[t_idx] = V_ul_stack[t_idx] / n_series
       
    # ---------------------------------------------------------------------------------
    # Compute fuel_cell_stack cell temperature 
    # --------------------------------------------------------------------------------- 
    P_H2_and_air  = 10
    alpha         = 0.05
    while abs(diff_V) < 1E-12:
        FAR         =  fuel_cell_conditions.fuel_to_air_ratio[t_idx] 
        fuel_cell_conditions.fuel_cell.inputs.hydrogen_pressure[t_idx] =  P_H2_and_air * FAR
        fuel_cell_conditions.fuel_cell.inputs.air_pressure[t_idx]      =  (1 - FAR) * P_H2_and_air
        
        mdot_H2, voltage, net_power, gross_power, gross_heat, compressor_power, mdot_air_in, mdot_air_out, expander_power =  evaluate_PEM(fuel_cell,fuel_cell_conditions, t_idx)
          
        diff_V =  (voltage - V_ul_fuel_cell) 
        P_H2_and_air    += diff_V * alpha 
        
    P_cell = -V_ul_fuel_cell[t_idx] * I_cell[t_idx] 
    
    # ---------------------------------------------------------------------------------------------------     
    # Future State 
    # --------------------------------------------------------------------------------------------------- 
    if t_idx != state.numerics.number_of_control_points-1:  

        # Compute cell temperature
        if HAS is not None:
            T_cell[t_idx+1]  = HAS.compute_thermal_performance(fuel_cell_stack,bus,coolant_line,Q_heat_fuel_cell[t_idx],T_cell[t_idx],state,delta_t[t_idx],t_idx)
        else:
            # Considers a thermally insulated system and the heat piles on in the system
            dT_dt              = Q_heat_fuel_cell[t_idx]/(fuel_cell_mass*Cp)
            T_cell[t_idx+1]    =  T_cell[t_idx] + dT_dt*delta_t[t_idx]
              
    stored_results_flag            = True
    stored_fuel_cell_stack_tag     = fuel_cell_stack.tag  

    return  stored_results_flag, stored_fuel_cell_stack_tag


def evaluate_PEM(fuel_cell_stack,fuel_cell_conditions,t_idx):
    """
    Determines the fuel cell state of the PEM fuel cell 

    Parameters: 
    ----------
    i: float 
        The current density to evaluate the cell voltage at (A/cm^2)
    stack_temperature: Temperature 
        Temperature of the fuel cell
    P_H2_input: Pressure
        Pressure of the hydrogen stream 
    FC_air_p: Pressure
        Pressure of the hydrogen air entering the fuel cell
    RH: float 
        Relative humidity of the air and hydrogen streams (0-1)
    air_excess_ratio: float 
        Air excess ratio (above stoichometric)
    thermo_state_in: ThermoState 
        Conditions of air entering the compressor
    degradation: float 
        The voltage drop due to degradation (V)
        optional, defaults to 0 V 

    Returns: 
    ----------
    float: 
        Hydrogen Mass flow (kg/s)
    float: 
        Net Power (W)
    float: 
        Gross power (W)
    float: 
        Gross heat (W)
    float: 
        Compressor Power (W)
    float: 
        mdot_air_in (kg/s)
    """
    fuel_cell = fuel_cell_stack.fuel_cell
    i         =  fuel_cell_conditions.fuel_cell.current_density[t_idx]  # input 
    air_excess_ratio =  fuel_cell_conditions.fuel_cell.air_excess_ratio[t_idx] # known  confirmed 
    
    fuel_cell_conditions.fuel_cell.p_drop_fc[t_idx] = calculate_P_drop_stack(fuel_cell,i)
    if fuel_cell.type == "LT":
        fuel_cell_conditions.fuel_cell.p_drop_hum[t_idx] = calculate_P_drop_hum(fuel_cell,i) 
    else: 
        fuel_cell_conditions.fuel_cell.p_drop_hum[t_idx] = 0 
    
    mdot_air_in     = i * fuel_cell.A * fuel_cell.MMO2 / (4 * fuel_cell.F * fuel_cell.O2_mass_frac) * air_excess_ratio
    mdot_H2         = i * fuel_cell.A / (2 * fuel_cell.F) * fuel_cell.MMH2
    V, V_loss       = calculate_voltage(fuel_cell,fuel_cell_conditions,t_idx)
    gross_power     = V * i * fuel_cell.A
    gross_heat      = V_loss * i * fuel_cell.A
    
    # evalaute CEM
    compressor_power, mdot_air_out, expander_power = evaluate_CEM(fuel_cell, fuel_cell_conditions,t_idx)
    parasitic_power  = fuel_cell.gamma_para * gross_power
    net_power        = gross_power - compressor_power - parasitic_power
    
    return mdot_H2,V, net_power, gross_power, gross_heat, compressor_power, mdot_air_in, mdot_air_out, expander_power


def evaluate_CEM(fuel_cell_stack,fuel_cell_conditions,t_idx):
    """
    Evaluates the power required by the CEM (compressor-expander module)

    Parameters: 
    ----------
    FC_air_p: float 
        Air pressure after the humidifier entering the fuel cell (bar)
    thermo_state_in: ThermoState 
        Air thermostate entering the compressor
    mdot_air_in: float 
        Mass flow of air entering the fuel cell and compressor (kg/s)
    air_excess_ratio: float 
        Oxygen excess ratio (above stoichometric)
    p_drop_hum: float 
        The pressure drop (bar) through the humidifier 
    p_drop_fc: float 
        The pressure drop (bar) through the fuel cell

    Returns: 
    ----------
    float: 
        The power required to run the CEM at the given operating conditions (W)
    """
    fuel_cell  = fuel_cell_stack.fuel_cell
    FC_air_p   = fuel_cell_conditions.fuel_cell.inputs.air_pressure[t_idx]
    p_drop_hum = fuel_cell_conditions.fuel_cell.p_drop_hum[t_idx]  
    fuel_cell_conditions.fuel_cell.p_air_out[t_idx]  =  FC_air_p  + p_drop_hum
    
    evaluate_CEM_model(fuel_cell.CEM,fuel_cell_conditions,t_idx)
    power_req      = fuel_cell_conditions.fuel_cell.CEM_power[t_idx]
    mdot_out       = fuel_cell_conditions.fuel_cell.mdot_out_exp[t_idx]
    expander_power = fuel_cell_conditions.fuel_cell.P_exp[t_idx]
    return power_req, mdot_out, expander_power


def calculate_voltage(i, fuel_cell_stack,fuel_cell_conditions,t_idx):
    """
    Calculates the output voltage of the fuel cell by subtracting the activation,
    ohmic, and concentration voltage losses from the reversible Nernst voltage, E_cell.

    Parameters:
    ----------
    i: float 
        The current density to evaluate the cell voltage at (A/cm^2)
    stack_temperature: float 
        Temperature of the fuel cell (K)
    P_H2_input: float 
        Pressure of the hydrogen stream (bar)
    P_air: float 
        Pressure of the incoming air (bar)
    RH: float 
        Relative humidity of the air and hydrogen streams (0-1)
    air_excess_ratio: float 
        Air excess ratio (above stoichometric)
    p_drop_fc: float 
        Pressure drop of the fuel cell at the rated current density (bar)
    degradation: float 
        The percent of maximumm degradation to evaluate divided by 100
        optional, defaults to 0 (0% of fuel_cell.maximum_deg)

    Returns:
    ----------
    float: 
        Output voltage of the fuel cell (V)
    """
    
    # unpack
    fuel_cell   = fuel_cell_stack.fuel_cell
    #i           = fuel_cell_conditions.fuel_cell.current_density[t_idx]   # input 
    stack_temperature        = fuel_cell_conditions.fuel_cell.stack_temperature[t_idx, 0]        # known confirmed 
    P_H2_input  = fuel_cell_conditions.fuel_cell.inputs.hydrogen_pressure[t_idx, 0]   
    P_air       = fuel_cell_conditions.fuel_cell.inputs.air_pressure[t_idx, 0]      
    RH          = fuel_cell_conditions.fuel_cell.oxygen_relative_humidity[t_idx, 0]           # known  confirmed    
    air_excess_ratio   = fuel_cell_conditions.fuel_cell.air_excess_ratio[t_idx, 0]     # known  confirmed 
    p_drop_fc   = fuel_cell_conditions.fuel_cell.p_drop_fc[t_idx, 0]      # known 
    degradation = fuel_cell_conditions.fuel_cell.degradation[t_idx, 0]    # known  confirmed  
    
    P_O2   = calculate_P_O2(fuel_cell_stack,P_air, stack_temperature, RH, air_excess_ratio, p_drop_fc, i)
    P_H2   = calculate_P_H2(fuel_cell_stack,P_H2_input, stack_temperature, RH, i)
    E_cell = calculate_E_cell(fuel_cell_stack,stack_temperature, P_H2, P_O2)
    
    if fuel_cell.type == "LT": 
        eta_ohmic  = calculate_ohmic_losses_LT(fuel_cell_stack,stack_temperature, i) 
        eta_conc   = calculate_concentration_losses_LT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, p_drop_fc, i)
    elif fuel_cell.type == "HT": 
        eta_ohmic = calculate_ohmic_losses_HT(fuel_cell_stack,stack_temperature, i) 
        eta_conc  = calculate_concentration_losses_HT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, p_drop_fc, i) 
    eta_act = calculate_activation_losses(fuel_cell_stack,stack_temperature, P_O2, i) 

    # Calculate the output voltage of the fuel cell
    V_cell = E_cell - eta_act - eta_ohmic - eta_conc - degradation * fuel_cell.maximum_deg
    V_loss = eta_act + eta_ohmic + eta_conc + degradation * fuel_cell.maximum_deg
    return V_cell, V_loss

def set_rated_cd(fuel_cell_stack, rated_cd, rated_pd): 
    """
    Sets the rated cd and pd of the fuel cell system 

    Parameters: 
    ----------
    rated_CD: float
        The current density (A/cm2) to set 
    rated_pd: float 
        The power density (W/cm2) to set 
    """
    fuel_cell   = fuel_cell_stack.fuel_cell
    fuel_cell.rated_cd = rated_cd 
    fuel_cell.rated_pd = rated_pd
    
    return 

def calculate_P_drop_hum(fuel_cell_stack, i):
    """
    Calculates the pressure drop across the humidifier for the rated current 

    Parameters: 
    ----------
    i: float 
        Current Density (Acm2) to calculate the pressure drop 

    Returns: 
    ----------
    float 
        The Humidifier pressure drop in bar
    """
    fuel_cell   = fuel_cell_stack.fuel_cell
    P_drop = (i/fuel_cell.rated_cd) ** 2 * fuel_cell.rated_p_drop_hum
    return P_drop

def calculate_P_drop_stack(fuel_cell_stack, i):
    """
    Calculates the pressure drop across the stack for the rated current 

    Parameters: 
    ----------
    i: float 
        Current Density (Acm2) to calculate the pressure drop

    Returns:
    ---------- 
    float 
        The stack pressure drop in bar 
    """
    fuel_cell   = fuel_cell_stack.fuel_cell
    P_drop = (i/fuel_cell.rated_cd) ** 2 * fuel_cell.rated_p_drop_fc
    return P_drop

def calculate_P_O2(fuel_cell_stack, P_air, stack_temperature, RH, air_excess_ratio, P_drop, i): 
    """
    Calculate the partial pressure of oxygen at the fuel cell cathode 

    Parameters: 
    ----------
    P_air: float 
        The input air pressure to the fuel cell (bar)
    stack_temperature: float 
        The fuel cell stack temperature (K)
    RH: float 
        The relative humidity of the oxygen stream (0-1)
    air_excess_ratio: float 
        The oxygen excess ratio (above stoichometric)
    P_drop: float 
        The pressure drop (bar) across the fuel cell cathode 
    i: float 
        The current density (Acm2) to calculate the partial pressure at

    Returns: 
    ----------
    float
        The oxygen partial pressure (bar)
    """ 
    T_C        = stack_temperature - 273.15
    log_P_H2O = -2.1794 + 0.02953 * T_C - 9.1837e-5 * T_C**2 + 1.4454e-7 * T_C**3
    P_H2O = 10 ** log_P_H2O
    N = 0.291 * i / (stack_temperature ** 0.832)
    P_O2 = 0.21 * (P_air - P_drop / 2 - RH * P_H2O) *  ((1 + (air_excess_ratio - 1) / air_excess_ratio) / 2)/ np.exp(N)
    return P_O2

def calculate_P_H2(fuel_cell_stack, P_H2_input, stack_temperature, RH, i):
    """
    Calculate the partial pressure of hydroen at the fuel cell anode

    Parameters: 
    ----------
    P_H2_input: float 
        The input hydrogen pressure to the fuel cell (bar)
    stack_temperature: float 
        The fuel cell stack temperature (K)
    RH: float 
        The relative humidity of the oxygen stream (0-1)
    i: float 
        The current density (Acm2) to calculate the partial pressure at

    Returns: 
    ----------
    float
        The hydrogen partial pressure (bar)
    """
    T_C = stack_temperature - 273.15
    log_P_H2O = -2.1794 + 0.02953 * T_C - 9.1837e-5 * T_C**2 + 1.4454e-7 * T_C**3
    P_H2O = 10 ** log_P_H2O
    P_H2 = 0.5 * (P_H2_input / np.exp(1.653 * i / stack_temperature**1.334) - RH * P_H2O)
    return P_H2

def calculate_E_cell(fuel_cell_stack, stack_temperature, P_H2, P_O2):
    """
    Calculates the reversible Nernst Voltage of the cell

    Parameters:
    ----------
    stack_temperature: float 
        The fuel cell stack temperature (K)
    P_H2: float 
        The hydrogen partial pressure (bar)
    P_O2: float 
        The oxygen partial pressure (bar)

    Returns:
    ----------
    float 
        The reversible cell potential (V)
    """
    fuel_cell   = fuel_cell_stack.fuel_cell
    try:
        E_cell = 1.229 - 8.45e-4 * (stack_temperature - 298.15) + \
        fuel_cell.R*stack_temperature / (4 * fuel_cell.alpha * fuel_cell.F) * (np.log(P_H2) + 0.5 * np.log(P_O2))
    except: 
        return -10
    return E_cell

def calculate_activation_losses(fuel_cell_stack, stack_temperature, P_O2, i):
    """
    calculation of activation losses for both high temperature and low temperature fuel cells

    Parameters: 
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    P_O2: float 
        Oxygen Partial Pressure (bar)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns: 
    ----------
    float: 
        Activation voltage loss (V)
    """
    fuel_cell = fuel_cell_stack.fuel_cell
    A_const   = fuel_cell.R * stack_temperature / (2 * fuel_cell.alpha * fuel_cell.F)
    i0        = fuel_cell.i0ref * fuel_cell.L_c * fuel_cell.a_c * (P_O2/fuel_cell.i0ref_P_ref) ** (fuel_cell.gamma) * \
        np.exp(-fuel_cell.E_C / (fuel_cell.R * stack_temperature) * (1 - (stack_temperature / fuel_cell.i0ref_T_ref)))
    eta_act = A_const * np.log(i/i0)
    return eta_act

def calculate_ohmic_losses_LT(fuel_cell_stack, stack_temperature, i):
    """
    Calculation of ohmic losses for low temperature fuel cells

    Parameters: 
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns: 
    ----------
    float: 
        Ohmic voltage loss (V)
    """
    fuel_cell  = fuel_cell_stack.fuel_cell
    t_m        = fuel_cell.t_m 
    lambda_eff = fuel_cell.lambda_eff
    num        = 181.6 * (1 + 0.03 * i + 0.062 * (stack_temperature/303) ** 2 * i ** 2.5)
    denom      = (lambda_eff - 0.634 - 3 * i) * np.exp(4.18 * (stack_temperature - 303) / stack_temperature)
    rho        = num/denom 
    eta_ohmic  = (rho * t_m) * i
    return eta_ohmic 

def calculate_ohmic_losses_HT(fuel_cell_stack, stack_temperature, i):
    """
    Calculation of ohmic losses for high temperature fuel cells

    Parameters: 
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns: 
    ----------
    float: 
        Ohmic voltage loss (V)
    """
    fuel_cell = fuel_cell_stack.fuel_cell
    t_m       = fuel_cell.t_m 
    c1        = fuel_cell.c1
    c2        = fuel_cell.c2
    s         = (stack_temperature - 373.15) / (100) * (c2 - c1) + c1
    rho       = 1/s 
    eta_ohmic = (rho * t_m) * i
    return eta_ohmic

def calculate_concentration_losses_LT(fuel_cell_stack, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i):
    """
    Calculation of concentration losses for low temperature fuel cells 

    Parameters:
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    P_O2: float 
        Oxygen partial pressure (bar)
    RH: float 
        Relative humidity of the oxygen stream (0-1)
    air_excess_ratio: float 
        Oxygen excess ratio (above stoichometric)
    P_drop: float 
        Pressure drop across the fuel cell stack (bar)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns:
    ----------
    float: 
        Concentration voltage loss (V)
    """
    fuel_cell =  fuel_cell_stack.fuel_cell
    i_lim =  calculate_limiting_current_density_LT(fuel_cell_stack, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i)
    if i >= i_lim: 
        return 10
    else: 
        eta_conc = (1 + 1 / fuel_cell.alpha) * fuel_cell.R * stack_temperature / (2 * fuel_cell.F) * np.log(i_lim / (i_lim - i)) 
        return eta_conc
    
def calculate_limiting_current_density_LT(fuel_cell_stack, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i, **kwargs): 
    """
    Calculation of the limiting current density for LT-PEM

    Parameters:
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    P_O2: float 
        Oxygen partial pressure (bar)
    RH: float 
        Relative humidity of the oxygen stream (0-1)
    air_excess_ratio: float 
        Oxygen excess ratio (above stoichometric)
    P_drop: float 
        Pressure drop across the fuel cell stack (bar)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns:
    -----------
    float: 
        limiting current density (A/cm^2)
    """
    fuel_cell        =  fuel_cell_stack.fuel_cell
    P_O2_ref_1_atm   = calculate_P_O2(fuel_cell_stack, 1, stack_temperature, RH, air_excess_ratio, P_drop, i)
    P_O2_ref_2_5_atm = calculate_P_O2(fuel_cell_stack, 2.5, stack_temperature, RH, air_excess_ratio, P_drop, i)
    i_lim = (2.25 - 1.65) * (P_O2 - P_O2_ref_1_atm)**1 / (P_O2_ref_2_5_atm-P_O2_ref_1_atm)**1 + 1.65
    return fuel_cell.current_density_limit_multiplier * i_lim
    
def calculate_concentration_losses_HT(fuel_cell_stack, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i):
    """
    Calculation of concentration losses for high temperature fuel cells 

    Parameters:
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    P_O2: float 
        Oxygen partial pressure (bar)
    RH: float 
        Relative humidity of the oxygen stream (0-1)
    air_excess_ratio: float 
        Oxygen excess ratio (above stoichometric)
    P_drop: float 
        Pressure drop across the fuel cell stack (bar)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns:
    -----------
    float: 
        Concentration voltage loss (V)
    """
    fuel_cell = fuel_cell_stack.fuel_cell
    i_lim = calculate_limiting_current_density_HT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i)
    if i >= i_lim: 
        return 10
    else: 
        eta_conc = (1 + 1.8/fuel_cell.alpha) * fuel_cell.R * stack_temperature / (2* fuel_cell.F) * np.log(i_lim / (i_lim - i)) 
        return eta_conc

def calculate_limiting_current_density_HT(fuel_cell_stack, stack_temperature, P_O2, RH, air_excess_ratio, P_drop, i): 
    """
    Calculation of the limiting current density for HT-PEM

    Parameters:
    ----------
    stack_temperature: float 
        Stack Temperature (K)
    P_O2: float 
        Oxygen partial pressure (bar)
    RH: float 
        Relative humidity of the oxygen stream (0-1)
    air_excess_ratio: float 
        Oxygen excess ratio (above stoichometric)
    P_drop: float 
        Pressure drop across the fuel cell stack (bar)
    i: float 
        Current density to evaluate activation losses (A/cm2)
    
    Returns:
    -----------
    float: 
        limiting current density (A/cm^2)
    """
    fuel_cell      = fuel_cell_stack.fuel_cell
    P_O2_ref_1_atm = calculate_P_O2(fuel_cell_stack, 1, stack_temperature, RH, air_excess_ratio, P_drop, i)
    P_O2_ref_2_atm = calculate_P_O2(fuel_cell_stack,2, stack_temperature, RH, air_excess_ratio, P_drop, i)
    i_lim = (2.15 - 1.4) * (P_O2 - P_O2_ref_1_atm)**1 / (P_O2_ref_2_atm-P_O2_ref_1_atm)**1 + 1.4
    return fuel_cell.current_density_limit_multiplier * i_lim


def evaluate_max_gross_power(fuel_cell_stack,fuel_cell_conditions,t_idx):

    fuel_cell    = fuel_cell_stack.fuel_cell
    FC_air_p     = fuel_cell_conditions.fuel_cell.inputs.air_pressure[t_idx, 0]    
    stack_temperature         = fuel_cell_conditions.fuel_cell.stack_temperature[t_idx, 0]        
    RH           = fuel_cell_conditions.fuel_cell.oxygen_relative_humidity[t_idx, 0]          
    air_excess_ratio    = fuel_cell_conditions.fuel_cell.air_excess_ratio[t_idx, 0] 
     
    P_O2 = calculate_P_O2(fuel_cell_stack,FC_air_p, stack_temperature, RH, air_excess_ratio, fuel_cell.rated_p_drop_fc, 0) 

    if fuel_cell.type == "LT":
        i_lim = calculate_limiting_current_density_LT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0)
    elif fuel_cell.type == "HT":
        i_lim = calculate_limiting_current_density_HT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0)  

    res = minimize_scalar(evaluate_power_func, args = (fuel_cell_stack,fuel_cell_conditions,t_idx), bounds = (0.2 * i_lim, 0.95 * i_lim))
    rated_cd  = res.x 
    rated_pd  = -res.fun 
     
    return rated_cd, rated_pd

def evaluate_power_func(i,fuel_cell_stack,fuel_cell_conditions,t_idx): 
    V_cell, V_loss = calculate_voltage(i,fuel_cell_stack,fuel_cell_conditions,t_idx)
    PD = -V_cell * i 
    return PD

def evaluate_max_net_power(fuel_cell_stack,fuel_cell_conditions,t_idx): 

    fuel_cell   = fuel_cell_stack.fuel_cell     
    FC_air_p     = fuel_cell_conditions.fuel_cell.inputs.air_pressure  
    stack_temperature         = fuel_cell_conditions.fuel_cell.stack_temperature      
    RH           = fuel_cell_conditions.fuel_cell.oxygen_relative_humidity        
    air_excess_ratio    = fuel_cell_conditions.fuel_cell.air_excess_ratio
    
    P_O2 =  calculate_P_O2(fuel_cell_stack,FC_air_p, stack_temperature, RH, air_excess_ratio, fuel_cell.rated_p_drop_fc, 0) 
    if fuel_cell.type == "LT":
        i_lim = calculate_limiting_current_density_LT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0)
    elif fuel_cell.type == "HT":
        i_lim = calculate_limiting_current_density_HT(fuel_cell_stack,stack_temperature, P_O2, RH, air_excess_ratio, 0, i=0) 
    compressor_powers = []
    def evaluate_power(i): 
        res = evaluate_PEM(fuel_cell_stack,fuel_cell_conditions,t_idx)
        net_power = res[2]
        compressor_powers.append(res[4])
        return -net_power
    
    res = minimize_scalar(evaluate_power, bounds = (0.2 * i_lim, 0.95 * i_lim))
    compressor_power = compressor_powers[-1]
    rated_cd = res.x 
    rated_power = -res.fun 
    return rated_cd, rated_power, compressor_power

def get_weight_estimate(fuel_cell):
    return fuel_cell.A / 100 / 100 * fuel_cell.area_specific_mass 

def generate_gross_polarization_curve_data(fuel_cell_stack,fuel_cell_conditions,t_idx,  no_points = 200):
    """
    Generates lists containing the output gross voltage as a function of current density of the fuel cell.

    Parameters:
    ----------
    stack_temperature: float
        Fuel cell stack temperature (K)
    P_H2_input: float 
        Input partial pressure of hydrogen (bar)
    P_air: float 
        Input partial pressure of air (bar)
    RH: float 
        Relative humidity (0 to 1)
    air_excess_ratio: float
        Air excess ratio (above stoichometric)
    CD_end: float 
        Current Density to end evaluation at 
    no_points: float 
        Number of current densities to evaluate

    Returns: 
    -----------
    list: 
        current densities that the fuel cell was evaluated at 
    list: 
        output voltages of the fuel cell
    """
    i = fuel_cell_conditions.fuel_cell.current_density[t_idx,0]  # Current densities from 0 to 2 A/cm^2 in steps of 0.01 A/cm^2 
    fuel_cell_conditions.fuel_cell.p_drop_fc[t_idx] =  calculate_P_drop_stack(fuel_cell_stack,i)
    v = calculate_voltage(i, fuel_cell_stack,fuel_cell_conditions,t_idx)[0] 
    if v <0:
        v =  np.nan 
    return i, v

def generate_net_polarization_curve_data(fuel_cell_stack,fuel_cell_conditions,t_idx, no_points = 200):
    """
    Generates lists containing the output net voltage as a function of current density of the fuel cell.

    Parameters:
    ----------
    stack_temperature: float
        Fuel cell stack temperature (K)
    P_H2_input: float 
        Input partial pressure of hydrogen (bar)
    P_air: float 
        Input partial pressure of air (bar)
    RH: float 
        Relative humidity (0 to 1)
    air_excess_ratio: float
        Air excess ratio (above stoichometric)
    CD_end: float 
        Current Density to end evaluation at 
    no_points: float 
        Number of current densities to evaluate

    Returns: 
    -----------
    list: 
        current densities that the fuel cell was evaluated at 
    list: 
        output voltages of the fuel cell
    """
    fuel_cell  = fuel_cell_stack.fuel_cell
    i          = fuel_cell_conditions.fuel_cell.current_density[t_idx,0]  # Current densities from 0 to 2 A/cm^2 in steps of 0.01 A/cm^2 
    v          = evaluate_PEM(fuel_cell_stack,fuel_cell_conditions,t_idx)[2] / i / fuel_cell.A 
    if v <0:
        v =  np.nan 
    return i, v

def evaluate_CEM_model(CEM,fuel_cell_conditions, t_idx): 
    Tt_in          = fuel_cell_conditions.fuel_cell.stagnation_temperature[t_idx] 
    Pt_in          = fuel_cell_conditions.fuel_cell.stagnation_presure[t_idx] 
    mdot_air_in    = fuel_cell_conditions.fuel_cell.mdot_air_in[t_idx]
    p_air_FC       = fuel_cell_conditions.fuel_cell.p_air_out[t_idx] 
    p_drop_hum     = fuel_cell_conditions.fuel_cell.p_drop_hum[t_idx]
    p_drop_fc      = fuel_cell_conditions.fuel_cell.p_drop_fc[t_idx]
    air_excess_ratio      = fuel_cell_conditions.fuel_cell.air_excess_ratio[t_idx] 
    
    Cp             = 1004
    gam            = 1.4
    comp_p_req     = mdot_air_in * Cp* Tt_in * (((p_air_FC + p_drop_hum) / Pt_in) ** ((gam - 1) / gam) - 1) / CEM.compressor_efficiency
    input_p        = comp_p_req / CEM.motor_efficiency 
    p_exp          = p_air_FC - p_drop_fc -p_drop_hum
    Tt_exp         = Tt_in * (p_exp / Pt_in) ** ((gam - 1) / gam)
    mdot_air_out   = mdot_air_in -  mdot_air_in /air_excess_ratio * 0.233
    exp_p_ext      = mdot_air_out * Cp * Tt_exp * (1 - (Pt_in / p_exp) ** ((gam - 1) / gam)) * CEM.expander_efficiency
    output_p       = exp_p_ext * CEM.generator_efficiency
    p_req          = input_p - output_p
     
    fuel_cell_conditions.fuel_cell.p_in_comp[t_idx]        = Pt_in 
    fuel_cell_conditions.fuel_cell.pi_comp[t_idx]          = (p_air_FC + p_drop_hum) / Pt_in 
    fuel_cell_conditions.fuel_cell.mdot_in_comp[t_idx]     = mdot_air_in 
    fuel_cell_conditions.fuel_cell.mdot_out_exp[t_idx]     = mdot_air_out 
    fuel_cell_conditions.fuel_cell.p_in_exp[t_idx]         = p_exp 
    fuel_cell_conditions.fuel_cell.pi_exp[t_idx]           = Pt_in / p_exp 
    fuel_cell_conditions.fuel_cell.P_comp[t_idx]           = comp_p_req
    fuel_cell_conditions.fuel_cell.P_motor_comp[t_idx]     = input_p
    fuel_cell_conditions.fuel_cell.P_exp[t_idx]            = exp_p_ext
    fuel_cell_conditions.fuel_cell.P_generator_exp[t_idx]  = output_p 
    fuel_cell_conditions.fuel_cell.CEM_power[t_idx]        = p_req
    return  

def set_CEM_weight(CEM, compressor_max_power):
    CEM.power_rating = compressor_max_power
    CEM.weight = compressor_max_power / CEM.specific_weight / 1000