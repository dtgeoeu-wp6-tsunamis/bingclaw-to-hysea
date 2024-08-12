"""
Script to remove the first timestep of the ground deformation output file
that comes out of the interface module. 
The ground deformation output file will be overvritten. 

Input needed:
 - intmod_output_dir    # Interface Module output directory
 - casename_from_intmod # Casename used in Interface Module to identify filter and resolution used for a specific scenario

Created by V. Magni (NGI)
"""

import os
from netCDF4 import Dataset
from datetime import datetime

def remove_first_timestep(intmod_output_dir, casename_from_intmod):
    print("* Executing remove_first_timestep")    
    
    # Get names of files created by the Interface Module
    dir_list = os.listdir(intmod_output_dir)
    deform = [x for x in dir_list if ('deformation' in x and casename_from_intmod in x)][0]
    deformation = os.path.join(intmod_output_dir, deform)
    print(f"Input filename: {deformation}.")
    donor = 'bingclaw'
    
    # Open files for reading and writing
    with Dataset(filename=deformation, mode='r', format='NETCDF4') as dsin:
        with Dataset(filename='tempfile', mode='w', format='NETCDF4') as dsout:
            dsout.title =  dsin.title
            today = datetime.today()
            dsout.history = f"{dsin.history}. Removed first timestep {today.strftime('%d/%m/%y')}."
            dsout.description = dsin.description 
          
            #Copy dimensions
            for dname, the_dim in dsin.dimensions.items():
                dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)
            
            # Copy variables
            for v_name, varin in dsin.variables.items():
                outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)
                outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
                
                # Remove the first timestep
                if v_name == 'time': 
                    dsout['time'][:] = dsin['time'][:-1]
                elif v_name == 'z':
                    dsout['z'][:] = dsin['z'][1:]
                else:
                    outVar[:] = varin[:]
                
    # Overwrite input file.
    command = "mv tmpfile " + deformation 
    os.system(command)
    print(f"* File {deformation} has been overwritten; first timestep output has been removed")

