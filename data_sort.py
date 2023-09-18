#!/bin/python3

"""Sort the data from csv files after image analysis"""

from datetime import datetime
import pandas as pd
import numpy as np

DATE = datetime.today().strftime('%Y-%m-%d')

with open("pipeline_parameters.txt", 'r') as anda_parameters:
    analysis_read = anda_parameters.read().splitlines()
dir_ = analysis_read[0]  # Directory
ar_threshold = analysis_read[6] # Aspect ratio threshold


with open(f'{dir_}/file_names.txt', 'r', encoding="utf8") as file_names:
    file_list = file_names.readlines()
file_list = [i.rstrip() for i in file_list]


cell_area = [] # Area selection, area preoccupied by identified particle
cell_width = [] # Width of minor axis of a fitted ellipse
cell_length = [] # Length of major axis of a fitted ellipse
cell_num_count = [] # Number of identified particles
cell_image = []


neurite_area = [] # Area selection, area preoccupied by identified particle
neurite_width = [] # Width of minor axis of a fitted ellipse
neurite_length = [] # Length of major axis of a fitted ellipse
neurite_num_count = [] # Number of identified particles
neurite_ar_removals = [] # Particles removed for not surpassing user set aspect ratio threshold
neurite_image = []


attachment_num_count = [] # Number of identified particles
attachment_image = []

def append_zeros(*args):
    """ Append zero to the parameter lists if no parameters were identified"""

    for i in args:
        i.append(0)
    return args


def write_dataframe(metric, output):
    """Convert metrics dictionary to pandas dataframe and write to csv"""

    dataframe = pd.DataFrame(data = metric)
    return dataframe.to_csv(f"{DATE}_{output}")


def cell_sort():
    """Sort cell body results"""

    for file_ in file_list:
        try:
            data = pd.read_csv(f"{dir_}_results_cells/{file_}.csv", \
            usecols = ['Area', 'Minor', 'Major'])

            count = len(data["Area"])
            mean_area = np.mean(data["Area"])
            mean_width = np.mean(data["Minor"])
            mean_length = np.mean(data["Major"])
            cell_num_count.append(count)
            cell_area.append(mean_area)
            cell_width.append(mean_width)
            cell_length.append(mean_length)
            cell_image.append(f"{file_}")

        except FileNotFoundError:
            append_zeros(cell_num_count, cell_area, cell_width, cell_length)
            cell_image.append(f"{file_}")

    metrics_dict = {'Image': cell_image,
         'Count': cell_num_count,
         'Mean_area': cell_area,
         'Mean_width': cell_width,
         'Mean_length': cell_length}

    write_dataframe(metrics_dict, "cells")

def neurite_sort():
    """Sort neurite length results"""

    for file_ in file_list:
        try:
            data = pd.read_csv(f"{dir_}_results_neurites/{file_}.csv", \
            usecols = ['Area', 'Minor', 'Major', 'AR'])

            if ar_threshold > 0:
                data_2 = data[data['AR'] > ar_threshold]
                mean_length = np.mean(data_2["Major"])
                mean_width = np.mean(data_2["Minor"])
                mean_area = np.mean(data_2["Area"])
                neurite_ar_removals.append(len(data) - len(data_2))
            else:
                mean_length = np.mean(data["Major"])
                mean_width = np.mean(data["Minor"])
                mean_area = np.mean(data["Area"])
                neurite_ar_removals.append(0)

            count = len(data["Area"])
            neurite_num_count.append(count)
            neurite_area.append(mean_area)
            neurite_width.append(mean_width)
            neurite_length.append(mean_length)
            neurite_image.append(f"{file_}")

        except :
            append_zeros(neurite_num_count, neurite_area, neurite_width, neurite_length)
            neurite_image.append(f"{file_}")

    metrics_dict = {'Image': neurite_image,
         'Count': neurite_num_count,
         'Mean_area': neurite_area,
         'Mean_width': neurite_width,
         'Mean_length': neurite_length}


    write_dataframe(metrics_dict, "neurites")


def attachment_sort():
    """Sort neurite attachment point results"""

    for file_ in file_list:
        try:
            data = pd.read_csv(f"{dir_}_results_attachments/{file_}.csv", usecols = ['Area'])
            count = len(data["Area"])
            attachment_num_count.append(count)
            attachment_image.append(f"{file_}")

        except FileNotFoundError:
            attachment_num_count.append(0)
            attachment_image.append(f"{file_}")

    metrics_dict = {'Image': attachment_image,
         'Count': attachment_num_count}

    write_dataframe(metrics_dict, "attachments")

cell_sort()
neurite_sort()
attachment_sort()
