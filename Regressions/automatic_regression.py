# Regressions/Tests/automatic_regression.py

""" RCAIDE Automatic Regression Tests with pytest """

import pytest
import matplotlib.pyplot as plt
import matplotlib
import os
import sys
import traceback
import time

matplotlib.use('Agg')

# List of regression modules to test
modules = [ 
    'Tests/analysis_aerodynamics/airfoil_panel_method_test.py',    
    'Tests/analysis_aerodynamics/airfoil_panel_method_convergence.py',
    'Tests/analysis_aerodynamics/VLM_control_surface_test.py',    
    'Tests/analysis_aerodynamics/VLM_moving_surface_test.py',    
    'Tests/atmosphere/atmosphere.py',
    'Tests/atmosphere/constant_temperature.py',
    'Tests/analysis_emissions/emissions_test.py',   
    'Tests/analysis_noise/digital_elevation_test.py',  
    'Tests/analysis_noise/frequency_domain_test.py', 
    'Tests/analysis_noise/empirical_jet_noise_test.py',    
    'Tests/analysis_stability/trimmed_flight_test.py', 
    'Tests/analysis_stability/untrimmed_flight_test.py', 
    'Tests/analysis_weights/operating_empty_weight_test.py',
    'Tests/analysis_weights/cg_and_moi_test.py',
    'Tests/energy_sources/cell_test.py',
    'Tests/geometry/airfoil_import_test.py', 
    'Tests/geometry/airfoil_interpolation_test.py',    
    'Tests/geometry/wing_volume_test.py',
    'Tests/geometry/wing_fuel_volume_compute.py',
    'Tests/geometry/fuselage_planform_compute.py',    
    'Tests/mission_segments/transition_segment_test.py', 
    'Tests/network_electric/electric_btms_test.py', 
    'Tests/network_ducted_fan/electric_ducted_fan_network_test.py',
    'Tests/network_turbofan/turbofan_network_test.py',
    'Tests/network_turbojet/turbojet_network_test.py',
    'Tests/network_turboprop/turboprop_network_test.py',
    'Tests/network_turboshaft/turboshaft_network_test.py',
    'Tests/network_internal_combustion_engine/ICE_test.py',
    'Tests/network_internal_combustion_engine/ICE_constant_speed_test.py',
    'Tests/optimization/optimization_packages.py',
    'Tests/performance/landing_field_length.py',
    'Tests/performance/payload_range_test.py',
    'Tests/performance/take_off_field_length.py',
    'Tests/performance/take_off_weight_from_tofl.py',    
]

# Parametrize the list of modules so each is run as a separate test
@pytest.mark.parametrize("module_path", modules)
def test_automatic_regressions(module_path):
    """ Run the regressions listed in the modules """
    original_dir = os.getcwd()
    
    try:
        # Get regression directory (where this script is)
        regression_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(regression_dir)
        
        # Convert module_path to full path
        full_module_path = os.path.join(regression_dir, module_path)
        test_dir = os.path.dirname(full_module_path)
        module_name = os.path.basename(module_path)
        
        # Check if file exists
        if not os.path.exists(full_module_path):
            pytest.fail(f'File {full_module_path} does not exist')
        
        # Change to test directory and import module
        if test_dir:
            sys.path.append(test_dir)
            os.chdir(test_dir)
        
        # Import and run the test
        name = os.path.splitext(module_name)[0]
        module = __import__(name)
        module.main()  # Run the main function of the test
        
        # Cleanup
        plt.close('all')
    
    except Exception as exc:
        pytest.fail(f'Test failed for {module_path}\n{traceback.format_exc()}')

    finally:
        # Ensure cleanup and return to original directory
        os.chdir(original_dir)
