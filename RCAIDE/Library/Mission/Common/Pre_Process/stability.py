## @ingroup Library-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Missions/Common/Pre_Process/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports  
import  RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  stability
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Common-Pre_Process
def stability(mission):
    """ Runs stability model and build surrogate
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None             
    """      
    last_tag = None
    for tag,segment in mission.segments.items():
        if segment.analyses.stability !=  None:
            if  (last_tag!=  None) and  ('compute' in mission.segments[last_tag].analyses.stability.process.keys()): 
                segment.analyses.stability.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.stability.process.compute.lift.inviscid_wings
                segment.analyses.stability.surrogates       = mission.segments[last_tag].analyses.stability.surrogates 
                segment.analyses.stability.reference_values = mission.segments[last_tag].analyses.stability.reference_values   
            else: # use aerodynamic results that have been previously processed 
                if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method) or\
                (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Athena_Vortex_Lattice) :
                    segment.analyses.stability.process.compute.lift.inviscid_wings = segment.analyses.aerodynamics.process.compute.lift.inviscid_wings 
                    segment.analyses.stability.surrogates       = segment.analyses.aerodynamics.surrogates 
                    segment.analyses.stability.reference_values = segment.analyses.aerodynamics.reference_values 
                    last_tag = tag                 
                else: # run new simulation 
                    stab = segment.analyses.stability
                    stab.initialize() 
                    last_tag = tag 
    return 