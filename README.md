# ANDA

ANDA is an image analysis tool used for analysis of microscopy images from 2d neuronal cell cultures. The pipeline is a series of Python scripts executed in succession to perform image analysis using Fiji modules. Important metrics in neurodevelopment, namely cell bodies, neurites and neurite attachment points are retrieved from images and analysed.

![image](https://github.com/EskelandLab/ANDA/blob/main/anda_logo.png "ANDA")


## Installing

Download ANDA:
```r
git clone https://github.com/EskelandLab/ANDA.git
```

## How to use

Before using ANDA, be sure to have back up of all images. Also ensure that you have enough space to run the analysis as the analysis creates output files that require some space. At least twice the space used by the images should be available.

Place all images in a folder separate from the ANDA directory.

## Starting the tool

From the terminal and while in the ANDA directory, start the Bash script by typing "bash ANDA.sh" or "./ ANDA.sh" and hit Enter.


When the analysis has finished, the results are stored in csv files named "results_{metric}.csv" in the same directory as the image subfolders.
Note that there are also csv files stored in the directories with names ending with "results". These csv files contain unsummarized data on every identified particle in every image.

