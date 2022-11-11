#!/usr/bin/python3

import tkinter as tk
import tkinter.filedialog



class PipelineStart:
    """
    * Present a GUI setting only the necessary parameters for analysis
    * Set analysis parameters with buttons and string input
    * Once parameters are set, the pipeline will proceed by itself
    """

    cell_lines = 'CGN;NT2N;PC12;'
    cell_lines_set = set(cell_lines.split(";")) # Split cell_lines into list
    labels = []

    def __init__(self, wndw):

        ### GUI aesthetics
        self.wndw = tk.Frame(wndw)
        wndw.title("Automated Neuronal Differentiation Analyzer")
        self.wndw.grid(column = 0,row = 0)
        self.wndw.columnconfigure(0, weight = 1)
        self.wndw.rowconfigure(0, weight = 1)
        self.wndw.pack()

        ### Image directories
        self.files_dir_button = tk.Button(self.wndw, text = "Select image directory            ", \
        borderwidth = 2, command = lambda : (self.get_files_dir()))

        # Select directory with the images to be analyzed
        self.files_dir_button.grid(row = 0, column = 0)

        self.imagej_button = tk.Button(self.wndw, text = "Full path to ImageJ directory     ", \
        borderwidth = 2, command = lambda : (self.get_imagej_path()))

        # Path to ImageJ program
        self.imagej_button.grid(row = 2, column = 0)

        ### Information about images
        self.ar_threshold = tk.Entry(self.wndw)
        self.ar_threshold_text = tk.StringVar(self.wndw)
        self.ar_threshold.grid(row = 3, column = 1, columnspan = 1)

        # String input for neurite aspect ratio threshold
        tk.Label(self.wndw, text = "Set neurite aspect ratio threshold").grid(row = 3, column = 0)

        self.image_height = tk.Entry(self.wndw)
        self.image_height_text = tk.StringVar(self.wndw)
        self.image_height.grid(row = 4, column = 1, columnspan = 1)

        # String input for image height
        tk.Label(self.wndw, text = "Set image height").grid(row = 4, column = 0)

        self.image_width = tk.Entry(self.wndw)
        self.image_width_text = tk.StringVar(self.wndw)
        self.image_width.grid(row = 5, column = 1, columnspan = 1)

        # String input for image width
        tk.Label(self.wndw, text = "Set image width").grid(row = 5, column = 0)


        self.cell_line = tk.StringVar(wndw)
        self.cell_line.set('CGN') # Pre-set selected cell line to CGN

        # Drop down menu
        self.choice_cell_line = tk.OptionMenu(self.wndw, self.cell_line, *self.cell_lines_set)

        self.choice_cell_line.grid(row = 10, column = 1)
        tk.Label(self.wndw, text = "Choose cell line").grid(row = 9, column = 1)


        ### Image analysis metrics
        self.params_list = []
        self.params_str = ""
        tk.Label(self.wndw, text = "Select analysis metrics:").grid(row = 9, column = 0)
        self.neurites = tk.Button(master = self.wndw, text = "Neurite lengths            ", \
        borderwidth = 2, command = lambda : (self.btn_neurites()))
        self.neurites.grid(row = 10, column = 0)

        self.cells = tk.Button(master = self.wndw, text = "Cell body count            ", \
        borderwidth = 2, command = lambda : (self.btn_cells()))
        self.cells.grid(row = 11, column = 0)

        self.attachment = tk.Button(master = self.wndw, text = "Neurite attachment points ", \
        borderwidth = 2, command = lambda : (self.btn_attachment()))
        self.attachment.grid(row = 12, column = 0)

        self.clear = tk.Button(master = self.wndw, text = "Clear metrics selection    ", \
        borderwidth = 2, command = lambda : (self.btn_clear()))
        self.clear.grid(row = 14, column = 0)

        # Pre-set to not apply watershed. When selected, watershed algorithm will be applied
        self.watershed = "no"
        self.watershed_button = tk.Button(master = self.wndw, text = "Apply watershed", \
        borderwidth = 2, command = lambda : (self.btn_watershed()))
        self.watershed_button.grid(row = 11, column = 1)

        # Pre-set to not show outlines. When selected, motif outlines will be saved
        self.show_outlines = "no"
        self.show_outlines_button = tk.Button(master = self.wndw, text = "Save motif outlines", \
        borderwidth = 2, command = lambda : (self.btn_save_outlines()))
        self.show_outlines_button.grid(row = 12, column = 1)


        self.submit_button = tk.Button(self.wndw, text = "Save and quit", cursor = "hand1", \
        borderwidth = 2, command = self.return_all)
        # Select this button to submit the txt file and continue with analysis
        self.submit_button.grid(row = 14, column = 1)

    def btn_save_outlines(self):
        """ Save motif outlines """
        self.show_outlines = "show_outlines"
        self.show_outlines_button.configure(state=tk.DISABLED)
        return self.show_outlines

    def get_ar_threshold(self):
        """ Aspect ratio threshold """
        return ar_threshold.get()

    def get_image_height(self):
        """ Image height in pixels """
        return image_height.get()

    def get_image_width(self):
        """ Image width in pixels """
        return image_width.get()

    def get_files_dir(self):
        """ Directory with images """
        self.files_dir = tk.filedialog.askdirectory()
        self.files_dir_button.configure(state=tk.DISABLED)
        return self.files_dir

    def get_imagej_path(self):
        """ Full path to ImageJ """
        self.imagej_path = tk.filedialog.askdirectory()
        self.imagej_button.configure(state=tk.DISABLED)
        return self.imagej_path

    def disable(self, btn):
        """ Disable button """
        self.labels[btn].configure(state=tk.DISABLED)

    def return_cell_line(self):
        """ Select cell line """
        return str(self.cell_line.get())

    def btn_neurites(self):
        """ Select neurites button """
        self.params_list.append("neurites")
        self.neurites.configure(state=tk.DISABLED)
        return self.params_list

    def btn_cells(self):
        """ Select cell bodies button """
        self.params_list.append("cells")
        self.cells.configure(state=tk.DISABLED)
        return self.params_list

    def btn_attachment(self):
        """ Select neurite attachment points button """
        self.params_list.append("attachment")
        self.attachment.configure(state=tk.DISABLED)
        return self.params_list

    def btn_watershed(self):
        """ Select watershed button """
        self.watershed = "apply_watershed"
        self.watershed_button.configure(state=tk.DISABLED)
        return self.watershed

    def btn_clear(self):
        """ Clear selection """
        self.functions_list = [self.neurites, self.cells, self.attachment]
        self.params_list.clear()
        for (count, func) in enumerate(self.functions_list):
            self.functions_list[func].configure(state=tk.NORMAL)
        return self.params_list

    def return_params_str(self):
        """ Return parameters in string """
        for param in self.params_list:
            self.params_str += param + ' '
        return self.params_str

    def return_params_compact(self):
        """ Return parameters in compacted list separated with ';' """
        self.params_compact = self.params_str.replace(' ', ';')
        return self.params_compact

    def return_all(self):
        """ Return all parameters """
        (self.ar_threshold, self.image_height, self.image_width) = \
        (self.ar_threshold.get(), self.image_height.get(), self.image_width.get())

        self.return_params_str()
        self.return_params_compact()
        self.wndw.quit()
        return (self.files_dir, self.imagej_path, self.ar_threshold, self.image_height, \
        self.image_width, self.params_str,  str(self.cell_line.get()), self.params_compact)

    def return_output_list(self):
        """ Output from selection of the parameters """
        self.output_list = [self.files_dir, self.imagej_path, self.params_str, \
        str(self.cell_line.get()), self.show_outlines, self.params_compact, self.ar_threshold, \
        self.image_height, self.image_width, self.watershed]

        return self.output_list


root = tk.Tk()
pipe_start = PipelineStart(root)
root.mainloop() # Call the GUI

with open('pipeline_parameters.txt', 'w') as f:# Write the parameters to txt file
    for i in pipe_start.return_output_list():
        f.write(i+'\n')
