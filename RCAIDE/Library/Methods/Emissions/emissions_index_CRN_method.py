# RCAIDE/Library/Methods/Emissions/emissions_index_CRN_method.py 
# 
# Created:  Jun 2024, M. Clarke


# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports 
# ----------------------------------------------------------------------------------------------------------------------   
import  numpy as  np 
import cantera as ct
import  time
# ---------------------------------------------------------------------------------------------------------------------- 
# emissions_index_CRN_method
# ----------------------------------------------------------------------------------------------------------------------    
def emissions_index_CRN_method(combustor,turbofan_conditions,conditions):
    """
    Chemical Reactor Network Method using Cantera 
    """


    ti        = time.time()

        
    # unpacking the values from conditions 
    Cp      =  conditions.freestream.specific_heat_at_constant_pressure 
    rho0    =  conditions.freestream.density 
    U0      =  conditions.freestream.velocity
    
    # designed
    combustor_conditions = turbofan_conditions[combustor.tag]
    Tt_in                = combustor_conditions.inputs.stagnation_temperature  
    Pt_in                = combustor_conditions.inputs.stagnation_pressure
    Tt_out               = combustor_conditions.outputs.stagnation_temperature
    Pt_out               = combustor_conditions.outputs.stagnation_pressure 
    ht_out               = combustor_conditions.outputs.stagnation_enthalpy   
    mdot_air_core        = turbofan_conditions.core_mass_flow_rate 
    f                    = turbofan_conditions.fuel_flow_rate        
    
    
    
    Tt_mix        = Tt_in      # We are using T of compressure, we need to update it to get to temp with fuel
    Pt_mix        = Pt_in      # Pa to atm We are using P of compressure, we need to update it to get to temp with fuel  

    Area_in           = 2.0  # NEED TO BE VALIDATED 
    psr_pfr_ratio     = 0.1  # NEED TO BE VALIDATED           
    equivalence_ratio = 0.9  # combustor.fuel_equivalency_ratio
    high_fi           = combustor.fuel_data.use_high_fidelity_kinetics_model 
    comb_D            = combustor.diameter
    comb_L            = combustor.length
    N                 = combustor.number_of_combustors

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
    gamma             = gas.cp_mass / gas.cv_mass
    rho               = gas.density_mass
    a                 = gas.sound_speed
    U0                = mdot_air_core/(rho*Area_in)
    M0                = U0/a # NEED TO BE VALIDATED 
    area_out          = N *  np.pi*(comb_D**2)/4
    temperature       = Tt_mix / (1 + 0.5 * (gamma - 1) * M0**2)                         # Static Temperature
    pressure          = Pt_mix / (1 + 0.5 * (gamma - 1) * M0**2)**(gamma / (gamma - 1))  # Static Pressure
    tpfr              = (comb_L/U0)*psr_pfr_ratio
    tpsr              = (comb_L/U0)*(1 - psr_pfr_ratio) 
    
    # Initialize Empty Arrays
    ctrl_pts               =  len(Tt_in[:,0])
    T_stag_out             = np.zeros((ctrl_pts,1))
    P_stag_out             = np.zeros((ctrl_pts,1))
    h_stag_out             = np.zeros((ctrl_pts,1))
    FAR                    = np.zeros((ctrl_pts,1))              
    species_mole_fractions = np.zeros((ctrl_pts,len(species_list)))
    species_mass_fractions = np.zeros((ctrl_pts,len(species_list))) 
    emission_indices       = np.zeros((ctrl_pts,len(species_list))) 
        
    for cpt in range(ctrl_pts):   
        """ combustor simulation using a simple psr-pfr reactor network with varying pfr residence time """
    
        gas.TP = temperature[cpt,0], pressure[cpt,0]*ct.one_atm
        gas.set_equivalence_ratio(equivalence_ratio, fuel = dict_fuel, oxidizer = dict_oxy )
            
        comp_fuel = list(dict_fuel.keys())
        Y_fuel    = gas[comp_fuel].Y
        
        # psr (flame zone) 
        upstream   = ct.Reservoir(gas)
            
        gas.equilibrate('HP')
        psr        = ct.IdealGasReactor(gas) 
        func_mdot  = lambda t: psr.mass/tpsr[cpt,0]
        
        inlet                = ct.MassFlowController(upstream, psr)
        inlet.mass_flow_rate = func_mdot
        sim_psr              = ct.ReactorNet([psr])
            
        try:
            sim_psr.advance_to_steady_state()
        except RuntimeError:
            pass
        
        # pfr (burn-out zone) 
        pfr     = ct.IdealGasConstPressureReactor(gas)
        sim_pfr = ct.ReactorNet([pfr])
        
        try:
            sim_pfr.advance(tpfr[cpt,0]) # sim_pfr.advance(tpfr)
        except RuntimeError:
            pass
        
        # Determine massflow rate of flow into combustion chamber 
        mdot           = inlet.mass_flow_rate
        mdot_fuel      = sum(mdot * Y_fuel)
        mdot_air       = mdot - mdot_fuel
        
        # Determine Emission Indices 
        EIs  = gas.Y * mdot/mdot_fuel
        
        # Extract properties of combustor flow 
        a_out      = gas.sound_speed  # Speed of sound at PFR outlet
        rho_out    = gas.density_mass # density of the gas in the combustor
        gamma      = gas.cp_mass / gas.cv_mass
        vel_out    = mdot / (rho_out * area_out)  # Outlet velocity (m/s)  
        M_out      = vel_out / a_out
   
        # Stagnation temperature 
        T_stag_out[cpt,0] = gas.T * (1 + 0.5 * (gamma - 1) * (M_out)**2)
        
        # stagnation pressure 
        P_stag_out[cpt,0] = (gas.P/ct.one_atm) * (1 + 0.5 * (gamma - 1) * (M_out)**2)**(gamma / (gamma - 1))
        
        # Stagnation enthalpy 
        h_stag_out[cpt,0] = T_stag_out[cpt,0] * gas.cp_mass
        
        # Fuel-to-air ratio (FAR)
        FAR[cpt,0]      = mdot_fuel / mdot_air    
    
        sp_idx = [gas.species_index(sp) for sp in species_list]
        emission_indices[cpt]       = EIs[sp_idx]
        species_mole_fractions[cpt] = gas.X[sp_idx]
        species_mass_fractions[cpt] = gas.Y[sp_idx] 
  
    print(Tt_out)
    print(T_stag_out)
    tf           = time.time()
    elapsed_time = round((tf-ti),2)
    print('Simulation Time: ' + str(elapsed_time) + ' seconds per timestep')     
    return