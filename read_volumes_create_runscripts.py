"""
Main script to launch landslide and tsunami simualtions from a list of release volumes

- Reads the .csv file with the list of release volumes to run in BingClaw
- Runs BingClaw, the interface module, and T-HySEA for each release volume in the list
- Copies output to P disk (for NGI only)

Created by V. Magni (NGI)
"""

import os 
import sys
import subprocess
import pandas as pd
from my_run_workflow_func import my_run_workflow_func

volumes_dir = "/home/vmg/NGI/P/2022/02/20220296/Calculations/release-volume-sampler_20250806_kl1558/messina_20250806/volumes/"
filename = os.path.join(volumes_dir,"volume_representatives.csv")
bingclaw_release_volume_dir = os.path.join(volumes_dir, 'rasters')

output_dir = "/home/vmg/SIM_OUT"   # Parent directory where results are stored (output_dir/scenario_dir) before copying them on P 
output_dir_P = "/home/vmg/NGI/P/2022/02/20220296/Calculations/Messina_simulations_August2025/" # Parent directory on P where results will be moved 

bingclaw_resolution = 40

df = pd.read_csv(filename, usecols=["id", "seed_triangles","LONLO", "LONHI", "LATLO", "LATHI"])

#torun = [7,8,10,11,19,24,25,31,38,46,48,50,52]
for i in range(0,len(df)): #torun:
    # Get id of the scenario
    scenario = str(int(df["id"][i]))
    # Get name of raster file with volume to input to BingClaw
    s = df["seed_triangles"][i][1:-1]
    tr_all = s.split(', ')
    name_seed_triangles = "-".join(str(x) for x in tr_all)
    bingclaw_scenario = "volume_id-" + str(int(df["id"][i])) + "_seed-" + name_seed_triangles + "-crop.asc"
    # Get coordinates of the computational domain for BingClaw
    bingclaw_box = [df["LONLO"][i], df["LONHI"][i], df["LATLO"][i], df["LATHI"][i]]
    
    print(f"Running workflow for scenario {scenario}")
    scenario_dir = os.path.join(output_dir, scenario)

    # Run workflow: bingclaw, interface module, T-HySEA
    my_run_workflow_func(scenario, scenario_dir, bingclaw_release_volume_dir, bingclaw_scenario, bingclaw_box, bingclaw_resolution)

    # Copy scenario folder from david to P and delete it on david
    command = f"cp -r {scenario_dir} {output_dir_P}"
    subprocess.run(command, shell=True, check=True)
    command = f"rm -r {scenario_dir}"
    subprocess.run(command, shell=True, check=True)    

