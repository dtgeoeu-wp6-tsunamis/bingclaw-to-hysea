"""
Script to launch a bingclaw simulation 

Input needed:
 - shaltop_input_dir       Name of directory with Shaltop input files
 - shaltop_output_dir      Name of directory where Shaltop outputs will be saved
 - bathymetry              Bathymetry file used in Shaltop simulations
 - scenario                Simulation name (same name as the .z files describing initial conditions)
 - image_type              Type of image: 'docker' or 'none'
 - image_name              Name of Shaltop docker image if type of image is set to 'docker'

Created by V. Magni (NGI)
"""
import os 
import sys
import shutil
from py.utils import filereplace

def run_shaltop(executable, input_dir, output_dir, bathymetry, proj, time, scenario, image_type, image_name):
    print(f"* Executing run_shaltop")
    
    # Create Shaltop output directory inside the scenario output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        # Create the default directory data2 for Shaltop output files
        os.makedirs(output_dir+'/data2')
    else:
        print(f"Directory {output_dir} for scenario {scenario} already exists, results will be overwritten")

    grid = proj[1:-1].split(",")

    xmax = float(grid[5])-float(grid[3])
    ymax = float(grid[6])-float(grid[4])

    # Copy template input (params.txt) in the scenario/shaltop output directory 
    # and insert paths/names of files required to run the simualtion
    params_template_file = os.path.join(input_dir, 'params_template.txt')
    params_file = os.path.join(output_dir, 'params.txt')
    cp = shutil.copy(params_template_file, params_file)
    filereplace(params_file, 'BATHYMETRY', bathymetry)
    filereplace(params_file, 'SCENARIO', scenario)
    filereplace(params_file, 'OUTPUT', output_dir)
    filereplace(params_file, 'FINALTIME', time[0])
    filereplace(params_file, 'NBIM', time[1])
    filereplace(params_file, 'NX', grid[0])
    filereplace(params_file, 'NY', grid[1])
    filereplace(params_file, 'XMAX', xmax)
    filereplace(params_file, 'YMAX', ymax)

    # Copy required files in output scenario folder
    input_file = os.path.join(input_dir, scenario)
    cp = shutil.copy(input_file, os.path.join(output_dir, scenario))
    cp = shutil.copy(os.path.join(input_dir, bathymetry), os.path.join(output_dir, bathymetry))
    
    # Run bingclaw simulation
    #tomount = os.path.join(os.getcwd(),output_dir)
    if image_type == 'docker':
        #command = f"docker run --rm -it -v {tomount}:/BingClaw/run {dockerimage_name}"
        #os.system(command)
        print(f"{image_type} is not implemented for now for Shaltop. Please use 'none' option to run Shaltop on the local environment. Skipping the Shaltop run...")
    elif image_type == 'none':
        command = f"{executable} {output_dir} > {output_dir}/shaltop.log"   
        os.system(command)
    else:
        print(f"{image_type} is not a valid image_type. Options are 'docker' or 'none'")


