# RCAIDE/Methods/Weights/Correlation_Buildups/BWB/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data 
from .compute_cabin_weight          import compute_cabin_weight
from .compute_aft_centerbody_weight import compute_aft_centerbody_weight
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Common     as Common
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion as Propulsion
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Transport  as Transport
from RCAIDE.Library.Attributes.Materials.Aluminum import Aluminum

# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle):
    """ This is for a BWB aircraft configuration.

    Assumptions:
         Calculated aircraft weight from correlations created per component of historical aircraft
         The wings are made out of aluminum.
         A wing with the tag 'main_wing' exists.

    Source:
        N/A

    Inputs:
        engine - a data dictionary with the fields:
            thrust_sls - sea level static thrust of a single engine                                        [Newtons]

        wing - a data dictionary with the fields:
            gross_area - wing gross area                                                                   [meters**2]
            span - span of the wing                                                                        [meters]
            taper - taper ratio of the wing                                                                [dimensionless]
            t_c - thickness-to-chord ratio of the wing                                                     [dimensionless]
            sweep - sweep angle of the wing                                                                [radians]
            mac - mean aerodynamic chord of the wing                                                       [meters]
            r_c - wing root chord                                                                          [meters]

        aircraft - a data dictionary with the fields:
            Nult - ultimate load of the aircraft                                                           [dimensionless]
            Nlim - limit load factor at zero fuel weight of the aircraft                                   [dimensionless]
            TOW - maximum takeoff weight of the aircraft                                                   [kilograms]
            zfw - maximum zero fuel weight of the aircraft                                                 [kilograms]
            num_eng - number of engines on the aircraft                                                    [dimensionless]
            num_pax - number of passengers on the aircraft                                                 [dimensionless]
            wt_cargo - weight of the bulk cargo being carried on the aircraft                              [kilograms]
            num_seats - number of seats installed on the aircraft                                          [dimensionless]
            ctrl - specifies if the control system is "fully powered", "partially powered", or not powered [dimensionless]
            ac - determines type of instruments, electronics, and operating items based on types:
                "short-range", "medium-range", "long-range", "business", "cargo", "commuter", "sst"        [dimensionless]

         fuselage - a data dictionary with the fields:
            area - fuselage wetted area                                                                    [meters**2]
            diff_p - Maximum fuselage pressure differential                                                [Pascal]
            width - width of the fuselage                                                                  [meters]
            height - height of the fuselage                                                                [meters]
            length - length of the fuselage                                                                [meters]

    Outputs:
        output - a data dictionary with fields:
            wt_payload - weight of the passengers plus baggage and paid cargo                              [kilograms]
            wt_pax - weight of all the passengers                                                          [kilogram]
            wt_bag - weight of all the baggage                                                             [kilogram]
            wt_fuel - weight of the fuel carried                                                           [kilogram]
            wt_empty - operating empty weight of the aircraft                                              [kilograms]

    Properties Used:
    N/A
    """

    # Unpack inputs
    TOW         = vehicle.mass_properties.max_takeoff
    
    for fuselage in vehicle.fuselages:
        if type(fuselage) ==  RCAIDE.Library.Components.Fuselages.Blended_Wing_Body_Fuselage: 
            bwb_aft_centerbody_area       = fuselage.aft_centerbody_area
            bwb_aft_centerbody_taper      = fuselage.aft_centerbody_taper 
            wt_cabin                      = compute_cabin_weight(fuselage.cabin_area, TOW)
            fuselage.mass_properties.mass = wt_cabin            
    
    # Compute Propulsor Weight 
    for network in vehicle.networks:
        wt_propulsion = 0
        no_of_engines = 0
        for fuel_line in network.fuel_lines: 
            for propulsor in fuel_line.propulsors:
                if type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan:
                    no_of_engines  += 1
                    thrust_sls      = network.sealevel_static_thrust
                    wt_engine_jet   = Propulsion.compute_jet_engine_weight(thrust_sls)
                    wt_propulsion   += Propulsion.integrated_propulsion(wt_engine_jet) 
        for bus in network.busses: 
            for propulsor in bus.propulsors:
                if type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan:
                    no_of_engines  += 1
                    thrust_sls      = network.sealevel_static_thrust
                    wt_engine_jet   = Propulsion.compute_jet_engine_weight(thrust_sls)
                    wt_propulsion   += Propulsion.integrated_propulsion(wt_engine_jet)                     
 
        network.mass_properties.mass = wt_propulsion
        
    # Compute Wing Weight 
    for wing in vehicle.wings():
        if isinstance(wing,RCAIDE.Library.Components.Wings.Main_Wing):
            rho      = Aluminum().density
            sigma    = Aluminum().yield_tensile_strength           
            wt_wing  = Common.compute_main_wing_weight(vehicle,wing, rho, sigma, computation_type='simple')
            wing.mass_properties.mass = wt_wing

    # Calculating Landing Gear Weight 
    landing_gear        = Common.compute_landing_gear_weight(vehicle)
    
    # Compute Aft Center Body Weight 
    wt_aft_centerbody   = compute_aft_centerbody_weight(bwb_aft_centerbody_area, bwb_aft_centerbody_taper, TOW)
    
    # Compute Systems Weight     
    systems_weights     = Common.compute_systems_weight(vehicle) 

    # Compute Payload Weight     
    payload = Common.compute_payload_weight(vehicle) 
    vehicle.payload.passengers = RCAIDE.Library.Components.Component()
    vehicle.payload.baggage    = RCAIDE.Library.Components.Component()
    vehicle.payload.cargo      = RCAIDE.Library.Components.Component()
    
    vehicle.payload.passengers.mass_properties.mass = payload.passengers
    vehicle.payload.baggage.mass_properties.mass    = payload.baggage
    vehicle.payload.cargo.mass_properties.mass      = payload.cargo    
    

    # Compute Peripheral Operating Items Weights 
    wt_oper = Transport.compute_operating_items_weight(vehicle)
    
    # Store Weights Results 
    output = Data()
    output.structures                               = Data()
    output.structures.wing                          = wt_wing
    output.structures.afterbody                     = wt_aft_centerbody
    output.structures.fuselage                      = wt_cabin
    output.structures.main_landing_gear             = landing_gear.main
    output.structures.nose_landing_gear             = landing_gear.nose
    output.structures.nacelle                       = 0
    output.structures.paint                         = 0  # TODO change
    output.structures.total                         = output.structures.wing + output.structures.afterbody \
                                                      + output.structures.fuselage + output.structures.main_landing_gear + output.structures.nose_landing_gear \
                                                      + output.structures.paint + output.structures.nacelle

    output.propulsion_breakdown                     = Data()
    output.propulsion_breakdown.total               = wt_propulsion
    output.propulsion_breakdown.engines             = 0
    output.propulsion_breakdown.thrust_reversers    = 0
    output.propulsion_breakdown.miscellaneous       = 0
    output.propulsion_breakdown.fuel_system         = 0

    output.systems_breakdown                        = Data()
    output.systems_breakdown.control_systems        = systems_weights.wt_flight_control
    output.systems_breakdown.apu                    = systems_weights.wt_apu
    output.systems_breakdown.electrical             = systems_weights.wt_elec
    output.systems_breakdown.avionics               = systems_weights.wt_avionics
    output.systems_breakdown.hydraulics             = systems_weights.wt_hyd_pnu
    output.systems_breakdown.furnish                = systems_weights.wt_furnish
    output.systems_breakdown.air_conditioner        = systems_weights.wt_ac
    output.systems_breakdown.instruments            = systems_weights.wt_instruments
    output.systems_breakdown.anti_ice               = 0
    output.systems_breakdown.total                  = output.systems_breakdown.control_systems + output.systems_breakdown.apu \
                                                      + output.systems_breakdown.electrical + output.systems_breakdown.avionics \
                                                       + output.systems_breakdown.hydraulics + output.systems_breakdown.furnish \
                                                       + output.systems_breakdown.air_conditioner + output.systems_breakdown.instruments \
                                                       + output.systems_breakdown.anti_ice
         
    output.payload_breakdown                         = Data()
    output.payload_breakdown                         = payload
                        
    output.operational_items                         = Data()
    output.operational_items                         = wt_oper
         
    output.empty                                     = output.structures.total + output.propulsion_breakdown.total + output.systems_breakdown.total
    output.operating_empty                           = output.empty + output.operational_items.total
    output.zero_fuel_weight                          = output.operating_empty + output.payload_breakdown.total
    output.fuel                                      = vehicle.mass_properties.max_takeoff - output.zero_fuel_weight
                        
    control_systems                                  = RCAIDE.Library.Components.Component()
    electrical_systems                               = RCAIDE.Library.Components.Component()
    furnishings                                      = RCAIDE.Library.Components.Component()
    air_conditioner                                  = RCAIDE.Library.Components.Component()
    fuel                                             = RCAIDE.Library.Components.Component()
    apu                                              = RCAIDE.Library.Components.Component()
    hydraulics                                       = RCAIDE.Library.Components.Component()
    avionics                                         = RCAIDE.Library.Components.Systems.Avionics()
    optionals                                        = RCAIDE.Library.Components.Component()
         
    vehicle.landing_gear.nose                        = RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()
    vehicle.landing_gear.nose.mass                   = output.structures.nose_landing_gear
    vehicle.landing_gear.main                        = RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()   
    vehicle.landing_gear.main.mass                   = output.structures.main_landing_gear  
         
    control_systems.mass_properties.mass             = output.systems_breakdown.control_systems
    electrical_systems.mass_properties.mass          = output.systems_breakdown.electrical
    furnishings.mass_properties.mass                 = output.systems_breakdown.furnish
    avionics.mass_properties.mass                    = output.systems_breakdown.avionics \
                                                     + output.systems_breakdown.instruments
    air_conditioner.mass_properties.mass             = output.systems_breakdown.air_conditioner
    fuel.mass_properties.mass                        = output.fuel
    apu.mass_properties.mass                         = output.systems_breakdown.apu
    hydraulics.mass_properties.mass                  = output.systems_breakdown.hydraulics
    optionals.mass_properties.mass                   = output.operational_items.operating_items_less_crew

    # assign components to vehicle
    vehicle.control_systems    = control_systems
    vehicle.electrical_systems = electrical_systems
    vehicle.avionics           = avionics
    vehicle.furnishings        = furnishings
    vehicle.air_conditioner    = air_conditioner
    vehicle.fuel               = fuel
    vehicle.apu                = apu
    vehicle.hydraulics         = hydraulics
    vehicle.optionals          = optionals

    return output
