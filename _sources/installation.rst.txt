============
Installation
============

Prerequisites
-------------

Install `Anaconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_.

Install `PDFgetX <https://www.diffpy.org/products/pdfgetx.html>`_ in the conda environment.

General Installation
--------------------

At the command line::

    $ conda install -c st3107 pdfstream

Development Installation
------------------------

Clone the github repo and change the current directory::

    $ git clone https://github.com/st3107/pdfstream
    $ cd pdfstream

Install the requirements::

    $ conda install -c conda-forge diffpy --file requirements/run.txt --file requirements/test.txt --file
    requirements/build.txt

Install the pdfstream in development mode::

    $ python -m pip install -e .

