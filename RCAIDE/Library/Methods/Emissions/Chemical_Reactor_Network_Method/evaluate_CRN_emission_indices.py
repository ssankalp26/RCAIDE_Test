# RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/evaluate_CRN_emission_indices.py
#  
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data
import RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_cantera as evaluate_cantera  

 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  evaluate_correlation_emissions_indices
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate_CRN_emission_indices_no_surrogate(segment,settings,vehicle):
  
    # unpack
    state     = segment.state
    I         = state.numerics.time.integrate
    
    CO2_total = 0 * state.ones_row(1)  
    CO_total  = 0 * state.ones_row(1) 
    H2O_total = 0 * state.ones_row(1) 
    NO_total  = 0 * state.ones_row(1) 
    NO2_total = 0 * state.ones_row(1) 

    for network in vehicle.networks:  
        for fuel_line in network.fuel_lines:
            if fuel_line.active:  
                    for propulsor in fuel_line.propulsors:
                        if propulsor.active == True: 
                            if (type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbofan) or \
                                type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboshaft or \
                                type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbojet:    
                            
                                combustor = propulsor.combustor
                            
                                # unpack component conditions
                                n_cp = state.numerics.number_of_control_points 
                                propulsor_conditions     = state.conditions.energy[fuel_line.tag][propulsor.tag] 
                                combustor_conditions    = propulsor_conditions[combustor.tag]  

                                
                                T    = combustor_conditions.inputs.stagnation_temperature
                                P    = combustor_conditions.inputs.stagnation_pressure 
                                mdot = propulsor_conditions.core_mass_flow_rate 
                                FAR  = combustor_conditions.outputs.fuel_to_air_ratio 

                                EI_CO2_p   = 0 * state.ones_row(1)   
                                EI_CO_p    = 0 * state.ones_row(1)  
                                EI_H2O_p   = 0 * state.ones_row(1)  
                                EI_NO_p    = 0 * state.ones_row(1)  
                                EI_NO2_p   = 0 * state.ones_row(1)                              
                                                         
                                for t_idx in range(n_cp):
                                    # Call cantera 
                                    results = evaluate_cantera(combustor,P[0,t_idx],T[0,t_idx],mdot[0,t_idx],FAR[0,t_idx])
                                    
                                    EI_CO2_p[0,t_idx] = results.EI_CO2
                                    EI_CO_p[0,t_idx] =  results.EI_CO 
                                    EI_H2O_p[0,t_idx] = results.EI_H2O
                                    EI_NO_p[0,t_idx] =  results.EI_NO 
                                    EI_NO2_p[0,t_idx] = results.EI_NO2 
                                      
                                CO2_total  += np.dot(I,mdot*EI_CO2_p)
                                CO_total   += np.dot(I,mdot *EI_CO_p )
                                H2O_total  += np.dot(I,mdot*EI_H2O_p)
                                NO_total   += np.dot(I,mdot *EI_NO_p ) 
                                NO2_total  += np.dot(I,mdot *EI_NO2_p)

    emissions               = Data()
    emissions.total         = Data()
    emissions.index         = Data() 
    emissions.total.CO2     = CO2_total  * combustor.fuel.global_warming_potential_100.NOx 
    emissions.total.CO      = CO_total   * combustor.fuel.global_warming_potential_100.CO2
    emissions.total.H2O     = H2O_total  * combustor.fuel.global_warming_potential_100.H2O  
    emissions.total.NO      = NO_total   * combustor.fuel.global_warming_potential_100.SO2  
    emissions.total.NO2     = NO2_total  * combustor.fuel.global_warming_potential_100.Soot  
    emissions.index.CO2     = EI_CO2_p
    emissions.index.CO      = EI_CO_p 
    emissions.index.H2O     = EI_H2O_p
    emissions.index.NO      = EI_NO_p 
    emissions.index.NO2     = EI_NO2_p
    
    state.conditions.emissions =  emissions
    return    
    

def evaluate_CRN_emission_indices_surrogate(segment,settings,vehicle): 
  
    I          = segment.state.numerics.time.integrate
    surrogates = segment.analyses.emissions.surrogates
    
    CO2_total = 0 * segment.state.ones_row(1)  
    CO_total  = 0 * segment.state.ones_row(1) 
    H2O_total = 0 * segment.state.ones_row(1) 
    NO_total  = 0 * segment.state.ones_row(1) 
    NO2_total = 0 * segment.state.ones_row(1) 

    for network in vehicle.networks:  
        for fuel_line in network.fuel_lines:
            if fuel_line.active:  
                    for propulsor in fuel_line.propulsors:
                        if propulsor.active == True: 
                            if (type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbofan) or \
                                type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboshaft or \
                                type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbojet:    
                            
                                combustor = propulsor.combustor
                            
                                # unpack component conditions
                                propulsor_conditions    = segment.state.conditions.energy[fuel_line.tag][propulsor.tag] 
                                combustor_conditions    = propulsor_conditions[combustor.tag]  

                                T    = combustor_conditions.inputs.stagnation_temperature
                                P    = combustor_conditions.inputs.stagnation_pressure 
                                mdot = propulsor_conditions.core_mass_flow_rate 
                                FAR  = combustor_conditions.outputs.fuel_to_air_ratio 
                                
                                pts = np.hstack((T,P,mdot,FAR )) 

                                EI_CO2_p  = np.atleast_2d(surrogates.EI_CO2(pts)).T
                                EI_CO_p   = np.atleast_2d(surrogates.EI_CO(pts)).T 
                                EI_H2O_p  = np.atleast_2d(surrogates.EI_H2O(pts)).T 
                                EI_NO_p   = np.atleast_2d(surrogates.EI_NO(pts)).T 
                                EI_NO2_p  = np.atleast_2d(surrogates.EI_NO2(pts)).T        
                                      
                                CO2_total += np.dot(I,mdot*EI_CO2_p)
                                CO_total  += np.dot(I,mdot *EI_CO_p )
                                H2O_total += np.dot(I,mdot*EI_H2O_p)
                                NO_total  += np.dot(I,mdot *EI_NO_p ) 
                                NO2_total += np.dot(I,mdot *EI_NO2_p)

    emissions                 = Data()
    emissions.total           = Data()
    emissions.index           = Data() 
    emissions.total.CO2       = CO2_total  * combustor.fuel_data.global_warming_potential_100.CO2 
    emissions.total.H2O       = H2O_total  * combustor.fuel_data.global_warming_potential_100.H2O  
    emissions.total.NOx       = (NO_total +NO2_total) * combustor.fuel_data.global_warming_potential_100.NOx 
    emissions.index.CO2       = EI_CO2_p
    emissions.index.CO        = EI_CO_p 
    emissions.index.H2O       = EI_H2O_p
    emissions.index.NO        = EI_NO_p 
    emissions.index.NO2       = EI_NO2_p 
 
    segment.state.conditions.emissions =  emissions
    return   

     