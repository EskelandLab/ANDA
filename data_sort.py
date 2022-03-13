#!/bin/python3

import pandas as pd
import numpy as np
import sys

analysis= sys.argv[1] # Cell bodies, neurites or neurite attachment points
dir_ =  sys.argv[2]  # Directory 
ar_threshold = int(sys.argv[3]) # Aspect ratio threshold
output = sys.argv[4]

def data_sort(metric):
    if metric == "cells": 
        area = [] # Area selection, area preoccupied by identified particle
        width = [] # Width of minor axis of a fitted ellipse
        length = [] # Length of major axis of a fitted ellipse
        num_count = [] # Number of identified particles
        image = []
        file_names = open(f'{dir_}/file_names.txt', 'r')
        file_list = file_names.readlines()
        file_names.close()
        file_list = [i.rstrip() for i in file_list]
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", usecols = ['Area', 'Minor', 'Major'])
                count = len(data["Area"])
                mean_area = np.mean(data["Area"])
                mean_width = np.mean(data["Minor"])
                mean_length = np.mean(data["Major"])
                num_count.append(count)
                area.append(mean_area)
                width.append(mean_width)
                length.append(mean_length)
                image.append(f"{file_}")

            except ValueError:
                num_count.append(0)
                area.append(0)
                width.append(0)
                length.append(0)            
                image.append(f"{file_}")
        
        d = {'Image': image,
             'Count': num_count,
             'Mean_area': area,
             'Mean_width': width,
             'Mean_length': length}
    
        df = pd.DataFrame(data = d)
        df.to_csv(f"{output}")
    
    elif metric == "neurites": 
        area = [] # Area selection, area preoccupied by identified particle
        width = [] # Width of minor axis of a fitted ellipse
        length = [] # Length of major axis of a fitted ellipse
        num_count = [] # Number of identified particles
        ar_removals = [] # Particles removed for not surpassing user set aspect ratio threshold
        image = []
        file_names = open(f'{dir_}/file_names.txt', 'r')
        file_list = file_names.readlines()
        file_names.close()
        file_list = [i.rstrip() for i in file_list]
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", usecols = ['Area', 'Minor', 'Major', 'AR'])
                if ar_threshold > 0:
                    data_2 = data[data['AR'] > ar_threshold]
                    mean_length = np.mean(data_2["Major"])
                    mean_width = np.mean(data_2["Minor"])
                    mean_area = np.mean(data_2["Area"])
                    ar_removals.append(len(data) - len(data_2))
                else:
                    mean_length = np.mean(data["Major"])
                    mean_width = np.mean(data["Minor"])
                    mean_area = np.mean(data["Area"])
                    ar_removals.append(0)
                count = len(data["Area"])
                num_count.append(count)
                area.append(mean_area)
                width.append(mean_width)
                length.append(mean_length)            
                image.append(f"{file_}")

            except ValueError:
                num_count.append(0)
                area.append(0)
                width.append(0)
                length.append(0)            
                image.append(f"{file_}")

        d = {'Image': image,
             'Count': num_count,
             'Mean_area': area,
             'Mean_width': width,
             'Mean_length': length}
    
    
        df = pd.DataFrame(data = d)
        df.to_csv(f"{output}")
    
    if metric == "attachment": 
        num_count = [] # Number of identified particles
        image = []
        file_names = open(f'{dir_}/file_names.txt', 'r')
        file_list = file_names.readlines()
        file_names.close()
        file_list = [i.rstrip() for i in file_list]
        for file_ in file_list:
            try:
                data = pd.read_csv(f"{dir_}_results_{metric}/{file_}.csv", usecols = ['Area'])
                count = len(data["Area"])
                num_count.append(count)
                image.append(f"{file_}")

            except ValueError:
                num_count.append(0)
                image.append(f"{file_}")
        
        d = {'Image': image,
             'Count': num_count}
    
        df = pd.DataFrame(data = d)
        df.to_csv(f"{output}")

data_sort(analysis)
