Use command line interface (CLI)
================================

PDFstream use `python-fire <https://github.com/google/python-fire>`_ to create the CLI tools. Please read
the `guide <https://google.github.io/python-fire/guide/>`_ to know about the syntax before using the PDFstream
CLI. Then, run the help command to look at the functionalities of pdfstream CLI::

    pdfstream -- --help

Average images
--------------

To average several diffraction images to be one image, use 'pdf_average'.
Run the command for help::

    pdfstream average -- -- help

Azimuthal integration
---------------------

To integrate the diffraction image in azimuthal direction, use 'pdf_integrate'.
Run the command for help::

    pdfstream integrate -- --help

Transformation
--------------

If the `diffpy.pdfgetx` is installed, transformation from XRD data to PDF data can be done using `pdfgetx3`
Run the command for help::

    pdfgetx3 --help

The `pdfstream` also provides a simple interface.
Run the command for help::

    pdfstream transform -- --help

Visualization
-------------

To visualize a single data file, use 'pdf_visualize'.
Run the command for help::

    pdfstream visualize -- --help

To visualize several data files, use 'pdf_waterfall'.
Run the command for help::

    $ pdfstream waterfall -- --help

