Use python
==========

The data processing are done by using python functions.

Average images
--------------

To average several diffraction images to be one image, use

.. autofunction:: pdfstream.cli.average

Azimuthal integration
---------------------

To integrate the diffraction image in azimuthal direction, use

.. autofunction:: pdfstream.cli.integrate

Instrumental Calibration
------------------------

To calibrate the instrumental effect on calibration, use

.. autofunction:: pdfstream.cli.instrucalib

Visualization
-------------

To visualize a single data file, use

.. autofunction:: pdfstream.cli.visualize

To visualize several data files, use

.. autofunction:: pdfstream.cli.waterfall


Modeling
--------

To create a fit recipe, use

.. autofunction:: pdfstream.modeling.main.multi_phase

To optimize the model in the recipe, use

.. autofunction:: pdfstream.modeling.main.optimize

To report the optimization results, use

.. autofunction:: pdfstream.modeling.main.report

To save the results, first generate the save function that link to db collections, using

.. autofunction:: pdfstream.modeling.csvdb.gen_fs_save

Then, use the returned function to save the recipe.
