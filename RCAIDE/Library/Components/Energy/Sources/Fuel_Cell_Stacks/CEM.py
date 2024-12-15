
class CEM_state: 
    p_in_comp: float = None
    pi_comp: float = None 
    mdot_in_comp: float = None 
    mdot_out_exp: float = None 
    p_in_exp: float = None 
    pi_exp: float = None 
    P_comp: float = None 
    P_motor_comp = None
    P_exp: float = None
    P_generator_exp: float = None
    P_CEM: float = None 

class CEM_Module: 
    def __init__(self, compressor_efficiency, expander_efficiency, motor_efficiency, generator_efficiency, specific_weight):
        self.compressor_efficiency = compressor_efficiency
        self.expander_efficiency = expander_efficiency 
        self.motor_efficiency = motor_efficiency 
        self.generator_efficiency = generator_efficiency
        self.specific_weight = specific_weight
        self.weight = 0

    def evaluate(self, p_air_FC, thermo_state_in, mdot_air_in, air_excess_ratio, p_drop_hum, p_drop_fc):
        Tt_in = thermo_state_in.Tt 
        Pt_in = thermo_state_in.Pt
        Cp = 1004
        gam = 1.4
        comp_p_req = mdot_air_in * Cp* Tt_in * (((p_air_FC + p_drop_hum) / Pt_in) ** ((gam - 1) / gam) - 1) / self.compressor_efficiency
        input_p = comp_p_req / self.motor_efficiency 
        p_exp = p_air_FC - p_drop_fc - p_drop_hum
        Tt_exp = Tt_in * (p_exp / Pt_in) ** ((gam - 1) / gam)
        mdot_air_out = mdot_air_in - mdot_air_in / air_excess_ratio * 0.233
        exp_p_ext = mdot_air_out * Cp * Tt_exp * (1 - (Pt_in / p_exp) ** ((gam - 1) / gam)) * self.expander_efficiency
        output_p = exp_p_ext * self.generator_efficiency
        p_req = input_p - output_p 
        state = CEM_state()
        state.p_in_comp = Pt_in 
        state.pi_comp = (p_air_FC + p_drop_hum) / Pt_in 
        state.mdot_in_comp = mdot_air_in 
        state.mdot_out_exp = mdot_air_out 
        state.p_in_exp = p_exp 
        state.pi_exp = Pt_in / p_exp 
        state.P_comp = comp_p_req
        state.P_motor_comp = input_p
        state.P_exp = exp_p_ext
        state.P_generator_exp = output_p 
        state.P_CEM = p_req
        return state

    def set_weight(self, compressor_max_power):
        self.power_rating = compressor_max_power
        self.weight = compressor_max_power / self.specific_weight / 1000