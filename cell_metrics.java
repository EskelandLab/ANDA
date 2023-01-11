import ij.IJ;
import ij.ImagePlus;
import ij.plugin.ImageCalculator;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;

public class ImageJScript {
    public static void main(String[] args) throws Exception {
        String input_analysis = "cells";
        String image_dir = "path/to/image_dir";
        String cell_parameters = "cell_parameters";
        String outlines = "show_outlines";
        int height = 800;
        int width = 800;
        String filenames = "image.tif";
        String outputfiles = "output/result.csv";
        String outlinefiles = "output/outlines.tif";

        File cellFile = new File(cell_parameters+"_parameters.txt");
        BufferedReader br = new BufferedReader(new FileReader(cellFile));
        String[] cell_line_parameters = br.lines().toArray(String[]::new);
        br.close();
        String PATH = cell_line_parameters[0];

        int min_cell_size = Integer.parseInt(cell_line_parameters[1]);
        int max_cell_size = Integer.parseInt(cell_line_parameters[2]);
        double min_cell_circularity = Double.parseDouble(cell_line_parameters[3]);
        double max_cell_circularity = Double.parseDouble(cell_line_parameters[4]);
        int min_neurite_size = Integer.parseInt(cell_line_parameters[5]);
        int max_neurite_size = Integer.parseInt(cell_line_parameters[6]);
        double min_neurite_circularity = Double.parseDouble(cell_line_parameters[7]);
        double max_neurite_circularity = Double.parseDouble(cell_line_parameters[8]);
        String CELL_THRESHOLD = cell_line_parameters[9];
        String NEURITE_THRESHOLD = cell_line_parameters[10];
        String WATERSHED_CHOICE = cell_line_parameters[11];

        if (CELL_THRESHOLD.equals("NO THRESHOLD")) {
            CELL_THRESHOLD = "Default";
        }
        if (NEURITE_THRESHOLD.equals("NO THRESHOLD")) {
            NEURITE_THRESHOLD = "Default";
        }

        IJ.run("Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction stack display add redirect=None decimal=3");
        ImageCalculator image_calc = new ImageCalculator();

        particle_analysis(input_analysis);
    }

public void particle_analysis(String analysis) {
    ImagePlus imp;
    if (analysis.equals("cells")) {
        IJ.open(image_dir + "/" + filenames);
        imp = IJ.getImage();
        IJ.run("8-bit");
        IJ.run("Auto Threshold", "method="+CELL_THRESHOLD);
        if (WATERSHED_CHOICE.equals("apply_watershed")) {
            IJ.run("Watershed");
            IJ.run("Analyze Particles...", "size="+ min_cell_size+"-"+max_cell_size+" pixel circularity="+ min_cell_circularity+"-"+max_cell_circularity+" show=Nothing display summarize");
        } else {
            IJ.run("Analyze Particles...", "size="+ min_cell_size+"-"+max_cell_size+" pixel circularity="+ min_cell_circularity+"-"+max_cell_circularity+" show=Nothing display summarize");
        }
        IJ.saveAs("Results", outputfiles);
        IJ.run("Clear Results");
        if (outlines.equals("show_outlines")) {
            IJ.run("Analyze Particles...", "size="+ min_cell_size+"-"+max_cell_size+" pixel circularity="+ min_cell_circularity+"-"+max_cell_circularity+" show=Nothing display summarize");
            ImagePlus overlay_ = ImagePlus.getOverlay(imp);
            IJ.newImage("blank_c", "RGB white", width, height, 1);
            imp = IJ.getImage();
            imp.setOverlay(overlay_);
            ImageProcessor imp3 = imp.flatten();
            IJ.run(imp3, "8-bit", "");
            IJ.saveAs(imp3, "Tiff", outputfiles);
        }
    } else if (analysis.equals("neurites")) {
        IJ.open(image_dir + "/" + filenames);
        imp = IJ.getImage();
        IJ.run("8-bit");
        IJ.run("Auto Threshold", "method="+NEURITE_THRESHOLD);
        if (WATERSHED_CHOICE.equals("apply_watershed")) {
            IJ.run("Watershed");
            IJ.run("Analyze Particles...", "size="+ min_neurite_size+"-"+max_neurite_size+" pixel circularity="+ min_neurite_circularity+"-"+max_neurite_circularity+" show=Nothing display summarize");
        } else {
            IJ.run("Analyze Particles...", "size="+ min_neurite_size+"-"+max_neurite_size+" pixel circularity="+ min_neurite_circularity+"-"+max_neurite_circularity+" show=Nothing display summarize");
        }
        IJ.saveAs("Results", outputfiles);
        IJ.run("Clear Results");
        if (outlines.equals("show_outlines")) {
            IJ.run("Analyze Particles...", "size="+ min_neurite_size+"-"+max_neurite_size+" pixel circularity="+ min_neurite_circularity+"-"+max_neurite_circularity+" show=Nothing display summarize");
            ImagePlus overlay_ = ImagePlus.getOverlay(imp);
            IJ.newImage("blank_c", "RGB white", width, height, 1);
            imp = IJ.getImage();
            imp.setOverlay(overlay_);
            ImageProcessor imp3 = imp.flatten();
            IJ.run(imp3, "8-bit", "");
            IJ.saveAs(imp3, "Tiff", outputfiles);
        }
    }
    } else if (analysis.equals("attachment")) { // Run neurite attachment point analysis
          ImagePlus img = IJ.open("{}/{}".format(image_dir, filenames));
          ImagePlus imp_c = IJ.getImage(); // Cell bodies
          ImagePlus imp_n = IJ.getImage(); // Neurites
          IJ.run(imp_c, "8-bit", "");
          IJ.run(imp_n, "8-bit", "");
      
          // Threshold highlighting neurites
          IJ.run(imp_c, "Auto Threshold", "method=" + NEURITE_THRESHOLD);
          IJ.run(imp_n, "Auto Threshold", "method=" + NEURITE_THRESHOLD);
          if (WATERSHED_CHOICE.equals("apply_watershed")) {
              IJ.run(imp_c, "Watershed", ""); // Watershed segmentation
              IJ.run(imp_c, "Analyze Particles...", "size=" + min_cell_size + "-" + max_cell_size + " pixel circularity=" + min_cell_circularity + "-" + max_cell_circularity + " show=Overlay"); // Use cell body parameters to extract overlay
              Overlay overlay_c = imp_c.getOverlay(); // Get cell body overlay
      
              IJ.run(imp_n, "Watershed", ""); // Watershed segmentation
              IJ.run(imp_n, "Analyze Particles...", "size=" + min_neurite_size + "-" + max_neurite_size + " pixel circularity=" + min_neurite_circularity + "-" + max_neurite_circularity + " show=Overlay"); // Use neurite parameters to extract overlay
              Overlay overlay_n = imp_n.getOverlay(); // Get neurite overlay
          } else {
              IJ.run(imp_c, "Analyze Particles...", "size=" + min_cell_size + "-" + max_cell_size + " pixel circularity=" + min_cell_circularity + "-" + max_cell_circularity + " show=Overlay"); // Use cell body parameters to extract overlay
              Overlay overlay_c = imp_c.getOverlay(); // Get cell body overlay
      
              IJ.run(imp_n, "Analyze Particles...", "size=" + min_neurite_size + "-" + max_neurite_size + " pixel circularity=" + min_neurite_circularity + "-" + max_neurite_circularity + " show=Overlay"); // Use neurite parameters to extract overlay
              Overlay overlay_n = imp_n.getOverlay(); // Get neurite overlay
          }
      
         // Blank image for pasting the overlay onto
        ImagePlus imp_c3 = IJ.createImage("{}_blank_c".format(filenames), "RGB white", width, height, 1);
        imp_c2 = IJ.getImage().setOverlay(overlay_c);
        imp_c2 = IJ.getImage();
        imp_c3 = imp_c2.flatten();
        IJ.run(imp_c3, "8-bit", "");
        IJ.run(imp_c3, "Make Binary", "");
        IJ.saveAs(imp_c3, "Tiff", "{}/imp_c3.tif".format(PATH));
        
        // Blank image for pasting the overlay onto
        ImagePlus imp_n3 = IJ.createImage("{}_blank_n".format(filenames), "RGB white", width, height, 1);
        imp_n2 = IJ.getImage().setOverlay(overlay_n);
        imp_n2 = IJ.getImage();
        imp_n3 = imp_n2.flatten();
        IJ.run(imp_n3, "8-bit", "");
        IJ.run(imp_n3, "Make Binary", "");
        IJ.saveAs(imp_n3, "Tiff", "{}/imp_n3.tif".format(PATH));
        IJ.run(imp_n3, "Find Edges", ""); // Sobel edge detector
        
        // Get the overlap between cell bodies and neurites - the attachment points
        ImageCalculator ic = new ImageCalculator();
        ImagePlus imp_res = ic.run("Multiply create", imp_n3, imp_c3);
        IJ.saveAs(imp_res, "Tiff", "{}/{}_imp_res.tif".format(PATH, filenames));
        IJ.run(imp_res, "Analyze Particles...", "size=0-100 pixel circularity=0.00-1.00 show=Nothing display summarize");
        IJ.saveAs("Results", "{}".format(str(outputfiles)));
        IJ.run("Clear Results");
        if (outlines.equals("show_outlines")) {
            IJ.run("Analyze Particles...", "size={}-{} pixel circularity={}-{} show=Nothing display summarize".format(min_cell_size, max_cell_size, min_cell_circularity, max_cell_circularity));
            overlay_ = ImagePlus.getOverlay(imp_res);
            ImagePlus imp2 = IJ.createImage("blank_b", "RGB white", width, height, 1);
            imp2 = IJ.getImage().setOverlay(overlay_);
            imp2 = IJ.getImage();
            ImagePlus imp3 = imp2.flatten();
            IJ.run(imp3, "8-bit", "");
            IJ.saveAs(imp3, "Tiff", "{}".format(str(outlinefiles)));
        }
public void fileRead() {
    try {
        FileReader output = new FileReader(outputfiles);
    } catch (IOException e) {
        try (FileWriter output = new FileWriter(outputfiles)) {
            output.write("NO IDENTIFIED MOTIFS");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}

fileRead();




