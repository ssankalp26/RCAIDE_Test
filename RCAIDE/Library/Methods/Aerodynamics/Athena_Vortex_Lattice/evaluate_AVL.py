# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/evaluate_AVL_surrogate.py
#  
# Created: Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core import  Data   

# package imports
import numpy   as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate_AVL_surrogate(state,settings,vehicle):
    """Evaluates surrogates forces and moments using built surrogates 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics : VLM analysis  [unitless]
        state        : flight conditions     [unitless]
        settings     : VLM analysis settings [unitless]
        vehicle      : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """          
    conditions          = state.conditions
    aerodynamics        = state.analyses.aerodynamics  
    Mach                = conditions.freestream.mach_number
    AoA                 = conditions.aerodynamics.angles.alpha
    lift_model          = aerodynamics.surrogates.lift_coefficient
    drag_model          = aerodynamics.surrogates.drag_coefficient
    e_model             = aerodynamics.surrogates.span_efficiency_factor
    moment_model        = aerodynamics.surrogates.moment_coefficient
    Cm_alpha_model      = aerodynamics.surrogates.Cm_alpha_moment_coefficient
    Cn_beta_model       = aerodynamics.surrogates.Cn_beta_moment_coefficient      
    neutral_point_model = aerodynamics.surrogates.neutral_point
    cg                  = vehicle.mass_properties.center_of_gravity[0]
    MAC                 = vehicle.wings.main_wing.chords.mean_aerodynamic

    # set up data structures
    static_stability    = Data()
    dynamic_stability   = Data()    

    #Run Analysis
    data_len            = len(AoA) 
    inviscid_lift       = np.zeros([data_len,1])
    inviscid_drag       = np.zeros([data_len,1])    
    span_efficiency     = np.zeros([data_len,1]) 
    CM                  = np.zeros([data_len,1])
    Cm_alpha            = np.zeros([data_len,1])
    Cn_beta             = np.zeros([data_len,1])
    NP                  = np.zeros([data_len,1]) 

    for i,_ in enumerate(AoA):           
        inviscid_lift[i]   = lift_model(AoA[i][0],Mach[i][0])[0] 
        inviscid_drag[i]   = drag_model(AoA[i][0],Mach[i][0])[0] 
        span_efficiency[i] = e_model(AoA[i][0],Mach[i][0])[0] 
        CM[i]              = moment_model(AoA[i][0],Mach[i][0])[0]  
        Cm_alpha[i]        = Cm_alpha_model(AoA[i][0],Mach[i][0])[0]  
        Cn_beta[i]         = Cn_beta_model(AoA[i][0],Mach[i][0])[0]  
        NP[i]              = neutral_point_model(AoA[i][0],Mach[i][0])[0]    

    static_stability.CM            = CM
    static_stability.Cm_alpha      = Cm_alpha 
    static_stability.Cn_beta       = Cn_beta   
    static_stability.neutral_point = NP 
    static_stability.static_margin = (NP - cg)/MAC    

    results         = Data()
    results.static  = static_stability
    results.dynamic = dynamic_stability
 

    # Store inviscid lift results     
    conditions.aerodynamics.lift_breakdown.inviscid_wings_lift = Data()
    conditions.aerodynamics.lift_breakdown.compressible_wings  = Data()
    conditions.aerodynamics.lift_breakdown.inviscid_wings_lift = inviscid_lift
    conditions.aerodynamics.coefficients.lift                   = inviscid_lift

    Sref = vehicle.reference_area
    for wing in vehicle.wings.values():
        wing_area                                                            = wing.areas.reference
        conditions.aerodynamics.lift_breakdown.compressible_wings[wing.tag]  = inviscid_lift*(wing_area/Sref)


    # Store inviscid drag results   
    state.conditions.aerodynamics.inviscid_drag_coefficient          = inviscid_drag
    state.conditions.aerodynamics.drag_breakdown.induced = Data(
            total                  = inviscid_drag   ,
            span_efficiency_factor = span_efficiency ,
        )
    

    return

def evaluate_AVL_no_surrogate():
    
    pass
 