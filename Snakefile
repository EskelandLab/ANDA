import os
from datetime import datetime

WORKDIR = os.getcwd()
cell_metrics = WORKDIR + "/cell_metrics.py"
data_sorting = WORKDIR + "/data_sorting.py"

DATE = datetime.today().strftime('%Y-%m-%d')


def param_file_read(parameter_file):
    with open(parameter_file, "r") as f:
        file_ = f.read()
    params_list = file_.split('\n')
    
    dir__name = params_list[0]
    imagej_path = params_list[1]
    input_params = params_list[2]
    cell_line = params_list[3]
    outlines_ = params_list[4]
    input_params_compact = params_list[5]
    ar_threshold = params_list[6]
    height = params_list[7]
    width = params_list[8]

    return [dir__name, imagej_path, input_params, cell_line, outlines_, input_params_compact, ar_threshold, height, width]


def file_read(input_filenames):
    with open(input_filenames, 'r') as f:
        file_ = f.readlines()
    file_list = [str(i.rstrip()) for i in file_]

    return file_list


FILENAMES = file_read("file_names.txt")

rule all:
    input:
        expand("{dir_}_results_{metric}/{file_}.csv", dir_ = param_file_read("pipeline_parameters.txt")[0], metric = param_file_read("pipeline_parameters.txt")[2].split(" ")[0:-1], file_ = FILENAMES, allow_missing=True),
        expand("{dir_}_outlines_{metric}/{file_}", dir_ = param_file_read("pipeline_parameters.txt")[0], metric = param_file_read("pipeline_parameters.txt")[2].split(" ")[0:-1], file_ = FILENAMES, allow_missing=True)

rule image_analysis:
    params:
        input_files = "{file_}",
        input_params = "{metric}",
        dir__name = param_file_read("pipeline_parameters.txt")[0],
        imagej_path = param_file_read("pipeline_parameters.txt")[1],
        cell_line = param_file_read("pipeline_parameters.txt")[3],
        outlines_ = param_file_read("pipeline_parameters.txt")[4],
        image_height = param_file_read("pipeline_parameters.txt")[7],
        image_width = param_file_read("pipeline_parameters.txt")[8]
    output:
        output_results="{dir_}_results_{metric}/{file_}.csv",
        output_outlines="{dir_}_outlines_{metric}/{file_}"

    shell:
        """
        {params.imagej_path}/ImageJ-linux64 --ij2 --headless --run {cell_metrics} "input_analysis='{params.input_params}', image_dir='{params.dir__name}', cell_parameters='{params.cell_line}', outlines='{params.outlines_}', height='{params.image_height}', width='{params.image_width}', filenames='{params.input_files}', outputfiles='{output.output_results}', outputimages='{output.output_outlines}'"
        touch {output.output_outlines}
        """
