XPD Server
==========

The XPD Server is a server designed for x-ray powder diffraction experiments. It will process image data from
a two dimensional detector.

.. _xpd-server-functionalities:

What does XPD Server do?
------------------------

The XPD Server receives the message from a proxy. Depending on what type of the data is in the message, the server
will apply different data processing method to it.

Calibration
^^^^^^^^^^^

If the XPD Server finds that the data is intended to be used to calibrate the sample detector distances along with
other experiment setup in the system, it will start the calibration process as followings:

#. Find the dark frame image in the database.

#. Subtract the light frame image in the message by the dark frame image and get the dark subtracted image.

#. Ask users to draw mask on the image.

#. Ask users to select several points on the inner Debye-Scherrer rings to allocate their positions.

#. Fit the ring positions to optimize the experiment setup geometry parameters including samples detector distance and detector frame orientation.

#. Use the parameters to do azimuthal integration on the image to get the integration results.

#. Ask users to check the results and save it in a poni file at the designated place.

Data Reduction
^^^^^^^^^^^^^^

If the XPD Server finds that the data is a light frame diffraction image of a sample, it will start the data
reduction process as followings:

#. Find the dark frame image in the database.

#. Find the background light frame image and its dark frame image in the database.

#. Do dark subtraction on the background image.

#. Do dark subtraction on the sample image.

#. Subtract the sample image by the background image.

#. Mask the bad pixels in the image.

#. Do azimuthal integration on the image to get the x-ray diffraction pattern (XRD) on momentum transfer grid.

#. Transfer the XRD pattern to the reduced pair distribution function (PDF).

#. (Optional) Dump the processed data with the independent variables (e. g. temperature) in the database.

#. (Optional) Export the processed images in tiff files.

#. (Optional) Export the reduced data in numpy files.

#. (Optional) Export the scalar data in the measurement in csv files.

#. (Optional) Export metadata in json files.

#. (Optional) Visualize the images in a window.

#. (Optional) Visualize the waterfall plot of the reduced data in a window.

#. (Optional) Visualize the scalar plot of the maximum peak height and peak position of the maximum peak in the XRD and PDF.

Dark frame
^^^^^^^^^^

If the XPD Server finds that the data is a dark frame image, it will ignore the data and do nothing. It assumes
that the data frame image has been already record in the database in another process.

How to setup a XPD Server?
--------------------------

There are only two steps: first, write a configuration file or download one; start a server in terminal using
that file.

Write the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The server needs a .ini file. This file contains all the configuration to build a server. An example of the file
is shown below. Please read the comments in the file to know what are the meaning of the parameters.

.. include:: ../_static/xpd_server.ini
   :literal:

The parameters you can change are the values that behind the equity symbol in each row. Usually, you don't need
to change the file structure but if you would like to do that, you can find what file structure is supported
`here <https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_.

Start the server
^^^^^^^^^^^^^^^^

Assume that you have written a configuration file and the path to it is "~/xpd_server.ini".

In terminal, run the command::

    run_server ~/xpd_server.ini

The server will start in terminal.

If you would like to terminate the server, press ``CTRL + C``.

(Recommended) Put the configuration file in default folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are tired of typing the path to the configuration file, you can put the .ini file in the default folder,
the software will find the configuration file for the server according to the name parameter in the
configuration file.

To know where the default configuration folder is, run the command::

    print_server_config_dir

You will find the path to the directory. Put the .ini file in that directory and then you can just run::

    run_server xpd_server

The server will start.

(Optional) Run the server in a detached background process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Similar to what you have done with the proxy, you can also run the server in background and detach it from the
terminal so that you don't need to start the server every time. To do this, in terminal, run command::

    nohup run_server ~/xpd_server.ini &

If you have put the "xpd_server.ini" in default folder, run this instead::

    nohup run_server xpd_server &

You will find the message from the server in file "nohup.out".

If you would like to terminate the background process, in terminal, run command::

    kill <job ID>

The ``<job ID>`` is a number that shows up after you run the command ``nohup run_server xpd &``.

How to do the calibration?
--------------------------

When you run the ``run_calibration()`` in ``bsui`` of xpdacq, the xpd server responds and gives you a window of
diffraction image. You will finish the calibration using that interface . Please see the
`tutorials <https://pyfai.readthedocs.io/en/master/usage/cookbook/calib-gui/index.html>`_ to learn
how to use it. When you are at the last step of the tutorials and you are going to save the geometry in a PONI
file, please save the file at exact where it is first shown in the finder window after you click the
"SAVE AS PONI" button. Only in this way the software ``xpdacq`` can find the file and use it.

How to do the data reduction?
-----------------------------

The data reduction is totally automatic after you start the server and finish your calibration run. The server
will process the streaming data by itself according to the configuration. You will find messages in the terminal
where the server is running. It tells you if the message of a run is received and if there are any errors.

.. _xpd-server-data:

How to get the data back home?
------------------------------

Database
^^^^^^^^

The processed data will be archived in the ``an_db`` database specified in the configuration.
It is the name of an intake catalog.
Please use `databroker <https://blueskyproject.io/databroker/>`_ to access it.

Files
^^^^^

The processed data will also be exported to the files in the ``tiff_base`` folder specified in the configuration.

Here is an example of the file structure that is generated from a temperature ramping.

.. code-block:: text

    tiff_base
    ├── array_data
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-data-1.csv
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-data-2.csv
    │   └── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-data-3.csv
    ├── images
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-bg_sub_image-0.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-bg_sub_image-1.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-bg_sub_image-2.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-dk_sub_image-0.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-dk_sub_image-1.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-dk_sub_image-2.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-mask-0.tiff
    │   ├── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-mask-1.tiff
    │   └── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-mask-2.tiff
    ├── metadata
    │   └── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_meta.json
    └── scalar_data
        └── 014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary.csv

The diffraction image data together with the mask data will be saved in .tiff files in the folder ``images``.
The scalar data like temperature will be in the .csv files in the folder ``scalar_data``.
You can match the scalar data with the image by the start id and the sequence number in the file.
The reduced data like XRD and PDF will be in the .csv files in folder ``array_data``.
Each column in the dataframe in the .csv files is an array data.
You can match the dataframe with the image by the start id and the sequence number in the file.
The metadata like the sample information, wavelength of the beam, and the experiment setup are saved in
the .json files in folder ``metadata``.

Meaning of file name
^^^^^^^^^^^^^^^^^^^^

Here, we use a file ``014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55_Ni_primary-bg_sub_image-1.tiff`` as an example.

The prefix of the file is defined in the configuration.
It usually includes a long non-human-readable string, like ``014cc82d-0631-4b8b-bbfd-7e6c7d7c8f55``.
This string is the unique ID of a bluesky run, or in plain words, one measurement.
It can be used to identify which data is from the same run.
After it, you may find other information about the measurement like the sample name ``Ni``.

If there is a ``-`` in file name. Usually, it means that the file is a part of the data from the measurement.
Which part it is is indicated by the name of the data key.
For example, ``bg_sub_image`` here means the data key of background subtracted image.
There might be multiple background subtracted images in one run so there is usually a number to index the image,
like ``1`` in the example.

The data keys and their meanings are defined in the schemas shown below.

.. code-block:: text

    dk_sub_image: the array of dark dark subtracted image
    bg_sub_image: the array of dark dark subtracted background subtracted image
    mask: the array of mask where 0 is good pixel and 1 is bad pixel
    chi_Q: the array of momentum transfer Q in azimuthal integration result I(Q)
    chi_I: the array of intensity in I azimuthal integration result I(Q)
    chi_max: the maximum value of I in azimuthal integration result I(Q)
    chi_argmax: the value of Q at the maximum I in azimuthal integration result I(Q)
    iq_Q: the array of momentum transfer Q in the cropped and interpolated I(Q)
    iq_I: the array of intensity I in the cropped and interpolated I(Q)
    sq_Q: the array of momentum transfer Q in the structure factor S(Q)
    sq_S: the array of intensity I in the structure factor S(Q)
    fq_Q: the array of momentum transfer Q in the reduced structure factor F(Q)
    fq_F: the array of intensity I in the reduced structure factor F(Q)
    gr_r: the array of atomic pair distance r in the reduced pair distribution function G(r)
    gr_G: the array of pair distribution function G in the reduced pair distribution function G(r)
    gr_max: the maximum value of G in the reduced pair distribution function G(r)
    gr_argmax: the value of r at the maximum of G in the reduced pair distribution function G(r)

The schemas may be different depending on the version of package.
If you would like to find out what is schemas for the package on your local machine, please run the command below
in terminal::

    python -c "from pdfstream.schemas import analysis_out_schemas, print_data_keys; print_data_keys(analysis_out_schemas)"

You can find the meanings of the data keys in the output.

I miss the good old days
^^^^^^^^^^^^^^^^^^^^^^^^

The xpd server also offers users the option to go back to the good old days of xpdAn.
By using ``export_files_in_xpdan_style = True`` in the configuraion file, the xpd server will output the files
in the same type of what xpdan uses and in the directory structure.

Below is an example of the output using the xpdAn file type and directory structure.

.. code-block:: text

    tiff_base
    └── Ni
        ├── dark_sub
        │   ├── 10fd020b-6704-4ba9-a016-d422484904f5_Ni_primary-bg_sub_image-0.tiff
        │   ├── 10fd020b-6704-4ba9-a016-d422484904f5_Ni_primary-dk_sub_image-0.tiff
        │   └── 10fd020b-6704-4ba9-a016-d422484904f5_Ni_primary-mask-0.tiff
        ├── fq
        │   └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-fq_Q-fq_F-1.txt
        ├── integration
        │   └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-chi_Q-chi_I-1.txt
        ├── iq
        │   └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-iq_Q-iq_I-1.txt
        ├── mask
        │   └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-mask-1.npy
        ├── meta
        │   └── 10fd020b-6704-4ba9-a016-d422484904f5_Ni_meta.json
        ├── pdf
        │   └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-gr_r-gr_G-1.txt
        ├── scalar_data
        │   └── 10fd020b-6704-4ba9-a016-d422484904f5_Ni_primary.csv
        └── sq
            └── d80fdb8d-0186-40f4-9aa4-9705a7cb915e_Ni_primary-sq_Q-sq_S-1.txt

.. _xpd-server-figures:

How to see the data during the experiment?
------------------------------------------

The data will be visualized in windows. The windows will pop up when you start the server and the plot will
automatically show up when you are running the experiments using xpdacq.

The images will be plotted in a two dimensional colorful histogram, you can move the cursor onto one point and
the pixel values in horizontal and vertical line across the point will be shown in the panels around the image.
Below is an example of the masked dark subtracted diffraction image.

.. figure:: ../_static/masked_image.png

The reduced data like XRD and PDF will be plotted in a waterfall plot, you can change the x-offset and y-offset
to move the curves in two dimensions. Below is an example of the waterfall plot of PDF.

.. figure:: ../_static/gr.png

The scalar data like the maximum points will be plotted in a line plot. The x-axis will be the independent
variable in the measurement. In the example below, the coordinates of maximum point in XRD and PDF are plotted
as a function of temperature.

.. figure:: ../_static/max.png


How to user configuration during the experiment?
------------------------------------------------

Users can give some of their own data to the server and let it use the data to do the analysis.

How to use user defined calibration?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can save their own calibration data in the poni file and replace the poni file specified in the
configuration file of the server with it. Thus, the server will use the calibration data from the user.

For example, if the setting in the configuration is
``calib_base = /nsls2/xf28id1/xpdacq_data/user_data/config_base`` and ``poni_file = xpdAcq_calib_info.poni``,
what users need to do is to copy and paste their poni file to replace the ``xpdAcq_calib_info.poni`` in the
directory ``/nsls2/xf28id1/xpdacq_data/user_data/config_base``.

How to use a user defined mask?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If users would like to apply their own mask before the auto masking, they can give a key word argument
``user_config`` in the xrun to specify the mask file that they would like to use.
The maks file can be a tiff file, a npy file or a numpy text file.
Below is an example of the code.

.. code-block:: python

    xrun(0, 0, user_config={"mask_file": "./my_mask.tiff"})

If users would like to use their mask file as it is without any further auto masking, they can add a statement
like the example below.

.. code-block:: python

    xrun(0, 0, user_config={"auto_mask": False, "mask_file": "./my_mask.tiff"})

If users don't want any masking, they can disable the auto masking with applying the mask as the following.

.. code-block:: python

    xrun(0, 0, user_config={"auto_mask": False})

