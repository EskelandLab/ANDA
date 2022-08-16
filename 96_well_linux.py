#!/usr/bin/python3

import sys
import tkinter as tk
from tkinter import filedialog

# Present a GUI setting only the necessary parameters for analysis
# Set analysis parameters with buttons and string input
# Once parameters are set, the pipeline will proceed by itself


class PipelineStart:

    cell_lines = 'CGN;NT2N;PC12;'
    cell_lines_set = set(cell_lines.split(";")) # Split cell_lines into list
    labels = []

    def __init__(self, wndw):
        
        ### GUI aesthetics
        self.wndw = tk.Frame(wndw)
        wndw.title("Automated Neuronal Differentiation Analyzer")
        self.wndw.grid(column=0,row=0)
        self.wndw.columnconfigure(0, weight = 1)
        self.wndw.rowconfigure(0, weight = 1)
        self.wndw.pack()

        ### Image directories
        self.files_dir_button = tk.Button(self.wndw, text = "Select image directory            ", borderwidth = 2, command = lambda : (self.get_files_dir()))
        self.files_dir_button.grid(row = 0, column = 0) # Select directory with the images to be analyzed

        self.imagej_button = tk.Button(self.wndw, text = "Full path to ImageJ directory     ", borderwidth = 2, command = lambda : (self.get_imagej_path()))
        self.imagej_button.grid(row = 2, column = 0) # Path to ImageJ program

        ### Information about images
        self.ar_threshold_text = tk.StringVar(self.wndw)
        self.ar_threshold = tk.Entry(self.wndw)
        self.ar_threshold.grid(row = 3, column = 1, columnspan = 1)
        tk.Label(self.wndw, text = "Set neurite aspect ratio threshold").grid(row = 3, column = 0) # String input for neurite aspect ratio threshold

        self.image_height_text = tk.StringVar(self.wndw)
        self.image_height = tk.Entry(self.wndw)
        self.image_height.grid(row = 4, column = 1, columnspan = 1)
        tk.Label(self.wndw, text = "Set image height").grid(row = 4, column = 0) # String input for image height 

        self.image_width_text = tk.StringVar(self.wndw)
        self.image_width = tk.Entry(self.wndw)
        self.image_width.grid(row = 5, column = 1, columnspan = 1)
        tk.Label(self.wndw, text = "Set image width").grid(row = 5, column = 0) # String input for image width


        self.cell_line = tk.StringVar(wndw)
        self.cell_line.set('CGN') # Pre-set selected cell line to CGN

        self.choice_cell_line = tk.OptionMenu(self.wndw, self.cell_line, *self.cell_lines_set) # Drop down menu

        self.choice_cell_line.grid(row = 10, column = 1)
        tk.Label(self.wndw, text = "Choose cell line").grid(row = 9, column = 1)


        ### Image analysis metrics
        self.params_list = []
        self.params_str = ""
        tk.Label(self.wndw, text = "Select analysis metrics:").grid(row = 9, column = 0)
        self.neurites = tk.Button(master = self.wndw, text = "Neurite lengths            ", borderwidth = 2, command = lambda : (self.btn_neurites()))
        self.neurites.grid(row = 10, column = 0)

        self.cells = tk.Button(master = self.wndw, text = "Cell body count            ", borderwidth = 2, command = lambda : (self.btn_cells()))
        self.cells.grid(row = 11, column = 0)

        self.branching = tk.Button(master = self.wndw, text = "Neurite attachment points ", borderwidth = 2, command = lambda : (self.btn_attachment()))
        self.branching.grid(row = 12, column = 0)
        
        self.clear = tk.Button(master = self.wndw, text = "Clear metrics selection    ", borderwidth = 2, command = lambda : (self.btn_clear()))
        self.clear.grid(row = 14, column = 0)

        self.show_outlines = "no" # Pre-set to not show outlines. When selected, motif outlines will be saved
        self.show_outlines_button = tk.Button(master = self.wndw, text = "Save motif outlines", borderwidth = 2, command = lambda : (self.btn_save_outlines()))
        self.show_outlines_button.grid(row = 11, column = 1)


        self.submit_button = tk.Button(self.wndw, text = "Save and quit", cursor = "hand1", borderwidth = 2, command = self.return_all)
        self.submit_button.grid(row = 13, column = 1) # Select this button to submit the txt file and continue with analysis
        
        # Save motif outlines
    def btn_save_outlines(self):
        self.show_outlines = "yes"
        self.show_outlines_button.configure(state=tk.DISABLED)
        return self.show_outlines

        # Aspect ratio threshold
    def get_ar_threshold(self):
        return ar_treshold.get()
    
        # Image height in pixels
    def get_image_height(self):
        return image_height.get()
    
        # Image width in pixels
    def get_image_width(self):
        return image_width.get()
        
        # Directory with images
    def get_files_dir(self):
        self.files_dir = tk.filedialog.askdirectory()
        self.files_dir_button.configure(state=tk.DISABLED)
        return self.files_dir

        # Full path to ImageJ
    def get_imagej_path(self):
        self.imagej_path = tk.filedialog.askdirectory()
        self.imagej_button.configure(state=tk.DISABLED)
        return self.imagej_path

        # Render click event
    def btn_click(self, item):
        self.wells_list.append(str(item))
        return self.wells_list
        
        # Disable button
    def disable(self, x):
        self.labels[x].configure(state=tk.DISABLED)

        # Select cell line
    def return_cell_line(self):
        return str(self.cell_line.get())

        # Select neurites button
    def btn_neurites(self):
        self.params_list.append("neurites")
        self.neurites.configure(state=tk.DISABLED)
        return self.params_list

        # Select cell bodies button
    def btn_cells(self):
        self.params_list.append("cells")
        self.cells.configure(state=tk.DISABLED)
        return self.params_list

        # Select neurite attachment points button
    def btn_attachment(self):
        self.params_list.append("attachment")
        self.branching.configure(state=tk.DISABLED)
        return self.params_list

        # Clear selection
    def btn_clear(self):
        self.functions_list = [self.neurites, self.cells, self.attachment]
        self.params_list.clear()
        for i in range(len(self.functions_list)):
            self.functions_list[i].configure(state=tk.NORMAL)
        return self.params_list

        # Return parameters in list
    def return_params_list(self):
        return self.params_list

        # Return parameters in string
    def return_params_str(self):
        for i in self.params_list:
            self.params_str += i+" "
        return self.params_str

        # Return parameters in compacted list separated with ";"
    def return_params_compact(self):
        self.params_compact = self.params_str.replace(" ", ";")
        return self.params_compact

        # Return all parameters
    def return_all(self):
        (self.ar_threshold, self.image_height, self.image_width) = (self.ar_threshold.get(), self.image_height.get(), self.image_width.get())
        self.return_params_str()
        self.return_params_compact()
        self.wndw.quit()
        return (self.files_dir, self.imagej_path, self.ar_threshold, self.image_height, self.image_width, self.params_str,  str(self.cell_line.get()), self.params_compact)

        # Output from selection of the parameters
    def return_output_list(self):
        self.output_list = [i for i in (self.files_dir, self.imagej_path, self.params_str, str(self.cell_line.get()), self.show_outlines, self.params_compact, self.ar_threshold, self.image_height, self.image_width)]
        return self.output_list


root = tk.Tk()
pipe_start = PipelineStart(root)
root.mainloop() # Call the GUI
f = open('pipeline_parameters.txt', 'w') # Write the parameters to txt file
for i in pipe_start.return_output_list():
    f.write(i+'\n')
f.close()

