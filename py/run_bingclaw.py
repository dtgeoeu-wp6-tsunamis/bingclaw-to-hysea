"""
Script to launch a bingclaw simulation 

Created by V. Magni (NGI)
"""
import os 
import sys
import shutil
from pyutil import filereplace

def run_bingclaw(io_path, scen_input_path, scen_output_path, bathymetry, scenario, dockerimage_name):
    print(f"Running BingClaw simulation {scenario}")
    
    # Create output folder for scenario
    scenario_dir = os.path.join(scen_output_path, scenario)
    if not os.path.exists(scenario_dir):
        os.makedirs(scenario_dir)
    else:
        print(f"WARNING: {scenario_dir} already exists, results will be overwritten")

    
    # Copy setrun.py in output scenario folder and change names of required files
    setrun_template_file = os.path.join(io_path, 'setrun_template.py')
    setrun_file = os.path.join(scenario_dir, 'setrun.py')
    cp = shutil.copy(setrun_template_file, setrun_file)
    filereplace(setrun_file, 'BATHYMETRY', bathymetry)
    filereplace(setrun_file, 'SCENARIO', scenario + '.tt3')

    # Copy required files in output scenario folder
    input_file = os.path.join(scen_input_path, (scenario + '.tt3'))
    cp = shutil.copy(input_file, os.path.join(scenario_dir, (scenario + '.tt3')))
    cp = shutil.copy(os.path.join(io_path, bathymetry),os.path.join(scenario_dir, bathymetry))
    
    # Run bingclaw simulation
    tomount = os.path.join(os.getcwd(),scenario_dir)
    command = f"docker run --rm -it -v {tomount}:/BingClaw/run {dockerimage_name}"
    os.system(command)