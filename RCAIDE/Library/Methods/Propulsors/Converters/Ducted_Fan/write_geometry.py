# RCAIDE/Library/Methods/Propulsor/Ducted_Fan_Propulsor/write_geometry.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Units 
from RCAIDE.Library.Methods.Geometry.Airfoil import  import_airfoil_geometry , compute_naca_4series
from .purge_files import purge_files   
import numpy as  np
 
# ---------------------------------------------------------------------------------------------------------------------- 
# Write Geometry 
# ---------------------------------------------------------------------------------------------------------------------- 
def write_geometry(dfdc_object,run_script_path):
    """This function writes the translated aircraft geometry into text file read 
    by DFDC when it is called 
    """     
    # unpack inputs 
    case_file   = dfdc_object.geometry.tag + '.case'   
    purge_files([case_file]) 
    geometry             = open(case_file,'w') 
    with open(case_file,'w') as geometry:
        make_header_text(dfdc_object,geometry)
        make_hub_text(dfdc_object,geometry)
        make_separator_text(dfdc_object,geometry)  
        make_duct_text(dfdc_object,geometry)
    return

def make_header_text(dfdc_object,geometry):  
    """This function writes the header using the template required for the DFDC executable to read
 
    """      
    header_1_text_template = \
'''DFDC Version  0.70 
Bladed rotor + actdisk stator test case                                             

OPER
!        Vinf         Vref          RPM          RPM
  {0}   {1}       {2}          0.0    
!         Rho          Vso          Rmu           Alt
   1.2260       340.00      0.17800E-04  0.00000E+00
!       XDwake        Nwake
  0.80000               20
!       Lwkrlx
            F
ENDOPER

AERO
!  #sections
     1
!   Xisection
  0.00000E+00
!       A0deg        dCLdA        CLmax         CLmin
  0.00000E+00   6.2800       1.5000      -1.0000    
!  dCLdAstall     dCLstall      Cmconst         Mcrit
  0.50000      0.20000      0.00000E+00  0.70000    
!       CDmin      CLCDmin     dCDdCL^2
  0.12000E-01  0.10000      0.50000E-02
!       REref        REexp
  0.20000E+06  0.35000    
ENDAERO

ROTOR
!       Xdisk        Nblds       NRsta
  {3}                {4}           {5}
!  #stations
    {6}
!           r        Chord         Beta
'''
    
    length                = dfdc_object.geometry.length
    x_disc_rotor          = dfdc_object.geometry.rotor.percent_x_location * length
    number_of_blades      = dfdc_object.geometry.number_of_rotor_blades 
    number_of_end_points  = dfdc_object.geometry.number_of_radial_stations + 1 
    number_of_stations    = dfdc_object.geometry.number_of_radial_stations  
    hub_radius            = dfdc_object.geometry.hub_radius
    clearance             = dfdc_object.geometry.blade_clearance
    design_RPM            = dfdc_object.geometry.cruise.design_angular_velocity /Units.rpm 
    tip_radius            = dfdc_object.geometry.tip_radius  
    V_inf                 = dfdc_object.geometry.cruise.design_freestream_velocity  
    V_ref                 = dfdc_object.geometry.cruise.design_reference_velocity  
    header_1_text         = header_1_text_template.format(V_inf,V_ref, design_RPM,x_disc_rotor,number_of_blades,number_of_end_points, number_of_stations)
   
    geometry.write(header_1_text)
    
    station_chords = np.linspace(0.4,0.3, number_of_stations)
    station_twists = np.linspace(77, 30, number_of_stations)
    station_radii  = np.linspace(hub_radius+clearance, tip_radius-clearance,number_of_stations )
    for i in range(number_of_stations): 
        station_radius = station_radii[i]
        station_chord  = station_chords[i] 
        station_twist  = station_twists[i]
        case_text = '  ' + format(station_radius, '.6f')+ "  " + format(station_chord, '.6f')+ "   " + format(station_twist, '.6f') + "\n" 
        geometry.write(case_text)
        
    header_2_text_template = \
'''ENDROTOR


AERO
!  #sections
     1
!   Xisection
  0.00000E+00
!       A0deg        dCLdA        CLmax         CLmin
  0.00000E+00   6.2800       1.0000      -1.5000    
!  dCLdAstall     dCLstall      Cmconst         Mcrit
  0.50000      0.20000      0.00000E+00  0.70000    
!       CDmin      CLCDmin     dCDdCL^2
  0.12000E-01 -0.10000      0.50000E-02
!       REref        REexp          TOC      dCDdCL^2
  0.20000E+06  0.35000      0.10000      0.20000E-01
ENDAERO

ACTDISK
! Xdisk   NRPdef
  {0}     15
! #stations
  3
! r     BGam
 0.02   -10.0
 0.06   -10.0
 0.10   -10.0
ENDACTDISK


DRAGOBJ
!  #pts
     4
!           x            r          CDA
  0.40000E-01  0.60000E-01  0.40000E-01
  0.40000E-01  0.80000E-01  0.35000E-01
  0.40000E-01  0.10000      0.30000E-01
  0.40000E-01  0.12000      0.30000E-01
ENDDRAGOBJ

'''
    x_disc_stator         = dfdc_object.geometry.stator.percent_x_location  * length  
    header_2_text         = header_2_text_template.format(x_disc_stator ) 
    geometry.write(header_2_text)     
    return  

def make_hub_text(dfdc_object,geometry):  
    """This function writes the rotor using the template required for the DFDC executable to read 
    """ 
    duct_header = \
'''GEOM
FatDuct + CB test case
''' 
    geometry.write(duct_header) 
    if len(dfdc_object.geometry.hub_geometry) > 0: 
        hub_filename = dfdc_object.geometry.airfoil
        hub_geometry = import_airfoil_geometry(hub_filename)      
    else: 
        hub_geometry =   np.array([[1.00000000e+00, 1.17266523e-01],[9.93570055e-01, 1.19658984e-01],
                                   [9.79097784e-01, 1.24590785e-01],[9.64028213e-01, 1.29081954e-01],[9.48612666e-01, 1.33014991e-01],[9.32772808e-01, 1.36406216e-01],[9.16479263e-01, 1.39278475e-01],
                                   [8.99777726e-01, 1.41641562e-01],[8.82788964e-01, 1.43508530e-01],[8.65552143e-01, 1.44879381e-01],[8.47956289e-01, 1.45770435e-01],[8.29384520e-01, 1.46217593e-01],
                                   [8.09040437e-01, 1.46344887e-01],[7.86845704e-01, 1.46351414e-01],[7.64030825e-01, 1.46374262e-01],[7.41062540e-01, 1.46406901e-01],[7.18064880e-01, 1.46429749e-01],
                                   [6.96242236e-01, 1.46449332e-01],[6.74413064e-01, 1.46472180e-01],[6.52574099e-01, 1.46491763e-01],[6.30735135e-01, 1.46514611e-01],[6.08899435e-01, 1.46537459e-01],
                                   [5.87063735e-01, 1.46557042e-01],[5.65221507e-01, 1.46579890e-01],[5.43392334e-01, 1.46599473e-01],[5.21566426e-01, 1.46622321e-01],[4.99747045e-01, 1.46645168e-01],
                                   [4.77947248e-01, 1.46668016e-01],[4.56167035e-01, 1.46684335e-01],[4.34445572e-01, 1.46710447e-01],[4.12903626e-01, 1.46733294e-01],[3.91671753e-01, 1.46733294e-01],
                                   [3.70208141e-01, 1.46785517e-01],[3.49958711e-01, 1.46883435e-01],[3.31096452e-01, 1.46746350e-01],[3.12208082e-01, 1.46243705e-01],[2.93420894e-01, 1.45417930e-01],
                                   [2.74937251e-01, 1.44265762e-01],[2.56704931e-01, 1.42761090e-01],[2.38750045e-01, 1.40894121e-01],[2.21108496e-01, 1.38655064e-01],[2.03793341e-01, 1.36021072e-01],
                                   [1.86811107e-01, 1.32982352e-01],[1.70256447e-01, 1.29542168e-01],[1.54155474e-01, 1.25684202e-01],[1.38527771e-01, 1.21388868e-01],[1.23432089e-01, 1.16662696e-01],
                                   [1.08936970e-01, 1.11505684e-01],[9.50946377e-02, 1.05911306e-01],[8.19671061e-02, 9.98926167e-02],[6.96229180e-02, 9.34561442e-02],[5.81240881e-02, 8.66214721e-02],
                                   [4.75391590e-02, 7.94081840e-02],[3.79203535e-02, 7.18423913e-02],[2.93231586e-02, 6.39534694e-02],[2.17802134e-02, 5.57707937e-02],[1.53306852e-02, 4.73074199e-02],
                                   [9.98436577e-03, 3.85894595e-02],[5.76083870e-03, 2.96201763e-02],[2.66989578e-03, 2.03571394e-02],[7.18064880e-04, 1.06795831e-02],[0.00000000e+00, 0.00000000e+00]]) 

    dim = len(hub_geometry)
    
    scaler =  dfdc_object.geometry.hub_radius / max(hub_geometry[:,1])
    for i in range(dim):
        x_coord  =  hub_geometry[i,0]*scaler  
        y_coord  =  hub_geometry[i,1]*scaler            
        case_text = '     ' + format(x_coord, '.6f')+ "    " + format(y_coord, '.6f') + "\n" 
        geometry.write(case_text)
              
    return


def make_separator_text(dfdc_object,geometry):  
    """This function writes the operating conditions using the template required for the DFDC executable to read 
    """      
    separator_text = \
'''  999.0 999.0
'''
    geometry.write(separator_text) 
    return


def make_duct_text(dfdc_object,geometry):  
    """This function writes the operating conditions using the template required for the DFDC executable to read
 
    """      
    if len(dfdc_object.geometry.duct_airfoil) > 0:
        airfoil_filename      = dfdc_object.geometry.airfoil.duct_airfoil
        airfoil_geometry_data = import_airfoil_geometry(airfoil_filename)
    else:  
        airfoil_geometry_data= compute_naca_4series('2208')    
    dim = len(airfoil_geometry_data.x_coordinates)

    x_coords  = airfoil_geometry_data.x_coordinates*dfdc_object.geometry.length 
    y_coords  = airfoil_geometry_data.y_coordinates*dfdc_object.geometry.length     
    offset    = abs(min(y_coords)) + dfdc_object.geometry.tip_radius
    for i in range(dim):  
        case_text = '     ' + format(x_coords[i], '.6f')+ "    " + format(y_coords[i] + offset, '.6f') + "\n" 
        geometry.write(case_text) 
    end_text = \
'''ENDGEOM
'''               
    geometry.write(end_text) 
    return  
 
