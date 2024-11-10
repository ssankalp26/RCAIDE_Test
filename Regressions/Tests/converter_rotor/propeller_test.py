# propeller_test.py 
#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units,  Data
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Rotor import design_propeller , design_lift_rotor
from RCAIDE.Library.Plots import *

import matplotlib.pyplot as plt   
import os 
import numpy as np
import copy, time

def main():
    
    # This script could fail if either the design or analysis scripts fail,
    # in case of failure check both. The design and analysis powers will 
    # differ because of karman-tsien compressibility corrections in the 
    # analysis scripts
    
    ospath                                = os.path.abspath(__file__)
    separator                             = os.path.sep 
   
    #------------------------------------------------------------------------------------------------------------------------------------ 
    # Design Gearbox 
    #------------------------------------------------------------------------------------------------------------------------------------ 
    gearbox                   = RCAIDE.Library.Components.Propulsors.Converters.Gearbox()
    gearbox.gearwheel_radius1 = 1
    gearbox.gearwheel_radius2 = 1
    gearbox.efficiency        = 0.95
    gearbox.inputs.torque     = 885.550158704757
    gearbox.inputs.speed      = 207.16160479940007
    gearbox.inputs.power      = 183451.9920076409
    gearbox.compute()

    #------------------------------------------------------------------------------------------------------------------------------------
    # Poorly design propeller
    #------------------------------------------------------------------------------------------------------------------------------------     
    bad_prop                                   = RCAIDE.Library.Components.Propulsors.Converters.Propeller() 
    bad_prop.tag                               = "Prop_W_Aifoil"
    bad_prop.number_of_blades                  = 2 
    bad_prop.tip_radius                        = 0.3
    bad_prop.hub_radius                        = 0.21336 
    bad_prop.cruise.design_freestream_velocity = 1
    bad_prop.cruise.design_tip_mach            = 0.1
    bad_prop.cruise.design_thrust              = 100000
    bad_prop.cruise.design_angular_velocity    = gearbox.inputs.speed  
    bad_prop.cruise.design_Cl                  = 0.7
    bad_prop.cruise.design_altitude            = 1. * Units.km
    
    # define airfoil 
    airfoil                                    = RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil()
    airfoil.tag                                = 'NACA_4412' 
    airfoil.NACA_4_Series_code                 = '4412'    
    bad_prop.append_airfoil(airfoil) # assign airfoil to rotor 
    
    # define polar stations on rotor 
    bad_prop.airfoil_polar_stations            =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    # design propeler 
    bad_prop                                   = design_propeller(bad_prop)
    
    #------------------------------------------------------------------------------------------------------------------------------------
    # Propeller with airfoil cross sections defined 
    #------------------------------------------------------------------------------------------------------------------------------------     
     
    prop_a                                    = RCAIDE.Library.Components.Propulsors.Converters.Propeller()
    prop_a.tag                                = "Prop_W_Aifoil"
    prop_a.number_of_blades                   = 3 
    prop_a.tip_radius                         = 1.0668
    prop_a.hub_radius                         = 0.21336
    prop_a.cruise.design_tip_mach             = 0.65
    prop_a.cruise.design_freestream_velocity  = 49.1744
    prop_a.cruise.design_angular_velocity     = gearbox.inputs.speed # 207.16160479940007
    prop_a.cruise.design_Cl                   = 0.7
    prop_a.cruise.design_thrust               = 3054.4809132125697
    prop_a.cruise.design_altitude             = 1. * Units.km 
    
    # define first airfoil 
    airfoil_1                                 = RCAIDE.Library.Components.Airfoils.Airfoil()
    airfoil_1.tag                             = 'NACA_4412'  
    airfoil_1.coordinate_file                  =  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'NACA_4412.txt'   # absolute path   
    airfoil_1.polar_files                      =[ '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_50000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_100000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_200000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_500000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_1000000.txt']   
    prop_a.append_airfoil(airfoil_1)     
             
    # define  second airfoil          
    airfoil_2                                 = RCAIDE.Library.Components.Airfoils.Airfoil()
    airfoil_2.tag                             = 'Clark_Y' 
    airfoil_2.coordinate_file                 =   '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Clark_y.txt' 
    airfoil_2.polar_files                     = [ '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'Clark_y_polar_Re_50000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'Clark_y_polar_Re_100000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'Clark_y_polar_Re_200000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'Clark_y_polar_Re_500000.txt',
                                                  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'Clark_y_polar_Re_1000000.txt'] 
    prop_a.append_airfoil(airfoil_2)  # append second airfoil 
             
    # define polar stations on rotor          
    prop_a.airfoil_polar_stations             = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1]
             
    # design propeler          
    prop_a                                    = design_propeller(prop_a)
    
    # plot propeller 
    plot_3d_rotor(prop_a)

    #------------------------------------------------------------------------------------------------------------------------------------   
    # Define propeller without airfoils defined 
    #------------------------------------------------------------------------------------------------------------------------------------  
    prop                                    = RCAIDE.Library.Components.Propulsors.Converters.Propeller()
    prop.tag                                = "Prop_No_Aifoil"
    prop.number_of_blades                   = 3 
    prop.tip_radius                         = 1.0668
    prop.hub_radius                         = 0.21336
    prop.cruise.design_tip_mach             = 0.65
    prop.cruise.design_freestream_velocity  = 49.1744
    prop.cruise.design_angular_velocity     = gearbox.inputs.speed
    prop.cruise.design_Cl                   = 0.7
    prop.cruise.design_altitude             = 1. * Units.km 
    prop.cruise.design_power                = gearbox.outputs.power
    prop                                    = design_propeller(prop)

    #------------------------------------------------------------------------------------------------------------------------------------      
    # Rotor with airfoil cross sections defined 
    #------------------------------------------------------------------------------------------------------------------------------------  
    rot_a                                   = RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor() 
    rot_a.tag                               = "Rot_W_Aifoil"
    rot_a.tip_radius                        = 2.8 * Units.feet
    rot_a.hub_radius                        = 0.35 * Units.feet      
    rot_a.number_of_blades                  = 2    
    rot_a.hover.design_freestream_velocity  = 500. * Units['ft/min']  
    rot_a.hover.design_angular_velocity     = 258.9520059992501
    rot_a.hover.design_tip_mach             = 0.65 
    rot_a.hover.design_Cl                   = 0.7
    rot_a.hover.design_altitude             = 20 * Units.feet                            
    rot_a.hover.design_thrust               = 2271.2220451593753
    
    airfoil                                 = RCAIDE.Library.Components.Airfoils.Airfoil()
    airfoil.tag                             = 'NACA_4412'  
    airfoil.coordinate_file                 =  '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'NACA_4412.txt'   # absolute path   
    airfoil.polar_files                     = [ '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_50000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_100000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_200000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_500000.txt',
                                                 '..' + separator + '..' + separator + 'Vehicles' + separator  + 'Airfoils' + separator  + 'Polars' + separator  + 'NACA_4412_polar_Re_1000000.txt']   
        
    rot_a.append_airfoil(airfoil)           
    rot_a.airfoil_polar_stations            = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    rot_a                                   = design_lift_rotor(rot_a) 

    #------------------------------------------------------------------------------------------------------------------------------------      
    #  Rotor without airfoils defined 
    #------------------------------------------------------------------------------------------------------------------------------------  
    rot                                     = RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor()
    rot.tag                                 = "Rot_No_Aifoil"
    rot.tip_radius                          = 2.8 * Units.feet
    rot.hub_radius                          = 0.35 * Units.feet
    rot.number_of_blades                    = 2
    rot.hover.design_tip_mach               = 0.65 
    rot.hover.design_freestream_velocity    = 500. * Units['ft/min']
    rot.hover.design_angular_velocity       = 258.9520059992501
    rot.hover.design_Cl                     = 0.7
    rot.hover.design_altitude               = 20 * Units.feet
    rot.hover.design_thrust                 = 2271.2220451593753
    rot                                     = design_lift_rotor(rot)  

    #------------------------------------------------------------------------------------------------------------------------------------      
    # Find the operating conditions
    #------------------------------------------------------------------------------------------------------------------------------------  
    atmosphere                                          = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere_conditions                               = atmosphere.compute_values(rot.hover.design_altitude)
    
    # cruise simulation                      
    V                                                   = prop.cruise.design_freestream_velocity 
    conditions                                          = RCAIDE.Framework.Mission.Common.Results()
    conditions._size                                    = 1
    conditions.freestream                               = Data()
    conditions.propulsion                               = Data()
    conditions.frames                                   = Data()
    conditions.frames.body                              = Data()
    conditions.frames.inertial                          = Data()
    conditions.freestream.update(atmosphere_conditions)
    conditions.freestream.dynamic_viscosity             = atmosphere_conditions.dynamic_viscosity
    conditions.frames.inertial.velocity_vector          = np.array([[V,0,0]])
    #conditions.propulsion.throttle                      = np.array([[1.0]])
    conditions.frames.body.transform_to_inertial        = np.array([np.eye(3)])
    conditions.frames.inertial.velocity_vector          = np.array([[V,0,0]])
    
    # hover simulation 
    conditions_r                                        = copy.deepcopy(conditions)
    Vr                                                  = rot.hover.design_freestream_velocity
    conditions_r.frames.inertial.velocity_vector        = np.array([[0,Vr,0]])
    
    # Create and attach this propeller 
    prop_a.inputs.omega  = np.array(prop_a.cruise.design_angular_velocity,ndmin=2)
    prop.inputs.omega    = np.array(prop.cruise.design_angular_velocity,ndmin=2)
    rot_a.inputs.omega   = np.array(rot_a.hover.design_angular_velocity,ndmin=2)
    rot.inputs.omega     = np.array(rot.hover.design_angular_velocity,ndmin=2)
    
    # propeller with airfoil results 
    prop_a.inputs.pitch_command                = 0.0*Units.degree
    F_a, Q_a, P_a, Cplast_a ,output_a , etap_a = prop_a.spin(conditions)  
    plot_results(output_a, prop_a,'blue','-','s')
    
    # propeller without airfoil results 
    prop.inputs.pitch_command           = 0.0*Units.degree
    F, Q, P, Cplast ,output , etap      = prop.spin(conditions)
    plot_results(output, prop,'red','-','o')
    
    # rotor with airfoil results 
    rot_a.inputs.pitch_command                     = 0.0*Units.degree
    Fr_a, Qr_a, Pr_a, Cplastr_a ,outputr_a , etapr = rot_a.spin(conditions_r)
    plot_results(outputr_a, rot_a,'green','-','^')
    
    # rotor with out airfoil results 
    rot.inputs.pitch_command              = 0.0*Units.degree
    Fr, Qr, Pr, Cplastr ,outputr , etapr  = rot.spin(conditions_r)
    plot_results(outputr, rot,'black','-','P')
    
    # Truth values for propeller with airfoil geometry defined 
    F_a_truth       = 3352.366469630676
    Q_a_truth       = 978.76113592
    P_a_truth       = 202761.72763161
    Cplast_a_truth  = 0.10450832
    
    # Truth values for propeller without airfoil geometry defined 
    F_truth         = 2682.883049614873
    Q_truth         = 804.66619031
    P_truth         = 166695.93931239
    Cplast_truth    = 0.08591914
     
    # Truth values for rotor with airfoil geometry defined 
    Fr_a_truth      = 2377.550472426044
    Qr_a_truth      = 209.67792589498526
    Pr_a_truth      = 58519.71135540301
    Cplastr_a_truth = 0.03764406668156589
    
    # Truth values for rotor without airfoil geometry defined 
    Fr_truth        = 2220.190067202391
    Qr_truth        = 225.69853847211746
    Pr_truth        = 62990.95752854608
    Cplastr_truth   = 0.04052029223348749
    
    # Store errors 
    error = Data()
    error.Thrust_a  = np.max(np.abs(np.linalg.norm(F_a) -F_a_truth))
    error.Torque_a  = np.max(np.abs(Q_a -Q_a_truth))    
    error.Power_a   = np.max(np.abs(P_a -P_a_truth))
    error.Cp_a      = np.max(np.abs(Cplast_a -Cplast_a_truth))  
    error.Thrust    = np.max(np.abs(np.linalg.norm(F)-F_truth))
    error.Torque    = np.max(np.abs(Q-Q_truth))    
    error.Power     = np.max(np.abs(P-P_truth))
    error.Cp        = np.max(np.abs(Cplast-Cplast_truth))  
    error.Thrustr_a = np.max(np.abs(np.linalg.norm(Fr_a)-Fr_a_truth))
    error.Torquer_a = np.max(np.abs(Qr_a-Qr_a_truth))    
    error.Powerr_a  = np.max(np.abs(Pr_a-Pr_a_truth))
    error.Cpr_a     = np.max(np.abs(Cplastr_a-Cplastr_a_truth))  
    error.Thrustr   = np.max(np.abs(np.linalg.norm(Fr)-Fr_truth))
    error.Torquer   = np.max(np.abs(Qr-Qr_truth))    
    error.Powerr    = np.max(np.abs(Pr-Pr_truth))
    error.Cpr       = np.max(np.abs(Cplastr-Cplastr_truth))     
    
    print('Errors:')
    print(error)
    
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)

    return

def plot_results(results,prop,c,ls,m):
    
    tag                = prop.tag
    va_ind             = results.blade_axial_induced_velocity[0]  
    vt_ind             = results.blade_tangential_induced_velocity[0]  
    r                  = prop.radius_distribution
    T_distribution     = results.blade_thrust_distribution[0] 
    vt                 = results.blade_tangential_velocity[0]  
    va                 = results.blade_axial_velocity[0] 
    Q_distribution     = results.blade_torque_distribution[0] 
        
    # ----------------------------------------------------------------------------
    # 2D - Plots  Plots    
    # ---------------------------------------------------------------------------- 
    # perpendicular velocity, up Plot 
    fig = plt.figure('va_ind')         
    plt.plot(r  , va_ind ,color = c  , marker = m, linestyle = ls , label =  tag)          
    plt.xlabel('Radial Location')
    plt.ylabel('Induced Axial Velocity') 
    plt.legend(loc='lower right') 
    
    fig = plt.figure('vt_ind')          
    plt.plot(r  , vt_ind ,color = c ,marker = m, linestyle = ls , label =  tag )       
    plt.xlabel('Radial Location')
    plt.ylabel('Induced Tangential Velocity') 
    plt.legend(loc='lower right')  
        
    fig = plt.figure('T')     
    plt.plot(r , T_distribution ,color = c ,marker = m, linestyle = ls, label =  tag  )    
    plt.xlabel('Radial Location')
    plt.ylabel('Trust, N')
    plt.legend(loc='lower right')
    
    fig = plt.figure('Q')
    plt.plot(r , Q_distribution ,color = c ,marker = m, linestyle = ls, label =  tag)            
    plt.xlabel('Radial Location')
    plt.ylabel('Torque, N-m')
    plt.legend(loc='lower right')
    
    fig = plt.figure('Va')     
    plt.plot(r , va ,color = c  ,marker =m, linestyle = ls, label =  tag + ': Axial vel')          
    plt.xlabel('Radial Location')
    plt.ylabel('Axial Velocity') 
    plt.legend(loc='lower right') 
    
    fig = plt.figure('Vt')       
    plt.plot(r , vt ,color = c ,marker = m, linestyle = ls, label =  tag )         
    plt.xlabel('Radial Location')
    plt.ylabel('Tangential Velocity') 
    plt.legend(loc='lower right')  
    
    return 

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    plt.show()