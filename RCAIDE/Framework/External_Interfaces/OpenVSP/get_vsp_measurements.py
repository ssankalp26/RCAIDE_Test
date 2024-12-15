## @ingroup Input_Output-OpenVSP
# get_vsp_measurements.py
# 
# Created:  --- 2016, T. MacDonald
# Modified: Aug 2017, T. MacDonald
#           Mar 2018, T. MacDonald
#           Jan 2020, T. MacDonald
#           Feb 2021, T. MacDonald

try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np

## @ingroup Input_Output-OpenVSP
def get_vsp_measurements(vehicle):
    """Gets measurements from OpenVSP using the VSP script

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vehicle - vehicle data structure

    Returns:
    data - OpenVSP results containing: wetted areas, reference areas, volumes, lengths, 
    widths, heights, aspect ratios for all components

    Properties Used:
    None
    """
    
    if measurement_type == 'wetted_area':
        output_ind = 2
    elif measurement_type == 'wetted_volume':
        output_ind = 4
    else:
        raise NotImplementedError
    
    half_mesh = False # Note that this does not affect the Gmsh/SU2 meshing process
    # it only affects how much area of a component is included in the output
    try:
        file_type = vsp.COMP_GEOM_CSV_TYPE
    except NameError:
        print('VSP import failed')
        return -1

    vsp.SetComputationFileName(file_type, filename)
    vsp.ComputeCompGeom(vsp.SET_ALL, half_mesh, file_type)
    
    f = open(filename)
    
    measurements = dict()
    
    # Extract wetted areas for each component
    for ii, line in enumerate(f):
        if ii == 0:
            pass
        elif line == '\n':
            break
        else:
            vals = line.split(',')
            item_tag = vals[0][:]
            item_w_area = float(vals[output_ind])
            if item_tag in measurements:
                item_w_area = measurements[item_tag] + item_w_area
            measurements[item_tag] = item_w_area
            
    f.close()
    
    return measurements