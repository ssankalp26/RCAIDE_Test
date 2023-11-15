## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/All_Electric.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports 
import RCAIDE 
from RCAIDE.Core                                                             import Data 
from RCAIDE.Analyses.Mission.Common                                          import Residuals 
from RCAIDE.Components.Component                                             import Container    
from RCAIDE.Methods.Power.Battery.Common                                     import pack_battery_conditions,append_initial_battery_conditions 
from RCAIDE.Methods.Propulsion.all_electric_ducted_fan_propulsor             import compute_propulsor_performance , compute_unique_propulsor_groups 
from .Network                                                                import Network  

 # package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  All Electric
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class All_Electric_Ducted_Fan(Network):
    """ Simply connects a battery to a ducted ducted_fan, with an assumed motor efficiency
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    def __defaults__(self):
        """ This sets the default values for the network to function.
            This network operates slightly different than most as it attaches a propulsor to the net.
    
            Assumptions:
            
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """          
        self.tag                          = 'Battery_ducted_fan'
        self.avionics                     = RCAIDE.Energy.Peripherals.Avionics()
        self.payload                      = RCAIDE.Energy.Peripherals.Payload()
        self.system_voltage               = None          

    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
            Constant mass batteries
            ESC input voltage is constant at max battery voltage
            
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
    
            Properties Used:
            Defaulted values
        """ 
        
        # unpack   
        conditions = state.conditions
        numerics   = state.numerics
        busses     = self.busses
        avionics   = self.avionics
        payload    = self.payload 
    
        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(3) 
        for bus in busses:
            batteries     = bus.batteries    
            ducted_fans   = bus.ducted_fans 
            escs          = bus.electronic_speed_controllers 
    
            for battery in batteries:               
                battery_conditions                = conditions.energy[bus.tag][battery.tag] 
                battery.pack.current_energy       = battery_conditions.pack.energy     
                battery.pack.temperature          = battery_conditions.pack.temperature
                battery.cell.age                  = battery_conditions.cell.cycle_in_day    
                battery.cell.charge_throughput    = battery_conditions.cell.charge_throughput   
                battery.cell.temperature          = battery_conditions.cell.temperature   
                battery_discharge_flag            = battery_conditions.battery_discharge_flag              
    
                if bus.fixed_voltage: 
                    voltage = bus.voltage * state.ones_row(1)
                else:    
                    voltage = battery.compute_voltage(battery_conditions)   
    
                if battery_discharge_flag:    
                    total_current  = 0. 
                    for i in range(conditions.energy[bus.tag].number_of_propulsor_groups):
                        if bus.active_propulsor_groups[i]:           
                            pg_tag              = conditions.energy[bus.tag].active_propulsor_groups[i]
                            N_ducted_fans       = conditions.energy[bus.tag].N_ducted_fans
                            T, P, I, eta,mdot,Isp,outputs  = compute_propulsor_performance(i,bus,pg_tag,ducted_fans,N_ducted_fans,escs,conditions,voltage) 
                            total_current       += I
                            total_thrust        += T    
                            total_power         += P
    
                    # Avionics Power Consumtion 
                    avionics.power() 
    
                    # Payload Power Consumtion 
                    payload.power()
    
                    if bus.fixed_voltage:      
                        bus.outputs.avionics_power  = avionics.inputs.power 
                        bus.outputs.payload_power   = payload.inputs.power 
                        bus.outputs.total_esc_power = total_current*voltage
                        bus.logic(conditions,numerics)             
    
                        # link to battery                  
                        battery.outputs.current     = bus.outputs.power/voltage
                        battery.outputs.power       = bus.outputs.power*battery.bus_power_split_ratio
    
                    else:       
                        # link to battery   
                        battery.outputs.current     = total_current + (avionics.inputs.power + payload.inputs.power)/voltage
                        battery.outputs.power       = battery.outputs.current*voltage
    
                    battery.energy_calc(numerics,conditions,bus.tag,battery_discharge_flag)       
                    pack_battery_conditions(battery_conditions,battery)               
    
                else: 
                    if bus.fixed_voltage:    
                        bus.inputs.secondary_source_power = -(battery.cell.charging_current * battery.pack.electrical_configuration.parallel) *\
                                (battery.cell.charging_voltage * battery.pack.electrical_configuration.series) * np.ones_like(voltage)       
                        bus.logic(conditions,numerics) 
    
                        # link to battery    
                        battery.outputs.current    = bus.outputs.power/voltage
                        battery.outputs.power      = -bus.outputs.power*battery.bus_power_split_ratio  
                    else: 
                        # link to battery     
                        battery.outputs.current    =  battery.cell.charging_current*battery.pack.electrical_configuration.parallel * np.ones_like(voltage) 
                        battery.outputs.power      = -battery.outputs.current * (battery.cell.charging_voltage*battery.pack.electrical_configuration.series) 
    
                    total_thrust  = np.zeros((len(voltage),3)) 
                    battery.energy_calc(numerics,conditions,bus.tag,battery_discharge_flag)      
                    pack_battery_conditions(battery_conditions,battery)             
    
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = state.ones_row(1)*0.0  
    
        # --------------------------------------------------        
        # A PATCH TO BE DELETED IN RCAIDE
        results                           = Data()
        results.thrust_force_vector       = total_thrust
        results.vehicle_mass_rate         = state.ones_row(1)*0.0         
        # --------------------------------------------------     
         
        return results
    def unpack_unknowns(self,segment):
        """ This adds additional unknowns which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            unknowns specific to the rotors                        [None] 
            unknowns specific to the battery cell                  
    
            Outputs:
            state.conditions.energy.bus.rotor.power_coefficient(s) [None] 
            conditions specific to the battery cell 
    
            Properties Used:
            N/A
        """                          
        # unpack the ones function
        ones_row     = segment.state.ones_row
        busses       = segment.analyses.energy.networks.battery_ducted_fan.busses
        
        for bus in busses:
            if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:  
                bus_results             = segment.state.conditions.energy[bus.tag] 
                active_propulsor_groups = bus_results.active_propulsor_groups
                for i in range(len(active_propulsor_groups)): 
                    pg_tag = active_propulsor_groups[i]            
                    if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:     
                        bus_results[pg_tag].ducted_fan.throttle = segment.state.unknowns[bus.tag + '_' + pg_tag + '_throttle']
                    else:  
                        bus_results[pg_tag].ducted_fan.throttle          = 0. * ones_row(1)  
     
            for battery in bus.batteries: 
                battery.assign_battery_unknowns(segment,bus,battery)        
        
        return       
    
    def residuals(self,segment):
        """ This packs the residuals to be sent to the mission solver.
   
           Assumptions:
           None
   
           Source:
           N/A
   
           Inputs:
           state.conditions.energy:
               motor(s).torque                      [N-m]
               rotor(s).torque                      [N-m] 
           residuals soecific to the battery cell   
           
           Outputs:
           residuals specific to battery cell and network
   
           Properties Used: 
           N/A
       """           
 
        busses   = segment.analyses.energy.networks.battery_ducted_fan.busses 
        for bus in busses:   
            for battery in bus.batteries: 
                battery.assign_battery_residuals(segment,bus,battery)    
         
        return     
    
    ## @ingroup Components-Energy-Networks
    def add_unknowns_and_residuals_to_segment(self, 
                                              segment, 
                                              estimated_propulsor_group_throttles = [[0.5]],  
                                              estimated_battery_voltages          = [[400]], 
                                              estimated_battery_cell_temperature  = [[283.]], 
                                              estimated_battery_state_of_charges  = [[0.5]],
                                              estimated_battery_cell_currents     = [[5.]]):
        """ This function sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment
            estimated_battery_voltages                                    [v]
            estimated_ducted_fan_power_coefficients                            [float]s
            estimated_battery_cell_temperature                            [Kelvin]
            estimated_battery_state_of_charges                            [unitless]
            estimated_battery_cell_currents                               [Amperes]
            
            Outputs: 
            segment
    
            Properties Used:
            N/A
        """              
        busses   = segment.analyses.energy.networks.battery_ducted_fan.busses
        ones_row = segment.state.ones_row 
        segment.state.residuals.network = Residuals() 
        
        if 'throttle' in segment.state.unknowns: 
            segment.state.unknowns.pop('throttle')
        if 'throttle' in segment.state.conditions.energy: 
            segment.state.conditions.energy.pop('throttle')
         
        for bus_i, bus in enumerate(busses):  
            active_propulsor_groups   = bus.active_propulsor_groups 
            N_active_propulsor_groups = len(active_propulsor_groups)
            batteries                 = bus.batteries 

            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Analyses.Mission.Common.Conditions()             
            sorted_propulsors                        = compute_unique_propulsor_groups(bus)
            bus_results                              = segment.state.conditions.energy[bus.tag]
            bus_results.number_of_propulsor_groups   = N_active_propulsor_groups
            bus_results.active_propulsor_groups      = active_propulsor_groups
            bus_results.N_ducted_fans                = sorted_propulsors.N_ducted_fans
            segment.state.conditions.noise[bus.tag]  = RCAIDE.Analyses.Mission.Common.Conditions()  
            noise_results                            = segment.state.conditions.noise[bus.tag]
    
            # ------------------------------------------------------------------------------------------------------
            # Assign battery residuals, unknowns and results data structures 
            # ------------------------------------------------------------------------------------------------------  
            
            if len(batteries) > 1 and (bus.fixed_voltage == False): 
                assert('The bus must have a fixed voltage is more than one battery is specified on the bus')  
                
            for b_i , battery in enumerate(batteries):         
                bus_results[battery.tag]                               = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].cell                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack.energy                   = ones_row(1)
                bus_results[battery.tag].pack.voltage_under_load       = ones_row(1)
                bus_results[battery.tag].pack.voltage_open_circuit     = ones_row(1)
                bus_results[battery.tag].pack.temperature              = ones_row(1)
                bus_results[battery.tag].cell.state_of_charge          = ones_row(1)
                bus_results[battery.tag].cell.temperature              = ones_row(1)
                bus_results[battery.tag].cell.charge_throughput        = ones_row(1) 
                bus_results[battery.tag].cell.cycle_in_day             = 0
                bus_results[battery.tag].cell.resistance_growth_factor = 1.
                bus_results[battery.tag].cell.capacity_fade_factor     = 1.  
                append_initial_battery_conditions(segment,bus,battery)    
                
                # add unknowns and residuals specific to battery cell
                battery.append_battery_unknowns_and_residuals_to_segment(segment,
                                                                         bus,
                                                                         battery,
                                                                         estimated_battery_voltages[bus_i][b_i],
                                                                         estimated_battery_cell_temperature[bus_i][b_i], 
                                                                         estimated_battery_state_of_charges[bus_i][b_i], 
                                                                         estimated_battery_cell_currents[bus_i][b_i] ) 
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for i in range(len(sorted_propulsors.unique_ducted_fan_tags)):   
                if type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:   
                    # appennd residuals and unknowns for recharge segment                     
                    segment.state.unknowns['recharge'+ active_propulsor_groups[i]]          =  0* ones_row(1)  
                    segment.state.residuals.network['recharge'+ active_propulsor_groups[i]] =  0* ones_row(1)
                else:   
                    
                    if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Takeoff or type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing:   
                        try: 
                            initial_throttle = estimated_propulsor_group_throttles[bus_i][i]
                        except:  
                            initial_throttle = 0.5 
                        segment.state.unknowns[bus.tag + '_' + active_propulsor_groups[i]+ '_throttle'] = initial_throttle* ones_row(1)    
                                 
                # Results data structure for each propulsor group    
                pg_tag                                      = active_propulsor_groups[i] 
                bus_results[pg_tag]                         = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[pg_tag].ducted_fan              = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[pg_tag].unique_ducted_fan_tags  = sorted_propulsors.unique_ducted_fan_tags 
                bus_results[pg_tag].unique_esc_tags         = sorted_propulsors.unique_esc_tags   
                bus_results[pg_tag].ducted_fan.throttle     = 0. * ones_row(1)  
                bus_results[pg_tag].ducted_fan.torque       = 0. * ones_row(1)
                bus_results[pg_tag].ducted_fan.thrust       = 0. * ones_row(1) 
                noise_results[pg_tag]                       = RCAIDE.Analyses.Mission.Common.Conditions()
                noise_results[pg_tag].ducted_fan            = RCAIDE.Analyses.Mission.Common.Conditions()
                
        
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network            = self.unpack_unknowns
        segment.process.iterate.residuals.network           = self.residuals                    
        return segment    
            
    __call__ = evaluate_thrust