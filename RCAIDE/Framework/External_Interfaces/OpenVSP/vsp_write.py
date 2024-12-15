## @ingroup Input_Output-OpenVSP
# vsp_write.py
# 
# Created:  Jul 2016, T. MacDonald
# Modified: Jun 2017, T. MacDonald
#           Jul 2017, T. MacDonald
#           Oct 2018, T. MacDonald
#           Nov 2018, T. MacDonald
#           Jan 2019, T. MacDonald
#           Jan 2020, T. MacDonald 
#           Mar 2020, M. Clarke
#           May 2020, E. Botero
#           Jul 2020, E. Botero 
#           Feb 2021, T. MacDonald
#           May 2021, E. Botero 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from RCAIDE.Framework.Core import Units, Data 
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_propeller import write_vsp_propeller_bem
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_fuselage  import write_vsp_fuselage
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_wing      import write_vsp_wing
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_nacelle   import write_vsp_nacelle 
try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np
import os

## @ingroup Input_Output-OpenVSP
def write(vehicle, tag, fuel_tank_set_names=None):
    """This writes a RCAIDE vehicle to OpenVSP format

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vehicle              - RCAIDE vehicle data structure
    tag                  - Name of vehicle in file
    fuel_tank_set_names - Names of fuel tank sets to write to OpenVSP format

    Returns:
    None - but writes the following files:
    - tag.vsp3 (OpenVSP vehicle file)
    - tag.fuse (OpenVSP fuselage file)
    - tag.wing (OpenVSP wing file)
    - tag.prop (OpenVSP propeller file)
    - tag.nacelle (OpenVSP nacelle file)

    Properties Used:
    None
    """
    
    # Reset OpenVSP to avoid including a previous vehicle
    print('Reseting OpenVSP Model in Memory')
    try:
        vsp.ClearVSPModel()
    except NameError:
        print('VSP import failed')
        return -1
    
    area_tags = dict() # for wetted area assignment
    
    # -------------
    # Wings
    # -------------
    
    # Default Set_0 in OpenVSP is index 3
    vsp.SetSetName(3, 'fuel_tanks')
    vsp.SetSetName(4, 'OML')
    
    for wing in vehicle.wings:       
        print('Writing '+wing.tag+' to OpenVSP Model')
        area_tags, wing_id = write_vsp_wing(vehicle,wing,area_tags, 3, 4)
        if wing.tag == 'main_wing':
            main_wing_id = wing_id    
    
    # -------------
    # Engines
    # -------------
    ## Skeleton code for props and pylons can be found in previous commits (~Dec 2016) if desired
    ## This was a place to start and may not still be functional   
    for network in vehicle.networks:
    
        if 'propellers' in  network:
            for prop in network.propellers:
                vsp_bem_filename = prop.tag + '.bem' 
                write_vsp_propeller_bem(vsp_bem_filename,prop) 
    
        if 'lift_rotors' in network:
            for rot in network.lift_rotors:
                vsp_bem_filename = rot.tag + '.bem' 
                write_vsp_propeller_bem(vsp_bem_filename,rot)    
    # -------------
    # Nacelle
    # ------------- 
    for key, nacelle in vehicle.nacelles.items():
        print('Writing '+ nacelle.tag +' to OpenVSP Model')
        write_vsp_nacelle(nacelle, 4)
                     
    # -------------
    # Fuselage
    # -------------     
    for key, fuselage in vehicle.fuselages.items():
        print('Writing '+fuselage.tag+' to OpenVSP Model')
        try:
            area_tags = write_vsp_fuselage(fuselage, area_tags, vehicle.wings.main_wing, 
                                          3, 4)
        except AttributeError:
            area_tags = write_vsp_fuselage(fuselage, area_tags, None, 3,
                                          4)
    
    vsp.Update()
    
    # Write the vehicle to the file    
    cwd = os.getcwd()
    filename = tag + ".vsp3"
    print('Saving OpenVSP File at '+ cwd + '/' + filename)
    vsp.WriteVSPFile(filename)
    
    return area_tags