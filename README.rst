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

Create a new environment.

``conda create -n pdfstream``

``conda activate pdfstream``

Install the diffpy.pdfgetx following the `instructions <https://www.diffpy.org/doc/pdfgetx/2.0.0/install.html>`_.

Install the pdfstream from the conda following the `webpage <https://anaconda.org/st3107/pdfstream>`_.

Features
--------

Integration
===========

It supports the azimuthal integration of the diffraction image to one dimensional diffraction pattern. It uses
the auto masking functionality in the xpdtools and the integration functionality in pyFAI.

It can be used in the command line interface (CLI). Try the following command in the terminal to learn about the
usage.

``integrate -- --help``

It can also be used in python scripts. See the function `pdfstream.cli.integrate`.