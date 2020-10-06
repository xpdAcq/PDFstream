Use python
==========

The data processing are done by using python functions.

Average images
--------------

To average several diffraction images to be one image, use the following function.

.. autofunction:: pdfstream.cli.average

Azimuthal integration
---------------------

To integrate the diffraction image in azimuthal direction, use the following function.

.. autofunction:: pdfstream.cli.integrate


Transformation
--------------

If the `diffpy.pdfgetx` is installed,
transformation from XRD data to PDF data can be done using the following funciton.

.. autofunction:: pdfstream.transformation.cli.transform

Visualization
-------------

To visualize a single data file, use the following function.

.. autofunction:: pdfstream.cli.visualize

To visualize several data files, use the following function.

.. autofunction:: pdfstream.cli.waterfall
