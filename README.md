# Automated Neuronal Differentiation Analyzer

Automated Neuronal Differentiation Analyzer (ANDA) is an image analysis tool used for analysis of microscopy images from 2d neuronal cell cultures. The pipeline is a series of Python scripts executed in succession by Snakemake. Important metrics in neurodevelopment, namely cell bodies, neurites and neurite attachment points are retrieved from images and analysed using [Fiji](https://imagej.net/Fiji/Downloads).


## Installing

### Dependencies
* [Fiji](https://imagej.net/Fiji/Downloads)
* Python 3
  - Packages:
    - numpy
    - pandas
    - tkinter
* [Snakemake](https://snakemake.readthedocs.io/en/stable/)

All necessary Python packages can be installed when installing [Anaconda](https://www.anaconda.com/products/individual).

Download ANDA:
```r
git clone https://github.com/EskelandLab/ANDA.git
```


## How to use

Before using ANDA, be sure to have back up of all images. Also ensure that you have enough space to run the analysis as the analysis creates output files that require some space. At least twice the space used by the images should be available.

Place all images in a folder separate from the ANDA directory.

## Starting the tool

From the terminal and while in the ANDA directory, start the Bash script by typing "bash ANDA.sh" or "./ ANDA.sh" and hit Enter.


### Setting the analysis parameters

In the next window set the analysis parameters by filling out the required information (figure 1).
* Choose the directory with the images as image directory.
* Select the full path to the ImageJ program. Usually this is /home/.../Fiji.app/
* Set neurite aspect ratio threshold for exclusion of false positive neurites. Set this value to zero if you want to include every identified object.
* Select analysis metrics and cell line.
* Select if you want to save motif outlines or not.
* Start the analysis by pressing "Save and quit".

![image](https://github.com/EskelandLab/ANDA/blob/main/anda_gui.png "Graphical user interface")

*Figure 1: TkInter graphical user interface for selecting parameters for image analysis.*
## Running the analysis

The tool will now run through the images and apply the analysis metric(s) you chose. Depending on the system you are running on, and the number of images you are analysing this will take a while. To abort press "Ctrl+C".

When the analysis has finished, the results are stored in csv files named "results_{metric}.csv" in the same directory as the image subfolders.
Note that there are also csv files stored in the directories with names ending with "results". These csv files contain unsummarized data on every identified particle in every image.
