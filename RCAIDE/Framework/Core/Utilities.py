# RCAIDE/Core/Utilities.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  interp2d
# ----------------------------------------------------------------------------------------------------------------------
 
def interp2d(x, y, z, xi, yi):
    """2D interpolation of z(x,y) at points (xi,yi)

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    x  - 1D array of x coordinates
    y  - 1D array of y coordinates
    z  - 2D array of z values with shape (len(x), len(y))
    xi - x coordinates to interpolate at
    yi - y coordinates to interpolate at

    Returns:
    zi - interpolated values at (xi,yi)
    """
    ix = np.clip(np.searchsorted(x, xi, side="right"), 1, len(x) - 1)
    iy = np.clip(np.searchsorted(y, yi, side="right"), 1, len(y) - 1)

    # Using Wikipedia's notation (https://en.wikipedia.org/wiki/Bilinear_interpolation)
    z_11 = z[ix - 1, iy - 1]
    z_21 = z[ix, iy - 1]
    z_12 = z[ix - 1, iy]
    z_22 = z[ix, iy]

    z_xy1 = (x[ix] - xi) / (x[ix] - x[ix - 1]) * z_11 + (xi - x[ix - 1]) / (
        x[ix] - x[ix - 1]
    ) * z_21
    z_xy2 = (x[ix] - xi) / (x[ix] - x[ix - 1]) * z_12 + (xi - x[ix - 1]) / (
        x[ix] - x[ix - 1]
    ) * z_22

    z = (y[iy] - yi) / (y[iy] - y[iy - 1]) * z_xy1 + (yi - y[iy - 1]) / (
        y[iy] - y[iy - 1]
    ) * z_xy2

    return z

# ----------------------------------------------------------------------------------------------------------------------
# orientation_product
# ----------------------------------------------------------------------------------------------------------------------
 
def orientation_product(T1,T2):
    """Multiplies two matrices T1 and T2, where T2 is a tensor of matrices

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    T1 - transformation matrix
    T2 - tensor of transformation matrices

    Returns:
    T3 - the product of T1 and T2
    """
    assert T1.ndim == 2
    assert T2.ndim == 3
    
    T3 = np.einsum('ij,ajk->aik', T1, T2)
    
    return T3

# ----------------------------------------------------------------------------------------------------------------------
# orientation_transpose
# ----------------------------------------------------------------------------------------------------------------------

def orientation_transpose(T):
    """Takes the transpose of a tensor of matrices

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    T - tensor of matrices

    Returns:
    Tt - transpose of T
    """
    
    assert T.ndim == 3
    
    Tt = np.swapaxes(T,1,2)
        
    return Tt

# ----------------------------------------------------------------------------------------------------------------------
# angles_to_dcms
# ----------------------------------------------------------------------------------------------------------------------

def angles_to_dcms(angles):
    """Converts a set of angles to direction cosine matrices

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    angles - array of angles in radians (phi, theta, psi)

    Returns:
    T - transformation tensor for given angles
    """

# ----------------------------------------------------------------------------------------------------------------------
# T0
# ----------------------------------------------------------------------------------------------------------------------  

def T0(a):
    """Rotation matrix about first axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[1,   0,  0],
    #               [0, cos,sin],
    #               [0,-sin,cos]])
    
    cos = np.cos(a)
    sin = np.sin(a)
                  
    T = new_tensor(a)
    
    T[:,1,1] = cos
    T[:,1,2] = sin
    T[:,2,1] = -sin
    T[:,2,2] = cos
    
    return T

# ----------------------------------------------------------------------------------------------------------------------
# T1
# ----------------------------------------------------------------------------------------------------------------------          

def T1(a):
    """Rotation matrix about second axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[cos,0,-sin],
    #               [0  ,1,   0],
    #               [sin,0, cos]])
    
    cos = np.cos(a)
    sin = np.sin(a)     
    
    T = new_tensor(a)
    
    T[:,0,0] = cos
    T[:,0,2] = -sin
    T[:,2,0] = sin
    T[:,2,2] = cos
    
    return T

# ----------------------------------------------------------------------------------------------------------------------
# T2
# ----------------------------------------------------------------------------------------------------------------------  

def T2(a):
    """Rotation matrix about third axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[cos ,sin,0],
    #               [-sin,cos,0],
    #               [0   ,0  ,1]])
        
    cos = np.cos(a)
    sin = np.sin(a)     
    
    T = new_tensor(a)
    
    T[:,0,0] = cos
    T[:,0,1] = sin
    T[:,1,0] = -sin
    T[:,1,1] = cos
        
    return T

# ----------------------------------------------------------------------------------------------------------------------
# new_tensor
# ----------------------------------------------------------------------------------------------------------------------  

def new_tensor(shape):
    """Creates a new tensor of matrices of a given shape

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    shape - the shape of the tensor to create

    Returns:
    T - the new tensor
    """
    assert a.ndim == 1
    n_a = len(a)
    
    T = np.eye(3)
    
    if a.dtype is np.dtype('complex'):
        T = T + 0j
    
    T = np.resize(T,[n_a,3,3])
    
    return T