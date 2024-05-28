"""
Script to launch a bingclaw simulation 

Input needed:
 - io_path          Name of parent directory for BingClaw Input-Output files and folders
 - bathymetry       Bathymetry file used in BingClaw simulations
 - scenario         Simulations name (same name as the .tt3 files describing initial conditions)
 - scen_input_dir   Name of directory where simualtion input files (.tt3) describing initial conditions are stored
 - scen_output_dir  Name of directory where simulation directory output will be created
 - image_type       Type of image: 'docker' or 'singularity'
 - image_name       Name of BingClaw docker image or singularity .sif file

An example of how the Input/Output directory for BingClaw files and folders is:
 io_path
 | - scen_input_dir
 |   | - scenario1.tt3
 |   | - scenario2.tt3
 |   | - ...
 | - scen_output_dir
 |   | - scenario1 (will be created at run time)
 |   |   | - bingclaw output files
 |   | - scenario2 (will be created at run time)
 |   |   | - bingclaw output files
 |   | - ...
 |   |   | - bingclaw output files
 | - bathymetry
 | - setrun_template.py

Created by V. Magni (NGI)
"""
import os 
import sys
import shutil
from pyutil import filereplace

def run_bingclaw(io_path, scen_input_dir, scen_output_dir, bathymetry, scenario, image_type, image_name):
    print(f"Preparing files to run BingClaw simulation {scenario}")
    
    # Create output folder for scenario
    scenario_dir = os.path.join(io_path, scen_output_dir, scenario)
    if not os.path.exists(scenario_dir):
        os.makedirs(scenario_dir)
    else:
        print(f"WARNING: {scenario_dir} already exists, results will be overwritten")

    
    # Copy setrun.py in output scenario folder and change names of files required to run the simualtion
    setrun_template_file = os.path.join(io_path, 'setrun_template.py')
    setrun_file = os.path.join(scenario_dir, 'setrun.py')
    cp = shutil.copy(setrun_template_file, setrun_file)
    filereplace(setrun_file, 'BATHYMETRY', bathymetry)
    filereplace(setrun_file, 'SCENARIO', scenario + '.tt3')

    # Copy required files in output scenario folder
    input_file = os.path.join(io_path, scen_input_dir, (scenario + '.tt3'))
    cp = shutil.copy(input_file, os.path.join(scenario_dir, (scenario + '.tt3')))
    cp = shutil.copy(os.path.join(io_path, bathymetry),os.path.join(scenario_dir, bathymetry))
    
    # Run bingclaw simulation
    tomount = os.path.join(os.getcwd(),scenario_dir)
    if image_type == 'docker':
        command = f"docker run --rm -it -v {tomount}:/BingClaw/run {dockerimage_name}"
        os.system(command)
    elif image_type == 'singularity':
        command = f"singularity exec -B {tomount}:/BingClaw/run --cleanenv {image_name} ./run_simulation.sh"   
        os.system(command)
    else:
        print(f"{image_type} is not a valid image_type. Options are 'docker' or 'singularity'")


