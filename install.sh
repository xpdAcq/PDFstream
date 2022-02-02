#!/bin/bash

set -e
read -p "Please give a name for the conda environment: " env
echo "Download crystalmapping repo ..."
conda env create -n $env
conda install -n $env -c conda-forge pdfstream
echo "Package has been successfully installed."
echo "Please run the following command to activate the environment."
echo ""
echo "    conda activate $env"
echo ""
echo "Please run the following command to install the pdfgetx."
echo ""
echo "    pdfstream_install <path to .whl file>"
