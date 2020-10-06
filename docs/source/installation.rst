============
Installation
============

Prerequisites
-------------

Install `Anaconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_.

After conda is installed, at the commnad line::

    conda config --append channels nsls2forge
    conda config --append channels conda-forge

(Optional) Get the .whl file of `PDFgetX <https://www.diffpy.org/products/pdfgetx.html>`_. This package is used
to transform the XRD data to PDF data.

General Installation
--------------------

Users can install the `pdfstream` using conda. It is suggested to create a new environment for it.

At the command line::

    conda create -n pdfstream_env pdfstream

The ``pdfstream_env`` in the command is the name of the environment. It can be changed to any name.

Before using the `pdfstream`, activate the environment::

    conda activate pdfstream_env

Development Installation
------------------------

**Fork** and clone the github repo and change the current directory::

    git clone https://github.com/<your account>/pdfstream

Remember to change ``<your account>`` to the name of your github account.

Change directory::

    cd pdfstream

Create an environment with all the requirements::

    conda create -n pdfstream_env --file requirements/build.txt --file requirements/run.txt --file requirements/test.txt

(Optional) For the maintainer, install the packages for building documents and releasing the software::

    conda install -n pdfstream_env --file requirements/docs.txt --file requirements/release.txt

Activate the environment::

    conda activate pdfstream_env

Install the `pdfstream` in development mode::

    python -m pip install -e .

