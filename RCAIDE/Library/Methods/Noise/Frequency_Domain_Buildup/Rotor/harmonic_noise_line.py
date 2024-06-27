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
from RCAIDE.Library.Methods.Aerodynamics.Airfoil_Panel_Method.airfoil_analysis   import airfoil_analysis

# Python Package imports  
import numpy as np
from scipy.special import jv 
import scipy as sp

# ----------------------------------------------------------------------------------------------------------------------
# Compute Harmonic Noise 
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor 
def harmonic_noise_line(harmonics_blade,harmonics_load,freestream,angle_of_attack,coordinates,
                           velocity_vector,rotor,aeroacoustic_data,settings,res):
    '''This computes the harmonic noise (i.e. thickness and loading noise) in the frequency domain 
    of a rotor at any angle of attack with load distribution along the blade span. This is a level 1 fidelity
    approach. The thickness source is however computed using the helicoidal surface theory.

    Assumptions:
    Acoustic compactness of thrust and torque along blade chord.

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
    '''     
    num_h_b      = len(harmonics_blade)
    num_h_l      = len(harmonics_load)
    num_cpt      = len(angle_of_attack) 
    num_mic      = len(coordinates.X_hub[0,:,0,0,0,0])
    num_rot      = len(coordinates.X_hub[0,0,:,0,0,0]) 
    phi_0        = np.array([rotor.phase_offset_angle])  # phase angle offset  
    num_sec      = len(rotor.radius_distribution)
    airfoil_geometry = rotor.Airfoils.airfoil.geometry
    chord_coord  = len(airfoil_geometry.camber_coordinates)
    orientation  = np.array(rotor.orientation_euler_angles) * 1 
    body2thrust  = sp.spatial.transform.Rotation.from_rotvec(orientation).as_matrix()
    
    
    # NIRANJAN 

    Re    = aeroacoustic_data.blade_reynolds_number   # number of control points x number of sections          
    alpha = aeroacoustic_data.blade_effective_angle_of_attack # number of control points x number of sections             
    
    # NIRANJAN
    
    
    # we only need fL, fD, CL and CD in this method
    fL_pre  = np.zeros_like(Re)
    fL      = np.tile(fL_pre[:,:,None],(1,1,chord_coord))
    fD_pre  = np.zeros_like(Re)
    fD      = np.tile(fD_pre[:,:,None],(1,1,chord_coord))
    CL = np.zeros_like(Re)
    CD = np.zeros_like(Re)
    
    for cpt in range (num_cpt):
        for sec in range(num_sec):
            airfoil_properties = airfoil_analysis(airfoil_geometry,np.atleast_2d(alpha[cpt,sec]),np.atleast_2d(Re[cpt,sec]))
            fL[cpt,sec,:] = airfoil_properties.fL[:,0,0]
            fD[cpt,sec,:] = airfoil_properties.fD[:,0,0]
            CL[cpt,sec]   = airfoil_properties.cl_invisc
            CD[cpt,sec]   = airfoil_properties.cd_visc
    
    
    # ----------------------------------------------------------------------------------
    # Rotational Noise  Thickness and Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point, microphones, rotors, radial distribution, blade harmonics, load harmonics]  
    m              = np.tile(harmonics_blade[None,None,None,None,:,None],(num_cpt,num_mic,num_rot,num_sec,1,num_h_l))                 # harmonic number 
    m_1d           = harmonics_blade                                                                                         
    p_ref          = 2E-5                                                                                        # referece atmospheric pressure
    a              = np.tile(freestream.speed_of_sound[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))      # speed of sound
    rho            = np.tile(freestream.density[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))             # air density   
    alpha          = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))          
    B              = rotor.number_of_blades                                                                      # number of rotor blades
    omega          = np.tile(aeroacoustic_data.omega[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))        # angular velocity       
    omega          = np.tile(aeroacoustic_data.omega[:,:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b,num_h_l))
    
    # rs             = radial location of point load application
    # dT_dr          = np.tile(aeroacoustic_data.blade_dT_dr[:,None,None,:,None,None],(1,num_mic,num_rot,1,num_h_b,num_h_l))      # nondimensionalized differential thrust distribution 
    # dQ_dr          = np.tile(aeroacoustic_data.blade_dQ_dr[:,None,None,:,None],(1,num_mic,num_rot,1,num_h_b))      # nondimensionalized differential torque distribution
    R              = np.tile(rotor.radius_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h_b)) # radial location     
    c              = np.tile(rotor.chord_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h_b))  # blade chord    
    R_tip          = rotor.tip_radius                                                     
    t_c            = np.tile(rotor.thickness_to_chord[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h_b))  # thickness to chord ratio
    MCA            = np.tile(rotor.mid_chord_alignment[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h_b)) # Mid Chord Alighment  
    phi_0_vec      = np.tile(phi_0[None,None,:,None,None],(num_cpt,num_mic,1,num_sec,num_h_b))
    res.f          = B*omega*m/(2*np.pi) 
    D              = 2*R[0,0,0,-1,:]                                                                             # rotor diameter    
    r              = R/R[0,0,0,-1,:]                                                                             # non dimensional radius distribution   
    Y              = np.tile(np.sqrt(coordinates.X_hub[:,:,:,0,:,1]**2 +  coordinates.X_hub[:,:,:,0,:,2] **2)[:,:,:,:,None],(1,1,1,1,num_h_b))                        # observer distance from rotor axis          
    V              = np.tile(np.linalg.norm(velocity_vector,axis =1) [:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h_b))                                                     # velocity magnitude
    M_x            = V/a                                                                                         
    V_tip          = R_tip*omega                                                                                 # blade_tip_speed 
    M_t            = V_tip/a                                                                                     # tip Mach number 
    M_r            = np.sqrt(M_x**2 + (r**2)*(M_t**2))                                                           # section relative Mach number     
    B_D            = c/D
    
    CL_tiled       = np.tile(CL[:,None,None,:,None],(1,num_mic,num_rot,1,num_h_b))
    CD_tiled       = np.tile(CD[:,None,None,:,None],(1,num_mic,num_rot,1,num_h_b))
    fL_tiled       = np.tile(fL[:,None,None,:,None,:],(1,num_mic,num_rot,1,num_h_b,1))
    fD_tiled       = np.tile(fD[:,None,None,:,None,:],(1,num_mic,num_rot,1,num_h_b,1))    
     
    phi            = np.tile(coordinates.phi_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h_b)) + phi_0_vec 

    # retarted theta angle in the retarded reference frame
    theta_r        = np.tile(coordinates.theta_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h_b))  
    theta_r_prime  = np.arccos(np.cos(theta_r)*np.cos(alpha) + np.sin(theta_r)*np.sin(phi)*np.sin(alpha) )
    S_r            = np.tile(np.linalg.norm(coordinates.X_hub_r[:,:,:,0,:,:], axis = 4)[:,:,:,:,None],(1,1,1,1,num_h_b))  

    # initialize thickness and loading noise matrices
    psi_L          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h_b))
    psi_V          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h_b))
    
    # dimensionless wavenumbers
    k_x            = ((2*m*B*B_D*M_t)/(M_r*(1 - M_x*np.cos(theta_r))))
    k_y            = ((2*m*B*B_D)/r*M_r)*((M_r**2*np.cos(theta_r) - M_x)/(1 - M_x*np.cos(theta_r)))
    
    # frequency domain source function for drag and lift
    kx_tiled       = np.tile(k_x[:,:,:,:,:,None],(1,1,1,1,1,chord_coord))
    X_edge         = np.linspace(-0.5,0.5,chord_coord+1)
    dX             = np.diff(X_edge)
    dX_tiled       = np.tile(dX[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    X              = 0.5*(X_edge[0:-1] + X_edge[1:])
    X_tiled        = np.tile(X[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    exp_term       = np.exp(1j*kx_tiled*X_tiled)
    psi_L          = np.sum(fL*exp_term*dX_tiled,axis=5)
    psi_D          = np.sum(fD*exp_term*dX_tiled,axis=5)
    
    # frequency domain source function for thickness distribution
    H              = airfoil_geometry.y_upper_surface - airfoil_geometry.y_lower_surface
    H_tiled        = np.tile(H[None,None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,num_h_b,1))
    psi_V          = np.sum(H*exp_term*dX_tiled,axis=5)