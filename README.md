# ANDA

ANDA is an image analysis tool used for analysis of microscopy images from two dimensional (2d) neuronal cell cultures. The pipeline is a series of Python scripts executed in succession to perform image analysis using Fiji modules. Important metrics in neurodevelopment, namely cell bodies, neurites and neurite attachment points are retrieved from images and analysed.

![image](https://github.com/EskelandLab/ANDA/blob/main/anda_logo.png "ANDA")


## Installing

Download files:

[ANDA.sh](https://github.com/EskelandLab/ANDA/blob/main/ANDA.sh)  
[cell_metrics.py](https://github.com/EskelandLab/ANDA/blob/main/cell_metrics.py)  
[data_sort.py](https://github.com/EskelandLab/ANDA/blob/main/data_sort.py)  
[The fiji folder](https://github.com/EskelandLab/ANDA/tree/main/fiji) or download [Fiji](https://imagej.net/software/fiji/downloads)


## How to use

Before using ANDA, be sure to have a back up of all images. Also ensure that you have enough space to run the analysis as the analysis creates output files. You will need at least twice the space used by the images.

Place all images in a folder separate from the ANDA directory.

### Create file with pipeline parameters
Create a txt file in this format:  
\<Full path to images>  
\<Full path to Fiji>  
\<Name of cell line>  
save_outlines OR no  
\<aspect ratio threshold>  

Name the file "pipeline_parameters.txt"
## Starting the tool

From the terminal and while in the ANDA directory, start the Bash script by typing "bash ANDA.sh" or "./ ANDA.sh" and hit Enter.


When the analysis has finished, the results are stored in csv files named "results_{metric}.csv" in the same directory as the image subfolders.
Note that there are also csv files stored in the directories with names ending with "results". These csv files contain unsummarized data on every identified particle in every image.

## Graphical Overview

![image](https://github.com/EskelandLab/ANDA/blob/main/ANDA.jpg)

## Example images
Example images generated in EskelandLab and PaulsenLab that have been analysed by ANDA can be downloaded with license CC BY 4.0. from [NeuroImaging Tools & Resources Collaboratory (NITRC)](https://www.nitrc.org/projects/anda_neuronal/)

## Citations information & Contributors
Please cite ANDA preprint in bioRxiv: 
[ANDA: An open-source tool for automated image analysis of neuronal differentiation](https://www.biorxiv.org/content/10.1101/2023.04.27.538564v1) 


ANDA has also been described in following publication: 
[Paracetamol perturbs neuronal arborization and disrupts the cytoskeletal proteins SPTBN1 and TUBB3 in both human and chicken in vitro models](https://doi.org/10.1016/j.taap.2022.116130).


## License
This project is licensed under the MIT.
