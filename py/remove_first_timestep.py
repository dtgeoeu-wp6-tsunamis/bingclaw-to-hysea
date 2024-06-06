"""
Script to remove the first timestep of the ground deformation output file
that comes out of the interface module. 
The ground deformation output file will be overvritten. 

Input needed:
 - intmod_output_dir    # Interface Module output directory
 - casename_from_intmod # Casename used in Interface Module to identify filter and resolution used for a specific scenario

Created by V. Magni (NGI)
"""

import sys, os
import numpy as np
import h5py
from netCDF4 import Dataset
from datetime import datetime

def remove_first_timestep(intmod_output_dir, casename_from_intmod):
    print("* Executing remove_first_timestep")    
    
    # Get names of files created by the Interface Module
    dir_list = os.listdir(intmod_output_dir)
    deform = [x for x in dir_list if ('deformation' in x and casename_from_intmod in x)][0]
    deformation = os.path.join(intmod_output_dir, deform)
    
    res2 = h5py.File(deformation, 'r')
                 
    x = res2['x']
    y = res2['y']
    bingclaw_def = res2['z'][1:]
    time2 = res2['time'][:-1]

    donor = 'bingclaw'
    ds = Dataset('tmpfile', 'w', format='NETCDF4')
    ds.title = f"{donor} model outputs converted to a structured mesh by interpolation"
    ds.history = "File written using netCDF4 Python module"
    today = datetime.today()
    ds.description = "Created " + today.strftime("%d/%m/%y")
    Nrow = len(y)
    Ncolumn = len(x)
    Ntime = np.shape(bingclaw_def)[0]

    lon_dim = ds.createDimension('x', Ncolumn)
    lat_dim = ds.createDimension('y', Nrow)
    time_dim = ds.createDimension('time', None)
  
    time = ds.createVariable('time', 'f4', ('time',))
    time.units = 'time step'
    latitude = ds.createVariable('y', 'f8', ('y',))
    latitude.units = 'degrees north (WGS84)'
    latitude.long_name = 'latitude'
    longitude = ds.createVariable('x', 'f8', ('x',))
    longitude.units = 'degrees east (WGS84)'
    longitude.long_name = 'longitude'
    longitude[:] = x
    latitude[:] = y

    z = ds.createVariable('z', 'f4', ('time', 'y', 'x'))
  
    for t in range(Ntime):
      time[t] = time2[t]
      z[t,:,:] = bingclaw_def[t]
  
    ds.close()

    command = "mv tmpfile " + deformation 
    os.system(command)
    print(f"* File {deformation} has been overwritten; first timestep output has been removed")

