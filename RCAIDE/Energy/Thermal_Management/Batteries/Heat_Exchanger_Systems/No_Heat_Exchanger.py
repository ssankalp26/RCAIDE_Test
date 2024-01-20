## @ingroup Energy-Thermal_Management-Batteries-Heat_Acquisition_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/Heat_Acquisition_Systems/No_Removal_System.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
  
from RCAIDE.Energy.Energy_Component import Energy_Component   
from RCAIDE.Methods.Energy.Thermal_Management.Batteries.Heat_Exchanger_Systems.No_Heat_Exchanger import no_heat_exchanger_model

# ----------------------------------------------------------------------------------------------------------------------
#  No_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Acquisition_Systems
class No_Heat_Exchanger(Energy_Component):
    """This provides output values for a direct convention heat exchanger of a bettery pack
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):  
        self.tag   = 'No_Heat_Exchanger'
        return
    
    def compute_heat_removed(HEX,HAS_outputs,state,dt,i): 
        '''Computes the heat removed to the atmosphwere with no heat exchanger system
        
        Assumtions:
        None
        
        Source
        None 
        
        Inputs:
        self                  - heat acquisition system                         [-]
        battery               - battery pack                                   [-]
        Q_heat_gen            - thermal load generated by battery              [W] 
        T_cell                - temperature of the battery cell                [K]
        state                 - conditions of system                           [-]
        dt                    - time step                                      [s]
        i                     - control point                                  [-]
        
        Outputs 
        Q_heat_gen_tot        - total heat generated by pack                   [W]
        Q_net                 - net heat accumulated in battery pack           [W]
        T_current             - updated battery temperature at new timestep    [K]
        ''' 
             
             
        HEX_results = no_heat_exchanger_model(HEX,HAS_outputs,state, dt, i)
              
        return HEX_results
     
    
        