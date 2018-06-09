#!/usr/bin/env bash

echo "Installing Python"

MINICONDA=Miniconda3-latest-Linux-x86_64.sh
PYTHON=3.6
CONDA_DIR=/opt/anaconda
CONDA_BIN=${CONDA_DIR}/bin/conda
ENV_NAME=server
PYTHON_BIN=${CONDA_DIR}/envs/${ENV_NAME}/bin/python

echo "Downloading miniconda installer"
wget --quiet http://repo.continuum.io/miniconda/${MINICONDA}

echo "Installing miniconda"
chmod +x ${MINICONDA}
./${MINICONDA} -b -p ${CONDA_DIR}
echo "export LC_CTYPE=en_US.UTF-8" >> /home/vagrant/.bashrc
echo "export LC_ALL=en_US.UTF-8" >> /home/vagrant/.bashrc
echo "PATH=/opt/anaconda/bin:\$PATH" >> /home/vagrant/.bashrc

rm ${MINICONDA}

echo "Creating new conda environment"
${CONDA_BIN} create -n ${ENV_NAME} -y -q python=${PYTHON}

echo "Installing requirements.txt"
${PYTHON_BIN} -m pip install --quiet -r /vagrant/requirements.txt 2> /dev/null
