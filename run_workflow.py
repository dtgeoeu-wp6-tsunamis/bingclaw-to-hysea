"""
Script to launch the workflow following the steps:
    - set up parameters, paths, flags to run the different modules
    - run BingClaw simulation
    - run interface module (takes output from BingClaw simulation and creates inputs for HySEA)
    - run T-HySEA simulation


Created by V. Magni (NGI)
"""

import os 
import sys

from py.run_interface_module import run_interface_module
from py.run_bingclaw import run_bingclaw

# Set BingClaw input paths and parameters
# TODO: What else needs to be changed in the setup_run.py that is simulation-dependent? 
#       For now I only change the name of the files from the template, but for sure other parameters need to be changed too
do_run_bingclaw = False                 # Run BingClaw simulation (True/False)
io_bingclaw_path = 'IO_bingclaw'       # Parent directory for BingClaw files
bathymetry = 'localMessinaBathy.tt3'            # Bathymetry file used in BingClaw simulations
scenario = 'mscen_v0.141_x0_15.471_y0_38.004'   # Simulations name (same name as the .tt3 files describing initial conditions)
scen_input_dir =  'scenarios_input'   # Name of directory where simualtion input files (.tt3) describing initial conditions are stored
scen_output_dir = 'scenarios_output'  # Name of directory where simulation directory output will be created
image_type = 'singularity'      # 'docker' # Type of image (docker/singularity)
image_name = 'bingclaw_latest.sif'           #'ngiacr.azurecr.io/bingclaw:latest'  # Name of BingClaw docker image

# Set Interface Module flags
do_run_interface_module = True                  # Run Interface Module (True/False)
io_intmod_path = 'IO_interface_module'          # Parent directory for interface module files
donor = 'bingclaw'
donor_output = os.path.join(io_bingclaw_path, scen_output_dir, scenario) # Bingclaw scenario output directory
bathy_file = 'MessinaGEBCO_forHySEA_HR.nc'      # Bathymetry file for interface module (where results of BingCalw are interpolated on)
resolution = 100                                # Resolution (m)
filter_type = 'kajiura'                         # Filter for deformation data (kajiura / none)
casename = os.path.join(io_intmod_path,scenario)   # String used to name output files from Interface Module (including directory where files are saved)

# Run BingClaw
if (do_run_bingclaw):
    run_bingclaw(io_bingclaw_path, scen_input_dir, scen_output_dir, bathymetry, scenario, image_type, image_name)
else:
    print('Skip running BingClaw simulation because do_run_bingclaw is set to False')

# Run interface module
if (do_run_interface_module):
    run_interface_module(io_intmod_path, donor, donor_output, bathy_file, resolution, filter_type, casename)
else:
    print('Skip running Interface Module because do_run_interface_module is set to False')

# Run HySEA
# run_HySEA()

print("Done")

