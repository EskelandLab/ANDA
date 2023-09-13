#!/bin/bash

scripts_dir=$(pwd) # Directory with scripts
dir_name=$(awk 'FNR == 1 {print}' ${scripts_dir}/pipeline_parameters.txt)
imagej_path=$(awk 'FNR == 2 {print}' ${scripts_dir}/pipeline_parameters.txt)
outlines_=$(awk 'FNR == 10 {print}' ${scripts_dir}/pipeline_parameters.txt)
cd ${dir_name}
ls | grep tif > file_names.txt # Write image file names to list
cd ..

dirs_len=${#dirs_[@]}


# Make directories to store results and/or outlines
mkdir ${dir_name}_results_cells
mkdir ${dir_name}_results_neurites
mkdir ${dir_name}_results_attachments
if [[ ${outlines} == "save_outlines"  ]]; then
  mkdir ${dir_name}_outlines_cells
  mkdir ${dir_name}_outlines_neurites
  mkdir ${dir_name}_outlines_attachments
fi

${imagej_path}/ImageJ-linux64 --ij2 --headless --run ${scripts_dir}/cell_metrics.py
python3 data_sort.py
