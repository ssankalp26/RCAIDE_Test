## @ingroup Input_Output-OpenVSP
# vsp_fuselage.py

# Created:  Jun 2018, T. St Francis
# Modified: Aug 2018, T. St Francis
#           Jan 2020, T. MacDonald
#           Jul 2020, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core import Units, Data  
import numpy as np
try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
# ----------------------------------------------------------------------
#  vsp read fuselage
# ----------------------------------------------------------------------

## @ingroup Input_Output-OpenVSP
def read_vsp_fuselage(vsp_fuselage_file):
    """Reads a OpenVSP fuselage file

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vsp_fuselage_file - XML file for fuselage outer mold line

    Returns:
    fuselage - Data structure containing fuselage properties including:
    nose_location, tail_location, lengths, widths, heights, areas, tag

    Properties Used:
    None
    """
    fuselage = RCAIDE.Library.Components.Fuselages.Fuselage()	

    # Implementation of read_vsp_fuselage function

    return fuselage


## @ingroup Input_Output-OpenVSP
def write_vsp_fuselage(fuselage, area_tags, write_file):
    """Writes a fuselage in OpenVSP format

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    fuselage   - RCAIDE fuselage data structure
    area_tags  - Tags for identifying wing segments
    write_file - VSP file to write fuselage to

    Returns:
    None

    Properties Used:
    None
    """

    # Implementation of write_vsp_fuselage function

    return


## @ingroup Input_Output-OpenVSP
def write_fuselage_conformal_fuel_tank(fuselage, fuel_tank, write_file):
    """Writes a conformal fuel tank in OpenVSP format

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    fuselage   - RCAIDE fuselage data structure
    fuel_tank  - RCAIDE fuel tank data structure
    write_file - VSP file to write fuel tank to

    Returns:
    None

    Properties Used:
    None
    """

    # Implementation of write_fuselage_conformal_fuel_tank function

    return