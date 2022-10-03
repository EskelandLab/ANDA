# @String input_analysis
# @String image_dir
# @String cell_parameters
# @String outlines
# @Integer height
# @Integer width
# @String filenames
# @String outputfiles
# @String outlinefiles

"""
Jython script to perform cell metric quantification in ImageJ
"""

from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator

# Open file with parameters for analyzing cell type
with open("{}_parameters.txt".format(cell_parameters), 'r') as cell:
    cell_read = cell.readlines()

cell_line_parameters = [str(i.rstrip()) for i in cell_read] # Cell parameters list
PATH = str(cell_line_parameters[0])

##### Cell metric parameters
min_cell_size = int(cell_line_parameters[1])
max_cell_size = int(cell_line_parameters[2])
min_cell_circularity = float(cell_line_parameters[3])
max_cell_circularity = float(cell_line_parameters[4])
min_neurite_size = int(cell_line_parameters[5])
max_neurite_size = int(cell_line_parameters[6])
min_neurite_circularity = float(cell_line_parameters[7])
max_neurite_circularity = float(cell_line_parameters[8])
CELL_THRESHOLD = str(cell_line_parameters[9])
NEURITE_THRESHOLD = str(cell_line_parameters[10])
WATERSHED_CHOICE = str(cell_line_parameters[11])


if CELL_THRESHOLD == "NO THRESHOLD":
    CELL_THRESHOLD = "Default" # Default thresholding method in ImageJ
if NEURITE_THRESHOLD == "NO THRESHOLD":
    NEURITE_THRESHOLD = "Default" # Default thresholding method in ImageJ

IJ.run("Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction stack display add redirect=None decimal=3") # All available measurements
def particle_analysis(analysis):
    """Quantify cell body count, neurite lengths and neurite attachment points"""

    if analysis == "cells": # Run cell body count analysis
        IJ.open("{}/{}".format(str(image_dir), str(filenames)))
        imp = IJ.getImage()
        IJ.run("8-bit")
        IJ.run("Auto Threshold", "method={}".format(CELL_THRESHOLD))
        if WATERSHED_CHOICE == "yes":
            IJ.run("Watershed")
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
        else:
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
        IJ.saveAs("Results", "{}".format(str(outputfiles)))
        IJ.run("Clear Results")
        if outlines == "yes":
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
            overlay_ = ImagePlus.getOverlay(imp)
            IJ.newImage("blank_c", "RGB white", width, height, 1)
            imp2 = IJ.getImage().setOverlay(overlay_)
            imp2 = IJ.getImage()
            imp3 = imp2.flatten()
            IJ.run(imp3, "8-bit", "")
            IJ.saveAs(imp3, "Tiff", "{}".format(str(outlinefiles)))





    elif analysis == "neurites": # Run neurite length analysis
        IJ.open("{}/{}".format(str(image_dir), str(filenames)))
        imp = IJ.getImage()
        IJ.run("8-bit")
        IJ.run("Auto Threshold", "method={}".format(NEURITE_THRESHOLD))
        if WATERSHED_CHOICE == "yes":
            IJ.run("Watershed")
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
        else:
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
        IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_neurite_size, max_neurite_size, min_neurite_circularity, max_neurite_circularity))
        IJ.saveAs("Results", "{}".format(str(outputfiles)))
        IJ.run("Clear Results")
        if outlines == "yes":
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
            overlay_ = ImagePlus.getOverlay(imp)
            IJ.newImage("blank_n", "RGB white", width, height, 1)
            imp2 = IJ.getImage().setOverlay(overlay_)
            imp2 = IJ.getImage()
            imp3 = imp2.flatten()
            IJ.run(imp3, "8-bit", "")
            IJ.saveAs(imp3, "Tiff", "{}".format(str(outlinefiles)))


    elif analysis == "attachment": # Run neurite attachment point analysis
        image_calc = ImageCalculator() # ImageJ plugin
        img = IJ.open("{}/{}".format(str(image_dir), str(filenames)))
        imp_c = IJ.getImage() # Cell bodies
        imp_n = IJ.getImage() # Neurites
        IJ.run(imp_c, "8-bit", "")
        IJ.run(imp_n, "8-bit", "")

        # Threshold highlighting neurites
        IJ.run(imp_c, "Auto Threshold", "method={}".format(NEURITE_THRESHOLD))
        IJ.run(imp_n, "Auto Threshold", "method={}".format(NEURITE_THRESHOLD))
        if WATERSHED_CHOICE == "yes":
            IJ.run(imp_c, "Watershed", "") # Watershed segmentation
            IJ.run(imp_c, "Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Overlay".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity)) # Use cell body parameters to extract overlay
            overlay_c = ImagePlus.getOverlay(imp_c) # Get cell body overlay

            IJ.run(imp_n, "Watershed", "") # Watershed segmentation
            IJ.run(imp_n, "Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Overlay".format(min_neurite_size, max_neurite_size, min_neurite_circularity, max_neurite_circularity)) # Use neurite parameters to extract overlay
            overlay_n = ImagePlus.getOverlay(imp_n) # Get neurite overlay
        else:
            IJ.run(imp_c, "Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Overlay".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity)) # Use cell body parameters to extract overlay
            overlay_c = ImagePlus.getOverlay(imp_c) # Get cell body overlay

            IJ.run(imp_n, "Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Overlay".format(min_neurite_size, max_neurite_size, min_neurite_circularity, max_neurite_circularity)) # Use neurite parameters to extract overlay
            overlay_n = ImagePlus.getOverlay(imp_n) # Get neurite overlay

        # Blank image for pasting the overlay onto
        IJ.newImage("{}_blank_c".format(filenames), "RGB white", 1408, 1040, 1)
        imp_c2 = IJ.getImage().setOverlay(overlay_c)
        imp_c2 = IJ.getImage()
        imp_c3 = imp_c2.flatten()
        IJ.run(imp_c3, "8-bit", "")
        IJ.run(imp_c3, "Make Binary", "")
        IJ.saveAs(imp_c3, "Tiff", "{}/imp_c3.tif".format(PATH))

        # Blank image for pasting the overlay onto
        IJ.newImage("{}_blank_n".format(filenames), "RGB white", 1408, 1040, 1)
        imp_n2 = IJ.getImage().setOverlay(overlay_n)
        imp_n2 = IJ.getImage()
        imp_n3 = imp_n2.flatten()
        IJ.run(imp_n3, "8-bit", "")
        IJ.run(imp_n3, "Make Binary", "")
        IJ.saveAs(imp_n3, "Tiff", "{}/imp_n3.tif".format(PATH))
        IJ.run(imp_n3, "Find Edges", "") # Sobel edge detector

        # Get the overlap between cell bodies and neurites - the attachment points
        imp_res = ic.run("Multiply create", imp_n3, imp_c3)
        IJ.saveAs(imp_res, "Tiff", "{}/{}_imp_res.tif".format(PATH, filenames))
        IJ.run(imp_res, "Analyze Particles...", "size=0-100 pixel circularity=0.00-1.00 show=Nothing display summarize")
        IJ.saveAs("Results", "{}".format(str(outputfiles)))
        IJ.run("Clear Results")
        if outlines == "yes":
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity))
            overlay_ = ImagePlus.getOverlay(imp_res)
            IJ.newImage("blank_b", "RGB white", width, height, 1)
            imp2 = IJ.getImage().setOverlay(overlay_)
            imp2 = IJ.getImage()
            imp3 = imp2.flatten()
            IJ.run(imp3, "8-bit", "")
            IJ.saveAs(imp3, "Tiff", "{}".format(str(outlinefiles)))

particle_analysis(input_analysis)

# If ouputfile is not written, write an empty outputfile

def file_read():
    try:
        output = open(outputfiles, "r")
    except IOError:
        with open(outputfiles, "w") as output:
            output.write("NO IDENTIFIED MOTIFS")

file_read()
