=========
pdfstream
=========

.. image:: https://img.shields.io/travis/st3107/pdfstream.svg
        :target: https://travis-ci.org/st3107/pdfstream

.. image:: https://img.shields.io/pypi/v/pdfstream.svg
        :target: https://pypi.python.org/pypi/pdfstream


The data streaming PDF analysis software

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://st3107.github.io/pdfstream.

Installation
------------

Development mode
================

Install the packages listed in the requirements.txt and requirement-dev.txt using anaconda.

``conda install --file requirements.txt -c diffpy -c conda-forge --yes``

``conda install --file requirements-dev.txt -c diffpy -c conda-forge --yes``

Then clone this repo and tnstall this package in development mode..

``git clone https://gitlab.thebillingegroup.com/stao/pdfstream.git``

``cd pdfstream``

``pip install -e . --no-deps``

Features
--------

Integration
===========

It supports the azimuthal integration of the diffraction image to one dimensional diffraction pattern. It uses
the auto masking functionality in the xpdtools and the integration functionality in pyFAI.

It can be used in the command line interface (CLI). Try the following command in the terminal to learn about the
usage.

``image_to_iq -- --help``

It can also be used in python scripts. See the function `pdfstream.cli.image_to_iq`.