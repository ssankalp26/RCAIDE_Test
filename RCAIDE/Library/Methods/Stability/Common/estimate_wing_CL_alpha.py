
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
from RCAIDE.Library.Methods.Geometry.Planform.convert_sweep import convert_sweep

# ----------------------------------------------------------------------
#  Method
# ---------------------------------------------------------------------- 
def estimate_wing_CL_alpha(wing,mach):
    """ This method uses the DATCOM formula to compute dCL/dalpha without 
    correlations for downwash of lifting surfaces further ahead on the 
    aircraft or upwash resulting from the position of the wing on the body.

    CAUTION: The method presented here is applicable for subsonic speeds.
    May be inaccurate for transonic or supersonic flight. A correction factor
    for supersonic flight is included, but may not be completely accurate.

    Assumptions:
    Mach number should not be transonic
    
    Source:
        None
         
    Inputs:
        wing - a data dictionary with the fields:
            effective_apsect_ratio - wing aspect ratio [dimensionless]. If 
            this variable is not inlcuded in the input, the method will look
            for a variable named 'aspect_ratio'.
            sweep_le - wing leading-edge sweep angle [radians]
            taper - wing taper ratio [dimensionless]
        mach - flight Mach number [dimensionless]. Should be a numpy array
            with one or more elements.

    Outputs:
        cL_alpha - The derivative of 3D lift coefficient with respect to AoA

    Properties Used:
    N/A
    """         
    
    #Unpack inputs
    if 'effective_aspect_ratio' in wing:
        ar = wing.effective_aspect_ratio
    elif 'extended' in wing:
        if 'aspect_ratio' in wing.extended:
            ar = wing.extended.aspect_ratio
        else:
            ar = wing.aspect_ratio
    else:
        ar = wing.aspect_ratio    
        
    #Compute relevent parameters
    cL_alpha = []
    half_chord_sweep = convert_sweep(wing,0.25,0.5)  #Assumes original sweep is that of LE
    
    #Compute k correction factor for Mach number    
    #First, compute corrected 2D section lift curve slope (C_la) for the given Mach number
    cla = 6.13          #Section C_la at M = 0; Roskam Airplane Design Part VI, Table 8.1  
    
    cL_alpha = np.ones_like(mach)
    Beta     = np.ones_like(mach)
    k        = np.ones_like(mach)
    cla_M    = np.ones_like(mach)
    
    Beta[mach<1.]  = (1.0-mach[mach<1.]**2.0)**0.5
    Beta[mach>1.]  = (mach[mach>1.]**2.0-1.0)**0.5
    cla_M[mach<1.] = cla/Beta[mach<1.]
    cla_M[mach>1.] = 4.0/Beta[mach>1.]
    k              = cla_M/(2.0*np.pi/Beta)
    
    #Compute aerodynamic surface 3D lift curve slope using the DATCOM formula
    cL_alpha =(2.0*np.pi*ar/(2.0+((ar**2.0*(Beta*Beta)/(k*k))*(1.0+(np.tan(half_chord_sweep))**2.0/(Beta*Beta))+4.0)**0.5))
    
    return cL_alpha
