# RCAIDE/Library/Methods/Propulsors/Converters/Combustor/compute_PSR_PFR_combustor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke


# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports 
# ----------------------------------------------------------------------------------------------------------------------   
import  numpy as  np 

# ---------------------------------------------------------------------------------------------------------------------- 
#compute_PSR_PFR_combustor_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_PSR_PFR_combustor_performance(combustor,combustor_conditions,conditions):
    """ This computes the output values from the input values according to
        equations from the source. The following properties are computed         
        combustor_conditions.outputs.
          stagnation_temperature             (numpy.ndarray):  [K]  
          stagnation_pressure                (numpy.ndarray):  [Pa]
          stagnation_enthalpy                (numpy.ndarray):  [J/kg]
          fuel_to_air_ratio                  (numpy.ndarray):  [unitless] 

    Assumptions:
        Constant efficiency and pressure ratio

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor        (numpy.ndarray):  [unitless]
          specific_heat_at_constant_pressure (numpy.ndarray):  [J/(kg K)]
          temperature                        (numpy.ndarray):  [K]
          stagnation_temperature             (numpy.ndarray):  [K]
        combustor_conditions.inputs.
          stagnation_temperature             (numpy.ndarray):  [K]
          stagnation_pressure                (numpy.ndarray):  [Pa]
          nondim_mass_ratio                  (numpy.ndarray):  [unitless] 
        combustor.
          turbine_inlet_temperature                  (float):  [K]
          pressure_ratio                             (float):  [unitless]
          efficiency                                 (float):  [unitless]
          area_ratio                                 (float):  [unitless]
          fuel_data.specific_energy                  (float):  [J/kg]
      
    Returns:
        None
    """ 
    # unpacking the values from conditions 
    Cp      =  conditions.freestream.specific_heat_at_constant_pressure 
    
    # unpacking the values form inputs
    Tt_in    = combustor_conditions.inputs.stagnation_temperature
    Pt_in    = combustor_conditions.inputs.stagnation_pressure
    nondim_r = combustor_conditions.inputs.nondim_mass_ratio 
    Tt4      = combustor.turbine_inlet_temperature *  np.ones_like(Tt_in)
    pib      = combustor.pressure_ratio
    eta_b    = combustor.efficiency
    htf      = combustor.fuel_data.specific_energy
    high_fi  = combustor.fuel_data.use_high_fidelity_kinetics_model 
    comb_D   = combustor.diameter
    comb_L   = combustor.length 

    dict_oxy     = combustor.fuel_data.air_chemical_properties    
    if high_fi:
        gas          = combustor.fuel_data.chemical_kinetics
        species_list = combustor.fuel_data.species_list
        dict_fuel    = combustor.fuel_data.fuel_chemical_properties
    else: 
        gas          = combustor.fuel_data.surrogate_chemical_kinetics
        species_list = combustor.fuel_data.surrogate_species_list
        dict_fuel    = combustor.fuel_data.fuel_surrogate_chemical_properties
     

    # ENGINE DESIGN PARAMETRS 
    area_out          = 0 # EDIT MATTEO  
    temperature       = 0 # EDIT MATTEO 
    pressure          = 0 # EDIT MATTEO 
    equivalence_ratio = 0 # EDIT MATTEO 
    tpfr              = 0 # EDIT MATTEO 
    tpsr              = 0 # EDIT MATTEO  
    
    # Initialize Empty Arrays
    ctrl_pts =  len(Tt_in[:,0])
    enthalpy               = np.zeors((ctrl_pts,1))
    phi                    = np.zeors((ctrl_pts,1))
    tau_b                  = np.zeors((ctrl_pts,1))
    pi_b                   = np.zeors((ctrl_pts,1))
    species_mole_fractions = np.zeors((ctrl_pts,len(species_list)))
    species_mass_fractions = np.zeors((ctrl_pts,len(species_list))) 
    emission_indexes       = np.zeors((ctrl_pts,len(species_list))) 
        
    for cpt in range(ctrl_pts):   
        """ combustor simulation using a simple psr-pfr reactor network with varying pfr residence time """
    
        gas.TP = temperature[cpt], pressure[cpt]*ct.one_atm
        gas.set_equivalence_ratio(equivalence_ratio[cpt], fuel = dict_fuel, oxidizer = dict_oxy )
            
        comp_fuel = list(dict_fuel.keys())
        Y_fuel = gas[comp_fuel].Y
        
        # psr (flame zone) 
        upstream   = ct.Reservoir(gas)
        downstream = ct.Reservoir(gas)
            
        gas.equilibrate('HP')
        psr        = ct.IdealGasReactor(gas) 
        func_mdot  = lambda t: psr.mass/tpsr[cpt]
        
        inlet                = ct.MassFlowController(upstream, psr)
        inlet.mass_flow_rate = func_mdot
        outlet               = ct.Valve(psr, downstream, K=100) 
        sim_psr              = ct.ReactorNet([psr])
            
        try:
            sim_psr.advance_to_steady_state()
        except RuntimeError:
            pass
        
        # pfr (burn-out zone) 
        pfr     = ct.IdealGasConstPressureReactor(gas)
        sim_pfr = ct.ReactorNet([pfr])
        
        try:
            sim_pfr.advance(tpfr[cpt]) # sim_pfr.advance(tpfr)
        except RuntimeError:
            pass
        
        # Determine massflow rate of flow into combustion chamber 
        mdot           = inlet.mass_flow_rate
        mdot_fuel      = sum(mdot * Y_fuel)
        mdot_air       = mdot - mdot_fuel
        
        # Determine Emission Indices 
        emission_indexes[cpt] = gas.Y * mdot/mdot_fuel 
        
        # Extract properties of combustor flow 
        a_out[cpt]      = gas.sound_speed  # Speed of sound at PFR outlet
        rho_out[cpt]    = gas.density # density of the gas in the combustor
        gamma[cpt]      = gas.cp_mass / gas.cv_mass
        h[cpt]          = gas.h # enthalpy
        vel_out[cpt]    = mdot / (rho_out[cpt] * area_out)  # Outlet velocity (m/s)  
        M_out[cpt]      = vel_out[cpt] / a_out[cpt] 
        phi[cpt]        = gas.equivalence_ratio(fuel = dict_fuel, oxidizer = dict_oxy ) 
        
        # Stagnation temperature 
        T_stag_out[cpt] = gas.T * (1 + 0.5 * (gamma[cpt] - 1) * (M_out[cpt])**2)
        
        # stagnation pressure 
        P_stag_out[cpt] = gas.P * (1 + 0.5 * (gamma[cpt] - 1) * (M_out[cpt])**2)**(gamma[cpt] / (gamma[cpt] - 1))
        
        # Stagnation enthalpy 
        h_stag_out[cpt] = h[cpt] + 0.5 * vel_out[cpt]**2 
        
        # Fuel-to-air ratio (FAR)
        FAR[cpt]      = mdot_fuel / mdot_air    
             
    
        sp_idx = [gas.species_index(sp) for sp in species_list]
        species_mole_fractions[cpt] = gas.X[sp_idx]
        species_mass_fractions[cpt] = gas.Y[sp_idx] 
  
    
    # Pack results 
    combustor_conditions.outputs.stagnation_temperature  = T_stag_out
    combustor_conditions.outputs.stagnation_pressure     = P_stag_out
    combustor_conditions.outputs.stagnation_enthalpy     = h_stag_out
    combustor_conditions.outputs.fuel_to_air_ratio       = FAR 
    
    return