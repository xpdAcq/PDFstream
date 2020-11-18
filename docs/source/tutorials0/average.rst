Average
=======

When we have a series of diffraction images for one sample and we would like to calculate the average of them
to minimize the fluctuation in the intensity, we can use the average tool in `pdfstream`.

A simple average
----------------

For example, we have "image1.tiff", "image2.tiff", "image3.tiff" and we would like to calculate the average of
them and save the results in the file "averaged_image.tiff".

.. code-block:: python

    from pdfstream.cli import average

    average(
        "averaged_image.tiff",
        "image1.tiff",
        "image2.tiff",
        "image3.tiff"
    )

We can also do it in command line::

    pdfstream average averaged_image.tiff image1.tiff image2.tiff image3.tiff

Add weights
-----------

If we would like to calculated a weighted average, we can use the key ``weights``
For example, "image1.tiff", "image2.tiff", "image3.tiff" have weights 0.6, 0.2, 0.2.

.. code-block:: python

    average(
        "averaged_image.tiff",
        "image1.tiff",
        "image2.tiff",
        "image3.tiff",
        weights=[0.6, 0.2, 0.2]
    )

We can also do it in command line::

    pdfstream average averaged_image.tiff image1.tiff image2.tiff image3.tiff --weights=[0.6,0.2,0.2]

