#!/bin/bash

: '
This script runs the Automated Neuronal Differentiation Analyzer GUI for setting the parameters for running the
image analysis. These input parameters include:

    * Workdirectory - Directory where the images are saved
    * Full path to ImageJ program
    * Aspect ratio threshold for excluding neurites and neurite attachment points
    * Cell analysis metrics
    * Whether to save outlines of identified structures or not

These parameters are written to the file pipeline_parameters.txt in the same directory as the scripts.
After the GUI has been presented and input has been set, the file names from the workdirectory are extracted
and saved in the file_names.txt file in the same directory as the scripts and a results directory is created.
If outlines are set to be saved, an additional directory is created.
'

python3 96_well_linux.py

scripts_dir=$(pwd) # Directory with scripts
dir_name=$(awk 'FNR == 1 {print}' ${scripts_dir}/pipeline_parameters.txt)
outlines_=$(awk 'FNR == 10 {print}' ${scripts_dir}/pipeline_parameters.txt)
cd ${dir_name}
ls | grep tif > file_names.txt # Write image file names to list
cd ..

dirs_len=${#dirs_[@]}


mkdir ${dir_name}_results_cells # Results directory for cells
mkdir ${dir_name}_results_neurites # Results directory for neurites
mkdir ${dir_name}_results_branching # Results directory for neurite attachment points
if [[ ${outlines} == "yes"  ]]; then
  mkdir ${dir_name}_outlines_cells # Outlines directory for cells
  mkdir ${dir_name}_outlines_neurites # Outlines directory for neurites
  mkdir ${dir_name}_outlines_branching # Outlines directory for neurite attachment points
fi

snakemake --snakefile data_snakefile # Run snakefile
