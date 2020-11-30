Integration
===========

What does integration do?
-------------------------

Integration is to calculate XRD data from diffraction image.
There are four steps in PDFstream integration:
background subtraction, auto masking, histogram calculation with corrections, and visualization.

The background subtraction is to subtract the diffraction image from the sample by the diffraction image of the
background multiplied by a scalar which is one in default. The background diffraction image is usually the
diffraction of air and container of the sample. Two images must have the same dimension.

The auto masking is to mask the background subtracted image automatically. In default settings, the pixels at
the margin of the image, the pixels whose intensity is below the low threshold or above the high threshold and
the pixels whose intensity is too far away from the median value of the pixels in a ring will be masked out.
The masked pixles will not be counted in the histogram calculation.

The histogram calculation is to calculate a histogram of intensities on the pixels. The pixels are binned in
rings and the mean value will be calculated for the bins. The rings will be mapped to the momentum transfer value,
two theta value or radius according to users' settings. The result will be the XRD data and it will be saved
in .chi files.
This step is based on the
`pyFAI.azimuthalIntegrator <https://pyfai.readthedocs.io/en/latest/api/pyFAI.html#module-pyFAI.azimuthalIntegrator>`_.
Before the histogram, polarization correction and other processes will be done according to the settings.

The visualization is to show the masked background subtracted image and the result of the histogram. Users
can tune the visualization settings to achieve their desired effects.

How to do integration?
----------------------

Here shows the python example how to do the integration. Since
there is a one-to-one relation ship between the python function in `pdfstream` and the command line,
the same tasks can be done using the command line.

Import the function to start.

.. code-block:: python

    from pdfstream.cli import integrate

A simple integration
^^^^^^^^^^^^^^^^^^^^

For example, we are going to calculate XRD data I(Q) using diffraction image "sample_diffraction.tiff".
We have already done the calibration and gotten the .poni file "geometry.poni".

We run the following line to calculate XRD data I(Q).

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff"
    )

After it finishes, we will find a file "sample_diffraction.chi" in the same folder where we run the script.

If we would like to integrate another image "another_sample_diffraction.tiff" using the same .poni file.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        "another_sample_diffraction.tiff"
    )

We can add an arbitrary number of image files after the first argument. The configuration for the integration is
all in the key word arguments described in the following sections.


Output directory
^^^^^^^^^^^^^^^^

If we would like to output the files in a directory called ``data``, we can use key ``output_dir``.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        output_dir="data"
    )

If the folder ``data`` doesn't exist, it will be created.

Background subtraction
^^^^^^^^^^^^^^^^^^^^^^

Continuing with the last example, we would like to subtract the background scattering from the air and the
container of our sample and the scattering is measured and saved in the "background_diffraction.tiff".
We run the following line. Remember that all the arguments except .poni file and image files muse be key word
arguments.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        bg_img_file="background_diffraction.tiff"
    )

If the background image is measured using a 10 times stronger beam intensity, we can use ``bg_scale`` to scale
the background image.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        bg_img_file="background_diffraction.tiff",
        bg_scale=0.1
    )

Auto masking
^^^^^^^^^^^^

In default, the auto masking is applied using the default setting.

If we would like to tune the setting, we can use the key ``mask_setting``

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        mask_setting={
            "alpha": 1.5,
            "lower_thresh": 1.,
            "upper_thresh": 1e5,
            "edge": 50
        }
    )

If we would like to use our own mask "user_mask.npy" overlapping with the auto generated mask,
we can use the key ``mask_file``.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        mask_file="user_mask.npy"
    )

Note that `PDFstream` use the `pyFAI` convention of masking. The mask is an array of integers. The 0 pixels are
good and the 1 pixels are bad which will be masked out.

If we don't want the auto masking, we can set the ``mask_setting`` to ``"OFF"``

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        mask_file="user_mask.npy"
        mask_setting="OFF"
    )

This will allow us to use our own mask. Also, we can run without any masks using the following line.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        mask_setting="OFF"
    )

Histogram Calculation
^^^^^^^^^^^^^^^^^^^^^

In default, the histogram calculation is applied using the default setting.

The configuration can be tuned by the key ``integ_setting``. An example below shows how to tune the configuration
to calculate a histogram of I(2theta) with 2048 points using the numpy method.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        integ_setting={
            "npt": 2048,
            "unit": "2th_deg",
            "method": "numpy"
        }
    )

For details of the configuration, please see
`pyFAI <https://pyfai.readthedocs.io/en/latest/usage/cookbook/integration_with_python.html?highlight=integrate1d#Azimuthal-averaging-using-pyFAI>`_

Visualization
^^^^^^^^^^^^^

In default, the visualization configuration is applied using the default setting.

We can use the key ``img_setting`` to tune how the image is shown. The keys are the same as those of
`matplotlib.axes.Axes.matshow <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.matshow.html>`_.
An additional key is ``z_score``. It determines the maximum and minimum values for the color map. The color
map is determined by vmin = mean - z_score * std, vamx = mean + z_score * std, where mean is the mean value of
the image, std is the standard deviation of the image. If we would like to show image in a large constrast,
we can tune down the ``z_score`` to 1 for example.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        img_setting={'z_score': 1}
    )

We can use the key ``plot_setting`` to tune how the result of integration is shown. The keys are the same as those
of the `matplotlib.axes.Axes.plot <https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html>`_.
For example, we would like to plot a line with green circles.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        plot_setting={'marker': 'o', 'color': 'green'}
    )

Both of the key ``img_setting`` and ``plot_setting`` can be set to ``OFF`` to skip the visualization steps.

.. code-block:: python

    integrate(
        "geometry.poni",
        "sample_diffraction.tiff",
        img_setting="OFF",
        plot_setting="OFF"
    )

Parallel Computing
^^^^^^^^^^^^^^^^^^

The `integrate` supports parallel computing for multiple images.
If we would like to use the parallel computing for the integration for a long list of images, we can use the
key ``parallel``.

.. code-block:: python

    integrate(
        "geometry.poni",
        a_long_list_of_image_files,
        img_setting="OFF",
        plot_setting="OFF",
        parallel=True
    )

The efficiency depends on how many cores our machine has. It is recommended to turn off the visualization if
there are a large number of images.
