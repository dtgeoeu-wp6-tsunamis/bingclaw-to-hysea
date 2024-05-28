"""
Script to launch a bingclaw simulation 

Input needed:
 - bingclaw_input_dir       Name of directory with BingClaw input files
 - bingclaw_output_dir      Name of parent directory where BingClaw output folder will be saved
 - bathymetry               Bathymetry file used in BingClaw simulations
 - scenario                 Simulation name (same name as the .tt3 files describing initial conditions)
 - image_type               Type of image: 'docker' or 'singularity'
 - image_name               Name of BingClaw docker image or singularity .sif file

Created by V. Magni (NGI)
"""
import os 
import sys
import shutil
from pyutil import filereplace

def run_bingclaw(input_dir, output_dir, bathymetry, scenario, image_type, image_name):
    print(f"** Executing run_bingclaw")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        print(f"Directory {output_dir} for scenario {scenario} already exists, results will be overwritten")

    # Copy setrun.py in output scenario folder and change names of files required to run the simualtion
    setrun_template_file = os.path.join(input_dir, 'setrun_template.py')
    setrun_file = os.path.join(output_dir, 'setrun.py')
    cp = shutil.copy(setrun_template_file, setrun_file)
    filereplace(setrun_file, 'BATHYMETRY', bathymetry)
    filereplace(setrun_file, 'SCENARIO', scenario)

    # Copy required files in output scenario folder
    input_file = os.path.join(input_dir, scenario)
    cp = shutil.copy(input_file, os.path.join(output_dir, scenario))
    cp = shutil.copy(os.path.join(input_dir, bathymetry), os.path.join(output_dir, bathymetry))
    
    # Run bingclaw simulation
    tomount = os.path.join(os.getcwd(),output_dir)
    if image_type == 'docker':
        command = f"docker run --rm -it -v {tomount}:/BingClaw/run {dockerimage_name}"
        os.system(command)
    elif image_type == 'singularity':
        command = f"singularity exec -B {tomount}:/BingClaw/run --cleanenv {image_name} ./run_simulation.sh"   
        os.system(command)
    else:
        print(f"{image_type} is not a valid image_type. Options are 'docker' or 'singularity'")


