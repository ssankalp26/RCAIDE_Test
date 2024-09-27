# RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/evaluate_cantera.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from   RCAIDE.Framework.Core import Data  
import cantera               as ct 
import pandas                as pd
import numpy                 as np
import sys
import os 

# ----------------------------------------------------------------------------------------------------------------------
#  evaluate_cantera
# ----------------------------------------------------------------------------------------------------------------------  
def evaluate_cantera(combustor,T,P,mdot,FAR):  

    # ------------------------------------------------------------------------------              
    # ------------------------------ Combustor Inputs ------------------------------              
    # ------------------------------------------------------------------------------              
    
    high_fidelity_kin_mech  = False                                                 # [-]       True (simulation time around 300 s): Computes EI_CO2, EI_CO, EI_H2O, EI_NO2, EI_NO, EI_CSOOT; False (simulation time around 60 s): Computes EI_CO2, EI_CO, EI_H2O
    T_stag_0                = T                                                     # [K]       Stagnation Temperature entering all combustors
    P_stag_0                = P                                                     # [Pa]      Stagnation Pressure entering all combustors
    FAR                     = FAR                                                   # [-]       Fuel-to-Air ratio
    m_dot_air_tot           = mdot                                                  # [kg/s]    Air mass flow going through all combustors
    
    f_air_PZ                = combustor.f_air_PZ                                    # [-]       Fraction of total air present in the combustor that enters the Primary Zone         
    FAR_st                  = combustor.FAR_st                                      # [-]       Stoichiometric Fuel to Air ratio 
    N_comb                  = combustor.N_comb                                      # [-]       Number of can-annular combustors
    N_PZ                    = combustor.N_PZ                                        # [-]       Number of PSR (EVEN, must match the number of PSR below)
    A_PZ                    = combustor.A_PZ                                        # [m**2]    Primary Zone cross-sectional area     
    L_PZ                    = combustor.L_PZ                                        # [m]       Primary Zone length  
    N_SZ                    = combustor.N_SZ                                        # [-]       Number of dilution air inlets        
    A_SZ                    = combustor.A_SZ                                        # [m**2]    Secondary Zone cross-sectional area
    L_SZ                    = combustor.L_SZ                                        # [m]       Secondary Zone length  
    phi_SZ                  = combustor.phi_SZ                                      # [-]       Equivalence Ratio for PFR    phi_PZ_des              = 0.6                                                   # [-]       Primary Zone Design Equivalence Ratio
    S_PZ                    = combustor.S_PZ                                        # [-]       Mixing parameter, used to define the Equivalence Ratio standard deviation  
    F_SC                    = combustor.F_SC                                        # [-]       Fuel scaler
    
    m_dot_fuel_tot          = m_dot_air_tot*FAR                                     # [kg/s]    Fuel mass flow going through all combustors
    m_dot_air               = m_dot_air_tot/N_comb                                  # [kg/s]    Air mass flow inside each combustor, scaled inside each PSR to vary the Equivalence Ratio
    m_dot_fuel              = m_dot_fuel_tot/N_comb                                 # [kg/s]    Fuel mass flow inside each combustor                                                                                                                                                                    
    phi_sign                = (m_dot_fuel_tot*F_SC)/(m_dot_air_tot*f_air_PZ*FAR_st) # [-]       Primary Zone mean Equivalence Ratio
    sigma_phi               = phi_sign*S_PZ                                         # [-]       Primary Zone Equivalence Ratio standard deviation                                                                                                                                                      
    
    if high_fidelity_kin_mech:                                                               
        dict_fuel           = combustor.fuel_data.fuel_chemical_properties  # [-]       Fuel species and corresponding mole fractions for full fuel model
        kinetics_model      = combustor.fuel_data.surrogate_chemical_kinetics
    else:                                                                                      
        dict_fuel           = combustor.fuel_data.fuel_surrogate_chemical_properties              # [-]       Fuel species and corresponding mole fractions for surrogate fuel model 
        kinetics_model      = combustor.fuel_data.surrogate_chemical_kinetics
    dict_oxy                = combustor.fuel_data.air_chemical_properties              # [-]       Air species and corresponding mole fractions     
    
    if high_fidelity_kin_mech:                                                                           
        list_sp             = combustor.fuel_data.species_list             # [-]       Fuel species for Emission Index analysis
    else:                                                                                       
        list_sp             = combustor.fuel_data.surrogate_species_list                                   # [-]       Fuel species for Emission Index analysis
    
    col_names = ['EI_' +str(sp) for sp in list_sp] # [-]       Define output variables 
    df                      = pd.DataFrame(columns=col_names)                       # [-]       Assign output variables space to df
    
    gas, EI = combustor_model(kinetics_model,high_fidelity_kin_mech, dict_fuel, dict_oxy, T_stag_0, P_stag_0, FAR, m_dot_fuel, m_dot_air, N_PZ, A_PZ, L_PZ, phi_sign, phi_SZ, A_SZ, L_SZ, f_air_PZ, N_SZ, sigma_phi) # [-]       Run combustor function
    
    sp_idx                  = [gas.species_index(sp) for sp in list_sp]             # [-]       Retrieve the species index
    data_n                  = list(EI[sp_idx])                                      # [-]       Assign output variables  
    df.loc[0]               = data_n                                                # [-]       Assign output variables to df 
    
    results = Data()
    results.EI_CO2 = df.loc[0, 'EI_CO2']
    results.EI_CO = df.loc[0, 'EI_CO']
    results.EI_H2O = df.loc[0, 'EI_H2O']
    results.EI_NO = 0
    results.EI_NO2 = 0   
    
    if high_fidelity_kin_mech:  
        results.EI_NO = df.loc[0, 'EI_NO']
        results.EI_NO2 = df.loc[0, 'EI_NO2']
    
    return results

def combustor_model(kinetics_model,high_fidelity_kin_mech, dict_fuel, dict_oxy, T_stag_0, P_stag_0, FAR, m_dot_fuel, m_dot_air, N_PZ, A_PZ, L_PZ, phi_sign, phi_SZ, A_SZ, L_SZ, f_air_PZ, N_SZ, sigma_phi):
 

    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator + "Data" + separator      

    # ------------------------------------------------------------------------------
    # ----------------------------- Initial Parameters -----------------------------
    # ------------------------------------------------------------------------------    
      
    f_air_SZ                = 1 - f_air_PZ                                          # [-]       Fraction of total air present in the combustor that enters the Secondary Zone  
    m_dot_air_PSR           = f_air_PZ*m_dot_air                                    # [kg/s]    Air mass flow going through each PSR  
    m_dot_fuel_PSR          = m_dot_fuel                                            # [kg/s]    Fuel mass flow going through each PSR    
    m_dot_air_SZ            = (f_air_SZ*m_dot_air)/N_SZ                             # [kg/s]    Air mass flow going through each dilution air inlet (3 inlets)
    V_PZ_PSR                = (A_PZ*L_PZ)/N_PZ                                      # [m**3]    Volume of each PSR
    phi_PSR                 = np.linspace(0.001, 2*phi_sign, N_PZ)                  # [-]       Distribution of Equivalence Ratio through the PSRs
    Delta_phi               = np.abs(phi_PSR[0] - phi_PSR[1])                       # [-]       Difference between two subsequent Equivalence Ratios
    comp_fuel               = list(dict_fuel.keys())                                # [-]       Fuel components
    
    # ------------------------------------------------------------------------------
    # ----------------------------------- PSR #1 -----------------------------------
    # ------------------------------------------------------------------------------ 
    mixer_list = []
    Fuel_list  = []
    mass_flow_rates = []
    half = int(N_PZ/2)
    for PSR_i in range(N_PZ):     
        f_PZ_1                  = (1 / (np.sqrt(2 * np.pi) * sigma_phi)) * np.exp((-(phi_PSR[PSR_i] - phi_sign) ** 2) / (2 * sigma_phi ** 2)) * Delta_phi # [-]       Fraction of mass flow entering the PSR at the PSR equivalence ratio                                                                                       
        Fuel_list[PSR_i]                  = ct.Solution(rel_path+kinetics_model)                               # [-]       Import surrogate fuel kinematic mechanism
        Fuel_list[PSR_i].TP               = T_stag_0, P_stag_0                                    # [-]       Set the fuel temperature and pressure
        Fuel_list[PSR_i].set_equivalence_ratio(phi_PSR[PSR_i], fuel=dict_fuel, oxidizer=dict_oxy)     # [-]       Set the euivalence ratio inside the PSR
        Fuel_list[PSR_i].equilibrate('HP')                                                        # [-]       Fix the specific enthalpy and pressure 
        rho_1                   = Fuel_list[PSR_i].density                                        # [kg/m**3] Fuel density
        m_dot_air_1             = m_dot_air_PSR * f_PZ_1                                # [kg/s]    Air mass flow inside the PSR    
        m_dot_fuel_1            = m_dot_fuel_PSR * f_PZ_1                               # [kg/s]    Fuel mass flow inside the PSR
        mass_flow_rates.append(m_dot_fuel_1 + m_dot_air_1)                          # [kg/s]    Total mass flow inside the PSR  
        upstream_1              = ct.Reservoir(Fuel_list[PSR_i])                                  # [-]       Create a resevoir for the Fuel upstream of the PSR
        mixer_list.append(ct.IdealGasReactor(Fuel_list[PSR_i]))                                   # [-]       Create the reactor for the downstream mixer
        PSR_1                   = ct.IdealGasReactor(Fuel_list[PSR_i])                            # [-]       Create the reactor for the PSR 
        PSR_1.volume            = V_PZ_PSR                                              # [m**3]    Set the PSR volume
        inlet_1                 = ct.MassFlowController(upstream_1, PSR_1)              # [-]       Connect the upstream resevoir with the PSR 
        inlet_1.mass_flow_rate  = mass_flow_rates[PSR_i]                                     # [kg/s]    Prescribe the inlet mass flow rate 
        outlet_1                = ct.MassFlowController(PSR_1, mixer_list[PSR_i], mdot=mass_flow_rates[PSR_i]) # [-]       Connect the PSR with the downstream mixer with the same mass flow rate                                     
        t_res_PSR_1             = (rho_1 * V_PZ_PSR) / (mass_flow_rates[PSR_i])               # [s]       Compute the residence time inside the PSR
        sim_PSR_1               = ct.ReactorNet([PSR_1])                                # [-]       Set the PSR simulation
        sim_PSR_1.advance(t_res_PSR_1)                                                  # [-]       Run the simulation until the residence time is reached
        Y_fuel_1                = Fuel_list[PSR_i][comp_fuel].Y                                   # [-]       Store mass fractions inside the PSR
    
              
        
    # ------------------------------------------------------------------------------
    # --------------------------------- Mixing 1-2 ---------------------------------
    # ------------------------------------------------------------------------------ 
    mixer_1234              = ct.IdealGasReactor(Fuel_1)                            # [-]       Create the reactor for the downstream mixer
    outlet_12               = ct.MassFlowController(mixer_12, mixer_1234, mdot = (mass_flow_rate_1 + mass_flow_rate_2)) # [-]       Connect the mixer with the downstream mixer     
    sim_mixer_12            = ct.ReactorNet([mixer_12])                             # [-]       Set the mixer simulation  
    sim_mixer_12.advance_to_steady_state()                                          # [-]       Run the simulation until it reaches steady state
    
    # ------------------------------------------------------------------------------
    # --------------------------------- Mixing 3-4 ---------------------------------
    # ------------------------------------------------------------------------------     
    
    outlet_34               = ct.MassFlowController(mixer_34, mixer_1234, mdot = (mass_flow_rate_3 + mass_flow_rate_4)) # [-]       Connect the mixer with the downstream mixer
    sim_mixer_34            = ct.ReactorNet([mixer_34])                             # [-]       Set the mixer simulation  
    sim_mixer_34.advance_to_steady_state()                                          # [-]       Run the simulation until it reaches steady state
    
    
    
    # ------------------------------------------------------------------------------
    # --------------------------------- Mixing 5-6 ---------------------------------
    # ------------------------------------------------------------------------------     
    
    mixer_5678              = ct.IdealGasReactor(Fuel_5)                            # [-]       Create the reactor for the downstream mixer
    outlet_56               = ct.MassFlowController(mixer_56, mixer_5678, mdot = (mass_flow_rate_5 + mass_flow_rate_6)) # [-]       Connect the mixer with the downstream mixer     
    sim_mixer_56            = ct.ReactorNet([mixer_56])                             # [-]       Set the mixer simulation  
    sim_mixer_56.advance_to_steady_state()                                          # [-]       Run the simulation until it reaches steady state
    
    # ------------------------------------------------------------------------------
    # --------------------------------- Mixing 7-8 ---------------------------------
    # ------------------------------------------------------------------------------     
    
    outlet_78               = ct.MassFlowController(mixer_78, mixer_5678, mdot = (mass_flow_rate_7 + mass_flow_rate_8)) # [-]       Connect the mixer with the downstream mixer
    sim_mixer_78            = ct.ReactorNet([mixer_78])                             # [-]       Set the mixer simulation  
    sim_mixer_78.advance_to_steady_state()                                          # [-]       Run the simulation until it reaches steady state
    
    
    
    
    # ------------------------------------------------------------------------------
    # ------------------------------- Mixing 1-2-3-4 -------------------------------
    # ------------------------------------------------------------------------------     
    
    mixer_12345678          = ct.IdealGasReactor(Fuel_1)                            # [-]       Create the reactor for the downstream mixer
    outlet_1234             = ct.MassFlowController(mixer_1234, mixer_12345678, mdot =  np.sum(np.array(mass_flow_rates)[0:half])) # [-]       Connect the mixer with the downstream mixer     
    sim_mixer_1234          = ct.ReactorNet([mixer_1234])                           # [-]       Set the mixer simulation  
    sim_mixer_1234.advance_to_steady_state()                                        # [-]       Run the simulation until it reaches steady state
    
    # ------------------------------------------------------------------------------
    # ------------------------------- Mixing 5-6-7-8 -------------------------------
    # ------------------------------------------------------------------------------     

    outlet_5678             = ct.MassFlowController(mixer_5678, mixer_12345678, mdot =  np.sum(np.array(mass_flow_rates)[half+1:])) # [-]       Connect the mixer with the downstream mixer     
    sim_mixer_5678          = ct.ReactorNet([mixer_5678])                           # [-]       Set the mixer simulation  
    sim_mixer_5678.advance_to_steady_state()                                        # [-]       Run the simulation until it reaches steady state
    
    
    
    
    
    # ------------------------------------------------------------------------------
    # --------------------------- Mixing 1-2-3-4-5-6-7-8 ---------------------------
    # ------------------------------------------------------------------------------     

    mixer_air_1             = ct.IdealGasReactor(Fuel_list[0])                            # [-]       Create the reactor for the downstream mixer
    outlet_12345678         = ct.MassFlowController(mixer_12345678, mixer_air_1, mdot =  np.sum(np.array(mass_flow_rates))) # [-]       Connect the mixer with the downstream mixer     
    sim_mixer_12345678      = ct.ReactorNet([mixer_12345678])                       # [-]       Set the mixer simulation  
    sim_mixer_12345678.advance_to_steady_state()                                    # [-]       Run the simulation until it reaches steady state
     
    
    # ------------------------------------------------------------------------------
    # -------------------------------- Mixing 1-Air --------------------------------
    # ------------------------------------------------------------------------------
    total_mass_flow = np.sum(np.array(mass_flow_rates))
    for _ in  range(3): 
        Air_1                   = ct.Solution(rel_path+oxidizer_model)                  # [-]       Import air kinematic mechanism           
        Air_1.TPX               = T_stag_0, P_stag_0, dict_oxy                          # [-]       Set the air temperature, pressure and mole fractions
        rho_air_1               = Air_1.density                                         # [kg/m**3] Fuel density
        res_air_1               = ct.Reservoir(Air_1)                                   # [-]       Create a resevoir for the air upstream of the mixer
        PFR_1                   = ct.IdealGasConstPressureReactor(Fuel_1)               # [-]       Create the reactor for the PFR
        PFR_1.volume            = A_SZ*(L_SZ/3)                                         # [m**3]    Set the PFR volume
        inlet_air_1             = ct.MassFlowController(res_air_1, mixer_air_1, mdot= m_dot_air_SZ) # [-]       Connect the upstream resevoir with the mixer
        m_dot_air_1             = total_mass_flow + m_dot_air_SZ # [kg/s]    Total mass flow inside the mixer  
        outlet_air_1            = ct.MassFlowController(mixer_air_1, PFR_1, mdot=m_dot_air_1) # [-]       Connect the mixer with the downstream PFR with the same mass flow rate           
        sim_mixer_air_1         = ct.ReactorNet([mixer_air_1])                          # [-]       Set the mixer simulation  
        sim_mixer_air_1.advance_to_steady_state()                                       # [-]       Run the simulation until it reaches steady state
        
        # ------------------------------------------------------------------------------
        # ----------------------------------- PFR #1 -----------------------------------
        # ------------------------------------------------------------------------------ 
        
        mixer_air_1             = ct.IdealGasReactor(Fuel_list[0])                            # [-]       Create the reactor for the downstream mixer
        outlet_PFR_1            = ct.MassFlowController(PFR_1, mixer_air_1, mdot=m_dot_air_1) # [-]       Connect the PFR with the downstream mixer                                 
        t_res_PFR_1             = (Fuel_list[0].density * PFR_1.volume) / (m_dot_air_1)       # [s]       Compute the residence time inside the PFR           
        Fuel_list[0].set_equivalence_ratio(phi_SZ, fuel=dict_fuel, oxidizer=dict_oxy)   # [-]       Set the euivalence ratio inside the PFR
        sim_PFR_1               = ct.ReactorNet([PFR_1])                                # [-]       Set the PFR simulation
        sim_PFR_1.advance(t_res_PFR_1)                                                  # [-]       Run the simulation until the residence time is reached 
    
    # ------------------------------------------------------------------------------
    # ---------------------------- Additional computations -------------------------
    # ------------------------------------------------------------------------------    

    m_dot_input_combustor   = m_dot_fuel + m_dot_air                             # [kg/s]    Total mass flow rate entering a single combustor (air + fuel)
    Emission_Index          = Fuel_list[0].Y * (m_dot_input_combustor)/m_dot_fuel         # [-]       Computation of the Emission Index   

    return (Fuel_list[0], Emission_Index)  