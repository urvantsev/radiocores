# Verible stage
FROM hdlc/verible:latest AS verible

# Verilator stage
FROM verilator/verilator:v5.024 AS verilator

# Base image
FROM python:3-slim

ENV LC_ALL=C

# Copy Verible binaries from the verible stage
COPY --from=verible /usr/local/bin/verible* /usr/local/bin/

# Copy Verilator binaries and other necessary files from the verilator stage
COPY --from=verilator /usr/local/bin/verilator* /usr/local/bin/
COPY --from=verilator /usr/local/share/verilator/ /usr/local/share/verilator/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    make \
    git \
    clang \
    build-essential \
    libffi-dev \
    python3-dev \
    ccache \
    wget \
    tar \
    cmake \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxmu-dev \
    g++ \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Define the SystemC version and installation directory
# ENV SYSTEMC_VERSION=2.3.3
# ENV SYSTEMC_DIR=/usr/local/systemc-$SYSTEMC_VERSION

# Download and install SystemC
# RUN wget http://www.accellera.org/images/downloads/standards/systemc/systemc-$SYSTEMC_VERSION.tar.gz && \
#     tar -xvf systemc-$SYSTEMC_VERSION.tar.gz && \
#     cd systemc-$SYSTEMC_VERSION && \
#     mkdir objdir && \
#     cd objdir && \
#     cmake .. -DCMAKE_INSTALL_PREFIX=$SYSTEMC_DIR -DCMAKE_CXX_STANDARD=11 && \
#     make -j$(nproc) && \
#     make install && \
#     cd ../.. && \
#     rm -rf systemc-$SYSTEMC_VERSION systemc-$SYSTEMC_VERSION.tar.gz

# Set environment variables for SystemC
# ENV SYSTEMC_HOME=$SYSTEMC_DIR
ENV LD_LIBRARY_PATH=$SYSTEMC_HOME/lib:$LD_LIBRARY_PATH
ENV CPLUS_INCLUDE_PATH=$SYSTEMC_HOME/include:$CPLUS_INCLUDE_PATH

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Re-synchronize the OS package index
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the default command to execute when running the container
CMD ["bash"]
