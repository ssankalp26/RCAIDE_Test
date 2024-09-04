# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_wing_moment_of_inertia.py 
# 
# Created:  Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE
from RCAIDE.Framework.Core import Units    

# package imports 
import numpy as np  
# ----------------------------------------------------------------------------------------------------------------------
#  Compute Wing Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------  
def compute_wing_moment_of_inertia(wing, center_of_gravity, mass): 
    
    tr = wing.thickness_to_chord # root thickness as percent of chord
    tt = wing.thickness_to_chord #tip thickness as a percent of chord
    ct = wing.chords.tip # tip chord 
    cr = wing.chords.root # root chord
    
    b = wing.spans.total / 2 # half-span of the wing
    A = wing.sweeps.quarter_chord * np.pi / 180 # sweep angle in radians (located at quarter chord)
    dihedral = wing.dihedral * np.pi /180 # Wing dihedral. Converts it to radians
        
    # a0-a4 values are defined below for a NACA 4-digit airfoil. This holds for all NACA airfoils
    # These values help define the thickness distribution. 
    a0 = 2.969
    a1 = -1.260
    a2 = -3.516
    a3 = 2.843
    a4 = -1.015
    
    # Calculate constants. These constants are defined in the paper.
    ka = tr * (3 * cr ** 2 + 2 * cr * ct + ct ** 2) + tt * (cr ** 2 + 2 * cr * ct + 3 * ct ** 2)
    kd = (tr * (ct + cr) * (2 * cr ** 2 + cr * ct + 2 * ct ** 2)
          + tt * (cr ** 3 + 3 * cr ** 2 * ct + 6 * cr * ct ** 2 + 10 * ct ** 3))
    ke = (tr * (5 * cr ** 4 + 4 * cr ** 3 * ct + 3 * cr ** 2 * ct ** 2 + 2 * cr * ct ** 3 + ct ** 4)
          + tt * (cr ** 4 + 2 * cr ** 3 * ct + 3 * cr ** 2 * ct ** 2 + 4 * cr * ct ** 3 + 5 * ct ** 4))    
    kf = (tr * (cr ** 2 + 2 * cr * ct + 2 * ct ** 2) + tt * (cr ** 2 + 4 * cr * ct
                                                             + 10 * ct ** 2))
    kg = (tr ** 3 * (35 * cr ** 4 + 20 * cr ** 3 * ct + 10 * cr ** 2 * ct ** 2 + 4 * cr * ct ** 3 + ct ** 4)
          + tr ** 2 * tt * (15 * cr ** 4 + 20 * cr ** 3 * ct + 18 * cr ** 2 * ct ** 2 + 12 * cr * ct ** 3 + 5 * ct ** 4)
          + tr * tt ** 2 * (5 * cr ** 4 + 12 * cr ** 3 * ct + 18 * cr ** 2 * ct ** 2 + 20 * cr * ct ** 3 + 15 * ct ** 4)
          + tt ** 3 * (cr ** 4 + 4 * cr ** 3 * ct + 10 * cr ** 2 * ct ** 2 + 20 * cr * ct ** 3 + 35 * ct ** 4))
    
    v0 = 1 / 60 * (40 * a0 + 30 * a1 + 20 * a2 + 15 * a3 + 12 * a4) # NACA 4 digit integral of thickness distribution.
    v1 = 1 / 60 * (56 * a0 + 50 * a1 + 40 * a2 + 33 * a3 + 28 * a4)
    v2 = 1 / 980 * (856 * a0 + 770 * a1 + 644 * a2 + 553 * a3 + 484 * a4)
    v3 = (2 / 5 * a0 ** 3 + a0 ** 2 * a1 + 3 / 4 * a0 ** 2 * a2 + 3 / 5 * a0 ** 2 * a3 + 1 / 2 * a0 ** 2 * a4 + 6 / 7 * a0 * a1 ** 2
          + 4 / 3 * a0 * a1 * a2 + 12 / 11 * a0 * a1 * a3 + 12 / 13 * a0 * a1 * a4 + 6 / 11 * a0 * a2 ** 2 + 12 / 13 * a0 * a2 * a3
          + 4 / 5 * a0 * a2 * a4 + 2 / 5 * a0 * a3 ** 2 + 12 / 17 * a0 * a3 * a4 + 6 / 19 * a0 * a4 ** 2 + 1 / 4 * a1 ** 3
          + 3 / 5 * a1 ** 2 * a2 + 1 / 2 * a1 ** 2 * a3 + 3 / 7 * a1 ** 2 * a4 + 1 / 2 * a1 * a2 ** 2 + 6 / 7 * a1 * a2 * a3
          + 3 / 4 * a1 * a2 * a4 + 3 / 8 * a1 * a3 ** 2 + 2 / 3 * a1 * a3 * a4 + 3 / 10 * a1 * a4 ** 2 + 1 / 7 * a2 ** 3
          + 3 / 8 * a2 ** 2 * a3 + 1 / 3 * a2 ** 2 * a4 + 1 / 3 * a2 * a3 ** 2 + 3 / 5 * a2 * a3 * a4 + 3 / 11 * a2 * a4 ** 2
          + 1 / 10 * a3 ** 3 + 3 / 11 * a3 ** 2 * a4 + 1 / 4 * a3 * a4 ** 2 + 1 / 13 * a4 ** 3)
    
    # Moment of inertia in local system
    delta = 1 # 1 for right wing, -1 for left wing. Assumes all non-symmetric wings are right-wings.
    
    Ixx = mass * (56 * b ** 2 * kf * v0 + kg * v3) / (280 * ka * v0)
    Iyy = mass * (84 * b * (2 * b * kf * v0 * np.tan(A) ** 2 + kd * v1 * np.tan(A)) + 49 * ke * v2 + 3 * kg * v3) / (840 * ka * v0)
    Izz = mass * (12 * b * (2 * b * (np.tan(A) ** 2 + 1) * kf * v0 + kd * v1 * np.tan(A)) + 7 * ke * v2) / (120 * ka * v0)
    Ixy = -1 * delta * b * mass * (4 * b * kf * v0 * np.tan(A) + kd * v1) / (20 * ka * v0)
    ## Ixz, Iyz are 0
    Ixz = 0
    Iyz = 0
    I_wing_sys = [[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]] # inertia tensor int eh wing system
    
    # Dihedral. -1*dihedral for the right wing
    R = np.array([[1, 0, 0], [0, np.cos(-1*dihedral), -1 * np.sin(-1*dihedral)], [0, np.sin(-1*dihedral), np.cos(-1*dihedral)]])
    I_local = R *I_wing_sys *np.transpose(R) 
        
    if wing.symmetric: # wing is symmetric
        print("symmetric")
        R = np.array([[1, 0, 0], [0, np.cos(dihedral), -1 * np.sin(dihedral)], [0, np.sin(dihedral), np.cos(dihedral)]])        
        
        delta = -1 # left wing
        Ixx = mass * (56 * b ** 2 * kf * v0 + kg * v3) / (280 * ka * v0)
        Iyy = mass * (84 * b * (2 * b * kf * v0 * np.tan(A) ** 2 + kd * v1 * np.tan(A)) + 49 * ke * v2 + 3 * kg * v3) / (840 * ka * v0)
        Izz = mass * (12 * b * (2 * b * (np.tan(A) ** 2 + 1) * kf * v0 + kd * v1 * np.tan(A)) + 7 * ke * v2) / (120 * ka * v0)
        Ixy = -1 * delta * b * mass * (4 * b * kf * v0 * np.tan(A) + kd * v1) / (20 * ka * v0)
        I_local_left = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]])
        
        I_local_left = R *I_local_left * np.transpose(R)
        
        I_local = I_local + I_local_left # Add the left wing inertia tensor if wing is symmetric
        
    if wing.vertical: # If it is a vertical tail
        R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) # Rotation matrix for a vertical surface

        I_rotated = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]]) # Inertia matrix in the unrotated frame
        I_local = R * I_rotated * np.transpose(R) # Rotation of ienrtia matrix to a vertical frame of reference         
    
    # global system
    s = np.array(wing.origin) - np.array(center_of_gravity) # Vector for the parallel axis theorem
    
    I = np.array(I_local) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s * np.transpose(s))
    
    return I  

