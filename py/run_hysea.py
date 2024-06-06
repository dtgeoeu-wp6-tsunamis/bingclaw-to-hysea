"""
Script to launch a T-HySEA simulation 

Input needed:
 - hysea_input_dir      # Name of directory with T-HySEA input files (containing input file template and orignial bathymetry)
 - hysea_output_dir     # Name of directory where T-HySEA outputs will be saved 
 - intmod_output_dir    # Interface Module output directory
 - hysea_executable     # Full path of location of T-HySEA executable
 - scenario             # Simulation name
 - casename_from_intmod # Casename used in Interface Module to identify filter and resolution used for a specific scenario

Created by V. Magni (NGI)
"""

import os 
import sys
import shutil
from pyutil import filereplace

# TODO: WORK IN PROGRESS
def run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, hysea_executable, output_time_series, pois_file, scenario, casename_from_intmod):
    print("* Executing run_hysea")

    # Check that Interface Module output directory exists
    if not os.path.exists(intmod_output_dir):
        sys.exit(f"run_hysea cannot read output from Interface Module because {intmod_output_dir} does not exist")

    # Create T-HySEA output directory inside the scenario output directory
    if not os.path.exists(hysea_output_dir):
        os.makedirs(hysea_output_dir)
    else:
        print(f"Directory {hysea_output_dir} already exists")
    
    # Get names of files created by the Interface Module 
    dir_list = os.listdir(intmod_output_dir)
    bathy = [x for x in dir_list if ('bathymetry' in x and casename_from_intmod in x)][0]
    bathymetry = os.path.join(intmod_output_dir, bathy)
    deform = [x for x in dir_list if ('deformation' in x and casename_from_intmod in x)][0]
    deformation = os.path.join(intmod_output_dir, deform)

    # Copy template input file in the scenario/hysea output directory 
    # and insert paths/names of files required to run the simualtion
    if output_time_series:
        hysea_template_file = os.path.join(hysea_input_dir, 'hysea_input_ts.template') 
        pois_file_full = os.path.join(hysea_input_dir, pois_file)
    else:
        hysea_template_file = os.path.join(hysea_input_dir, 'hysea_input.template') 

    hysea_outname = os.path.join(hysea_output_dir,casename_from_intmod)
    hysea_input_file = os.path.join(hysea_output_dir, (casename_from_intmod + '.txt'))
    cp = shutil.copy(hysea_template_file, hysea_input_file)
    filereplace(hysea_input_file, 'BATHYMETRY', bathymetry)
    filereplace(hysea_input_file, 'SCENARIO_NAME', scenario)
    filereplace(hysea_input_file, 'HYSEA_OUTNAME', hysea_outname)
    filereplace(hysea_input_file, 'DEFORMATION_FILE', deformation)
    if output_time_series:
        filereplace(hysea_input_file, 'POIS_FILE', pois_file_full)
    
    # Run T-HySEA simulation
    command = f"echo {hysea_input_file} > 'simulations.txt'; mpirun -np 1 {hysea_executable} 'simulations.txt'"
    os.system(command)
