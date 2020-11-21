Transformation
==============

The transformation can be done using the `diffpy.pdfgetx <https://www.diffpy.org/doc/pdfgetx/2.1.0/index.html>`_.
Run the following command for help::

    pdfgetx3 --help

The software supports interactive mode and was better for the exploration of suitable parameters for the data.
The following section is about the transformation in `PDFstream`.
If you are going to use `diffpy.pdfgetx`, please skip the following sections.

A simple transformation
^^^^^^^^^^^^^^^^^^^^^^^

The `PDFstream` also provides a simple interface for the transformation.
At command line::

    pdfgetx3 --createconfig pdfconfig.cfg

It will creat a configuration file. Edit the file to change the configuration for data processing.
Close the file and run the command::

    pdfstream transform pdfconfig.cfg xrd_data.chi

Or run the function in python.

.. code-block:: python

    from pdfstream.transformation.cli import transform

    transform(
        "pdfconfig.cfg",
        "sample_diffraction.tiff"
    )

The output files will be saved in the current directory.

Output directory
^^^^^^^^^^^^^^^^

If we would like to output the files in a specific directory called ``data_folder``, we can use the key
``output_dir``.

.. code-block:: python

    transform(
        "pdfconfig.cfg",
        "sample_diffraction.tiff",
        output_dir="data_folder"
    )

Visualization
^^^^^^^^^^^^^

If we would like to tune the visualization of data, we can use the key ``plot_setting``.
The keys are the same as those
of the `matplotlib.axes.Axes.plot <https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html>`_.

For example, we would like to plot a line with green circles.

.. code-block:: python

    transform(
        "pdfconfig.cfg",
        "sample_diffraction.tiff",
        plot_setting={'marker': 'o', 'color': 'green'}
    )

If we don't want visualization, we can turn if off by set the ``plot_setting`` to "OFF".

.. code-block:: python

    transform(
        "pdfconfig.cfg",
        "sample_diffraction.tiff",
        plot_setting="OFF"
    )


Parallel computing
^^^^^^^^^^^^^^^^^^

The `transform` supports parallel computing for multiple images.
If we would like to use the parallel computing for the integration for a long list of images, we can use the
key ``parallel``.

.. code-block:: python

    transform(
        "pdfconfig.cfg",
        "sample_diffraction.tiff",
        plot_setting="OFF",
        parallel=True
    )

The efficiency depends on how many cores our machine has. It is recommended to turn off the visualization if
there are a large number of data files. Because the transformation is relatively quick, the acceleration of the
speed may not be obvious.
