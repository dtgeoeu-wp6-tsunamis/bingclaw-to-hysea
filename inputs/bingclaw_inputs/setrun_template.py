""" 
Module to set up run time parameters for Clawpack -- AMRClaw code.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
""" 

from __future__ import absolute_import
from __future__ import print_function
import os
import numpy as np

# try:
#     CLAW = os.environ['CLAW']
# except:
#     raise Exception("*** Must first set CLAW enviornment variable")

#Parameters

rho_a = 1000.0        # Density of ambient fluid
rho_s = 1800.0        # Density of slide
n_param = .5          # Bing rheology parameter
gamma_r = 1e3        # Reference strain rate
c_mass = 0.1           # Added Mass
hydrodrag = True      # Use hydrodrag force?
cF_hyd = 0.001
cP_hyd = 0.25 
remolding = True     # remolding? if not, only tauy_i is used
tauy_i = 10000.0       # initial yield strength (Pa)
tauy_r = 2000.0       # residual yield strength (Pa)
remold_coeff = 1e-1  # remolding parameter

vel_tol = 0.001        # velocity tolerance for stopping
t_vel_tol = 60.      # velocity tolerance is imposed after this time

#Initial Condition
qinit_style = -3         # topotype style initial conditions
use_var_tau_y = False    # Setup the varialbe yield strength?
fname_tau_y = 'dummy.tt3'          # File for the variable



import os
import numpy as np

#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------
    
    """ 
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData 
    
    """ 
    
    from clawpack.clawutil import data 
    
    
    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------
    probdata = rundata.new_UserData(name='probdata',fname='setprob.data')
    probdata.add_param('rho_a'       ,  rho_a       ,'Density of ambient fluid')
    probdata.add_param('rho_s'       ,  rho_s       ,'Density of slide')
    probdata.add_param('n_param'     ,  n_param     ,'Bing rheology parameter')
    probdata.add_param('gamma_r'     ,  gamma_r     ,'Reference strain rate')
    probdata.add_param('c_mass'      ,  c_mass      ,'Added mass coeff.')
    probdata.add_param('hydrodrag'   ,  hydrodrag   ,'Hydrodrag?')
    probdata.add_param('cF_hyd'      ,  cF_hyd      ,'Hydrodrag coeff.')
    probdata.add_param('cP_hyd'      ,  cP_hyd      ,'Hydrodrag coeff.')
    probdata.add_param('remolding'   ,  remolding   ,'Remolding?')
    probdata.add_param('tauy_i'      ,  tauy_i      ,'Initial yield strength')
    probdata.add_param('tauy_r'      ,  tauy_r      ,'Residual yield strength')
    probdata.add_param('remold_coeff',  remold_coeff,'Remolding param. gamma')
    probdata.add_param('qinit_style' ,  qinit_style ,'Data style of the IC')
    probdata.add_param('vel_tol'     ,  vel_tol     ,'Velocity tolerance for stopping')
    probdata.add_param('t_vel_tol'   ,  t_vel_tol   ,'Time to apply velocity tolerance')
    probdata.add_param('use_var_tau_y',use_var_tau_y,'Use variablt tau_y?')
    probdata.add_param('fname_tau_y' ,  '../'+fname_tau_y   ,'File name for variable tau_y')

    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------
    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)
    
    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated

    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    #clawdata.lower[0] = 298000
    #clawdata.upper[0] = 299400
    #clawdata.lower[1] = 6667000 
    #clawdata.upper[1] = 6668500
    clawdata.lower[0] = 15.4
    clawdata.upper[0] = 15.7
    clawdata.lower[1] = 37.8 
    clawdata.upper[1] = 38.2

    # Number of grid cells: Coarsest grid
    # clawdata.num_cells[0] = 560
    # clawdata.num_cells[1] = 600
    clawdata.num_cells[0] = 300
    clawdata.num_cells[1] = 400

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 6

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 7
    
    # Index of aux array corresponding to capacity function, if there is one:
    # Capaindex = 0 for cartesian coordinates, 2 for spherical
    # clawdata.capa_index = 0
    clawdata.capa_index = 2
    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0
    

    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False              # True to restart from prior results
    clawdata.restart_file = 'fort.chk00018'  # File to use for restart data
    
    
    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
 
    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output ntimes frames at equally spaced times up to tfinal:
        # Can specify num_output_times = 0 for no output
        clawdata.num_output_times = 90
        clawdata.tfinal = 900
        clawdata.output_t0 = True  # output at initial (or restart) time?
        
    elif clawdata.output_style == 2:
        # Specify a list or numpy array of output times:
        # Include t0 if you want output at the initial time.
        clawdata.output_times = np.linspace(20,60,81)*60
 
    elif clawdata.output_style == 3:
        # Output every step_interval timesteps over total_steps timesteps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 3
        clawdata.output_t0 = True  # output at initial (or restart) time?
        

    clawdata.output_format == 'ascii'      # 'ascii', 'binary', 'netcdf'

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all'  # could be list
    clawdata.output_aux_onlyonce = False    # output aux arrays only at t0
    

    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:  
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 0    

    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==True:  variable time steps used based on cfl_desired,
    # if dt_variable==Falseixed time steps dt = dt_initial always used.
    clawdata.dt_variable = True
    
    # Initial time step for variable dt.  
    # (If dt_variable==0 then dt=dt_initial for all steps)
    clawdata.dt_initial = 0.016
    
    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99
    
    # Desired Courant number if variable dt used 
    clawdata.cfl_desired = 0.45

    # max Courant number to allow without retaking step with a smaller dt:
    clawdata.cfl_max = 0.5
    
    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 50000


    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 1
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 0
    
    # Number of waves in the Riemann solution:
    clawdata.num_waves = 6
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'vanleer'  ==> van Leer
    #   4 or 'mc'       ==> MC limiter
    clawdata.limiter = [4,4,4,4,4,4]
    
    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 1
    
    
    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2
    
    # Choice of BCs at xlower and xupper:
    #   0 or 'user'     => user specified (must modify bcNamr.f to use this option)
    #   1 or 'extrap'   => extrapolation (non-reflecting outflow)
    #   2 or 'periodic' => periodic (must specify this at both boundaries)
    #   3 or 'wall'     => solid wall for systems where q(2) is normal velocity
    
    clawdata.bc_lower[0] = 'extrap'   # at xlower
    clawdata.bc_upper[0] = 'extrap'   # at xupper

    clawdata.bc_lower[1] = 'extrap'   # at ylower
    clawdata.bc_upper[1] = 'extrap'   # at yupper
                  
       
    # ---------------
    # Gauges:
    # ---------------
    gauges = rundata.gaugedata.gauges
    # Landslide Area
    # gauges.append([1, 298214, 6669190, 0, 120])
    # gauges.append([2, 298214, 6669240, 0, 120])
    # gauges.append([3, 298214, 6669290, 0, 120])
    # gauges.append([4, 298314, 6669190, 0, 120])
    # gauges.append([5, 298314, 6669240, 0, 120])
    # gauges.append([6, 298314, 6669290, 0, 120])
    # gauges.append([7, 298400, 6669060, 0, 120])
    
    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 0

    if clawdata.checkpt_style == 0:
      # Do not checkpoint at all
      pass

    elif clawdata.checkpt_style == 1:
      # Checkpoint only at tfinal.
      pass

    elif clawdata.checkpt_style == 2:
      # Specify a list of checkpoint times.  
      clawdata.checkpt_times = [0.1,0.15]

    elif clawdata.checkpt_style == 3:
      # Checkpoint every checkpt_interval timesteps (on Level 1)
      # and at the final time.
      clawdata.checkpt_interval = 5

    # ---------------
    # AMR parameters:   (written to amr.data)
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 1

    # List of refinement ratios at each level (length at least amr_level_max-1)
    amrdata.refinement_ratios_x = [1,1]
    amrdata.refinement_ratios_y = [1,1]
    amrdata.refinement_ratios_t = [1,1]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length num_aux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).
    # Capacity input for cartesian coordinates:
    # amrdata.aux_type = ['center', 'center', 'yleft', 'center', 'center','center','center']
    # Here we use spherical coordinates:
    amrdata.aux_type = ['center', 'capacity', 'yleft', 'center', 'center','center','center']


    # Flag for refinement based on Richardson error estimater:
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag_richardson_tol = 1.0  # Richardson tolerance
    
    # Flag for refinement using routine flag2refine:
    amrdata.flag2refine = True      # use this?
    amrdata.flag2refine_tol = 0.5  # tolerance used in this routine
    # Note: in geoclaw the refinement tolerance is set as wave_tolerance below 
    # and flag2refine_tol is unused!

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3       

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.7

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0      


    # ---------------
    # Regions:
    # ---------------
    regions = rundata.regiondata.regions 
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    regions.append([1, 5, 0., 1e9, -1e9, 1e9, -1e9, 1e9]) #whole domain

    #  ----- For developers ----- 
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    return rundata

    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    """

    try:
        geo_data = rundata.geo_data
    except:
        print ("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")

    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system =  2  # 1 for cartesian, 2 for spherical
    geo_data.earth_radius = 6367500.0

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 0.001
    geo_data.friction_forcing = False
    geo_data.manning_coefficient = 0.0
    #geo_data.manning_coefficient = [0.025,0.04]
    #geo_data.manning_break = [0.]
    geo_data.friction_depth = 200.0

    # Refinement settings
    refinement_data = rundata.refinement_data
    refinement_data.variable_dt_refinement_ratios = False
    refinement_data.wave_tolerance = 0.02
    refinement_data.deep_depth = 2.0
    refinement_data.max_level_deep = 3

    # == settopo.data values ==
    topofiles = rundata.topo_data.topofiles
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fname]
    topofiles.append([3, 1, 1, 0., 1.e10, 'BATHYMETRY'])

    # == setdtopo.data values ==
    dtopofiles = rundata.dtopo_data.dtopofiles
    # for moving topography, append lines of the form :  
    #   [topotype, minlevel,maxlevel,fname]

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type =  1
    rundata.qinit_data.qinitfiles = []
    qinitfiles = rundata.qinit_data.qinitfiles
    qinitfiles.append([1,1,'SCENARIO'])
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == fixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    fixedgrids = rundata.fixed_grid_data.fixedgrids
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # == fgmax.data values ==
    fgmax_files = rundata.fgmax_data.fgmax_files
    # for fixed grids append to this list names of any fgmax input files
    #fgmax_files.append('fgmax_grid.txt')
    #fixedgrids.append([0.,1000.,101,0.,25000.,-10.,10.,1000+1,2,0,0])
    
    return rundata
    # end of function setgeo
    # ----------------------

if __name__ == '__main__':

    if os.path.exists('fgmax_grid.txt'):
        print ("File fgmax_grid.txt exists, not regenerating")
    else:
        try:    
            fname = 'make_fgmax_grid.py'
            execfile(fname)
            print ("Created fixed grid data by running ",fname)
        except:
            print ("Did not find fixed grid specification ", fname)


    # Set up run-time parameters and write all data fijles.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()
    

