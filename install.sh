#!/bin/bash

set -e
read -r -p "Please give a name for the conda environment: " env
conda create -n "$env" --yes
conda install -n "$env" -c conda-forge --file requirements/build.txt \
--file requirements/run.txt \
--file requirements/test.txt \
--file requirements/docs.txt \
--yes
conda run --live-stream --no-capture-output -n "$env" pip install -r requirements/pip.txt
conda run --live-stream --no-capture-output -n "$env" pip install -e .
echo "Package has been successfully installed."
echo "Please run the following command to activate the environment."
echo ""
echo "    conda activate $env"
echo ""
echo "Please run the following command to install the pdfgetx."
echo ""
echo "    pdfstream_install <path to .whl file>"
