FROM gitpod/workspace-full-vnc

USER gitpod

## Install Python with --enable-shared
ARG PYTHON_VERSION=3.9.2
RUN rm -rf ${HOME}/.pyenv/versions/${PYTHON_VERSION}
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

RUN pip3 install --upgrade pip

# Install extra packages
RUN pip3 install -U cocotb numpy

# Re-synchronize the OS package index
RUN sudo apt-get update

# Install all needed packages for all simulators
RUN sudo apt-get install -y perl make flex gnat swig autoconf g++ bison libfl2 libfl-dev ccache libgoogle-perftools-dev numactl perl-doc
RUN sudo rm -rf /var/lib/apt/lists/*

## Install Verilator
#ENV VERILATOR_BRANCH=stable
ENV VERILATOR_BRANCH=v4.106

RUN git clone https://github.com/verilator/verilator.git --branch ${VERILATOR_BRANCH} verilator \
    && unset VERILATOR_ROOT \
    && cd verilator \
    && autoconf \
    && ./configure \
    && make --silent \
    && sudo make --silent install \
    && cd .. \
    && rm -rf verilator
