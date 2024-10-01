# RCAIDE/Methods/Weights/Buildups/eVTOL/compute_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
import RCAIDE
from RCAIDE.Framework.Core                                          import Units, Data 
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_fuselage_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_boom_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_rotor_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_wiring_weight
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Common   import compute_wing_weight

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle, miscelleneous_weight_factor   = 1.1): 
    """ Calculates the empty vehicle mass for an EVTOL-type aircraft including seats,
        avionics, servomotors, ballistic recovery system, rotor and hub assembly,
        transmission, and landing gear. 
        
        Sources:
        Project Vahana Conceptual Trade Study
        https://github.com/VahanaOpenSource


        Inputs: 
            vehicle:                     RCAIDE Config Data Stucture 
            max_tip_mach:               Allowable Tip Mach Number                      [Unitless]
            disk_area_factor:           Inverse of Disk Area Efficiency                [Unitless]
            max_thrust_to_weight_ratio: Allowable Thrust to Weight Ratio               [Unitless]
            safety_factor               Safety Factor in vehicle design                [Unitless]
            max_g_load                  Maximum g-forces load for certification        [UNitless]
            motor_efficiency:           Motor Efficiency                               [Unitless]

        Outputs: 
            outputs:                    Data Dictionary of Component Masses [kg]

        Output data dictionary has the following book-keeping hierarchical structure:

            Output
                Total.
                    Empty.
                        Structural.
                            Fuselage
                            Wings
                            Landing Gear
                            Rotors
                            Hubs
                        Seats
                        Battery
                        Motors
                        Servo
                    Systems.
                        Avionics
                        ECS               - Environmental Control System
                        BRS               - Ballistic Recovery System
                        Wiring            - Aircraft Electronic Wiring
                    Payload

    """

    # Set up data structures for RCAIDE weight methods
    weight                   = Data()  
    weight.battery           = 0.0
    weight.payload           = 0.0
    weight.servos            = 0.0
    weight.hubs              = 0.0
    weight.booms             = 0.0
    weight.BRS               = 0.0  
    weight.motors            = 0.0
    weight.rotors            = 0.0
    weight.rotors            = 0.0
    weight.fuselage          = 0.0
    weight.wiring            = 0.0
    weight.wings             = Data()
    weight.wings_total       = 0.0

    vehicle.payload.passengers  = RCAIDE.Library.Components.Component()
    vehicle.payload.baggage     = RCAIDE.Library.Components.Component()
    vehicle.payload.cargo       = RCAIDE.Library.Components.Component()
    control_systems             = RCAIDE.Library.Components.Component()
    electrical_systems          = RCAIDE.Library.Components.Component()
    furnishings                 = RCAIDE.Library.Components.Component()
    air_conditioner             = RCAIDE.Library.Components.Component()
    fuel                        = RCAIDE.Library.Components.Component()
    apu                         = RCAIDE.Library.Components.Component()
    hydraulics                  = RCAIDE.Library.Components.Component()
    avionics                    = RCAIDE.Library.Components.Systems.Avionics()
    optionals                   = RCAIDE.Library.Components.Component()

    # assign components to vehicle
    vehicle.systems.control_systems    = control_systems
    vehicle.systems.electrical_systems = electrical_systems
    vehicle.systems.avionics           = avionics
    vehicle.systems.furnishings        = furnishings
    vehicle.systems.air_conditioner    = air_conditioner
    vehicle.systems.fuel               = fuel
    vehicle.systems.apu                = apu
    vehicle.systems.hydraulics         = hydraulics
    vehicle.systems.optionals          = optionals 

    #-------------------------------------------------------------------------------
    # Default Values
    #------------------------------------------------------------------------------- 
    MTOW                          = vehicle.mass_properties.max_takeoff
    atmosphere                    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976() 
    atmo_data                     = atmosphere.compute_values(0, 0) 
    safety_factor                 = 1.5   
    disk_area_factor              = 1.15     
    max_thrust_to_weight_ratio    = 1.1
    max_g_load                    = 3.8
    rho_ref                       = atmo_data.density 
    maxLift                       = MTOW * max_thrust_to_weight_ratio * 9.81           
    AvgBladeCD                    = 0.012         

    #-------------------------------------------------------------------------------
    # Fixed Weights
    #-------------------------------------------------------------------------------
    weight.seats        = vehicle.passengers * 15.   * Units.kg
    weight.passengers   = vehicle.passengers * 70.   * Units.kg
    weight.avionics     = 15.                        * Units.kg
    weight.landing_gear = MTOW * 0.02                * Units.kg
    weight.ECS          = vehicle.passengers * 7.    * Units.kg

    # Determine length scale 
    length_scale = 1.  
    if len(vehicle.fuselages) == 0.:
        for wing in vehicle.wings:
            if isinstance(wing ,RCAIDE.Library.Components.Wings.Main_Wing): 
                if wing.chords.root>length_scale:
                    length_scale = wing.chords.root
                    nose_length  = 0.25*wing.chords.root
    else:
        for fuse in vehicle.fuselages:
            nose   = fuse.lengths.nose
            length = fuse.lengths.total
            if length > length_scale:
                length_scale = length
                nose_length  = nose 
                            
    #-------------------------------------------------------------------------------
    # Environmental Control System
    #-------------------------------------------------------------------------------
    vehicle.systems.air_conditioner.origin[0][0]          = 0.51 * length_scale
    vehicle.systems.air_conditioner.mass_properties.mass  = weight.ECS

    #-------------------------------------------------------------------------------
    # Network Weight
    #-------------------------------------------------------------------------------
    maxLiftPower           = 0
    total_number_of_rotors = 0 
    for network in vehicle.networks: 
        for bus in network.busses:  
            #------------------------------------------------------------------------------- 
            # Payload Weight
            #-------------------------------------------------------------------------------
            if bus.payload.origin[0][0] == 0:
                bus.payload.origin[0][0]  = 0.5 * length_scale
            weight.payload  += bus.payload.mass_properties.mass * Units.kg
     
            #-------------------------------------------------------------------------------
            # Avionics Weight
            #-------------------------------------------------------------------------------
            if bus.avionics.origin[0][0] == 0:
                bus.avionics.origin[0][0]                          = 0.4 * nose_length
            bus.avionics.mass_properties.center_of_gravity[0][0]   = 0.0
            weight.avionics += bus.avionics.mass_properties.mass   
                        
<<<<<<< HEAD:RCAIDE/Library/Methods/Weights/Physics_Based_Buildups/Electric/compute_operating_empty_weight.py
            for battery in bus.batteries: 
                weight.battery += battery.mass_properties.mass * Units.kg 
=======
            for battery in bus.battery_modules: 
                weight.battery                                            += battery.mass_properties.mass * Units.kg 
>>>>>>> 42165ad86d788a72a8e2711cd410700702655591:RCAIDE/Library/Methods/Weights/Physics_Based_Buildups/Electric/compute_weight.py
        
            # Servo, Hub and BRS Weights
            lift_rotor_hub_weight   = 4.   * Units.kg
            prop_hub_weight         = MTOW * 0.04  * Units.kg
            lift_rotor_BRS_weight   = 16.  * Units.kg
    
            # Rotor Weight
            number_of_propellers    = 0.0  
            number_of_lift_rotors   = 0.0   
            total_number_of_rotors  = 0.0      
            lift_rotor_servo_weight = 0.0  
            
            for propulsor in bus.propulsors: 
                # Rotor 
                rotor = propulsor.rotor   
                if type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Propeller:
                    ''' Propeller Weight '''  
                    number_of_propellers       += 1   
                    rTip_ref                   = rotor.tip_radius 
                    bladeSol_ref               = rotor.blade_solidity 
                    prop_servo_weight          = 5.2 * Units.kg  
                    propeller_mass             = compute_rotor_weight(rotor, maxLift/5.) * Units.kg
                    weight.rotors              += propeller_mass 
                    rotor.mass_properties.mass =  propeller_mass + prop_hub_weight + prop_servo_weight
                    weight.servos              += prop_servo_weight
                    weight.hubs                += prop_hub_weight
                    
                if (type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor or type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor) or type(rotor) == RCAIDE.Library.Components.Propulsors.Converters.Rotor:
                    ''' Lift Rotor, Prop-Rotor or Rotor Weight '''  
                    number_of_lift_rotors       += 1  
                    rTip_ref                    = rotor.tip_radius
                    bladeSol_ref                = rotor.blade_solidity 
                    maxVTip                     = rotor.hover.design_angular_velocity * rotor.tip_radius
                    lift_rotor_servo_weight     = 0.65 * Units.kg 
                    if rotor.oei.design_thrust == None:
                        design_thrust = rotor.hover.design_thrust
                    else:
                        design_thrust =rotor.oei.design_thrust
                    lift_rotor_mass             = compute_rotor_weight(rotor,design_thrust)
                    weight.rotors               += lift_rotor_mass 
                    rotor.mass_properties.mass  =  lift_rotor_mass + lift_rotor_hub_weight + lift_rotor_servo_weight
                    weight.servos               += lift_rotor_servo_weight
                    weight.hubs                 += lift_rotor_hub_weight 
                
                # Motor 
                eta             = propulsor.motor.efficiency  
                weight.motors  += propulsor.motor.mass_properties.mass  
               
        total_number_of_rotors  = int(number_of_lift_rotors + number_of_propellers)  
        if total_number_of_rotors > 1:
            prop_BRS_weight     = 16.   * Units.kg
        else:
            prop_BRS_weight     = 0.   * Units.kg
 
        # Add associated weights  
        weight.BRS   += (prop_BRS_weight + lift_rotor_BRS_weight)  
        maxLiftPower = 1.15*maxLift*(disk_area_factor*np.sqrt(maxLift/(2*rho_ref*np.pi*rTip_ref**2)) + bladeSol_ref*AvgBladeCD/8*maxVTip**3/(maxLift/(rho_ref*np.pi*rTip_ref**2)))
        # Tail Rotor
        if number_of_lift_rotors == 1: # this assumes that the vehicle is an electric helicopter with a tail rotor 
            maxLiftOmega   = maxVTip/rTip_ref
            maxLiftTorque  = maxLiftPower / maxLiftOmega  
            for bus in network.busses: 
                tailrotor = next(iter(bus.lift_rotors))
                weight.tail_rotor  = compute_rotor_weight(tailrotor, 1.5*maxLiftTorque/(1.25*rTip_ref))*0.2 * Units.kg
                weight.rotors     += weight.tail_rotor 

    #-------------------------------------------------------------------------------
    # Wing and Motor Wiring Weight
    #-------------------------------------------------------------------------------
    maxSpan =  0
    for wing in vehicle.wings: 
        maxSpan = max(wing.spans.projected, maxSpan)  
        if wing.symbolic:
            wing_weight = 0
        else:
            wing_weight               = compute_wing_weight(wing, vehicle, maxLift/5, safety_factor= safety_factor, max_g_load =  max_g_load )
            wing_tag                  = wing.tag
            weight.wings[wing_tag]    = wing_weight
            wing.mass_properties.mass = wing_weight 
        weight.wings_total           += wing_weight

        # compute_wiring_weight weight
        wiring_weight  = compute_wiring_weight(wing, vehicle, maxLiftPower/(eta*total_number_of_rotors)) * Units.kg  
        weight.wiring  += wiring_weight[0][0]

    #-------------------------------------------------------------------------------
    # Landing Gear Weight
    #-------------------------------------------------------------------------------
    if not hasattr(vehicle.landing_gear, 'nose'):
        vehicle.landing_gear.nose       = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()
    vehicle.landing_gear.nose.mass      = 0.0
    if not hasattr(vehicle.landing_gear, 'main'):
        vehicle.landing_gear.main       = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()
    vehicle.landing_gear.main.mass      = weight.landing_gear

    #-------------------------------------------------------------------------------
    # Fuselage  Weight  
    #-------------------------------------------------------------------------------
    for fuse in  vehicle.fuselages: 
        fuselage_weight = compute_fuselage_weight(fuse, maxSpan, MTOW )  
        fuse.mass_properties.center_of_gravity[0][0] = .45*fuse.lengths.total
        fuse.mass_properties.mass                    =  fuselage_weight + weight.passengers + weight.seats + weight.wiring + weight.BRS
        weight.fuselage += fuselage_weight  

    #-------------------------------------------------------------------------------
    # Boom Weight
    #-------------------------------------------------------------------------------
    for boom in vehicle.booms:
        boom_weight                = compute_boom_weight(boom) * Units.kg
        weight.booms               += boom_weight 
        boom.mass_properties.mass  =  boom_weight 
    
    #-------------------------------------------------------------------------------
    # Pack Up Outputs
    #-------------------------------------------------------------------------------
    output                                    = Data()
    output.structural_breakdown               = Data()
    output.structural_breakdown.total         = weight.booms + weight.fuselage + weight.landing_gear +weight.wings_total 
    output.structural_breakdown.booms         = weight.booms 
    output.structural_breakdown.fusleage      = weight.fuselage  
    output.structural_breakdown.landing_gear  = weight.landing_gear  
    output.structural_breakdown.wings         = weight.wings_total 

    output.propulsion_breakdown               = Data()
    output.propulsion_breakdown.motors        = weight.motors
    output.propulsion_breakdown.rotors        = weight.rotors
    output.propulsion_breakdown.hubs          = weight.hubs 
    output.propulsion_breakdown.servos        = weight.servos
    output.propulsion_breakdown.wiring        = weight.wiring 
    output.propulsion_breakdown.battery       = weight.battery
    output.propulsion_breakdown.total         = weight.rotors + weight.hubs +  weight.battery +  weight.motors +   weight.wiring +   weight.servos

    output.systems_breakdown                              = Data()
    output.systems_breakdown.environmental_control_system = weight.ECS
    output.systems_breakdown.avionics                     = weight.avionics  
    output.systems_breakdown.seats                        = weight.seats  
    output.systems_breakdown.balistic_recovery_system     = weight.BRS
    output.systems_breakdown.total                        = weight.ECS + weight.avionics +   weight.BRS +  weight.seats  
    
    output.empty       = (miscelleneous_weight_factor * (output.structural_breakdown.total + output.propulsion_breakdown.total + output.systems_breakdown.total) )   
    output.total       = output.empty + weight.payload + weight.passengers
    output.passengers  = weight.passengers
    output.payload     = weight.payload  
    return output
