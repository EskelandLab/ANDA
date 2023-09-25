FROM fiji/fiji:latest

# Set working directory
WORKDIR /workspace

RUN apt-get update && apt-get install -y openjdk-11-jre

# Download and install ImageJ
RUN wget https://downloads.imagej.net/fiji/latest/fiji-linux64.zip -O fiji-linux64.zip && \
    unzip fiji-linux64.zip && \
    rm fiji-linux64.zip && \
    mv Fiji.app /app/Fiji.app

COPY ANDA.sh /workspace/
COPY pipeline_parameters.txt /workspace/
COPY cell_metrics.py /workspace/
COPY data_sort.py /workspace/

RUN chmod +x /workspace/ANDA.sh
RUN /workspace/ANDA.sh /workspace/pipeline_parameters.txt
