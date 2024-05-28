"""
Script to launch a T-HySEA simulation 

Input needed:
 - hysea_input_dir
 - hysea_output_dir
 - intmod_output_dir
 - scenario


Created by V. Magni (NGI)
"""

import os 
import sys
# TODO: WORK IN PROGRESS
def run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, scenario):
    print("**** Exectuing run_hysea")

    if not os.path.exists(intmod_output_dir):
        sys.exit(f"run_hysea cannot read output from Interface Module because {intmod_output_dir} does not exist")

    if not os.path.exists(hysea_output_dir):
        os.makedirs(hysea_output_dir)
    else:
        print(f"Directory {hysea_output_dir} for scenario {scenario} already exists, results will be overwritten")