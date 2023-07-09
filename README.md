# ANDA

ANDA is an image analysis tool used for analysis of microscopy images from two dimensional (2d) neuronal cell cultures. The pipeline is a series of Python scripts executed in succession to perform image analysis using Fiji modules. Important metrics in neurodevelopment, namely cell bodies, neurites and neurite attachment points are retrieved from images and analysed.

![image](https://github.com/EskelandLab/ANDA/blob/main/anda_logo.png "ANDA")


## Installing

Download ANDA:
```r
git clone https://github.com/EskelandLab/ANDA.git
```

## How to use

Before using ANDA, be sure to have a back up of all images. Also ensure that you have enough space to run the analysis as the analysis creates output files. You will need at least twice the space used by the images.

Place all images in a folder separate from the ANDA directory.

## Starting the tool

From the terminal and while in the ANDA directory, start the Bash script by typing "bash ANDA.sh" or "./ ANDA.sh" and hit Enter.


When the analysis has finished, the results are stored in csv files named "results_{metric}.csv" in the same directory as the image subfolders.
Note that there are also csv files stored in the directories with names ending with "results". These csv files contain unsummarized data on every identified particle in every image.

## Graphical Overview

![image](https://github.com/EskelandLab/ANDA/blob/main/ANDA.jpg)

## Example images
Example images generated in EskelandLab and PaulsenLab that have been analysed by ANDA can be downloaded with license CC BY 4.0. from NeuroImaging Tools & Resources Collaboratory (NITRC) https://www.nitrc.org/projects/anda_neuronal/

## Citations information & Contributors
Please cite ANDA preprint in bioRxiv.
ANDA: An open-source tool for automated image analysis of neuronal differentiation
Hallvard Austin Wæhler, Nils-Anders Labba, Ragnhild Elisabeth Paulsen,  Geir Kjetil Sandve,  Ragnhild Eskeland
doi: https://doi.org/10.1101/2023.04.27.538564
https://www.biorxiv.org/content/10.1101/2023.04.27.538564v1

ANDA has also been described in following publication:
Nils-Anders Labba, Hallvard Austin Wæhler, Nora Houdaifi, Denis Zosen,
Fred Haugen, Ragnhild Elisabeth Paulsen, Mussie Ghezu Hadera, Ragnhild Eskeland 
Paracetamol perturbs neuronal arborization and disrupts the cytoskeletal proteins SPTBN1 and TUBB3 in both human and chicken in vitro models. Toxicology and Applied Pharmacology. 2022;449:116130.
https://doi.org/10.1016/j.taap.2022.116130

## Acknowledgements
ANDA is a desktop application built with TAURI that uses Python 3 scripts for data handling and function-call execution, summoning ImageJ functions from Fiji.

## License
his project is licensed under the MIT.
