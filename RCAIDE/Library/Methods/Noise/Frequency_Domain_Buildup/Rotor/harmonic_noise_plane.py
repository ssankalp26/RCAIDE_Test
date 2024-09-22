## @ingroup Methods-Noise-Multi_Fidelity
# RCAIDE/Methods/Noise/Multi_Fidelity/harmonic_noise_plane.py
# 
# 
# Created:  Jul 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE
from RCAIDE.Framework.Core                                 import orientation_product, orientation_transpose  
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
    
    Code Convention - The number in front of a variable name indicates the number of dimensions of the variable.
                      For instance, m_6 is the 6 dimensional harmonic modes variable, m_5 is 5 dimensional harmonic modes variable
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
    Re      = aeroacoustic_data.blade_reynolds_number
    AOA_sec = aeroacoustic_data.blade_effective_angle_of_attack
    
    
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
                airfoil_properties = airfoil_analysis(airfoil_geometry,np.atleast_2d(AOA_sec[cpt,sec,az]),np.atleast_2d(Re[cpt,sec,az]))
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
    # Rotational Noise - Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics]  
    
    # freestream density and speed of sound
    rho_4          = np.tile(freestream.density[:,:,None],(1,num_mic,num_h_b))
    a_4            = np.tile(freestream.speed_of_sound[:,:,None],(1,num_mic,num_h_b))
    
    B              = rotor.number_of_blades
    
    # blade harmonics
    m_4            = np.tile(harmonics_blade[None,None,:],(num_cpt,num_mic,1))
    m_5            = np.tile(harmonics_blade[None,None,:,None],(num_cpt,num_mic,1,num_h_l))
    m_6            = np.tile(harmonics_blade[None,None,None,:,None],(num_cpt,num_mic,num_sec,1,num_h_l))
    m_7            = np.tile(harmonics_blade[None,None,None,:,None,None],(num_cpt,num_mic,num_sec,1,num_h_l,chord_coord))
                                                                                            
    # loading harmonics
    k_5            = np.tile(harmonics_load[None,None,None,:],(num_cpt,num_mic,num_h_b,1))
    k_6            = np.tile(harmonics_load[None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,1))
    k_7            = np.tile(harmonics_load[None,None,None,None,:,None],(num_cpt,num_mic,num_sec,num_h_b,1,chord_coord))
    
    # reference atmospheric pressure
    p_ref          = 2E-5
    
    # net angle of inclination of propeller axis wrt inertial axis
    alpha_5        = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None],(1,num_mic,num_h_b,num_h_l))
    alpha_6        = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None],(1,num_mic,num_sec,num_h_b,num_h_l))
    alpha_7        = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None,None],(1,num_mic,num_sec,num_h_b,num_h_l,chord_coord))
    
    # rotor angular speed
    omega_4        = np.tile(aeroacoustic_data.omega[:,:,None],(1,num_mic,num_h_b))   
    
    R              = rotor.radius_distribution
    
    # Non-dimensional radius distribution
    z_6            = np.tile((R/R[-1])[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    z_7            = np.tile((R/R[-1])[None,None,:,None,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l,chord_coord))
    
    # Radial chord distribution
    c_6            = np.tile(rotor.chord_distribution[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    c_7            = np.tile(rotor.chord_distribution[None,None,:,None,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l,chord_coord))
    
    MCA_6          = np.tile(rotor.mid_chord_alignment[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    
    # chord to diameter ratio
    R_tip          = rotor.tip_radius
    D              = 2*R[-1]
    B_D_6          = c_6/D
    B_D_7          = c_7/D
    
    # maximum thickness to chord ratio
    t_b            = rotor.thickness_to_chord
    t_b_6          = np.tile(t_b[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    
    # chordwise thickness distribution normalized wrt chord
    y_u_7          = np.tile(airfoil_geometry.y_upper_surface[None,None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,num_h_l,1))
    y_l_7          = np.tile(airfoil_geometry.y_lower_surface[None,None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,num_h_l,1))
    H_7            = (y_u_7 - y_l_7)/c_7
    
    
    # Rotorcraft speed and mach number
    V_4            = np.tile(np.linalg.norm(velocity_vector, axis=1) [:,None,None],(1,num_mic,num_h_b))
    M_4            = V_4/a_4
    M_6            = np.tile(M_4[:,:,:,None,:,None],(1,1,1,num_sec,1,num_h_l))
    M_7            = np.tile(M_4[:,:,:,None,:,None,None],(1,1,1,num_sec,1,num_h_l,chord_coord))
    
    # Rotor tip speed and mach number
    V_tip          = R_tip*omega_4                                                        
    M_t_4          = V_tip/a_4
    M_t_6          = np.tile(M_t_4[:,:,:,None,:,None],(1,1,1,num_sec,1,num_h_l))
    M_t_7          = np.tile(M_t_4[:,:,:,None,:,None,None],(1,1,1,num_sec,1,num_h_l,chord_coord))
    
    # Section relative mach number
    M_r_6          = np.sqrt(M_6**2 + (z_6**2)*(M_t_6**2))
    
    # retarded theta
    theta_r        = coordinates.theta_hub_r[:,:,0,0,0]
    theta_r_4      = np.tile(theta_r[:,:None],(1,1,num_h_b))
    theta_r_5      = np.tile(theta_r[:,:,None,None],(1,1,num_h_b,num_h_l))
    theta_r_6      = np.tile(theta_r[:,:,None,None,None],(1,1,num_sec,num_h_b,num_h_l))
    theta_r_7      = np.tile(theta_r[:,:,None,None,None,None],(1,1,num_sec,num_h_b,num_h_l,chord_coord))
    
    # retarded distance to source
    Y              = np.sqrt(coordinates.X_hub[:,:,:,0,0,1]**2 +  coordinates.X_hub[:,:,:,0,0,2] **2)
    Y_4            = np.tile(Y[:,:,:,None],(1,1,1,num_h_b))
    r_4            = Y_4/np.sin(theta_r_4)
    
    # phase angles
    phi_0_vec      = np.tile(phi_0[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    phi_5          = np.tile(coordinates.phi_hub_r[:,:,:,0,0,None,None],(1,1,1,num_h_b,num_h_l)) + phi_0_vec
    phi_6          = np.tile(phi_5[:,:,:,None,:,:],(1,1,1,num_sec,1,1))
    phi_7          = np.tile(phi_5[:,:,:,None,:,:,None],(1,1,1,num_sec,1,1,chord_coord))
    
    # total angle between propeller axis and r vector
    theta_r_prime_5 = np.arccos(np.cos(theta_r_5)*np.cos(alpha_5) + np.sin(theta_r_5)*np.sin(phi_5)*np.sin(alpha_5))
    theta_r_prime_6 = np.arccos(np.cos(theta_r_6)*np.cos(alpha_6) + np.sin(theta_r_6)*np.sin(phi_6)*np.sin(alpha_6))
    theta_r_prime_7 = np.arccos(np.cos(theta_r_7)*np.cos(alpha_7) + np.sin(theta_r_7)*np.sin(phi_7)*np.sin(alpha_7))
        
    phi_prime_5    = np.arccos((np.sin(theta_r_5)*np.cos(phi_5))/np.sin(theta_r_prime_5))
    
    # Velocity in the rotor frame
    T_body2inertial = conditions.frames.body.transform_to_inertial
    T_inertial2body = orientation_transpose(T_body2inertial)
    V_body          = orientation_product(T_inertial2body,velocity_vector)
    body2thrust     = rotor.body_to_prop_vel()
    T_body2thrust   = orientation_transpose(np.ones_like(T_body2inertial[:])*body2thrust)
    V_thrust        = orientation_product(T_body2thrust,V_body)
    V_thrust_perp   = V_thrust[:,0,None]
    V_thrust_perp_4 = np.tile(V_thrust_perp[:,:,None],(1,num_mic,num_h_b))
    M_thrust_4      = V_thrust_perp_4/a_4
    M_thrust_6      = np.tile(M_thrust_4[:,:,:,None,:,None],(1,1,1,num_sec,1,num_h_l))
    
    # helicoid angle
    zeta_6          = np.arctan(M_thrust_6/(z_6*M_t_6))
    zeta_7          = np.tile(zeta_6[:,:,:,:,:,:,None],(1,1,1,1,1,1,chord_coord))
    
    # wavenumbers
    k_m_4          = m_4*B*omega_4/a_4
    k_m_bar        = k_m_4/(1 - M_4*np.cos(theta_r_4))
    k_x_hat_6      = 2*B_D_6*(((m_6*B-k_6)*np.cos(zeta_6))/z_6 + (m_6*B*M_t_6*np.cos(theta_r_prime_6)*np.sin(zeta_6))/(1-M_6*np.cos(theta_r_6)))
    k_x_hat_7      = 2*B_D_7*(((m_7*B-k_7)*np.cos(zeta_7))/z_7 + (m_7*B*M_t_7*np.cos(theta_r_prime_7)*np.sin(zeta_7))/(1-M_7*np.cos(theta_r_7)))
    k_y_hat_6      = 2*B_D_6*(((m_6*B-k_6)*np.sin(zeta_6))/z_6 - (m_6*B*M_t_6*np.cos(theta_r_prime_6)*np.cos(zeta_6))/(1-M_6*np.cos(theta_r_6)))
    
    # phase angles
    phi_s_6        = k_x_hat_6*MCA_6/c_6
    # phi_FA         = k_x_hat*
    
    res.f          = B*m_4*omega_4/(2*np.pi)

    
    CL_k_6         = np.tile(CL_k[:,None,:,None,0:num_h_l],(1,num_mic,1,num_h_b,1))
    CD_k_6         = np.tile(CD_k[:,None,:,None,0:num_h_l],(1,num_mic,1,num_h_b,1))
    
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics, chordwise coordinate]
    fL_k_7         = np.tile(fL_k[:,None,:,None,0:num_h_l,:],(1,num_mic,1,num_h_b,1,1))
    fD_k_7         = np.tile(fD_k[:,None,:,None,0:num_h_l,:],(1,num_mic,1,num_h_b,1,1))   
      
    
    S_r            = np.tile(np.linalg.norm(coordinates.X_hub_r[:,:,:,0,:,:], axis = 4)[:,:,:,:,None],(1,1,1,1,num_h_b))  
    
    
    # frequency domain source function for drag and lift
    X_edge         = np.linspace(-0.5,0.5,chord_coord+1)
    dX             = np.diff(X_edge)
    dX_tiled_7     = np.tile(dX[None,None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,num_h_l,1))
    X              = 0.5*(X_edge[0:-1] + X_edge[1:])
    X_7            = np.tile(X[None,None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,num_h_l,1))
    exp_term_7     = np.exp(1j*k_x_hat_7*X_7)
    psi_Lk_6       = np.trapz(fL_k_7*exp_term_7, x=X, axis=6)
    psi_Dk_6       = np.trapz(fD_k_7*exp_term_7, x=X, axis=6)
    
    psi_hat_Lk_6   = psi_Lk_6*np.exp(1j*(phi_s_6 + phi_6))
    psi_hat_Dk_6   = psi_Dk_6*np.exp(1j*(phi_s_6 + phi_6))
    psi_hat_Fk_6   = 0.5*(k_y_hat_6*CL_k_6*psi_hat_Lk_6 + k_x_hat_6*CD_k_6*psi_hat_Dk_6)
    
    
    # FREQUENCY DOMAIN PRESSURE TERM FOR LOADING
    J_mBk_6        = jv(m_6*B-k_6, (m_6*B*z_6*M_t_6*np.sin(theta_r_prime_6))/(1-M_6*np.cos(theta_r_6)))
    L_Integrand_6  = (M_r_6**2)*psi_hat_Fk_6*J_mBk_6
    L_Summand_5    = np.trapz(L_Integrand_6, x=z_6[0,0,0,:,0,0], axis=3)*np.exp(1j*(m_5*B-k_5)*(phi_prime_5-(np.pi/2)))
    L_Summation_4  = np.sum(L_Summand_5, axis=4)
    P_Lm           = (-1j*rho_4*(a_4**2)*B*np.exp(1j*k_m_4*r_4)*L_Summation_4)/(4*np.pi*(r_4/R_tip)*(1-M_4*np.cos(theta_r_4)))
    
    # frequency domain source function for drag and lift
    psi_V_6        = np.trapz(H_7*exp_term_7, x=X, axis=6)
    
    # FREQUENCY DOMAIN PRESSURE TERM FOR THICKNESS
    V_Integrand_6  = (M_r_6**2)*(k_x_hat_6**2)*t_b_6*psi_V_6*J_mBk_6
    V_Summand_5    = np.trapz(V_Integrand_6, x=z_6[0,0,0,:,0,0], axis=3)*np.exp(1j*m_5*B*(phi_prime_5-(np.pi/2)))
    
    # we take a single dimension along the 4th axis because we only want the loading mode corresponding to k=0
    V_Summation_4  = V_Summand_5[:,:,:,:,0]
    P_Vm           = (-rho_4*(a_4**2)*B*np.exp(1j*k_m_4*r_4)*V_Summation_4)/(4*np.pi*(r_4/R_tip)*(1-M_4*np.cos(theta_r_4)))
    
    
    # SOUND PRESSURE LEVELS
    P_Lm_abs       = np.abs(P_Lm)
    P_Vm_abs       = np.abs(P_Vm)
    res.SPL_prop_harmonic_bpf_spectrum     = 20*np.log10((abs(P_Lm_abs + P_Vm_abs))/p_ref)  
    res.SPL_prop_harmonic_1_3_spectrum     = convert_to_third_octave_band(res.SPL_prop_harmonic_bpf_spectrum,res.f[:,0,0,:],settings)          
    res.SPL_prop_harmonic_1_3_spectrum[np.isinf(res.SPL_prop_harmonic_1_3_spectrum)]         = 0 
    
    return
    