"""
Script to launch the interface module 

Created by V. Magni (NGI)
"""
import os 
import sys


def run_interface_module(io_intmod_path, donor, donor_output, bathy_file, resolution, filter, casename):
    print("Running Interface module")
    
    bathymetry = os.path.join(io_intmod_path, bathy_file)
    
    tolaunch = os.path.join(os.getcwd(),'Interface-module','interface_module.py')
    command = f"python {tolaunch} --donor {donor} {donor_output} {bathymetry} \
                --resolution {resolution} --filter {filter} --casename {casename}"
    os.system(command)

