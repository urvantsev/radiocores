# Verible
FROM hdlc/verible:latest AS verible

# Verilator
# Copy verible binaries from previous stage
FROM hdlc/verilator:latest
COPY --from=verible /usr/local/bin/verible* /usr/local/bin

ENV LC_ALL=C

# Install cocotb
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-tk git
RUN pip3 install --upgrade pip
RUN pip3 install -U cocotb numpy matplotlib ipykernel scipy pandas scikit-commpy toolz pytest

# Re-synchronize the OS package index
RUN apt-get update
