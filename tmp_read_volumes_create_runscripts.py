# Read release volumes and crete run_workflow scripts
import os 
import sys
import pandas as pd
from tmp_my_run_workflow_func import tmp_my_run_workflow_func

#volumes_dir = "../../release-volume-sampler_20250602_kl1242/volumes/"
#filename = os.path.join(volumes_dir,"Clusters_sorted_by_volume.csv")
volumes_dir = "../../testing-release-volume-sampler/messina_maxnseed200_maxnsim4/volumes/"
filename = os.path.join(volumes_dir,"volumes.csv")
bingclaw_release_volume_dir = os.path.join(volumes_dir, 'rasters')

bingclaw_resolution = 40

#df = pd.read_csv(filename, usecols=["id", "seed_triangle","seed_triangle2","LONLO", "LONHI", "LATLO", "LATHI"])
df = pd.read_csv(filename, usecols=["id", "seed_triangles","LONLO", "LONHI", "LATLO", "LATHI"])

torun = [68]
for i in torun: #range(444,501):#,len(df)):
    scenario = str(int(df["id"][i]))
    s = df["seed_triangles"][i][1:-1]
    tr_all = s.split(', ')
    name_seed_triangles = "-".join(str(x) for x in tr_all)
    bingclaw_scenario = "volume_id-" + str(int(df["id"][i])) + "_seed-" + name_seed_triangles + "-crop.asc"
    #bingclaw_scenario = "volume_id-" + str(df["id"][i]) + "_seed-" + str(df["seed_triangle"][i]) + "-" + str(df["seed_triangle2"][i]) + ".asc"
    print(bingclaw_scenario) 
    bingclaw_box = [df["LONLO"][i], df["LONHI"][i], df["LATLO"][i], df["LATHI"][i]]
    print(f"Running workflow for scenario {scenario}")
    tmp_my_run_workflow_func(scenario, bingclaw_release_volume_dir, bingclaw_scenario, bingclaw_box, bingclaw_resolution)
