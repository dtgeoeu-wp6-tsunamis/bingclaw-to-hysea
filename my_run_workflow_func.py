"""
Function to launch landslide and tsunami simualtions following the steps:
    - set up parameters, paths, flags to run the different modules
    - run BingClaw simulation
    - run interface module (takes output from BingClaw simulation and creates inputs for HySEA)
      and remove first time step of the interface module (ground deformation) output
    - run T-HySEA simulation

Inputs needed:
- scenario: id of the scenario to run
- scenario_dir: path of the directory where the outputs are stored (created at run time if not present)
- bingclaw_release_volume_dir: string with path of the directory where release volume raster files are
- bingclaw_scenario: string with name of the release volume raster file
- bingclaw_box: array with coordinates of the computational domain for BingClaw simualtions (geographic)
- bingclaw_resolution: resolution of BingClaw grid (m)

For the structure of the input/output directories see README file of the this repo.

Created by V. Magni (NGI)
"""

def my_run_workflow_func(scenario, scenario_dir, bingclaw_release_volume_dir, bingclaw_scenario, bingclaw_box, bingclaw_resolution):
    import os 
    import sys
    import subprocess

    from py.run_interface_module import run_interface_module
    from py.run_bingclaw import run_bingclaw
    from py.run_hysea import run_hysea
    from py.set_first_timestep_to_zero import set_first_timestep_to_zero

    # ============  INPUT PARAMETERS  ============
    # Set folder and file names
    # Parameters marked with *** in the comment are the bare minimum for the 
    # user to check and change 
    input_dir  = 'inputs'        # Parent directory with input files for BingClaw and T-HySEA

    bingclaw_output_dir = os.path.join(scenario_dir, 'bingclaw_out')  # Directory where BingClaw outputs will be saved
    intmod_output_dir = os.path.join(scenario_dir, 'intmod_out')      # Directory where Interface Module outputs will be saved
    hysea_output_dir = os.path.join(scenario_dir, 'hysea_out')        # Directory where T-HySEA outputs will be saved

    # For BingClaw   
    do_run_bingclaw = True                  # Run BingClaw simulation (True/False)
    bingclaw_input_dir = os.path.join(input_dir, 'bingclaw_inputs')     # Directory with BingClaw input files
    bingclaw_bathymetry = 'GEBCO2024_100m_15_1650_36_3840.tt3'  # ***Bathymetry file used in BingClaw simulations
    image_type = 'singularity'              # ***Type of image (docker/singularity)
    image_name = '/home/vmg/bingclaw-to-hysea-old/bingclaw_latest.sif'      # ***Name of BingClaw docker image     #'ngiacr.azurecr.io/bingclaw:latest'  

    # For Interface Module 
    do_run_interface_module = True                  # Run Interface Module (True/False)
    donor = 'bingclaw'
    bathy_file = 'GEBCO2024_100m_15_1650_36_3840.nc' #'MessinaGEBCO_forHySEA_HR.nc'   # ***Bathymetry file for interface module (where results of BingClaw are interpolated on)
    resolution = 100                                # ***Resolution (m)
    filter_type = 'kajiura'                            # ***Filter for deformation data (kajiura / none)
    filename_prefix = 'filter' + filter_type + '_res' + str(resolution) # Prefix used by Interface Module to name output files
    casename = os.path.join(intmod_output_dir, filename_prefix)         # Add path of directory where output is saved to prefix string

    # For T-HySEA 
    do_run_hysea = True                  # Run T-HySEA (True/False)
    hysea_input_dir = os.path.join(input_dir, 'hysea_inputs')     # Directory with HySEA useful files
    hysea_executable = '/home/vmg/T-HySEA_4.0.0_MC/build/TsunamiHySEA'  # ***Full path of location of T-HySEA executable
    casename_from_intmod = filename_prefix
    output_time_series = True           # ***Output time series. If true, template hysea_input.template is used; if False, hysea_input_ts.template
    pois_file = 'messina_tms_HySEA.txt' # 'Messina_pois_1411_1650_3575_3840.dat'      # ***Name of file with list of POIs for storing time series (relevant if output_time_series is True)

    # ============  RUN WORKFLOW  ============ 
    print(f"\n* Running workflow bingclaw-to-hysea for scenario '{scenario}' with filter '{filter_type}' and resolution {resolution} m")

    # Create parent scenario directory for storing outputs
    if not os.path.exists(scenario_dir):
        os.makedirs(scenario_dir)
    else:
        print(f"WARNING: The output folder {scenario_dir} already exists")

    # Run BingClaw
    if (do_run_bingclaw):
        run_bingclaw(bingclaw_input_dir, bingclaw_release_volume_dir, bingclaw_output_dir, bingclaw_bathymetry, bingclaw_scenario, bingclaw_box, bingclaw_resolution, image_type, image_name)
        command = f"rm {bingclaw_output_dir}/fort.a*"
        subprocess.run(command, shell=True, check=True)
    else:
        print('Skip running BingClaw simulation because do_run_bingclaw is set to False')

    # Run interface module
    if (do_run_interface_module):
        run_interface_module(bingclaw_output_dir, intmod_output_dir, hysea_input_dir, donor, bathy_file, resolution, filter_type, casename, casename_from_intmod)
    else:
        print('Skip running Interface Module because do_run_interface_module is set to False')

    # Run T-HySEA
    if (do_run_hysea):
        run_hysea(hysea_input_dir, hysea_output_dir, intmod_output_dir, hysea_executable, output_time_series, pois_file, scenario, casename_from_intmod)
    else:
        print('Skip running T-HySEA simulation because do_run_hysea is set to False')


    print(f"\n* Done running workflow bingclaw-to-hysea for scenario '{scenario}' with filter '{filter_type}' and resolution {resolution} m")
    print(f"* BingClaw outputs are stored in {bingclaw_output_dir}")
    print(f"* Interface Module outputs are stored in {intmod_output_dir} and have prefix '{filename_prefix}'")
    print(f"* T-HySEA outputs are stored in {hysea_output_dir} and have prefix '{filename_prefix}' \n")

