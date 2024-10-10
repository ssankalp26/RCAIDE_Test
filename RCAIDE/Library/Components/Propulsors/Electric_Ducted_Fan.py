## @ingroup Components-Propulsors-Electric_Ducted_Fan
# RCAIDE/Library/Components/Propulsors/Electric_Ducted_Fan.py
# 
# 
# 
# Created:  Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from .   import Propulsor  
from RCAIDE.Library.Methods.Propulsors.Electric_Ducted_Fan_Propulsor.append_electric_ducted_fan_conditions     import append_electric_ducted_fan_conditions
from RCAIDE.Library.Methods.Propulsors.Electric_Ducted_Fan_Propulsor.unpack_electric_ducted_fan_unknowns       import unpack_electric_ducted_fan_unknowns
from RCAIDE.Library.Methods.Propulsors.Electric_Ducted_Fan_Propulsor.pack_electric_ducted_fan_residuals        import pack_electric_ducted_fan_residuals 
from RCAIDE.Library.Methods.Propulsors.Electric_Ducted_Fan_Propulsor.compute_electric_ducted_fan_performance   import compute_electric_ducted_fan_performance, reuse_stored_electric_ducted_fan_data

# ----------------------------------------------------------------------
#  Electric Ducted Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class Electric_Ducted_Fan(Propulsor):
    """This is a electric motor-ducted_fan propulsor 
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'electric_ducted_fan'    
        self.motor                        = None
        self.ducted_fan                        = None 
        self.electronic_speed_controller  = None
        self.active_busses                = None 

    def append_operating_conditions(self,segment,bus,add_additional_network_equation = False):
        append_electric_ducted_fan_conditions(self,segment,bus,add_additional_network_equation)
        return 

    def unpack_propulsor_unknowns(self,reference_propulsor,segment,bus):  
        unpack_electric_ducted_fan_unknowns(self,reference_propulsor,segment,bus)
        return 

    def pack_propulsor_residuals(self,segment,bus): 
        pack_electric_ducted_fan_residuals(self,segment,bus)
        return        
    
    def compute_performance(self,state,bus,voltage,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_electric_ducted_fan_performance(self,state,bus,voltage,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboshaft,state,bus,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power = reuse_stored_electric_ducted_fan_data(turboshaft,state,bus,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power
