"""
Script to launch the interface module 

Input needed:
 - bingclaw_output_dir   # Bingclaw scenario output directory
 - intmod_output_dir     # Interface module output directory
 - hysea_input_dir       # Input folder of HySEA (needed to get bathymetry file for interpolation: bathy_file)
 - donor                 # Flag for interface module: 'bingclaw'
 - bathy_file            # Bathymetry file for interface module (where results of BingClaw are interpolated on)
 - resolution            # Flag for interface module: Resolution (m)
 - filter_type           # Flag for interface module: Filter for deformation data (kajiura / none)
 - casename              # Flag for interface module: String used to name output files from Interface Module (including directory where files are saved)

Created by V. Magni (NGI)
"""
import os 
import sys


def run_interface_module(bingclaw_output_dir, intmod_output_dir, hysea_input_dir, donor, bathy_file, resolution, filter_type, casename):
    print("*** Exectuing run_interface_module")
    
    if not os.path.exists(bingclaw_output_dir):
        sys.exit(f"Interface module cannot read BingClaw output because {bingclaw_output_dir} does not exist")

    if not os.path.exists(intmod_output_dir):
        os.makedirs(intmod_output_dir)
    else:
        print(f"Directory {intmod_output_dir} for scenario {scenario} already exists, results will be overwritten")

    bathymetry = os.path.join(hysea_input_dir, bathy_file)
    
    tolaunch = os.path.join(os.getcwd(),'Interface-module','interface_module.py')
    command = f"python {tolaunch} --donor {donor} {bingclaw_output_dir} {bathymetry} \
                --resolution {resolution} --filter {filter_type} --casename {casename}"
    os.system(command)

