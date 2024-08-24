## @ingroup Library-Methods-Performance
# RCAIDE/Library/Methods/Performance/payload_range_diagram.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core import Units , Data  
 
# Pacakge imports 
import numpy as np
from matplotlib import pyplot as plt
 
# ----------------------------------------------------------------------
#  Calculate vehicle Payload Range Diagram
# ---------------------------------------------------------------------- 
def payload_range_diagram(vehicle,mission,cruise_segment_tag,reserves=0., plot_diagram = True): 
    for network in vehicle.networks:
        if type(network) == RCAIDE.Framework.Networks.Fuel:
            payload_range  =  conventional_payload_range_diagram(vehicle,mission,cruise_segment_tag,reserves,plot_diagram) 
        elif type(network) == RCAIDE.Framework.Networks.Electric:
            payload_range  =  electric_payload_range_diagram(vehicle,mission,cruise_segment_tag,plot_diagram)
    return payload_range 
            
def conventional_payload_range_diagram(vehicle,mission,cruise_segment_tag,reserves,plot_diagram):
    #unpack
    masses = vehicle.mass_properties
    if not masses.operating_empty:
        print("Error calculating Payload Range Diagram: Vehicle Operating Empty not defined")
        return True
    else:
        OEW = masses.operating_empty

    if not masses.max_zero_fuel:
        print("Error calculating Payload Range Diagram: Vehicle MZFW not defined")
        return True
    else:
        MZFW = vehicle.mass_properties.max_zero_fuel

    if not masses.max_takeoff:
        print("Error calculating Payload Range Diagram: Vehicle MTOW not defined")
        return True
    else:
        MTOW = vehicle.mass_properties.max_takeoff

    if not masses.max_payload:
        MaxPLD = MZFW - OEW  # If payload max not defined, calculate based in design weights
    else:
        MaxPLD = vehicle.mass_properties.max_payload
        MaxPLD = min(MaxPLD , MZFW - OEW) #limit in structural capability

    if not masses.max_fuel:
        MaxFuel = MTOW - OEW # If not defined, calculate based in design weights
    else:
        MaxFuel = vehicle.mass_properties.max_fuel  # If max fuel capacity not defined
        MaxFuel = min(MaxFuel, MTOW - OEW)


    # Define payload range points
    #Point  = [ RANGE WITH MAX. PLD   , RANGE WITH MAX. FUEL , FERRY RANGE   ]
    TOW     = [ MTOW                               , MTOW                   , OEW + MaxFuel ]
    FUEL    = [ min(TOW[1] - OEW - MaxPLD,MaxFuel) , MaxFuel                , MaxFuel       ]
    PLD     = [ MaxPLD                             , MTOW - MaxFuel - OEW   , 0.            ]

    # allocating Range array
    R       = [0,0,0]

    # evaluate the mission 

    # loop for each point of Payload Range Diagram
    for i in range(len(TOW)):
        ##    for i in [2]: 
        # Define takeoff weight
        mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff = TOW[i]

        # Evaluate mission with current TOW
        results = mission.evaluate()
        segment = results.segments[cruise_segment_tag]

        # Distance convergency in order to have total fuel equal to target fuel
        #
        # User don't have the option of run a mission for a given fuel. So, we
        # have to iterate distance in order to have total fuel equal to target fuel
        #

        maxIter = 10 # maximum iteration limit
        tol = 1.     # fuel convergency tolerance
        err = 9999.  # error to be minimized
        iter = 0     # iteration count

        while abs(err) > tol and iter < maxIter:
            iter = iter + 1

            # Current total fuel burned in mission
            TotalFuel  = TOW[i] - results.segments[-1].conditions.weights.total_mass[-1,0]

            # Difference between burned fuel and target fuel
            missingFuel = FUEL[i] - TotalFuel - reserves

            # Current distance and fuel consuption in the cruise segment
            CruiseDist = np.diff( segment.conditions.frames.inertial.position_vector[[0,-1],0] )[0]        # Distance [m]
            CruiseFuel = segment.conditions.weights.total_mass[0,0] - segment.conditions.weights.total_mass[-1,0]    # [kg]
            # Current specific range (m/kg)
            CruiseSR    = CruiseDist / CruiseFuel        # [m/kg]

            # Estimated distance that will result in total fuel burn = target fuel
            DeltaDist  =  CruiseSR *  missingFuel
            mission.segments[cruise_segment_tag].distance = (CruiseDist + DeltaDist)

            # running mission with new distance
            results = mission.evaluate()
            segment = results.segments[cruise_segment_tag]

            # Difference between burned fuel and target fuel
            err = ( TOW[i] - results.segments[-1].conditions.weights.total_mass[-1,0] ) - FUEL[i] + reserves 

        # Allocating resulting range in ouput array.
        R[i] = ( results.segments[-1].conditions.frames.inertial.position_vector[-1,0] ) * Units.m / Units.nautical_mile      #Distance [nm]

    # Inserting point (0,0) in output arrays
    R.insert(0,0)
    PLD.insert(0,MaxPLD)
    FUEL.insert(0,0)
    TOW.insert(0,0)

    # packing results
    payload_range                =  Data()
    payload_range.range          = np.multiply(R,1.0*Units.nautical_mile / Units.m) # [m]
    payload_range.payload        = PLD
    payload_range.fuel           = FUEL
    payload_range.takeoff_weight = TOW
    payload_range.reserves       = reserves
    
    if plot_diagram: 

        title = "Payload Range Diagram"
        plt.figure(0)
        plt.plot(R,PLD,'r')
        plt.xlabel('Range (nm)'); plt.ylabel('Payload (kg)'); plt.title(title)
        plt.grid(True)
        plt.show()        

    return payload_range 
 
def electric_payload_range_diagram(vehicle,mission,cruise_segment_tag,plot_diagram):

    masses = vehicle.mass_properties

    if not masses.operating_empty:
        print("Error calculating Payload Range Diagram: vehicle Operating Empty Weight is undefined.")
        return True
    else:
        OEW = masses.operating_empty

    if not masses.max_payload:
        print("Error calculating Payload Range Diagram: vehicle Maximum Payload Weight is undefined.")
        return True
    else:
        MaxPLD = masses.max_payload

    if not masses.max_takeoff:
        print("Error calculating Payload Range Diagram: vehicle Maximum Payload Weight is undefined.")
        return True
    else:
        MTOW = masses.max_takeoff

    # Define Diagram Points
    # Point = [Value at Maximum Payload Range,  Value at Ferry Range]

    TOW =   [MTOW,      OEW]    # Takeoff Weights
    PLD =   [MaxPLD,    0.]     # Payload Weights

    # Initialize Range Array

    R = np.zeros(2)

    # Calculate Vehicle Range for Max Payload and Ferry Conditions
    

    for i in range(2):
        mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff = TOW[i]
        results = mission.evaluate()
        segment = results.segments[cruise_segment_tag]
        R[i]    = segment.conditions.frames.inertial.position_vector[-1,0] 

    # Insert Starting Point for Diagram Construction

    R = np.insert(R, 0, 0)
    PLD = np.insert(PLD, 0, MaxPLD)
    TOW = np.insert(TOW, 0, 0)

    # Pack Results

    payload_range = Data()
    payload_range.range             = R
    payload_range.payload           = PLD
    payload_range.takeoff_weight    = TOW

    if plot_diagram: 
        plt.plot(R, PLD, 'r')
        plt.xlabel('Range (m)')
        plt.ylabel('Payload (kg)')
        plt.title('Payload Range Diagram')
        plt.grid(True) 

    return payload_range
