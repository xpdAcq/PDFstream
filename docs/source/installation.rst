============
Installation
============

Prerequisites
-------------

Install `Anaconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_.

After conda is installed, at the commnad line::

    $ conda config --append channels diffpy
    $ conda config --append channels conda-forge

Install `PDFgetX <https://www.diffpy.org/products/pdfgetx.html>`_ in the conda environment where the pdfstream will be installed.

General Installation
--------------------

At the command line::

    $ conda install pdfstream

Development Installation
------------------------

Fork and clone the github repo and change the current directory::

    $ git clone https://github.com/<your account>/pdfstream

Remember to change `<your account>` to the name of your github account.

Change directory::

    $ cd pdfstream

Install the requirements::

    $ conda install --file requirements/build.txt --file requirements/run.txt --file requirements/test.txt

If you are the maintainer, you also need to install the packages for building docs and release::

    $ conda install --file requirements/docs.txt --file requirements/release.txt

Install the pdfstream in development mode::

    $ python -m pip install -e .

