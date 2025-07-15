"""
Script to launch the workflow following the steps:
    - set up parameters, paths, flags to run the different modules
    - run BingClaw simulation
    - run interface module (takes output from BingClaw simulation and creates inputs for HySEA)
    - remove first time step of the interface module (ground deformation) output
    - run T-HySEA simulation

For the structure of the input/output directories see README file of the this repo.

Created by V. Magni (NGI)
"""

import os 
import sys

from py.run_interface_module import run_interface_module
from py.run_bingclaw import run_bingclaw
from py.run_shaltop import run_shaltop
from py.run_hysea import run_hysea

# ============  INPUT PARAMETERS  ============
# Set folder and file names
# Parameters marked with *** in the comment are the bare minimum for the 
# user to check and change
# WARNING: absolute paths for input_dir and output_dir are preferred to avoid errors 
scenario   = 'scenario1'     # ***Simulation name
input_dir  = 'inputs'        # Parent directory with input files for BingClaw, Shaltop and T-HySEA
output_dir = 'outputs'       # Parent directory where scenario output folder will be created

scenario_dir = os.path.join(output_dir, scenario)                 # Scenario output directory
bingclaw_output_dir = os.path.join(scenario_dir, 'bingclaw_out')  # Directory where BingClaw outputs will be saved
shaltop_output_dir = os.path.join(scenario_dir, 'shaltop_out')  # Directory where Shaltop outputs will be saved
intmod_output_dir = os.path.join(scenario_dir, 'intmod_out')      # Directory where Interface Module outputs will be saved
hysea_output_dir = os.path.join(scenario_dir, 'hysea_out')        # Directory where T-HySEA outputs will be saved

# For BingClaw 
# TODO: What else needs to be changed in the setup_run.py that is simulation-dependent? 
#       For now I only change the name of the files from the template, but for sure other parameters need to be changed too
do_run_bingclaw = False                  # Run BingClaw simulation (True/False)
bingclaw_input_dir = os.path.join(input_dir, 'bingclaw_inputs')     # Directory with BingClaw input files
bingclaw_bathymetry = 'bathymetry.tt3'  # ***Bathymetry file used in BingClaw simulations
bingclaw_scenario = scenario + '.tt3'   # ***Name of .tt3 file describing initial conditions for BingClaw simulation
bingclaw_proj = 'epsg:4326'             # Projection parameters (in Proj4 format) for converting from Cartesian to geographic (lon, lat) coordinates
image_type = 'docker/singularity'       # ***Type of image (docker/singularity)
image_name = 'image_name'               # ***Name of BingClaw docker image     #'ngiacr.azurecr.io/bingclaw:latest'  

# For Shaltop
#       For now I only change the name of the files from the template, but for sure other parameters need to be changed too
do_run_shaltop = True                  # Run Shaltop simulation (True/False)
shaltop_exectuable = '/FULL_PATH_TO/shaltop_executable'
shaltop_input_dir = os.path.join(input_dir, 'shaltop_inputs')     # Directory with Shaltop input files
shaltop_bathymetry = 'bathymetry.d'  # ***Bathymetry file used in Shaltop simulations
# The projection parameter is different given the local coordinates (m) implemented by Shaltop.
# - Paramters nx,ny,xmax,xmin,ymin,ymax are the grid information used for the Shaltop simulation. xmax,xmin,ymax,ymin are local coordinates (m) given in localCRS. xmin = ymin = 0 in Shaltop.
# - For a conversion to geographic coordinates (lat, lon), we need the bounds of the box in the given localCRS
# The projection parameter for Shaltop is a string (the interface module needs a string) containing the list of Shaltop info
shaltop_proj = "[nx,ny,localCRS,xmin,ymin,xmax,ymax]"
shaltop_time = [tmax,nbim] # Final time tmax (s) and output number nbim for Shaltop: [tmax,nbim]. Shaltop outputs every tmax/nbim (s)
shaltop_scenario = scenario + '.d'   # ***Name of .d file describing initial conditions for Shaltop simulation
image_type = 'docker/none'             # ***Type of image (docker/none)
image_name = 'image_name'              # ***Name of Shaltop docker image 

# For Interface Module 
do_run_interface_module = False          # Run Interface Module (True/False)
donor = 'bingclaw/shaltop'
bathy_file = 'bathymetry.nc'            # ***Bathymetry file for interface module (where results of BingClaw are interpolated on)
resolution = XXX                        # ***Resolution (m)
filter_type = 'kajiura/none'            # ***Filter for deformation data (kajiura / none)
filename_prefix = 'filter' + filter_type + '_res' + str(resolution) # Prefix used by Interface Module to name output files
casename = os.path.join(intmod_output_dir, filename_prefix)         # Add path of directory where output is saved to prefix string

# For T-HySEA 
do_run_hysea = False                     # Run T-HySEA (True/False)
hysea_input_dir = os.path.join(input_dir, 'hysea_inputs')   # Directory with HySEA useful files
hysea_executable = '/FULL_PATH_TO/T-HySEA_executable'       # ***Full path of location of T-HySEA executable
casename_from_intmod = filename_prefix
output_time_series = True           # ***Output time series. If true, template hysea_input.template is used; if False, hysea_input_ts.template
pois_file = 'filename'              # ***Name of file with list of POIs for storing time series (relevant if output_time_series is True)

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
    donor_output_dir = bingclaw_output_dir
    donor_proj = bingclaw_proj
else:
    print('Skip running BingClaw simulation because do_run_bingclaw is set to False')

# Run Shaltop
if (do_run_shaltop):
    run_shaltop(shaltop_exectuable, shaltop_input_dir, shaltop_output_dir, shaltop_bathymetry, shaltop_grid, shaltop_scenario, image_type, image_name)
    donor_output_dir = shaltop_output_dir
    donor_proj = shaltop_proj
else:
    print('Skip running Shaltop simulation because do_run_shaltop is set to False')

# Run interface module
if (do_run_interface_module):
    run_interface_module(donor_output_dir, intmod_output_dir, hysea_input_dir, donor, donor_proj, bathy_file, resolution, filter_type, casename)
    if (do_run_bingclaw):
        remove_first_timestep(intmod_output_dir, casename_from_intmod)
else:
    print('Skip running Interface Module because do_run_interface_module is set to False')

# Run T-HySEA
if (do_run_hysea):
    run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, hysea_executable, output_time_series, pois_file, scenario, casename_from_intmod)
else:
    print('Skip running T-HySEA simulation because do_run_hysea is set to False')


print(f"\n* Done running workflow bingclaw-to-hysea for scenario '{scenario}' with filter '{filter_type}' and resolution {resolution} m")
print(f"* BingClaw outputs are stored in {bingclaw_output_dir}")
print(f"* Shaltop outputs are stored in {shaltop_output_dir}")
print(f"* Interface Module outputs are stored in {intmod_output_dir} and have prefix '{filename_prefix}'")
print(f"* T-HySEA outputs are stored in {hysea_output_dir} and have prefix '{filename_prefix}'")

