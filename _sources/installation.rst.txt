============
Installation
============

Prerequisites
-------------

Install `Anaconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_.

After conda is installed, at the commnad line::

    conda config --append channels nsls2forge

(Optional) Get the .whl file of `PDFgetX <https://www.diffpy.org/products/pdfgetx.html>`_. This package is used
to transform the XRD data to PDF data.

General Installation
--------------------

This is the instructions for the users. It is suggested to install it in a clean environment.

At the command line::

    conda create -n pdfstream_env pdfstream

The ``pdfstream_env`` in the command is the name of the environment. It can be changed to any name.

Activate the environment::

    conda activate pdfstream_env

(Optional) Install the `diffpy.pdfgetx` using .whl file::

    python -m pip install <path to .whl file>

Change the ``<path to .whl file>`` to the path of the .whl file on your computer.

Before using the `PDFstream`, remember to activate the environment::

    conda activate pdfstream_env

Development Installation
------------------------

This is the instructions for the developers and maintainers of the package.

**Fork** and clone the github repo and change the current directory::

    git clone https://github.com/<your account>/pdfstream

Remember to change ``<your account>`` to the name of your github account.

Change directory::

    cd pdfstream

Create an environment with all the requirements::

    conda create -n pdfstream_env --file requirements/build.txt --file requirements/run.txt --file requirements/test.txt

Install the packages for building documents and releasing the software::

    conda install -n pdfstream_env -c conda-forge --file requirements/docs.txt --file requirements/release.txt

Activate the environment::

    conda activate pdfstream_env

Install the `diffpy.pdfgetx` using .whl file::

    python -m pip install <path to .whl file>

Install the necessary pypi packages::

    python -m pip install -r requirements/pip.txt

Change the ``<path to .whl file>`` to the path of the .whl file on your computer.

Install the `PDFstream` in development mode::

    python -m pip install -e . --no-deps

