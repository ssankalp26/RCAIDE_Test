## @ingroup Methods-Noise-Multi_Fidelity
# RCAIDE/Methods/Noise/Multi_Fidelity/harmonic_noise_plane.py
# 
# 
# Created:  Jul 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE
from RCAIDE.Framework.Core                                 import Data , Units, Container,orientation_product, orientation_transpose  
from RCAIDE.Library.Methods.Noise.Common                   import convert_to_third_octave_band
from RCAIDE.Library.Methods.Aerodynamics.Airfoil_Panel_Method.airfoil_analysis   import airfoil_analysis

# Python Package imports  
import numpy as np
from scipy.special import jv 
import scipy as sp

# ----------------------------------------------------------------------------------------------------------------------
# Compute Harmonic Noise 
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor 
def harmonic_noise_plane(conditions,harmonics_blade,harmonics_load,freestream,angle_of_attack,coordinates,
                           velocity_vector,rotor,aeroacoustic_data,settings,res):
    '''This computes the harmonic noise (i.e. thickness and loading noise) in the frequency domain 
    of a rotor at any angle of attack with load distribution along the blade span and blade chord. This is a 
    level 3 fidelity approach. All sources are computed using the helicoidal surface theory.

    Assumptions:
    1) Acoustic non-compactness of loads along blade chord.
    2) Acoustic non-compactness of loads along blade span.
    3) Acoustic compactness of loads along blade thickness.

    Source:
    1) Hanson, D. B. (1995). Sound from a propeller at angle of attack: a new theoretical viewpoint. 
    Proceedings - Royal Society of London, A, 449(1936).
    
    2) Hanson, D. B. "Noise radiation of propeller loading sources with angular inflow" AIAA 1990-3955.
    13th Aeroacoustics Conference. October 1990.
    
    3) Hanson, Donald B. "Helicoidal surface theory for harmonic noise of rotors in the far field."
    AIAA Journal 18.10 (1980): 1213-1220.

    3) Hubbard, Harvey H., ed. Aeroacoustics of flight vehicles: theory and practice. Vol. 1.
    NASA Office of Management, Scientific and Technical Information Program, 1991.


    Inputs: 
        harmonics_blade               - blade harmonics                                                            [Unitless]
        harmonics_load                - loading harmonics (modes within each blade harmonic mode)                  [Unitless]
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


    Properties Used:
        N/A   
    '''     
    num_h_b      = len(harmonics_blade)
    num_h_l      = len(harmonics_load)
    num_cpt      = len(angle_of_attack) 
    num_mic      = len(coordinates.X_hub[0,:,0,0,0,0])
    num_rot      = len(coordinates.X_hub[0,0,:,0,0,0]) 
    phi_0        = np.array([rotor.phase_offset_angle])  # phase angle offset  
    num_sec      = len(rotor.radius_distribution)
    num_az       = aeroacoustic_data.number_azimuthal_stations
    airfoil_geometry = rotor.Airfoils.airfoil.geometry
    chord_coord  = len(airfoil_geometry.camber_coordinates)
    orientation  = np.array(rotor.orientation_euler_angles) * 1 
    body2thrust  = sp.spatial.transform.Rotation.from_rotvec(orientation).as_matrix()

    # Reynolds number and AOA of each blade section at each azimuthal station
    Re    = aeroacoustic_data.blade_reynolds_number
    alpha = aeroacoustic_data.blade_effective_angle_of_attack
    
    
    # Lift and Drag - coefficients and distributions
    fL_pre  = np.zeros_like(Re)
    fL      = np.tile(fL_pre[:,:,:,None],(1,1,1,chord_coord))
    fD_pre  = np.zeros_like(Re)
    fD      = np.tile(fD_pre[:,:,:,None],(1,1,1,chord_coord))
    CL = np.zeros_like(Re)
    CD = np.zeros_like(Re)
    
    for cpt in range (num_cpt):
        for sec in range(num_sec):
            for az in range(num_az):
                airfoil_properties = airfoil_analysis(airfoil_geometry,np.atleast_2d(alpha[cpt,sec,az]),np.atleast_2d(Re[cpt,sec,az]))
                fL[cpt,sec,az,:] = airfoil_properties.fL[:,0,0]
                fD[cpt,sec,az,:] = airfoil_properties.fD[:,0,0]
                CL[cpt,sec,az]   = airfoil_properties.cl_invisc
                CD[cpt,sec,az]   = airfoil_properties.cd_visc
    
    
    # DFT to get loading modes
    CL_k           = sp.fft.rfft(CL, axis=2)
    CD_k           = sp.fft.rfft(CD, axis=2)
    fL_k           = sp.fft.rfft(fL, axis=2)
    fD_k           = sp.fft.rfft(fD, axis=2)
    
    
    # ----------------------------------------------------------------------------------
    # Rotational Noise  Thickness and Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics]  
    
    # freestream density and speed of sound
    rho            = np.tile(freestream.density[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    a              = np.tile(freestream.speed_of_sound[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    
    B              = rotor.number_of_blades
    
    # blade and loading harmonics
    m              = np.tile(harmonics_blade[None,None,None,None,:,None],(num_cpt,num_mic,num_rot,num_sec,1,num_h_l))  
    m_1d           = harmonics_blade                                                                                         
    k              = np.tile(harmonics_load[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    
    # reference atmospheric pressure
    p_ref          = 2E-5
    
    # net angle of inclination of propeller axis wrt inertial axis
    alpha          = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    
    # rotor angular speed
    omega          = np.tile(aeroacoustic_data.omega[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))   
    
    # rotor blade - radial distribution of radius, chord, thickness/chord and MCA
    R              = np.tile(rotor.radius_distribution[None,None,None,:,None,None],(num_cpt,num_mic,num_rot,1,num_h_b,num_h_l))
    r              = R/R[0,0,0,-1,0,0]
    c              = np.tile(rotor.chord_distribution[None,None,None,:,None,None],(num_cpt,num_mic,num_rot,1,num_h_b,num_h_l))   
    t_c            = np.tile(rotor.thickness_to_chord[None,None,None,:,None,None],(num_cpt,num_mic,num_rot,1,num_h_b,num_h_l))
    MCA            = np.tile(rotor.mid_chord_alignment[None,None,None,:,None,None],(num_cpt,num_mic,num_rot,1,num_h_b,num_h_l))
    
    R_tip          = rotor.tip_radius
    D              = 2*R[0,0,0,-1,0,0]
    B_D            = c/D
    
    # Rotorcraft speed and mach number
    V              = np.tile(np.linalg.norm(velocity_vector,axis =1) [:,None,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    M_x            = V/a
    
    # Rotor tip speed and mach number
    V_tip          = R_tip*omega                                                        
    M_t            = V_tip/a
    
    # Section relative mach number
    M_r            = np.sqrt(M_x**2 + (r**2)*(M_t**2))                                                   # section relative Mach number
    
    # retarded coordinates
    theta_r        = np.tile(coordinates.theta_hub_r[:,:,:,0,:,None,None],(1,1,1,1,num_h_b,num_h_l))
    Y              = np.tile(np.sqrt(coordinates.X_hub[:,:,:,0,:,1]**2 +  coordinates.X_hub[:,:,:,0,:,2] **2)[:,:,:,:,None,None],(1,1,1,1,num_h_b,num_h_l))
    r_dist         = Y/np.sin(theta_r)
    
    # phase and inclination angles
    phi_0_vec      = np.tile(phi_0[None,None,:,None,None,None],(num_cpt,num_mic,1,num_sec,num_h_b,num_h_l))
    phi            = np.tile(coordinates.phi_hub_r[:,:,:,0,:,None,None],(1,1,1,1,num_h_b,num_h_l)) + phi_0_vec
    theta_r_prime  = np.arccos(np.cos(theta_r)*np.cos(alpha) + np.sin(theta_r)*np.sin(phi)*np.sin(alpha))
    phi_prime      = np.arccos((np.sin(theta_r)*np.cos(phi))/np.sin(theta_r_prime))
    
    # Velocity in the rotor frame
    T_body2inertial = conditions.frames.body.transform_to_inertial
    T_inertial2body = orientation_transpose(T_body2inertial)
    V_body          = orientation_product(T_inertial2body,velocity_vector)
    body2thrust     = rotor.body_to_prop_vel()
    T_body2thrust   = orientation_transpose(np.ones_like(T_body2inertial[:])*body2thrust)
    V_thrust        = orientation_product(T_body2thrust,V_body)
    V_thrust_perp   = V_thrust[:,0,None]
    V_thrust_perp_tiled = np.tile(V_thrust_perp[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    M_thrust        = V_thrust_perp_tiled/a
    
    # helicoid angle
    zeta           = np.arctan(M_thrust/(r*M_t))
    
    # wavenumbers
    k_m            = m*B*omega/a
    k_m_bar        = k_m/(1 - M_x*np.cos(theta_r))
    k_x_hat        = 2*B_D*(((m*B-k)*np.cos(zeta))/r + (m*B*M_t*np.cos(theta_r_prime)*np.sin(zeta))/(1-M_x*np.cos(theta_r)))
    k_y_hat        = 2*B_D*(((m*B-k)*np.sin(zeta))/r - (m*B*M_t*np.cos(theta_r_prime)*np.cos(zeta))/(1-M_x*np.cos(theta_r)))
    
    # phase angles
    phi_s          = k_x_hat*MCA/c
    # phi_FA         = k_x_hat*
    
    res.f          = B*omega*m/(2*np.pi)

    
    CL_k_tiled     = np.tile(CL_k[:,None,None,:,None,0:num_h_l],(1,num_mic,num_rot,1,num_h_b,1))
    CD_k_tiled     = np.tile(CD_k[:,None,None,:,None,0:num_h_l],(1,num_mic,num_rot,1,num_h_b,1))
    
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics, chordwise coordinate]
    fL_k_tiled     = np.tile(fL_k[:,None,None,:,None,0:num_h_l,:],(1,num_mic,num_rot,1,num_h_b,1,1))
    fD_k_tiled     = np.tile(fD_k[:,None,None,:,None,0:num_h_l,:],(1,num_mic,num_rot,1,num_h_b,1,1))   
      
    
    S_r            = np.tile(np.linalg.norm(coordinates.X_hub_r[:,:,:,0,:,:], axis = 4)[:,:,:,:,None],(1,1,1,1,num_h_b))  
    
    
    # frequency domain source function for drag and lift
    k_x_hat_tiled  = np.tile(k_x_hat[:,:,:,:,:,:,None],(1,1,1,1,1,1,chord_coord))
    X_edge         = np.linspace(-0.5,0.5,chord_coord+1)
    dX             = np.diff(X_edge)
    dX_tiled       = np.tile(dX[None,None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,num_h_l,1))
    X              = 0.5*(X_edge[0:-1] + X_edge[1:])
    X_tiled        = np.tile(X[None,None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,num_h_l,1))
    exp_term       = np.exp(1j*k_x_hat_tiled*X_tiled)
    psi_Lk         = np.sum(fL_k_tiled*exp_term*dX_tiled,axis=5)
    psi_Dk         = np.sum(fD_k_tiled*exp_term*dX_tiled,axis=5)
    
    # frequency domain source function for thickness distribution
    H              = airfoil_geometry.y_upper_surface - airfoil_geometry.y_lower_surface
    H_tiled        = np.tile(H[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    psi_V          = np.sum(H*exp_term*dX_tiled,axis=5)