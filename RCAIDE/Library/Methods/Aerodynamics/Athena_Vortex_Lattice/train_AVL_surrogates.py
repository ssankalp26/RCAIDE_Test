# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/train_VLM_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core import Units, Data, redirect  
from RCAIDE.Framework.Mission.Common    import Results 
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.write_geometry           import write_geometry
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.write_mass_file          import write_mass_file
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.write_run_cases          import write_run_cases
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.write_input_deck         import write_input_deck
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.run_analysis             import run_analysis
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.translate_data           import translate_conditions_to_cases, translate_results_to_conditions 
from RCAIDE.Library.Methods.Geometry.Planform.populate_control_sections                 import populate_control_sections   
from RCAIDE.Library.Components.Wings.Control_Surfaces import Aileron , Elevator , Slat , Flap , Rudder 
 
# Package imports 
import os
import numpy as np
import sys  
from shutil import rmtree   

# ----------------------------------------------------------------------------------------------------------------------
#  train_VLM_surrogates
# ---------------------------------------------------------------------------------------------------------------------- 
def train_VLM_surrogates(aerodynamics):
    """Call methods to run VLM for sample point evaluation. 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : VLM analysis          [unitless] 
        
    Returns: 
        None    
    """
 
 
 
 
    run_folder             = os.path.abspath(self.settings.filenames.run_folder)
    vehicle               = self.vehicle
    training               = self.training 
    trim_aircraft          = self.settings.trim_aircraft  
    AoA                    = training.angle_of_attack
    Mach                   = training.Mach
    side_slip_angle        = self.settings.side_slip_angle
    roll_rate_coefficient  = self.settings.roll_rate_coefficient
    pitch_rate_coefficient = self.settings.pitch_rate_coefficient
    lift_coefficient       = self.settings.lift_coefficient
    atmosphere             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data              = atmosphere.compute_values(altitude = 0.0)         
    
    len_AoA  =  len(AoA)
    len_Mach =  len(Mach)
    CM       = np.zeros((len_AoA,len_Mach))
    Cm_alpha = np.zeros_like(CM)
    Cn_beta  = np.zeros_like(CM)
    NP       = np.zeros_like(CM)

    # remove old files in run directory  
    if os.path.exists('avl_files'):
        if not self.settings.regression_flag:
            rmtree(run_folder)

    for i,_ in enumerate(Mach):
        # Set training conditions
        run_conditions = Results()
        run_conditions.freestream.density                  = atmo_data.density[0,0] 
        run_conditions.freestream.gravity                  = 9.81            
        run_conditions.freestream.speed_of_sound           = atmo_data.speed_of_sound[0,0]  
        run_conditions.freestream.velocity                 = Mach[i] * run_conditions.freestream.speed_of_sound
        run_conditions.freestream.mach_number              = Mach[i] 
        run_conditions.aerodynamics.side_slip_angle        = side_slip_angle
        run_conditions.aerodynamics.angle_of_attack        = AoA 
        run_conditions.aerodynamics.roll_rate_coefficient  = roll_rate_coefficient
        run_conditions.aerodynamics.lift_coefficient       = lift_coefficient
        run_conditions.aerodynamics.pitch_rate_coefficient = pitch_rate_coefficient

        # Run Analysis at AoA[i] and Mach[i]
        results =  self.evaluate_conditions(run_conditions, trim_aircraft)
 
        CL[:,i]       = results.aerodynamics.lift_coefficient[:,0]
        CD[:,i]       = results.aerodynamics.drag_breakdown.induced.total[:,0]      
        e [:,i]       = results.aerodynamics.drag_breakdown.induced.efficiency_factor[:,0]   
        CM[:,i]       = results.aerodynamics.Cmtot[:,0]
        Cm_alpha[:,i] = results.stability.static.Cm_alpha[:,0]
        Cn_beta[:,i]  = results.stability.static.Cn_beta[:,0]
        NP[:,i]       = results.stability.static.neutral_point[:,0]

    if self.training_file:
        # load data 
        data_array   = np.loadtxt(self.training_file)

        
        # convert from 1D to 2D        
        CL_1D         = np.atleast_2d(data_array[:,0]) 
        CD_1D         = np.atleast_2d(data_array[:,1])            
        e_1D          = np.atleast_2d(data_array[:,2])
        CM_1D         = np.atleast_2d(data_array[:,3]) 
        Cm_alpha_1D   = np.atleast_2d(data_array[:,4])            
        Cn_beta_1D    = np.atleast_2d(data_array[:,5])
        NP_1D         = np.atleast_2d(data_array[:,6])

        # convert from 1D to 2D
        CL        = np.reshape(CL_1D, (len_AoA,-1))
        CD        = np.reshape(CD_1D, (len_AoA,-1))
        e         = np.reshape(e_1D , (len_AoA,-1)) 
        CM        = np.reshape(CM_1D, (len_AoA,-1))
        Cm_alpha  = np.reshape(Cm_alpha_1D, (len_AoA,-1))
        Cn_beta   = np.reshape(Cn_beta_1D , (len_AoA,-1))
        NP        = np.reshape(NP_1D , (len_AoA,-1))

    # Save the data for regression 
    if self.settings.save_regression_results:
        # convert from 2D to 1D
        CL_1D       = CL.reshape([len_AoA*len_Mach,1]) 
        CD_1D       = CD.reshape([len_AoA*len_Mach,1])  
        e_1D        = e.reshape([len_AoA*len_Mach,1]) 
        CM_1D       = CM.reshape([len_AoA*len_Mach,1]) 
        Cm_alpha_1D = Cm_alpha.reshape([len_AoA*len_Mach,1])  
        Cn_beta_1D  = Cn_beta.reshape([len_AoA*len_Mach,1])         
        NP_1D       = Cn_beta.reshape([len_AoA*len_Mach,1]) 
        np.savetxt(vehicle.tag+'_stability_data.txt',np.hstack([CL_1D,CD_1D,e_1D,CM_1D,Cm_alpha_1D, Cn_beta_1D,NP_1D ]),fmt='%10.8f',header='   CM       Cm_alpha       Cn_beta       NP ')

    # Store training data
    # Save the data for regression
    training_data = np.zeros((4,len_AoA,len_Mach))
    training_data[0,:,:] = CL 
    training_data[1,:,:] = CD 
    training_data[2,:,:] = e  
    training_data[3,:,:] = CM       
    training_data[4,:,:] = Cm_alpha 
    training_data[5,:,:] = Cn_beta  
    training_data[6,:,:] = NP      

    # Store training data
    training.coefficients = training_data
    
    
def evaluate_conditions(self,run_conditions, trim_aircraft ):
    """Process vehicle to setup avl geometry, condititons, and configurations.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    run_conditions <RCAIDE data type> aerodynamic conditions; until input
            method is finalized, will assume mass_properties are always as 
            defined in self.features

    Outputs:
    results        <RCAIDE data type>

    Properties Used:
    self.settings.filenames.
      run_folder
      output_template
      batch_template
      deck_template
    self.current_status.
      batch_index
      batch_file
      deck_file
      cases
    """           
    
    # unpack
    run_folder                       = os.path.abspath(self.settings.filenames.run_folder)
    run_script_path                  = run_folder.rstrip('avl_files').rstrip('/')   
    aero_results_template_1          = self.settings.filenames.aero_output_template_1       # 'stability_axis_derivatives_{}.dat' 
    aero_results_template_2          = self.settings.filenames.aero_output_template_2       # 'surface_forces_{}.dat'
    aero_results_template_3          = self.settings.filenames.aero_output_template_3       # 'strip_forces_{}.dat'      
    aero_results_template_4          = self.settings.filenames.aero_output_template_4       # 'body_axis_derivatives_{}.dat' 
    dynamic_results_template_1       = self.settings.filenames.dynamic_output_template_1    # 'eigen_mode_{}.dat'
    dynamic_results_template_2       = self.settings.filenames.dynamic_output_template_2    # 'system_matrix_{}.dat'
    batch_template                   = self.settings.filenames.batch_template
    deck_template                    = self.settings.filenames.deck_template 
    print_output                     = self.settings.print_output 

    # rename defaul avl aircraft tag
    self.tag                         = 'avl_analysis_of_{}'.format(self.geometry.tag) 
    self.settings.filenames.features = self.geometry._base.tag + '.avl'
    self.settings.filenames.mass_file= self.geometry._base.tag + '.mass'
    
    # update current status
    self.current_status.batch_index += 1
    batch_index                      = self.current_status.batch_index
    self.current_status.batch_file   = batch_template.format(batch_index)
    self.current_status.deck_file    = deck_template.format(batch_index)
           
    # control surfaces
    num_cs       = 0
    cs_names     = []
    cs_functions = [] 
    control_surfaces = False
    
    for wing in self.geometry.wings: # this parses through the wings to determine how many control surfaces does the vehicle have 
        if wing.control_surfaces:
            control_surfaces = True 
            wing = populate_control_sections(wing)     
            num_cs_on_wing = len(wing.control_surfaces)
            num_cs +=  num_cs_on_wing
            for cs in wing.control_surfaces:
                ctrl_surf = cs    
                cs_names.append(ctrl_surf.tag)  
                if (type(ctrl_surf) ==  Slat):
                    ctrl_surf_function  = 'slat'
                elif (type(ctrl_surf) ==  Flap):
                    ctrl_surf_function  = 'flap' 
                elif (type(ctrl_surf) ==  Aileron):
                    ctrl_surf_function  = 'aileron'                          
                elif (type(ctrl_surf) ==  Elevator):
                    ctrl_surf_function  = 'elevator' 
                elif (type(ctrl_surf) ==  Rudder):
                    ctrl_surf_function = 'rudder'                      
                cs_functions.append(ctrl_surf_function)  

    # translate conditions
    cases                            = translate_conditions_to_cases(self,run_conditions)    
    for case in cases:
        case.stability_and_control.number_control_surfaces = num_cs
        case.stability_and_control.control_surface_names   = cs_names
    self.current_status.cases                              = cases  
     
    for case in cases:  
        case.aero_result_filename_1     = aero_results_template_1.format(case.tag)        # 'stability_axis_derivatives_{}.dat'  
        case.aero_result_filename_2     = aero_results_template_2.format(case.tag)        # 'surface_forces_{}.dat'
        case.aero_result_filename_3     = aero_results_template_3.format(case.tag)        # 'strip_forces_{}.dat'          
        case.aero_result_filename_4     = aero_results_template_4.format(case.tag)        # 'body_axis_derivatives_{}.dat'            
        case.eigen_result_filename_1    = dynamic_results_template_1.format(case.tag)     # 'eigen_mode_{}.dat'
        case.eigen_result_filename_2    = dynamic_results_template_2.format(case.tag)     # 'system_matrix_{}.dat'
    
    # write the input files
    with redirect.folder(run_folder,force=False):
        write_geometry(self,run_script_path)
        write_mass_file(self,run_conditions)
        write_run_cases(self,trim_aircraft)
        write_input_deck(self, trim_aircraft,control_surfaces)

        # RUN AVL!
        results_avl = run_analysis(self,print_output)

    # translate results
    results = translate_results_to_conditions(cases,results_avl)

    if not self.settings.keep_files:
        rmtree( run_folder )
        
    return results    