"""
Script to launch the interface module 

Input needed:
 - io_intmod_path      # Parent directory for interface module files
 - donor               # Flag for interface module: 'bingclaw'
 - donor_output        # Bingclaw scenario output directory
 - bathy_file          # Bathymetry file for interface module (where results of BingCalw are interpolated on)
 - resolution          # Flag for interface module: Resolution (m)
 - filter_type         # Flag for interface module: Filter for deformation data (kajiura / none)
 - casename            # Flag for interface module: String used to name output files from Interface Module (including directory where files are saved)

Created by V. Magni (NGI)
"""
import os 
import sys


def run_interface_module(io_intmod_path, donor, donor_output, bathy_file, resolution, filter_type, casename):
    print("Running Interface module")
    
    bathymetry = os.path.join(io_intmod_path, bathy_file)
    
    tolaunch = os.path.join(os.getcwd(),'Interface-module','interface_module.py')
    command = f"python {tolaunch} --donor {donor} {donor_output} {bathymetry} \
                --resolution {resolution} --filter {filter_type} --casename {casename}"
    os.system(command)

