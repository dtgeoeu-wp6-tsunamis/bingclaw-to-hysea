# Workflow from Bingclaw to T-HySEA
**WORK IN PROGRESS**

Mini worflow that goes from running a landslide simulation with the code [BingClaw](https://github.com/norwegian-geotechnical-institute/BingCLAW_5.6.1) to running a tsunami simulation with the code [Tsunami-HySEA](https://github.com/edanya-uma/Tsunami-HySEA).   
This workflow uses the [Interface Module](https://github.com/dtgeoeu-wp6-tsunamis/Interface-module) to convert the output of BingClaw to inputs readable by T-HySEA: it interpolates the ground deformation coming from the landslide model to a new bathymetry that is used in the tsunami simulation, and, optionally, it applies the Kajiura filter to the ground deformation.

The workflow follows the steps:
 - set up parameters, paths, flags to run the different modules
 - run BingClaw simulation
 - run interface module 
 - run T-HySEA simulation
   
The workflow needs the following input files:
 - For BingClaw: a bathymetry file (e.g., inputs/bingclaw_inputs/localMessinaBathy.tt3)   
 - For BingClaw: an initialisation file (e.g., inputs/bingclaw_inputs/mscen*.tt3)
 - For BingClaw: A configuration file for setting up relevant parameters  (this file is created by the workflow using the template inputs/bingclaw_inputs/setrun_template.py)   
 - For BingClaw (only for singularity): a .sh script with commands to run inside the container (run_simulations.sh)
 - For T-HySEA: a bathymetry file (e.g., inputs/hysea/MessinaGEBCO_forHySEA_HR.nc). The spatial domain of this bathymetry needs to be larger than that used in the BingClaw simulation.   
 - For T-HySEA: a parameter file (this file is created by the workflow using the template inputs/hysea_inputs/hysea_input.template) 
 - TODO: for T-HySEA: add file for time series and option in thw workflow to use time series (change other parameters in the input file for HySEA)
    
   
## Instructions   
 1. Clone this repo and load the submodule Interface-module
 ```
 git clone git@github.com:dtgeoeu-wp6-tsunamis/bingclaw-to-hysea.git
 git submodule update --init --recursive
 ```

### *Set up the environment and check the requirements*
2. Set up the python environment. If you use Poetry, you can simply type `poetry install` inside the repo directory to install the necessary python packages. Alternatively, check the list of python packages in the requirements below and install them.
3. Check the rest of the requirements below. This workflow includes running codes that have a lot of requirements. It uses Docker or Singularity to run BingClaw, which makes it possible to run it on any PC or clsuter. However, Tsunami-HySEA uses CUDA-capable GPUs, which means that an image of HySEA would need to be specific for the cluster you are using. Therefore, at the moment, this workflow assumes T-HySEA is installed on the cluster you are using.   

### *Prepare files* 
4. Make sure you have all the input files needed. Change parameters in the bingclaw and hysea template files, if needed. Note that the workflow will take care of inserting the right file names, so you do not need to change that now. However, if there is any other parameter (e.g., simualtion time, friction values, ...) that you want to change, do so in the template.
5. Open the file `run_workflow.py` and set names and parameters in the section INPUT PARAMETERS

### *Run the workflow*
6. Run the workflow with the following command
```
python run_workflow.py
```   
At the end of the run, you should have an output directory with the name of the scenario and with subdirectories where the output of BingClaw, Interface Module, and T-HySEA are stored. You can see the structure of the repo and of the input/output files below.

## Requirements
### *Python packages*   
[List of python packages](https://github.com/dtgeoeu-wp6-tsunamis/Interface-module?tab=readme-ov-file#required-python-packages) needed by the Interface Module.    
Other python pacakges needed:   
- python-util

### *Requirements for running BingClaw*
BingClaw runs inside either a docker or a singularity container. Therefore, [Docker Desktop](https://docs.docker.com/) or [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/index.html) need to be installed in the system where you run the workflow.   

A docker image of BingClaw can be found in the packages section of the dtgeoeu-wp6-tsunamis organisation. Please note that you need to be a member of the organisation to be able to see it and download it.

If you are using Docker, you can pull the BingClaw docker image with the command :
```
docker pull ghcr.io/dtgeoeu-wp6-tsunamis/bingclaw:latest
```
If you are using Singularity, you can pull the same image, but using a command that will convert the docker image to a singularity one, creating a .sif file:
```
singularity pull --docker-login docker://ghcr.io/dtgeoeu-wp6-tsunamis/bingclaw:latest
```
### *Requirements for running Tsunami-HySEA*
Tsunami-HySEA needs to run on system with CUDA-capable GPUs, needs openMPI and NetCDF. The CINECA cluster Leonardo can be used, as well as any other cluster with T-HySEA is already installed (e.g., Mare Nostrum, Power9, Mercalli, David@NGI, ...). On Leonardo, a compiled version of T-HySEA is available for DTGEO-WP6 memebers and istructions on how to set up the environment and how to use it can be found [here](https://dtgeoeu-wp6-tsunamis.github.io/dt-geo-wp6-docs/Tsunami-HySEA/leonardo/).

## Structure of repository
The structure of this repo and of the Input/Output directories is:
```
 bingclaw-to-hysea
 | - inputs
 |   | - bingclaw_inputs
 |   |   | - bathymetry
 |   |   | - setrun_template.py
 |   |   | - scenario1.tt3
 |   |   | - scenario2.tt3
 |   |   | - ...
 |   | - hysea_inputs
 |   |   | - bathymetry
 |   |   | - hysea_input.template
 | - outputs
 |   | - scenario1 (will be created at run time)
 |   |   | - bingclaw_out
 |   |   |   | - bingclaw output files
 |   |   | - intmod_out
 |   |   |   | - interface module output files
 |   |   | - hysea_out
 |   |   |   | - bingclaw output files
 |   | - scenario2 (will be created at run time)
 |   |   | - bingclaw_out
 |   |   |   | - bingclaw output files
 |   |   | - intmod_out
 |   |   |   | - interface module output files
 |   |   | - hysea_out
 |   |   |   | - bingclaw output files
 |   | - ...
 | - py
 |   | - run_bingclaw.py
 |   | - run_interface_module.py
 |   | - run_hysea.py
 | - run_workflow.py
 | - pyproject.toml
 | - run_simulation.sh (needed only for running BingClaw with Singularity)
 ```

