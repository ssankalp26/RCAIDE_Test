# nonuniform_propeller_inflow.py

import RCAIDE 
from RCAIDE.Framework.Core import Units, Data 
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Rotor         import design_propeller  
from RCAIDE.Framework.Networks.All_Electric_Network                    import All_Electric_Network
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Rotor         import design_propeller   
from RCAIDE.Library.Methods.Aerodynamics.Common.Lift.compute_wing_wake import compute_wing_wake
from RCAIDE.Library.Methods.Aerodynamics.Common.Lift.compute_propeller_nonuniform_freestream import compute_propeller_nonuniform_freestream  
from RCAIDE.Library.Plots import * 

import os 
import numpy as np
import pylab as plt
 

def main():
    '''
    This example shows a propeller operating in three cases of nonuniform freestream flow:
    First, a propeller operates at a nonzero thrust angle relative to the freestream.
    Second, a propeller operates with an arbitrary upstream disturbance.
    Third, a propeller operates in the wake of an upstream wing

    '''
    # setup a simple vehicle
    vehicle = vehicle_setup(Na=24, Nr=101)

    # setup the atmospheric conditions
    conditions = test_conditions()
    
    #-------------------------------------------------------------
    # test propeller at inclined thrust angle
    #-------------------------------------------------------------
    case_1(vehicle, conditions)
    
    
    #-------------------------------------------------------------
    # test propeller in arbitrary nonuniform freestream disturbance
    #-------------------------------------------------------------     
    case_2(vehicle, conditions)
    
    
    #-------------------------------------------------------------
    # This example shows a propeller operating in a nonuniform freestream flow.
    # A wing in front of the propeller produces a wake, which is accounted for in the propeller analysis.
    #------------------------------------------------------------- 
    #case_3(vehicle, conditions) 

    return

#-------------------------------------------------------------
# Case 1 
#-------------------------------------------------------------
def case_1(vehicle, conditions):
    # set operating conditions for propeller test
    prop                           = vehicle.networks.all_electric.busses.bus.propulsors.starboard_propulsor.rotor
    prop.inputs.omega              = np.ones_like(conditions.aerodynamics.angles.alpha)*prop.cruise.design_angular_velocity
    prop.orientation_euler_angles  = [0.,20.*Units.degrees,0]
    prop.use_2d_analysis           = True
    
    # spin propeller in nonuniform flow
    thrust, torque, power, Cp, outputs , etap = prop.spin(conditions)

    # plot velocities at propeller plane and resulting performance
    plot_rotor_disc_performance(prop,outputs,title='Case 1: Operating at Thrust Angle')
    
    thrust   = np.linalg.norm(thrust)
    thrust_r = 1743.0258191335301
    torque_r = 748.87304348
    power_r  = 101948.342247
    Cp_r     = 0.46942838
    etap_r   = 0.71821729
    print('\nCase 1 Errors: \n')
    print('Thrust difference = ', np.abs(thrust - thrust_r) / thrust_r )
    print('Torque difference = ', np.abs(torque - torque_r) / torque_r )
    print('Power difference = ', np.abs(power - power_r) / power_r )
    print('Cp difference = ', np.abs(Cp - Cp_r) / Cp_r )
    print('Etap difference = ', np.abs(etap - etap_r) / etap_r )
    assert (np.abs(thrust - thrust_r) / thrust_r < 1e-6), "Nonuniform Propeller Thrust Angle Regression Failed at Thrust Test"
    assert (np.abs(torque - torque_r) / torque_r < 1e-6), "Nonuniform Propeller Thrust Angle Regression Failed at Torque Test"
    assert (np.abs(power - power_r) / power_r < 1e-6), "Nonuniform Propeller Thrust Angle Regression Failed at Power Test"
    assert (np.abs(Cp - Cp_r) / Cp_r < 1e-6), "Nonuniform Propeller Thrust Angle Regression Failed at Power Coefficient Test"
    assert (np.abs(etap - etap_r) / etap_r < 1e-6), "Nonuniform Propeller Thrust Angle Regression Failed at Efficiency Test"

    return

#-------------------------------------------------------------
# Case 2
#-------------------------------------------------------------
def case_2(vehicle,conditions, Na=24, Nr=101):
    prop                           = vehicle.networks.all_electric.busses.bus.propulsors.starboard_propulsor.rotor
    prop.nonuniform_freestream     = True
    prop.orientation_euler_angles  = [0,0,0]
    prop.inputs.omega              = np.ones_like(conditions.aerodynamics.angles.alpha)*prop.cruise.design_angular_velocity
    ctrl_pts                       = len(conditions.aerodynamics.angles.alpha)

    # azimuthal distribution
    psi            = np.linspace(0,2*np.pi,Na+1)[:-1]
    psi_2d         = np.tile(np.atleast_2d(psi),(Nr,1))
    psi_2d         = np.repeat(psi_2d[None,:,:], ctrl_pts, axis=0)

    # set an arbitrary nonuniform freestream disturbance
    va = (1+psi_2d) * 1.1
    vt = (1+psi_2d) * 2.0
    vr = (1+psi_2d) * 0.9

    prop.tangential_velocities_2d = vt
    prop.axial_velocities_2d      = va
    prop.radial_velocities_2d     = vr

    # spin propeller in nonuniform flow
    thrust, torque, power, Cp, outputs , etap = prop.spin(conditions)

    # plot velocities at propeller plane and resulting performance
    plot_rotor_disc_performance(prop,outputs,title='Case 2: Arbitrary Freestream')

    # expected results
    thrust   = np.linalg.norm(thrust)
    thrust_r = 1150.8011515854673
    torque_r = 568.67821527
    power_r  = 77417.3964781
    Cp_r     = 0.3564739
    etap_r   = 0.66452008
    print('\nCase 2 Errors: \n')
    print('Thrust difference = ', np.abs(thrust - thrust_r) / thrust_r )
    print('Torque difference = ', np.abs(torque - torque_r) / torque_r )
    print('Power difference = ', np.abs(power - power_r) / power_r )
    print('Cp difference = ', np.abs(Cp - Cp_r) / Cp_r )
    print('Etap difference = ', np.abs(etap - etap_r) / etap_r )
    assert (np.abs(thrust - thrust_r) / thrust_r < 1e-6), "Nonuniform Propeller Inflow Regression Failed at Thrust Test"
    assert (np.abs(torque - torque_r) / torque_r < 1e-6), "Nonuniform Propeller Inflow Regression Failed at Torque Test"
    assert (np.abs(power - power_r) / power_r < 1e-6), "Nonuniform Propeller Inflow Regression Failed at Power Test"
    assert (np.abs(Cp - Cp_r) / Cp_r < 1e-6), "Nonuniform Propeller Inflow Regression Failed at Power Coefficient Test"
    assert (np.abs(etap - etap_r) / etap_r < 1e-6), "Nonuniform Propeller Inflow Regression Failed at Efficiency Test"

    return
 
#-------------------------------------------------------------
# Case 3
#-------------------------------------------------------------
def case_3(vehicle,conditions): 
    # set plot flag
    plot_flag = True


    # grid and VLM settings
    grid_settings, VLM_settings = simulation_settings(vehicle)

    #--------------------------------------------------------------------------------------
    # Part 1. Compute the velocities induced by the wing at the propeller plane downstream
    #--------------------------------------------------------------------------------------
    propeller     = vehicle.networks.all_electric.busses.bus.propulsors.starboard_propulsor.rotor
    prop_loc      = propeller.origin
    prop_x_center = np.array([vehicle.wings.main_wing.origin[0][0] + prop_loc[0][0]])
    wing_wake, _  = compute_wing_wake(vehicle,conditions,prop_x_center[0], grid_settings, VLM_settings, plot_grid=plot_flag, plot_wake=plot_flag)
 
    #--------------------------------------------------------------------------------------
    # Part 2. Compute and run the propeller in this nonuniform flow
    #--------------------------------------------------------------------------------------
    prop                       = compute_propeller_nonuniform_freestream(propeller, wing_wake,conditions)
    prop.nonuniform_freestream = True
    thrust, torque, power, Cp, outputs , etap = prop.spin(conditions)

    thrust   = np.linalg.norm(thrust)
    thrust_r, torque_r, power_r, Cp_r, etap_r = 1670.646434565442, 742.03162704, 101016.98135661, 0.46513986, 0.73932696
    print('\nCase 3 Errors: \n')
    print('Thrust difference = ', np.abs(thrust - thrust_r) / thrust_r )
    print('Torque difference = ', np.abs(torque - torque_r) / torque_r )
    print('Power difference = ', np.abs(power - power_r) / power_r )
    print('Cp difference = ', np.abs(Cp - Cp_r) / Cp_r )
    print('Etap difference = ', np.abs(etap - etap_r) / etap_r )
    assert (np.abs(thrust - thrust_r) / thrust_r < 1e-5), "Nonuniform Propeller Inflow Regression Failed at Thrust Test"
    assert (np.abs(torque - torque_r) / torque_r < 1e-5), "Nonuniform Propeller Inflow Regression Failed at Torque Test"
    assert (np.abs(power - power_r) / power_r < 1e-5), "Nonuniform Propeller Inflow Regression Failed at Power Test"
    assert (np.abs(Cp - Cp_r) / Cp_r < 1e-5), "Nonuniform Propeller Inflow Regression Failed at Power Coefficient Test"
    assert (np.abs(etap - etap_r) / etap_r < 1e-5), "Nonuniform Propeller Inflow Regression Failed at Efficiency Test"

    # Plot results
    if plot_flag:
        plot_rotor_disc_performance(prop,outputs, title='Case 3: Pusher Propeller')

    return

def test_conditions():
    # --------------------------------------------------------------------------------------------------
    # Atmosphere Conditions:
    # --------------------------------------------------------------------------------------------------
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data  = atmosphere.compute_values(altitude=14000 * Units.ft)
    rho        = atmo_data.density
    mu         = atmo_data.dynamic_viscosity
    T          = atmo_data.temperature
    a          = atmo_data.speed_of_sound 

    # aerodynamics analyzed for a fixed angle of attack
    aoa   = np.array([[ 3 * Units.deg  ]])
    Vv    = np.array([[ 100 * Units.mph]])
    ones  = np.ones_like(aoa)

    mach  = Vv/a

    conditions                              = RCAIDE.Framework.Mission.Common.Results()
    conditions.freestream.density           = rho* ones
    conditions.freestream.dynamic_viscosity = mu* ones
    conditions.freestream.speed_of_sound    = a* ones
    conditions.freestream.temperature       = T* ones
    conditions.freestream.mach_number       = mach* ones
    conditions.freestream.velocity          = Vv * ones
    conditions.aerodynamics.angles.alpha    = aoa
    conditions.frames.body.transform_to_inertial = np.array( [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]] ) 
    velocity_vector = np.zeros([len(aoa), 3])
    velocity_vector[:, 0] = Vv
    conditions.frames.inertial.velocity_vector = velocity_vector 

    return conditions



def vehicle_setup(Na, Nr): 
    
    #-----------------------------------------------------------------
    #   Vehicle Initialization:
    #-----------------------------------------------------------------
    vehicle = RCAIDE.Vehicle()
    vehicle.tag = 'simple_vehicle'

    # ------------------------------------------------------------------
    #   Wing Properties
    # ------------------------------------------------------------------  
    wing = RCAIDE.Library.Components.Wings.Wing()
    wing.tag = 'main_wing'

    wing.spans.projected         = 9.6
    wing.chords.root             = 0.7
    wing.chords.tip              = 0.3
    wing.areas.reference         = wing.spans.projected*(wing.chords.root+wing.chords.tip)/2
    vehicle.reference_area       = wing.areas.reference
    wing.aspect_ratio            = wing.spans.projected**2/wing.areas.reference
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees
    wing.sweeps.leading_edge     = 0.0
    wing.dihedral                = 0.0 * Units.degrees
    wing.span_efficiency         = 0.8
    wing.origin                  = np.array([[0.,0.,0.]])
    wing.vertical                = False
    wing.symmetric               = True

    vehicle.append_component(wing)

    # ########################################################  Energy Network  #########################################################  
    net                              = All_Electric_Network()    
    bus                              = RCAIDE.Library.Components.Energy.Distribution.Electrical_Bus() 
  
    #------------------------------------------------------------------------------------------------------------------------------------  
    #  Starboard Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------   
    starboard_propulsor                    = RCAIDE.Library.Components.Propulsors.Electric_Rotor()  
    starboard_propulsor.tag                = 'starboard_propulsor'  
   
    # Propeller
    prop                                   = RCAIDE.Library.Components.Propulsors.Converters.Propeller() 
    prop.number_of_blades                  = 2
    prop.tip_radius                        = 38.    * Units.inches
    prop.hub_radius                        = 8.     * Units.inches
    prop.cruise.design_freestream_velocity = 135.   * Units['mph']
    prop.cruise.design_angular_velocity    = 1300.  * Units.rpm
    prop.cruise.design_Cl                  = 0.8
    prop.cruise.design_altitude            = 12000. * Units.feet
    prop.cruise.design_thrust              = 1200.
    prop.origin                            = [[0.,0.,0.]]
    prop.number_azimuthal_stations         = Na
    prop.rotation                          = 1
    prop.symmetry                          = True 
    airfoil                                = RCAIDE.Library.Components.Airfoils.Airfoil()
    airfoil.tag                            = 'NACA_4412' 
    separator                             = os.path.sep 
    airfoil.coordinate_file                 =  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'NACA_4412.txt'   # absolute path   
    airfoil.polar_files                     = [ '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_50000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_100000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_200000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_500000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_1000000.txt']   
     
    prop.append_airfoil(airfoil)      
 
    
    prop.airfoil_polar_stations    = list(np.zeros(Nr).astype(int))
    prop                           = design_propeller(prop,Nr)    
    starboard_propulsor.rotor      = prop 
    
    # append propulsor to distribution line 
    bus.propulsors.append(starboard_propulsor) 
    
    # append bus   
    net.busses.append(bus)
    
    vehicle.append_energy_network(net)

    return vehicle
  

def simulation_settings(vehicle):

    grid_settings                                = Data()
    grid_settings.height                         = 12*vehicle.networks.all_electric.busses.bus.propulsors.starboard_propulsor.rotor.tip_radius / vehicle.wings.main_wing.spans.projected
    grid_settings.length                         = 1.2
    grid_settings.height_fine                    = 0.2 
    VLM_settings                                 = RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM().settings
    VLM_settings.number_spanwise_vortices        = 16
    VLM_settings.number_chordwise_vortices       = 4
    VLM_settings.use_surrogate                   = True
    VLM_settings.propeller_wake_model            = False
    VLM_settings.model_fuselage                  = False 
    VLM_settings.spanwise_cosine_spacing         = True
    VLM_settings.leading_edge_suction_multiplier = 1.

    return grid_settings, VLM_settings

if __name__ == '__main__':
    main()
    plt.show()
