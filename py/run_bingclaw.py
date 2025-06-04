"""
Script to launch a bingclaw simulation 

Input needed:
 - bingclaw_input_dir       Name of directory with BingClaw input files
 - bingclaw_output_dir      Name of directory where BingClaw outputs will be saved
 - bathymetry               Bathymetry file used in BingClaw simulations
 - scenario                 Simulation name (same name as the .tt3 files describing initial conditions)
 - box                      [Lon min, Lon max, Lat min, Lat max] Geographic coordinates of computational domain
 - resolution               Grid resolution in m
 - image_type               Type of image: 'docker' or 'singularity'
 - image_name               Name of BingClaw docker image or singularity .sif file

Created by V. Magni (NGI)
"""
import os 
import sys
import shutil
from pyutil import filereplace
from math import radians, cos, sin, asin, sqrt, ceil


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    distance_m = 6371* c * 1000
    return distance_m

def run_bingclaw(input_dir, output_dir, bathymetry, scenario, box, resolution, image_type, image_name):
    print(f"* Executing run_bingclaw")
    
    # Create BingClaw output directory inside the scenario output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        print(f"Directory {output_dir} for scenario {scenario} already exists, results will be overwritten")

    # Compute x and y size of the computational domain
    mid_lon = (box[1] - box[0])/2 + box[0]
    mid_lat = (box[3] - box[2])/2 + box[2]
    x_size = haversine(box[0],mid_lat,box[1],mid_lat)
    y_size = haversine(mid_lon,box[2],mid_lon,box[3])

    # Compute number of cells along x and y
    x_cells = ceil(x_size/resolution)
    y_cells = ceil(y_size/resolution)
    print(f"Bingclaw computation domain is {x_size}x{y_size}m; Number of cells: x={x_cells}, y={y_cells}")

    # Copy template input (setrun.py) in the scenario/bingclaw output directory 
    # and insert paths/names of files required to run the simualtion
    setrun_template_file = os.path.join(input_dir, 'setrun_template.py')
    setrun_file = os.path.join(output_dir, 'setrun.py')
    cp = shutil.copy(setrun_template_file, setrun_file)
    filereplace(setrun_file, 'BATHYMETRY', bathymetry)
    filereplace(setrun_file, 'SCENARIO', scenario)
    filereplace(setrun_file, 'LONMIN', str(box[0]))
    filereplace(setrun_file, 'LONMAX', str(box[1]))
    filereplace(setrun_file, 'LATMIN', str(box[2]))
    filereplace(setrun_file, 'LATMAX', str(box[3]))
    filereplace(setrun_file, 'X_CELLS', str(int(x_cells)))
    filereplace(setrun_file, 'Y_CELLS', str(int(y_cells)))

    # Copy required files in output scenario folder
    input_file = os.path.join(input_dir, scenario)
    cp = shutil.copy(input_file, os.path.join(output_dir, scenario))
    cp = shutil.copy(os.path.join(input_dir, bathymetry), os.path.join(output_dir, bathymetry))

    # Run bingclaw simulation
    tomount = os.path.join(os.getcwd(),output_dir)
    if image_type == 'docker':
        command = f"docker run --rm -it -v {tomount}:/BingClaw/run {dockerimage_name}"
        os.system(command)
    elif image_type == 'singularity':
        command = f"singularity exec -B {tomount}:/BingClaw/run --cleanenv {image_name} ./run_simulation.sh"   
        os.system(command)
    else:
        print(f"{image_type} is not a valid image_type. Options are 'docker' or 'singularity'")


