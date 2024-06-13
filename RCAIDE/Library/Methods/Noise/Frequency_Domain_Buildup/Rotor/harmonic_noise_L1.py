## @ingroup Methods-Noise-Multi_Fidelity
# RCAIDE/Methods/Noise/Multi_Fidelity/Level_1.py
# 
# 
# Created:  Apr 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports    
from RCAIDE.Framework.Core    import Data 
from RCAIDE.Library.Methods.Aerodynamics.Airfoil_Panel_Method    import airfoil_analysis
from RCAIDE.Library.Methods.Geometry.Two_Dimensional.Airfoil     import compute_naca_4series
from RCAIDE.Library.Methods.Geometry.Two_Dimensional.Airfoil     import import_airfoil_geometry

# package imports  
import numpy as np
import scipy as sp
from scipy.special import jv

# ----------------------------------------------------------------------------------------------------------------------
# Level_1
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Noise-Multi_Fidelity
def harmonic_noise_l1(harmonics,freestream,angle_of_attack,coordinates,velocity_vector,rotor,aeroacoustic_data,settings,res):
    '''This computes the  harmonic noise (i.e. thickness and loading noise) of a rotor or rotor
    in the frequency domain

    Assumptions:
    Compactness of thrust and torque along blade radius from root to tip
    Thin airfoil assumption

    Source:
    1) Hanson, Donald B. "Helicoidal surface theory for harmonic noise of rotors in the far field."
    AIAA Journal 18.10 (1980): 1213-1220.

    2) Hubbard, Harvey H., ed. Aeroacoustics of flight vehicles: theory and practice. Vol. 1.
    NASA Office of Management, Scientific and Technical Information Program, 1991.


    Inputs: 
        harmonics                     - harmomics                                                                  [Unitless]
        freestream                    - freestream data structure                                                  [m/s]
        angle_of_attack               - aircraft angle of attack                                                   [rad]
        position_vector               - position vector of aircraft                                                [m]
        velocity_vector               - velocity vector of aircraft                                                [m/s] 
        rotors                        - data structure of rotors                                                   [None]
        aeroacoustic_data             - data structure of acoustic data                                            [None]
        settings                      - accoustic settings                                                         [None] 
        res                           - results data structure                                                     [None] 

    Outputs 
        res.                                    *acoustic data is stored and passed in data structures*                                                                            
            SPL_prop_harmonic_bpf_spectrum       - harmonic noise in blade passing frequency spectrum              [dB]
            SPL_prop_harmonic_bpf_spectrum_dBA   - dBA-Weighted harmonic noise in blade passing frequency spectrum [dbA]                  
            SPL_prop_harmonic_1_3_spectrum       - harmonic noise in 1/3 octave spectrum                           [dB]
            SPL_prop_harmonic_1_3_spectrum_dBA   - dBA-Weighted harmonic noise in 1/3 octave spectrum              [dBA] 
            p_pref_harmonic                      - pressure ratio of harmonic noise                                [Unitless]
            p_pref_harmonic_dBA                  - pressure ratio of dBA-weighted harmonic noise                   [Unitless]

    '''
    
    num_h        = len(harmonics)     
    num_cpt      = len(angle_of_attack) 
    num_mic      = len(coordinates.X_hub[0,:,0,0,0,0])
    num_rot      = len(coordinates.X_hub[0,0,:,0,0,0]) 
    phi_0        = np.array([rotor.phase_offset_angle])  # phase angle offset  
    num_sec      = len(rotor.radius_distribution) 
    orientation  = np.array(rotor.orientation_euler_angles) * 1 
    body2thrust  = sp.spatial.transform.Rotation.from_rotvec(orientation).as_matrix()
    
    # ----------------------------------------------------------------------------------
    # Rotational Noise - Thickness and Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point ,microphones, rotors, radial distribution, harmonics]  
    m              = np.tile(harmonics[None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,1))                 # harmonic number 
    m_1d           = harmonics                                                                                         
    p_ref          = 2E-5                                                                                        # referece atmospheric pressure
    a              = np.tile(freestream.speed_of_sound[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))      # speed of sound
    rho            = np.tile(freestream.density[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))             # air density   
    alpha          = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))          
    B              = rotor.number_of_blades                                                                      # number of rotor blades
    omega          = np.tile(aeroacoustic_data.omega[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))        # angular velocity       
    dT_dr          = np.tile(aeroacoustic_data.blade_dT_dr[:,None,None,:,None],(1,num_mic,num_rot,1,num_h))      # nondimensionalized differential thrust distribution 
    dQ_dr          = np.tile(aeroacoustic_data.blade_dQ_dr[:,None,None,:,None],(1,num_mic,num_rot,1,num_h))      # nondimensionalized differential torque distribution
    R              = np.tile(rotor.radius_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h)) # radial location     
    c              = np.tile(rotor.chord_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h))  # blade chord    
    R_tip          = rotor.tip_radius                                                     
    t_c            = np.tile(rotor.thickness_to_chord[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h))  # thickness to chord ratio
    MCA            = np.tile(rotor.mid_chord_alignment[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h)) # Mid Chord Alighment  
    phi_0_vec      = np.tile(phi_0[None,None,:,None,None],(num_cpt,num_mic,1,num_sec,num_h))
    res.f          = B*omega*m/(2*np.pi) 
    D              = 2*R[0,0,0,-1,:]                                                                             # rotor diameter    
    r              = R/R[0,0,0,-1,:]                                                                             # non dimensional radius distribution   
    Y              = np.tile(np.sqrt(coordinates.X_hub[:,:,:,0,:,1]**2 +  coordinates.X_hub[:,:,:,0,:,2] **2)[:,:,:,:,None],(1,1,1,1,num_h))                        # observer distance from rotor axis          
    V              = np.tile(np.linalg.norm(velocity_vector,axis =1) [:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h))                                                     # velocity magnitude
    M_x            = V/a                                                                                         
    V_tip          = R_tip*omega                                                                                 # blade_tip_speed 
    M_t            = V_tip/a                                                                                     # tip Mach number 
    M_r            = np.sqrt(M_x**2 + (r**2)*(M_t**2))                                                           # section relative Mach number     
    B_D            = c/D     
     
    phi            = np.tile(coordinates.phi_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h)) + phi_0_vec 

    # retarted theta angle in the retarded reference frame
    theta_r        = np.tile(coordinates.theta_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h))  
    theta_r_prime  = np.arccos(np.cos(theta_r)*np.cos(alpha) + np.sin(theta_r)*np.sin(phi)*np.sin(alpha) )
    S_r            = np.tile(np.linalg.norm(coordinates.X_hub_r[:,:,:,0,:,:], axis = 4)[:,:,:,:,None],(1,1,1,1,num_h))  

    # initialize thickness and loading noise matrices
    psi_L          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h))
    psi_V          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h))
    
    # dimensionless wavenumbers
    k_x            = ((2*m*B*B_D*M_t)/(M_r*(1 - M_x*np.cos(theta_r))))
    k_y            = ((2*m*B*B_D)/r*M_r)*((M_r**2*np.cos(theta_r) - M_x)/(1 - M_x*np.cos(theta_r)))
    
    # thickness and loading shape functions
    
    