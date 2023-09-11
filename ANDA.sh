#!/bin/bash

scripts_dir=$(pwd) # Directory with scripts
dir_name=$(awk 'FNR == 1 {print}' ${scripts_dir}/pipeline_parameters.txt)
imagej_path=$(awk 'FNR == 2 {print}' ${scripts_dir}/pipeline_parameters.txt)
outlines_=$(awk 'FNR == 10 {print}' ${scripts_dir}/pipeline_parameters.txt)
cd ${dir_name}
ls | grep tif > file_names.txt # Write image file names to list
cd ..

dirs_len=${#dirs_[@]}


# Make directories to store results. Add numbersign # to skip these commands
mkdir ${dir_name}_results_cells # Results directory for cells
mkdir ${dir_name}_results_neurites # Results directory for neurites
mkdir ${dir_name}_results_branching # Results directory for neurite attachment points
if [[ ${outlines} == "save_outlines"  ]]; then
  mkdir ${dir_name}_outlines_cells # Outlines directory for cells
  mkdir ${dir_name}_outlines_neurites # Outlines directory for neurites
  mkdir ${dir_name}_outlines_branching # Outlines directory for neurite attachment points
fi

${imagej_path}/ImageJ-linux64 --ij2 --headless --run ${scripts_dir}/cell_metrics.py
python3 cell_metrics.py
python3 data_sort.py
