# Use a base image with the necessary OS and Python environment
FROM python:3.8

# Set a working directory within the container
WORKDIR /app

# Install Java (required for ImageJ)
RUN apt-get update && apt-get install -y openjdk-11-jre

# Download and install ImageJ
RUN wget https://downloads.imagej.net/fiji/latest/fiji-linux64.zip -O fiji-linux64.zip && \
    unzip fiji-linux64.zip && \
    rm fiji-linux64.zip && \
    mv Fiji.app /app/Fiji.app

# Copy the pipeline scripts, input files, and Snakefile into the container
COPY cell_metrics.py data_sorting.py pipeline_parameters.txt cell_parameters.txt Snakefile /app/

# Install any required Python dependencies (if any) using pip
# For example, if you need to install a specific package:
# RUN pip install package_name

# Define the entry point for your pipeline (the initial script to run)
CMD ["/app/Fiji.app/ImageJ-linux64", "--headless", "/app/cell_metrics.py"]
