## @ingroup Input_Output-OpenVSP
# get_fuel_tank_properties.py
# 
# Created:  Sep 2018, T. MacDonald
# Modified: Oct 2018, T. MacDonald
#           Jan 2020, T. MacDonald

try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np
from RCAIDE.Framework.Core import Data

## @ingroup Input_Output-OpenVSP
def get_fuel_tank_properties(vehicle):
    """Gets the fuel tank properties from OpenVSP

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vehicle - vehicle data structure

    Returns:
    data    - OpenVSP results containing: tag, volume, center_of_gravity, reference_area, 
    length_reference, width_reference, height_reference, max_length, max_width, max_height

    Properties Used:
    None
    """
    
    # Reset OpenVSP to avoid including a previous vehicle
    vsp.ClearVSPModel()    
    vsp.ReadVSPFile(tag + '.vsp3')
    
    # Extract fuel tanks from vehicle
    fuel_tanks = get_fuel_tanks(vehicle)
    
    num_slices = slices_for_calculation # Slices used to estimate mass distribution from areas in OpenVSP
    mass_props_output_file = tag + '_mass_props.txt'
    vsp.SetComputationFileName(vsp.MASS_PROP_TXT_TYPE,mass_props_output_file)
    print('Computing Fuel Tank Mass Properties... ')
    vsp.ComputeMassProps(fuel_tank_set_index, num_slices)
    print('Done')
    
    # Extract full tank mass properties from OpenVSP output file
    fo = open(mass_props_output_file)
    for line in fo:
        prop_list = line.split()
        try:
            if prop_list[0] in fuel_tanks:
                # Indices based on position in OpenVSP output (may change in the future)
                cg_x = float(prop_list[2])
                cg_y = float(prop_list[3])
                cg_z = float(prop_list[4])
                mass = float(prop_list[1])
                vol  = float(prop_list[-1])
                if 'center_of_gravity' not in fuel_tanks[prop_list[0]]: # assumes at most two identical tank names
                    fuel_tanks[prop_list[0]].center_of_gravity   = np.array([cg_x,cg_y,cg_z])
                    fuel_tanks[prop_list[0]].fuel_mass_when_full = mass
                    fuel_tanks[prop_list[0]].volume              = vol
                else:
                    fuel_tanks[prop_list[0]].center_of_gravity = \
                        (fuel_tanks[prop_list[0]].center_of_gravity+np.array([cg_x,cg_y,cg_z]))/2.
                    fuel_tanks[prop_list[0]].fuel_mass_when_full  += mass
                    fuel_tanks[prop_list[0]].volume               += vol                    
                    
        except IndexError:  # in case line is empty
            pass

    # Apply fuel tank properties to the vehicle
    vehicle = apply_properties(vehicle, fuel_tanks)
    
    
    return vehicle

## @ingroup Input_Output-OpenVSP
def apply_properties(vehicle):
    """Applies the fuel tank properties from OpenVSP to the vehicle

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vehicle - vehicle data structure with fuel and wings properties

    Returns:
    vehicle - vehicle data structure with updated fuel tank properties

    Properties Used:
    None
    """
    for wing in vehicle.wings:
        for tank in wing.Fuel_Tanks:
            tank.mass_properties.center_of_gravity     = fuel_tanks[tank.tag].center_of_gravity
            tank.mass_properties.fuel_mass_when_full   = fuel_tanks[tank.tag].fuel_mass_when_full
            tank.mass_properties.fuel_volume_when_full = fuel_tanks[tank.tag].volume
                
    for fuse in vehicle.fuselages:
        for tank in fuse.Fuel_Tanks:
            tank.mass_properties.center_of_gravity     = fuel_tanks[tank.tag].center_of_gravity
            tank.mass_properties.fuel_mass_when_full   = fuel_tanks[tank.tag].fuel_mass_when_full
            tank.mass_properties.fuel_volume_when_full = fuel_tanks[tank.tag].volume    
                    
    return vehicle
    
## @ingroup Input_Output-OpenVSP
def get_fuel_tanks(vehicle):
    """Creates a data structure with fuel tanks based on 
    fuel tanks present in the vehicle
    
    Assumptions:
    Fuel tanks exists in the fuselage and wings only

    Source:
    N/A

    Inputs:
    vehicle.fuselages.*.Fuel_Tanks.*.tag     [-]
    vehicle.wings.*.Fuel_Tanks.*.tag         [-]

    Outputs:    
    fuel_tanks.tag                           [-]

    Properties Used:
    N/A
    """       
    fuel_tanks = Data()
    
    for wing in vehicle.wings:
        for tank in wing.Fuel_Tanks:
            fuel_tanks[tank.tag] = Data()
                    
    for fuse in vehicle.fuselages:
        for tank in fuse.Fuel_Tanks:
            fuel_tanks[tank.tag] = Data()
                    
    return fuel_tanks