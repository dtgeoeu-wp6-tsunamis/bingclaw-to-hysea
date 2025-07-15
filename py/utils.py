def filereplace(file,toreplace,replace):
    # Read in the file
    sfile = str(file)
    storeplace = str(toreplace)
    sreplace = str(replace)
    with open(sfile, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(storeplace, sreplace)

    # Write the file out again
    with open(sfile, 'w') as file:
        file.write(filedata)