# Verible stage
FROM hdlc/verible:latest AS verible

# Verilator stage
FROM hdlc/verilator:latest AS verilator

# Base image
FROM python:3-slim

ENV LC_ALL=C

# Copy Verible binaries from the verible stage
COPY --from=verible /usr/local/bin/verible* /usr/local/bin/

# Copy Verilator binaries from the verilator stage
COPY --from=verilator /usr/local/bin/verilator* /usr/local/bin/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git

# Set the working directory to /app
WORKDIR /app

# Install cocotb and other Python dependencies
COPY ../requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Re-synchronize the OS package index
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*
