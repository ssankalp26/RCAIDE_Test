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
    area_out    = 1  # Assuming the area is 1 m^2 for simplification
    
    # initial conditions 
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
        
        # Determine Emission Indices 
        emission_indexes[cpt] = gas.Y * mdot/mdot_fuel 
        
        # Extract properties of combustor flow 
        #a           = gas.sound_speed # speed of sound 
        #rho_out     = pfr.thermo.density  # density of the gas in the combustor 
        #cp          = gas.cp_mass # specific heat at constant pressure 
        #cv          = gas.cv_mass # specific heat at constant volume 
        #gamma       = cp/cv
        enthalpy[cpt]           = gas.enthalpy # enthalpy
        #vel         = mdot / (rho_out * area_out) # velocity of flow exiting the combustor  
        #M           = vel/a # Mach number 
        
        phi[cpt] = gas.equivalence_ratio(fuel = dict_fuel, oxidizer = dict_oxy ) 
        
        ## Stagnation temperature 
        #T_stag = gas.T/(1 + ((gamma - 1)/2)*M**2)
        
        ## stagnation pressure 
        #P_stag = gas.P*(T_stag/gas.T)**(gamma/(gamma - 1))
        
        tau_b[cpt] = gas.T/temperature[cpt]
        pi_b[cpt]  = gas.P/(pressure[cpt]*ct.one_atm)
         
    
        sp_idx = [gas.species_index(sp) for sp in species_list]
        species_mole_fractions[cpt] = gas.X[sp_idx]
        species_mass_fractions[cpt] = gas.Y[sp_idx] 
  
    
    # Pack results 
    combustor_conditions.outputs.stagnation_temperature  = Tt4
    combustor_conditions.outputs.stagnation_pressure     = Pt_out
    combustor_conditions.outputs.stagnation_enthalpy     = ht_out
    combustor_conditions.outputs.fuel_to_air_ratio       = f 
    
    return