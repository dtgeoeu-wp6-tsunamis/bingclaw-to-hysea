"""
Script to launch the workflow following the steps:
    - set up parameters, paths, flags to run the different modules
    - run BingClaw simulation
    - run interface module (takes output from BingClaw simulation and creates inputs for HySEA)
    - run T-HySEA simulation

For the structure of the input/output directories see README file of the this repo.

Created by V. Magni (NGI)
"""

import os 
import sys

from py.run_interface_module import run_interface_module
from py.run_bingclaw import run_bingclaw
from py.run_hysea import run_hysea

# ============  INPUT PARAMETERS  ============
# Set folder and file names
# Parameters marked with *** in the comment are the bare minimum for the 
# user to check and change 
scenario   = 'mscen_v0.141_x0_15.471_y0_38.004'   # ***Simulation name
input_dir  = 'inputs'        # Parent directory with input files for BingClaw and T-HySEA
output_dir = 'outputs'       # Parent directory where scenario output folder will be created

scenario_dir = os.path.join(output_dir, scenario)                 # Scenario output directory
bingclaw_output_dir = os.path.join(scenario_dir, 'bingclaw_out')  # Directory where BingClaw outputs will be saved
intmod_output_dir = os.path.join(scenario_dir, 'intmod_out')      # Directory where Interface Module outputs will be saved
hysea_output_dir = os.path.join(scenario_dir, 'hysea_out')        # Directory where T-HySEA outputs will be saved

# For BingClaw 
# TODO: What else needs to be changed in the setup_run.py that is simulation-dependent? 
#       For now I only change the name of the files from the template, but for sure other parameters need to be changed too
do_run_bingclaw = True                  # Run BingClaw simulation (True/False)
bingclaw_input_dir = os.path.join(input_dir, 'bingclaw_inputs')     # Directory with BingClaw input files
bingclaw_bathymetry = 'localMessinaBathy.tt3'                       # ***Bathymetry file used in BingClaw simulations
bingclaw_scenario = scenario + '.tt3'                               # ***Name of .tt3 file describing initial conditions for BingClaw simulation
image_type = 'singularity'              # ***Type of image (docker/singularity)
image_name = 'bingclaw_latest.sif'      # ***Name of BingClaw docker image     #'ngiacr.azurecr.io/bingclaw:latest'  

# For Interface Module 
do_run_interface_module = True                  # Run Interface Module (True/False)
donor = 'bingclaw'
bathy_file = 'MessinaGEBCO_forHySEA_HR.nc'      # ***Bathymetry file for interface module (where results of BingClaw are interpolated on)
resolution = 100                                # ***Resolution (m)
filter_type = 'none'                            # ***Filter for deformation data (kajiura / none)
filename_prefix = 'filter' + filter_type + '_res' + str(resolution) # Prefix used by Interface Module to name output files
casename = os.path.join(intmod_output_dir, filename_prefix)         # Add path of directory where output is saved to prefix string

# For T-HySEA 
do_run_hysea = True                 # Run T-HySEA (True/False)
hysea_input_dir = os.path.join(input_dir, 'hysea_inputs')     # Directory with HySEA useful files
hysea_executable = '/home/vmg/T-HySEA_4.0.0_MC/build/TsunamiHySEA'  # ***Full path of location of T-HySEA executable
casename_from_intmod = filename_prefix

# ============  RUN WORKFLOW  ============ 
print(f"\n* Running workflow bingclaw-to-hysea for scenario '{scenario}' with filter '{filter_type}' and resolution {resolution} m")

# Create parent scenario directory for storing outputs
if not os.path.exists(scenario_dir):
    os.makedirs(scenario_dir)
else:
    print(f"WARNING: The output folder {scenario_dir} already exists")

# Run BingClaw
if (do_run_bingclaw):
    run_bingclaw(bingclaw_input_dir, bingclaw_output_dir, bingclaw_bathymetry, bingclaw_scenario, image_type, image_name)
else:
    print('Skip running BingClaw simulation because do_run_bingclaw is set to False')

# Run interface module
if (do_run_interface_module):
    run_interface_module(bingclaw_output_dir, intmod_output_dir, hysea_input_dir, donor, bathy_file, resolution, filter_type, casename)
else:
    print('Skip running Interface Module because do_run_interface_module is set to False')

# Run T-HySEA
if (do_run_hysea):
    run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, hysea_executable, scenario, casename_from_intmod)
else:
    print('Skip running T-HySEA simulation because do_run_hysea is set to False')


print(f"\n* Done running workflow bingclaw-to-hysea for scenario '{scenario}' with filter '{filter_type}' and resolution {resolution} m")
print(f"* BingClaw outputs are stored in {bingclaw_output_dir}")
print(f"* Interface Module outputs are stored in {intmod_output_dir} and have prefix '{filename_prefix}'")
print(f"* T-HySEA outputs are stored in {hysea_output_dir} and have prefix '{filename_prefix}'")

