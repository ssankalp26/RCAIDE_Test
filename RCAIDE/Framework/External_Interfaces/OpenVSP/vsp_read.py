## @ingroup Input_Output-OpenVSP
# vsp_read.py

# Created:  Jun 2018, T. St Francis
# Modified: Aug 2018, T. St Francis
#           Jan 2020, T. MacDonald
#           Jul 2020, E. Botero
#           Sep 2021, R. Erhard
#           Dec 2021, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import RCAIDE
from   RCAIDE.Framework.Core import Units, Data, Container 
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_propeller        import read_vsp_propeller
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_fuselage         import read_vsp_fuselage
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_wing             import read_vsp_wing
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_nacelle          import read_vsp_nacelle
from RCAIDE.Framework.External_Interfaces.OpenVSP.get_vsp_measurements import get_vsp_measurements


from copy import deepcopy

try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass


# ----------------------------------------------------------------------
#  vsp read
# ----------------------------------------------------------------------


## @ingroup Input_Output-OpenVSP
def vsp_read(vsp_file_in, tag_in):
    """This reads an OpenVSP vehicle geometry file and writes it into a RCAIDE vehicle format.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vsp_file_in - OpenVSP geometry file (.vsp3)
    tag_in      - Name of aircraft in file

    Returns:
    vehicle - Data structure containing vehicle geometry in RCAIDE format with:
    fuselages, wings, propellers, and nacelles, each containing tags, dimensions and areas

    Properties Used:
    None
    """

    vsp.ClearVSPModel() 
    vsp.ReadVSPFile(vsp_file_in)	

    vsp_fuselages     = []
    vsp_wings         = []	
    vsp_props         = [] 
    vsp_nacelles      = [] 
    vsp_nacelle_type  = []
    
    vsp_geoms         = vsp.FindGeoms()
    geom_names        = []

    vehicle           = RCAIDE.Vehicle()
    vehicle.tag       = tag_in 

    # The two for-loops below are in anticipation of an OpenVSP API update with a call for GETGEOMTYPE.
    # This print function allows user to enter VSP GeomID manually as first argument in vsp_read functions.

    print("VSP geometry IDs: ")	

    # Label each geom type by storing its VSP geom ID. 

    for geom in vsp_geoms: 
        geom_name = vsp.GetGeomName(geom)
        geom_names.append(geom_name)
        print(str(geom_name) + ': ' + geom)
        
        
    # Use OpenVSP to calculate wetted area
    measurements = get_vsp_measurements()
    if units_type == 'SI':
        units_factor = Units.meter * 1.
    elif units_type == 'imperial':
        units_factor = Units.foot * 1.
    elif units_type == 'inches':
        units_factor = Units.inch * 1.	         

    # --------------------------------
    # AUTOMATIC VSP ENTRY & PROCESSING
    # --------------------------------		

    for geom in vsp_geoms:
        geom_name = vsp.GetGeomName(geom)
        geom_type = vsp.GetGeomTypeName(str(geom))

        if geom_type == 'Fuselage':
            vsp_fuselages.append(geom)
        if geom_type == 'Wing':
            vsp_wings.append(geom)
        if geom_type == 'Propeller':
            vsp_props.append(geom) 
        if (geom_type == 'Stack') or (geom_type == 'BodyOfRevolution'):
            vsp_nacelle_type.append(geom_type)
            vsp_nacelles.append(geom) 
        
    # --------------------------------------------------			
    # Read Fuselages 
    # --------------------------------------------------			    
    for fuselage_id in vsp_fuselages:
        sym_planar = vsp.GetParmVal(fuselage_id, 'Sym_Planar_Flag', 'Sym') # Check for symmetry
        sym_origin = vsp.GetParmVal(fuselage_id, 'Sym_Ancestor_Origin_Flag', 'Sym') 
        if sym_planar == 2. and sym_origin == 1.:  
            num_fus  = 2 
            sym_flag = [1,-1]
        else: 
            num_fus  = 1 
            sym_flag = [1] 
        for fux_idx in range(num_fus):	# loop through fuselages on aircraft 
            fuselage = read_vsp_fuselage(fuselage_id,fux_idx,sym_flag[fux_idx],units_type,use_scaling)
            
            if calculate_wetted_area:
                fuselage.areas.wetted = measurements[vsp.GetGeomName(fuselage_id)] * (units_factor**2)
            
            vehicle.append_component(fuselage)
        
    # --------------------------------------------------			    
    # Read Wings 
    # --------------------------------------------------			
    for wing_id in vsp_wings:
        wing = read_vsp_wing(wing_id, units_type,use_scaling)
        if calculate_wetted_area:
            wing.areas.wetted = measurements[vsp.GetGeomName(wing_id)] * (units_factor**2)  
        vehicle.append_component(wing)		 
        
    # --------------------------------------------------			    
    # Read Nacelles 
    # --------------------------------------------------			
    for nac_id, nacelle_id in enumerate(vsp_nacelles):
        nacelle = read_vsp_nacelle(nacelle_id,vsp_nacelle_type[nac_id], units_type)
        if calculate_wetted_area:
            nacelle.areas.wetted = measurements[vsp.GetGeomName(nacelle_id)] * (units_factor**2)         
        vehicle.append_component(nacelle)	  
    
    # --------------------------------------------------			    
    # Read Propellers/Rotors and assign to a network
    # --------------------------------------------------			
    # Initialize rotor network elements
    number_of_lift_rotor_engines = 0
    number_of_propeller_engines  = 0
    lift_rotors = Container()
    propellers  = Container() 
    for prop_id in vsp_props:
        prop = read_vsp_propeller(prop_id,units_type)
        prop.tag = vsp.GetGeomName(prop_id)
        if prop.orientation_euler_angles[1] >= 70 * Units.degrees:
            lift_rotors.append(prop)
            number_of_lift_rotor_engines += 1 
            
            if vsp.GetParmVal(prop_id, 'Sym_Planar_Flag', 'Sym')== 2.0:
                number_of_lift_rotor_engines += 1 
                prop_sym = deepcopy(prop)
                prop_sym.origin[0][1] = - prop_sym.origin[0][1]
                lift_rotors.append(prop_sym)
            
        else:
            propellers.append(prop)
            number_of_propeller_engines += 1  
            
            if vsp.GetParmVal(prop_id, 'Sym_Planar_Flag', 'Sym')== 2.0:
                number_of_propeller_engines += 1      
                prop_sym = deepcopy(prop)
                prop_sym.origin[0][1] = - prop_sym.origin[0][1]   
                propellers.append(prop_sym)

    if specified_network == None: 
        net = RCIADE.Framework.Networks.Electric() 
    else:
        net = specified_network
    
     

    for i in range(number_of_lift_rotor_engines):
        propulsor = RCAIDE.Library.Components.Propulsors.Electric_Rotor()
        propulsor.tag =  'propulsor_' +  str(i+1)
        propulsor.rotor = lift_rotors[list(lift_rotors.keys())[i]]   
        net.propulsors.append(propulsor)         	

    vehicle.networks.append(net)

    return vehicle