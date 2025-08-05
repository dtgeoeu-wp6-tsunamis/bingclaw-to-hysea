# Read release volumes and crete run_workflow scripts
import os 
import sys
import pandas as pd
from my_run_workflow_func import my_run_workflow_func

volumes_dir = "../../release-volume-sampler_20250602_kl1242/volumes/"
filename = os.path.join(volumes_dir,"Clusters_sorted_by_volume.csv")
bingclaw_release_volume_dir = os.path.join(volumes_dir, 'rasters')

bingclaw_resolution = 40

df = pd.read_csv(filename, usecols=["id", "seed_triangle","seed_triangle2","LONLO", "LONHI", "LATLO", "LATHI"])
for i in range(4,len(df)):
    scenario = str(df["id"][i])
    bingclaw_scenario = "volume_id-" + str(df["id"][i]) + "_seed-" + str(df["seed_triangle"][i]) + "-" + str(df["seed_triangle2"][i]) + ".asc"
    
    bingclaw_box = [df["LONLO"][i], df["LONHI"][i], df["LATLO"][i], df["LATHI"][i]]
    print(f"Running workflow for scenario {scenario}")
    my_run_workflow_func(scenario, bingclaw_release_volume_dir, bingclaw_scenario, bingclaw_box, bingclaw_resolution)
