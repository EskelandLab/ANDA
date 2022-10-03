#!/bin/python3

"""Sort the data from csv files after image analysis"""

import sys
import pandas as pd
import numpy as np

analysis = sys.argv[1] # Cell bodies, neurites or neurite attachment points
dir_ = sys.argv[2]  # Directory
ar_threshold = int(sys.argv[3]) # Aspect ratio threshold
output = sys.argv[4]

with open(f'{dir_}/file_names.txt', 'r') as file_names:
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

def write_dataframe(metrics):
    """Convert metrics dictionary to pandas dataframe and write to csv"""

    dataframe = pd.DataFrame(data = metrics)
    return dataframe.to_csv(f"{output}")


def data_sort(metric):
    """Sort data into metrics specified by the analysis parameters"""

    if metric == "cells":
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", \
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

            except ValueError:
                cell_num_count.append(0)
                cell_area.append(0)
                cell_width.append(0)
                cell_length.append(0)
                cell_image.append(f"{file_}")

        metrics_dict = {'Image': cell_image,
             'Count': cell_num_count,
             'Mean_area': cell_area,
             'Mean_width': cell_width,
             'Mean_length': cell_length}

        write_dataframe(metrics_dict)

    elif metric == "neurites":
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", \
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

            except ValueError:
                neurite_num_count.append(0)
                neurite_area.append(0)
                neurite_width.append(0)
                neurite_length.append(0)
                neurite_image.append(f"{file_}")

        metrics_dict = {'Image': neurite_image,
             'Count': neurite_num_count,
             'Mean_area': neurite_area,
             'Mean_width': neurite_width,
             'Mean_length': neurite_length}


        write_dataframe(metrics_dict)

    if metric == "attachment":
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", usecols = ['Area'])
                count = len(data["Area"])
                attachment_num_count.append(count)
                attachment_image.append(f"{file_}")

            except ValueError:
                attachment_num_count.append(0)
                attachment_image.append(f"{file_}")

        metrics_dict = {'Image': attachment_image,
             'Count': attachment_num_count}

        write_dataframe(metrics_dict)

data_sort(analysis)
