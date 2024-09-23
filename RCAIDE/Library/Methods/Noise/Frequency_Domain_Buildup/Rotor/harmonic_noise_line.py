## @ingroup Methods-Noise-Multi_Fidelity
# RCAIDE/Methods/Noise/Multi_Fidelity/harmonic_noise_line.py
# 
# 
# Created:  Jun 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE    
from RCAIDE.Library.Methods.Noise.Common                         import convert_to_third_octave_band 

# Python Package imports  
import numpy as np
from scipy.special import jv 
import scipy as sp

# ----------------------------------------------------------------------------------------------------------------------
# Compute Harmonic Noise 
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor 
def harmonic_noise_line(harmonics_blade,harmonics_load,conditions,propulsor_conditions,coordinates,rotor,settings,Noise):
    '''This computes the harmonic noise (i.e. thickness and loading noise) in the frequency domain 
    of a rotor at any angle of attack with load distribution along the blade span. This is a level 1 fidelity
    approach. The thickness source is however computed using the helicoidal surface theory.

    Assumptions:
    1) Acoustic compactness of loads along blade chord.
    2) Acoustic non-compactness of loads along blade span.
    3) Acoustic compactness of loads along blade thickness.

    Source:
    1) Hanson, D. B. (1995). Sound from a propeller at angle of attack: a new theoretical viewpoint. 
    Proceedings - Royal Society of London, A, 449(1936). https://doi.org/10.1098/rspa.1995.0046
    
    2) Hanson, D. B. "Noise radiation of propeller loading sources with angular inflow" AIAA 1990-3955.
    13th Aeroacoustics Conference. October 1990. 

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

    aeroacoustic_data    = propulsor_conditions[rotor.tag] 
    angle_of_attack      = conditions.aerodynamics.angles.alpha 
    velocity_vector      = conditions.frames.inertial.velocity_vector 
    freestream           = conditions.freestream       
    num_h_b              = len(harmonics_blade)
    num_h_l              = len(harmonics_load)
    num_cpt              = len(angle_of_attack) 
    num_mic              = len(coordinates.X_hub[0,:,0,0,0]) 
    phi_0                = np.array([rotor.phase_offset_angle])  # phase angle offset  
    num_sec              = len(rotor.radius_distribution)
    num_az               = aeroacoustic_data.number_azimuthal_stations 
    orientation          = np.array(rotor.orientation_euler_angles) * 1 
    body2thrust          = sp.spatial.transform.Rotation.from_rotvec(orientation).as_matrix()  
    
    # ----------------------------------------------------------------------------------
    # Rotational Noise  Thickness and Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics]  
    
    # freestream density and speed of sound
    a_4            = np.tile(freestream.speed_of_sound[:,:,None],(1,num_mic,num_h_b))
    rho            = freestream.density
    
    B              = rotor.number_of_blades
    
    # blade harmonics
    m_4            = np.tile(harmonics_blade[None,None,:],(num_cpt,num_mic,1))
    m_5            = np.tile(harmonics_blade[None,None,:,None],(num_cpt,num_mic,1,num_h_l))
    m_6            = np.tile(harmonics_blade[None,None,None,:,None],(num_cpt,num_mic,num_sec,1,num_h_l))
    
    # loading harmonics
    k_5            = np.tile(harmonics_load[None,None,None,:],(num_cpt,num_mic,num_h_b,1))
    k_6            = np.tile(harmonics_load[None,None,None,None,:],(num_cpt,num_mic,num_sec,num_h_b,1))                                                                                        
    
    # reference atmospheric pressure
    p_ref          = 2E-5
        
    # net angle of inclination of propeller axis wrt inertial axis
    alpha_5        = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None],(1,num_mic,num_h_b,num_h_l))
    alpha_6        = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None],(1,num_mic,num_sec,num_h_b,num_h_l))
    
    # rotor angular speed
    omega_4        = np.tile(aeroacoustic_data.omega[:,:,None],(1,num_mic,num_h_b))
    
    R              = rotor.radius_distribution
    
    # Non-dimensional radius distribution
    z_6            = np.tile((R/R[-1])[None,None,:,None,None],(num_cpt,num_mic,1,num_h_b,num_h_l))
    
    R_tip          = rotor.tip_radius
    D              = 2*R[-1] 
    
    # Rotorcraft speed and mach number
    V_4            = np.tile(np.linalg.norm(velocity_vector, axis=1) [:,None,None],(1,num_mic,num_h_b))
    M_4            = V_4/a_4
    M_6            = np.tile(M_4[:,:,None,:,None],(1,1,num_sec,1,num_h_l))
    
    # Rotor tip speed and mach number
    V_tip          = R_tip*omega_4                                                        
    M_t_4          = V_tip/a_4
    M_t_6          = np.tile(M_t_4[:,:,None,:,None],(1,1,num_sec,1,num_h_l))
    
    # retarded theta
    theta_r        = coordinates.theta_hub_r[:,:,0,0]
    theta_r_4      = np.tile(theta_r[:,:,None],(1,1,num_h_b))
    theta_r_5      = np.tile(theta_r[:,:,None,None],(1,1,num_h_b,num_h_l))
    theta_r_6      = np.tile(theta_r[:,:,None,None,None],(1,1,num_sec,num_h_b,num_h_l))
    
    # retarded distance to source
    Y              = np.sqrt(coordinates.X_hub[:,:,0,0,1]**2 +  coordinates.X_hub[:,:,0,0,2] **2)
    Y_4            = np.tile(Y[:,:,None],(1,1,num_h_b))
    r_4            = Y_4/np.sin(theta_r_4)
    
    # phase angles
    phi_0_vec      = np.tile(phi_0[:,None,None,None],(num_cpt,num_mic,num_h_b,num_h_l))
    phi_5          = np.tile(coordinates.phi_hub_r[:,:,0,0,None,None],(1,1,num_h_b,num_h_l)) + phi_0_vec
    phi_6          = np.tile(phi_5[:,:,None,:,:],(1,1,num_sec,1,1))
    
    # total angle between propeller axis and r vector
    theta_r_prime_5 = np.arccos(np.cos(theta_r_5)*np.cos(alpha_5) + np.sin(theta_r_5)*np.sin(phi_5)*np.sin(alpha_5))
    theta_r_prime_6 = np.arccos(np.cos(theta_r_6)*np.cos(alpha_6) + np.sin(theta_r_6)*np.sin(phi_6)*np.sin(alpha_6))
    
    phi_prime_5    = np.arccos((np.sin(theta_r_5)*np.cos(phi_5))/np.sin(theta_r_prime_5))
    
    # wavenumbers
    k_m_4          = m_4*B*omega_4/a_4
    k_m_bar        = k_m_4/(1 - M_4*np.cos(theta_r_4))
    
    Noise.f          = B*omega_4*m_4/(2*np.pi)
    
    # Frequency domain loading modes
    F_x            = (1/R_tip)*aeroacoustic_data.disc_thrust_distribution
    R_temp         = np.tile(R[None,:,None],(num_cpt,1,num_az))
    F_phi          = (1/R_tip)*(1/R_temp)*aeroacoustic_data.disc_torque_distribution
    F_xk           = sp.fft.rfft(F_x, axis=2)
    F_phik         = sp.fft.rfft(F_phi, axis=2)
    F_xk_6         = np.tile(F_xk[:,None,:,None,0:num_h_l],(1,num_mic,1,num_h_b,1))
    F_phik_6       = np.tile(F_phik[:,None,:,None,0:num_h_l],(1,num_mic,1,num_h_b,1))
    
    # FREQUENCY DOMAIN PRESSURE TERM FOR LOADING
    J_mbk_6        = jv(m_6*B-k_6, (m_6*B*z_6*M_t_6*np.sin(theta_r_prime_6))/(1-M_6*np.cos(theta_r_6)))
    Term1_6        = ((m_6*B*z_6*M_t_6*np.cos(theta_r_prime_6))/(1-M_6*np.cos(theta_r_6)))*F_xk_6
    Term2_6        = -(m_6*B-k_6)*F_phik_6
    Integrand_6    = (1/z_6)*(Term1_6 + Term2_6)*J_mbk_6
    Summand_5      = np.trapz(Integrand_6, x=z_6[0,0,:,0,0], axis=2)*np.exp(1j*(m_5*B-k_5)*(phi_prime_5-(np.pi/2)))
    Summation_4    = np.sum(Summand_5, axis=3)
    P_Lm           = (1j*B*np.exp(1j*k_m_4*r_4)*Summation_4)/(4*np.pi*r_4*(1-M_4*np.cos(theta_r_4))) 
    
    # # frequency domain source function for thickness distribution
    # H              = airfoil_geometry.y_upper_surface - airfoil_geometry.y_lower_surface
    # H_tiled        = np.tile(H[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    # psi_V          = np.sum(H*exp_term*dX_tiled,axis=5) 

    # SOUND PRESSURE LEVELS
    P_Lm_abs       = np.abs(P_Lm)
    P_Vm_abs       = np.abs(P_Vm)
    Noise.SPL_prop_harmonic_bpf_spectrum     = 20*np.log10((abs(P_Lm_abs + P_Vm_abs))/p_ref)  
    Noise.SPL_prop_harmonic_1_3_spectrum     = convert_to_third_octave_band(Noise.SPL_prop_harmonic_bpf_spectrum,Noise.f[:,0,0,:],settings)          
    Noise.SPL_prop_harmonic_1_3_spectrum[np.isinf(Noise.SPL_prop_harmonic_1_3_spectrum)]         = 0     
    
    return 