# Read release volumes and crete run_workflow scripts
import os 
import sys
import pandas as pd
from tmp_my_run_workflow_func import tmp_my_run_workflow_func

volumes_dir = "../../release-volume-sampler_20250602_kl1242/volumes/"
filename = os.path.join(volumes_dir,"Clusters_sorted_by_volume.csv")
bingclaw_release_volume_dir = os.path.join(volumes_dir, 'rasters')

bingclaw_resolution = 40

df = pd.read_csv(filename, usecols=["id", "seed_triangle","seed_triangle2","LONLO", "LONHI", "LATLO", "LATHI"])
#idx_to_run = [92,105,107,120,133,136,258,263,302,311,323,337,347,365,380,383,395,396,399,443]
idx_to_run = [399]

#for i in range(453,len(df)):
for i in idx_to_run:
    scenario = str(int(df["id"][i]))

    bingclaw_scenario = "volume_id-" + str(int(df["id"][i])) + "_seed-" + str(int(df["seed_triangle"][i])) + "-" + str(int(df["seed_triangle2"][i])) + ".asc"
    
    bingclaw_box = [df["LONLO"][i], df["LONHI"][i], df["LATLO"][i], df["LATHI"][i]]
    print(f"Running workflow for scenario {scenario}")
    tmp_my_run_workflow_func(scenario, bingclaw_release_volume_dir, bingclaw_scenario, bingclaw_box, bingclaw_resolution)
