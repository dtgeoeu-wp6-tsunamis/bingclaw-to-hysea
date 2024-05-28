#!/bin/bash

# Find the directory containing setrun.py
setrun_dir=$(find / -type f -name "setrun.py" -exec dirname {} \; -quit)

if [ -z "$setrun_dir" ]; then
    echo "setrun.py not found"
    exit 1
fi

echo "Mouted input directory $setrun_dir"


# Find relative path between the setrun_dir and the directory with the BingClaw executable
bingclaw_dir=$(find / -type f -name "BingClaw5.6.1" -exec dirname {} \; -quit)
common_dir=$(realpath --relative-to="$setrun_dir" "$bingclaw_dir")

echo "Relative directory between BingClaw and mounted input folder $common_dir"
cd $setrun_dir

# Prepare parameters
python setrun.py 

# Run BingClaw in right relative path, save logs
echo "Running simulation"
./$common_dir/BingClaw5.6.1 >> run_log 2>&1
echo "Log is saved in the file run_log"