## @ingroup Methods-Missions-Common-Update
# RCAIDE/Methods/Missions/Common/Update/thrust.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Thrust
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Missions-Common-Update
def thrust(segment):
    """  
    """    

    # unpack
    energy_model = segment.analyses.energy

    # evaluate
    energy_model.evaluate_thrust(segment.state)

    # pack conditions
    conditions = segment.state.conditions
    conditions.frames.body.thrust_force_vector       = conditions.energy.thrust_force_vector
    conditions.weights.vehicle_mass_rate             = conditions.energy.vehicle_mass_rate 

    if "vehicle_additional_fuel_rate" in conditions.energy: 
        conditions.weights.has_additional_fuel             = True
        conditions.weights.vehicle_fuel_rate               = conditions.energy.vehicle_fuel_rate
        conditions.weights.vehicle_additional_fuel_rate    = conditions.energy.vehicle_additional_fuel_rate  