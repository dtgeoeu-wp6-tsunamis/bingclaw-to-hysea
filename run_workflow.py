"""
Script to launch the workflow following the steps:
    - set up parameters, paths, flags to run the different modules
    - run BingClaw simulation
    - run interface module (takes output from BingClaw simulation and creates inputs for HySEA)
    - run T-HySEA simulation

The structure of this repo and of the Input/Output directories is:
 bingclaw-to-hysea
 | - inputs
 |   | - bingclaw_inputs
 |   |   | - bathymetry
 |   |   | - setrun_template.py
 |   |   | - scenario1.tt3
 |   |   | - scenario2.tt3
 |   |   | - ...
 |   | - hysea_inputs
 |   |   | - bathymetry
 |   |   | - hysea_input.template
 | - outputs
 |   | - scenario1 (will be created at run time)
 |   |   | - bingclaw_out
 |   |   |   | - bingclaw output files
 |   |   | - intmod_out
 |   |   |   | - interface module output files
 |   |   | - hysea_out
 |   |   |   | - bingclaw output files
 |   | - scenario2 (will be created at run time)
 |   |   | - bingclaw_out
 |   |   |   | - bingclaw output files
 |   |   | - intmod_out
 |   |   |   | - interface module output files
 |   |   | - hysea_out
 |   |   |   | - bingclaw output files
 |   | - ...
 | - py
 |   | - run_bingclaw.py
 |   | - run_interface_module.py
 |   | - run_hysea.py
 | - run_workflow.py
 | - pyproject.toml
 | - run_simulation.sh (needed only for running BingClaw with Singularity)

Created by V. Magni (NGI)
"""

import os 
import sys

from py.run_interface_module import run_interface_module
from py.run_bingclaw import run_bingclaw
from py.run_hysea import run_hysea

# ============  INPUT PARAMETERS  ============
# Set folder and file names
scenario   = 'mscen_v0.141_x0_15.471_y0_38.004'   # Simulation name
input_dir  = 'inputs'        # Parent directory with input files for BingClaw and T-HySEA
output_dir = 'outputs'       # Parent directory where scenario output folder will be created

scenario_dir = os.path.join(output_dir, scenario)                 # Scenario output directory
bingclaw_output_dir = os.path.join(scenario_dir, 'bingclaw_out')  # Directory where BingClaw outputs will be saved
intmod_output_dir = os.path.join(scenario_dir, 'intmod_out')      # Directory where Interface Module outputs will be saved
hysea_output_dir = os.path.join(scenario_dir, 'hysea_out')        # Directory where T-HySEA outputs will be saved

# For BingClaw 
# TODO: What else needs to be changed in the setup_run.py that is simulation-dependent? 
#       For now I only change the name of the files from the template, but for sure other parameters need to be changed too
do_run_bingclaw = True                 # Run BingClaw simulation (True/False)
bingclaw_input_dir = os.path.join(input_dir, 'bingclaw_inputs')     # Directory with BingClaw input files
bingclaw_bathymetry = 'localMessinaBathy.tt3'                       # Bathymetry file used in BingClaw simulations
bingclaw_scenario = scenario + '.tt3'                               # Name of .tt3 file describing initial conditions for BingClaw simulation
image_type = 'singularity'      # 'docker' # Type of image (docker/singularity)
image_name = 'bingclaw_latest.sif'           #'ngiacr.azurecr.io/bingclaw:latest'  # Name of BingClaw docker image

# For Interface Module 
do_run_interface_module = True                  # Run Interface Module (True/False)
donor = 'bingclaw'
bathy_file = 'MessinaGEBCO_forHySEA_HR.nc'      # Bathymetry file for interface module (where results of BingClaw are interpolated on)
resolution = 100                                # Resolution (m)
filter_type = 'kajiura'                         # Filter for deformation data (kajiura / none)
casename = os.path.join(intmod_output_dir, scenario)   # String used to name output files from Interface Module (including directory where files are saved)

# For T-HySEA 
do_run_hysea = False                 # Run T-HySEA (True/False)
hysea_input_dir = os.path.join(input_dir, 'hysea_inputs')     # Directory with HySEA useful files


# ============  RUN WORKFLOW  ============ 
print(f"\n* Running workflow bingclaw-to-hysea for scenario {scenario}")

# Create parent scenario directory for storing outputs
if not os.path.exists(scenario_dir):
    os.makedirs(scenario_dir)
else:
    print(f"WARNING: The output folder {scenario_dir} already exists, results will be overwritten")

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
    run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, scenario)
else:
    print('Skip running T-HySEA simulation because do_run_hysea is set to False')


print("Done")

