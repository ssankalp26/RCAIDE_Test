## @ingroup Input_Output-OpenVSP
# vsp_propeller.py

# Created:  Sep 2021, R. Erhard
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units , Data
import numpy as np
import scipy as sp
import string
try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass

# This enforces lowercase names
chars = string.punctuation + string.whitespace
t_table = str.maketrans( chars          + string.ascii_uppercase ,
                         '_'*len(chars) + string.ascii_lowercase )

# ----------------------------------------------------------------------
#  vsp read prop
# ----------------------------------------------------------------------

## @ingroup Input_Output-OpenVSP
def read_vsp_propeller(vsp_propeller_file):
    """Reads a OpenVSP propeller file

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vsp_propeller_file - XML file for propeller outer mold line

    Returns:
    propeller - Data structure containing propeller properties including radius, 
    chord, twist, sweep, max thickness, and airfoil coordinates

    Properties Used:
    None
    """

    # Check if this is a propeller or a lift rotor
    # Check if the thrust angle	is > 70 deg in pitch
    if vsp.GetParmVal( prop_id,'Y_Rotation','XForm') >= 70:
        # Assume lift rotor
        prop 	= RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor()
    else:
        # Instantiate a propeller
        prop 	= RCAIDE.Library.Components.Propulsors.Converters.Propeller()

    # Set the units
    if units_type == 'SI':
        units_factor = Units.meter * 1.
    elif units_type == 'imperial':
        units_factor = Units.foot * 1.
    elif units_type == 'inches':
        units_factor = Units.inch * 1.

    # Apply a tag to the prop
    if vsp.GetGeomName(prop_id):
        tag = vsp.GetGeomName(prop_id)
        tag = tag.translate(t_table)
        prop.tag = tag
    else:
        prop.tag = 'propgeom'


    scaling           = vsp.GetParmVal(prop_id, 'Scale', 'XForm')
    units_factor      = units_factor*scaling

    # Propeller location (absolute)
    prop.origin 	= [[0.0,0.0,0.0]]
    prop.origin[0][0] 	= vsp.GetParmVal(prop_id, 'X_Location', 'XForm') * units_factor
    prop.origin[0][1] 	= vsp.GetParmVal(prop_id, 'Y_Location', 'XForm') * units_factor
    prop.origin[0][2] 	= vsp.GetParmVal(prop_id, 'Z_Location', 'XForm') * units_factor

    # Propeller orientation
    prop.orientation_euler_angles 	= [0.0,0.0,0.0]
    prop.orientation_euler_angles[0] 	= vsp.GetParmVal(prop_id, 'X_Rotation', 'XForm') * Units.degrees
    prop.orientation_euler_angles[1] 	= vsp.GetParmVal(prop_id, 'Y_Rotation', 'XForm') * Units.degrees
    prop.orientation_euler_angles[2] 	= vsp.GetParmVal(prop_id, 'Z_Rotation', 'XForm') * Units.degrees

    # Get the propeller parameter IDs
    parm_id    = vsp.GetGeomParmIDs(prop_id)
    parm_names = []
    for i in range(len(parm_id)):
        parm_name = vsp.GetParmName(parm_id[i])
        parm_names.append(parm_name)

    # Run the vsp Blade Element analysis
    vsp.SetStringAnalysisInput( "BladeElement" , "PropID" , (prop_id,) )
    rid = vsp.ExecAnalysis( "BladeElement" )
    Nc  = len(vsp.GetDoubleResults(rid,"YSection_000"))

    prop.vtk_airfoil_points           = 2*Nc
    prop.CLi                          = vsp.GetParmVal(parm_id[parm_names.index('CLi')])
    prop.blade_solidity               = vsp.GetParmVal(parm_id[parm_names.index('Solidity')])
    prop.number_of_blades             = int(vsp.GetParmVal(parm_id[parm_names.index('NumBlade')]))

    prop.tip_radius                   = vsp.GetDoubleResults(rid, "Diameter" )[0] / 2 * units_factor
    prop.radius_distribution          = np.array(vsp.GetDoubleResults(rid, "Radius" )) * prop.tip_radius

    prop.radius_distribution[-1]      = 0.99 * prop.tip_radius # BEMT requires max nondimensional radius to be less than 1.0
    if prop.radius_distribution[0] == 0.:
        start = 1
        prop.radius_distribution = prop.radius_distribution[start:]
    else:
        start = 0

    prop.hub_radius                   = prop.radius_distribution[0]

    prop.chord_distribution           = np.array(vsp.GetDoubleResults(rid, "Chord" ))[start:]  * prop.tip_radius # vsp gives c/R
    prop.twist_distribution           = np.array(vsp.GetDoubleResults(rid, "Twist" ))[start:]  * Units.degrees
    prop.sweep_distribution           = np.array(vsp.GetDoubleResults(rid, "Sweep" ))[start:]
    prop.mid_chord_alignment          = np.tan(prop.sweep_distribution*Units.degrees)  * prop.radius_distribution
    prop.thickness_to_chord           = np.array(vsp.GetDoubleResults(rid, "Thick" ))[start:]
    prop.max_thickness_distribution   = prop.thickness_to_chord*prop.chord_distribution * units_factor
    prop.Cl_distribution              = np.array(vsp.GetDoubleResults(rid, "CLi" ))[start:]

    # Extra data from VSP BEM for future use in BEVW
    prop.beta34                       = vsp.GetDoubleResults(rid, "Beta34" )[0]  # pitch at 3/4 radius
    prop.pre_cone                     = vsp.GetDoubleResults(rid, "Pre_Cone")[0]
    prop.rake                         = np.array(vsp.GetDoubleResults(rid, "Rake"))[start:]
    prop.skew                         = np.array(vsp.GetDoubleResults(rid, "Skew"))[start:]
    prop.axial                        = np.array(vsp.GetDoubleResults(rid, "Axial"))[start:]
    prop.tangential                   = np.array(vsp.GetDoubleResults(rid, "Tangential"))[start:]

    # Set prop rotation
    prop.rotation = 1

    # ---------------------------------------------
    # Rotor Airfoil
    # ---------------------------------------------
    if write_airfoil_file:
        print("Airfoil write not yet implemented. Defaulting to NACA 4412 airfoil for propeller cross section.")

    return prop

## @ingroup Input_Output-OpenVSP
def write_vsp_propeller_bem(prop, write_file):
    """Writes a propeller in OpenVSP BEM format

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    prop       - RCAIDE propeller data structure
    write_file - VSP file to write propeller to

    Returns:
    None

    Properties Used:
    None
    """
    vsp_bem = open(write_file,'w')
    with open(write_file,'w') as vsp_bem:
        make_header_text(vsp_bem, prop)

        make_section_text(vsp_bem,prop)

        make_airfoil_text(vsp_bem,prop)

    # Now import this prop
    vsp.ImportFile(write_file,vsp.IMPORT_BEM,'')

    return



## @ingroup Input_Output-OpenVSP
def make_header_text(prop):
    """Creates header text for VSP propeller file

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    prop - RCAIDE propeller data structure

    Returns:
    header_text - Formatted header text string

    Properties Used:
    None
    """
    header_base = \
'''...{0}...
Num_Sections: {1}
Num_Blade: {2}
Diameter: {3}
Beta 3/4 (deg): {4}
Feather (deg): 0.00000000
Pre_Cone (deg): 0.00000000
Center: {5}, {6}, {7}
Normal: {8}, {9}, {10}
'''
    # Unpack inputs
    name      = prop.tag
    N         = len(prop.radius_distribution)
    B         = int(prop.number_of_blades)
    D         = np.round(prop.tip_radius*2,5)
    beta      = np.round(prop.twist_distribution/Units.degrees,5)
    X         = np.round(prop.origin[0][0],5)
    Y         = np.round(prop.origin[0][1],5)
    Z         = np.round(prop.origin[0][2],5)
    rotations = np.dot(prop.body_to_prop_vel(),np.array([-1,0,0])) # The sign is because props point opposite flow
    Xn        = np.round(rotations[0][0],5)
    Yn        = np.round(rotations[0][1],5)
    Zn        = np.round(rotations[0][2],5)

    beta_3_4  = np.interp(prop.tip_radius*0.75,prop.radius_distribution,beta)

    # Insert inputs into the template
    header_text = header_base.format(name,N,B,D,beta_3_4,X,Y,Z,Xn,Yn,Zn)
    vsp_bem.write(header_text)

    return

## @ingroup Input_Output-OpenVSP
def make_section_text(prop):
    """Creates section text for VSP propeller file

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    prop - RCAIDE propeller data structure

    Returns:
    section_text - Formatted section text string

    Properties Used:
    None
    """
    header = \
        '''Radius/R, Chord/R, Twist (deg), Rake/R, Skew/R, Sweep, t/c, CLi, Axial, Tangential\n'''

    N          = len(prop.radius_distribution)
    r_R        = np.zeros(N)
    c_R        = np.zeros(N)
    r_R        = prop.radius_distribution/prop.tip_radius
    c_R        = prop.chord_distribution/prop.tip_radius
    beta_deg   = prop.twist_distribution/Units.degrees
    Rake_R     = np.zeros(N)
    Skew_R     = np.zeros(N)
    Sweep      = np.arctan(prop.mid_chord_alignment/prop.radius_distribution)
    t_c        = prop.thickness_to_chord
    CLi        = np.ones(N)*prop.design_Cl
    Axial      = np.zeros(N)
    Tangential = np.zeros(N)

    # Write propeller station imformation
    vsp_bem.write(header)
    for i in range(N):
        section_text = format(r_R[i], '.7f')+ ", " + format(c_R[i], '.7f')+ ", " + format(beta_deg[i], '.7f')+ ", " +\
            format( Rake_R[i], '.7f')+ ", " + format(Skew_R[i], '.7f')+ ", " + format(Sweep[i], '.7f')+ ", " +\
            format(t_c[i], '.7f')+ ", " + format(CLi[i], '.7f') + ", "+ format(Axial[i], '.7f') + ", " +\
            format(Tangential[i], '.7f') + "\n"
        vsp_bem.write(section_text)

    return

## @ingroup Input_Output-OpenVSP
def make_airfoil_text(prop):
    """Creates airfoil text for VSP propeller file

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    prop - RCAIDE propeller data structure

    Returns:
    airfoil_text - Formatted airfoil text string

    Properties Used:
    None
    """

    N             = len(prop.radius_distribution)
    airfoil_data  = prop.airfoil_data
    a_sec         = prop.airfoil_polar_stations
    for i in range(N):
        airfoil_station_header = '\nSection ' + str(i) + ' X, Y\n'
        vsp_bem.write(airfoil_station_header)

        airfoil_x     = airfoil_data.x_coordinates[int(a_sec[i])]
        airfoil_y     = airfoil_data.y_coordinates[int(a_sec[i])]

        for j in range(len(airfoil_x)):
            section_text = format(airfoil_x[j], '.7f')+ ", " + format(airfoil_y[j], '.7f') + "\n"
            vsp_bem.write(section_text)
    return
