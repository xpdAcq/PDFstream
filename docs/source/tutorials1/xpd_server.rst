XPD Server
==========

The XPD Server is a server designed for x-ray powder diffraction experiments. It will process image data from
a two dimensional detector.

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

You can download the file here. The parameters you can change are the values that behind the equity symbol in each
row.


Start the server
^^^^^^^^^^^^^^^^

Assume that you have written a configuration file and the path to it is "~/xpd_server.ini".

In terminal, run the command::

    run_server xpd ~/xpd_server.ini

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

    run_server xpd

The server will start.

(Optional) Run the server in a detached background process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Similar to what you have done with the proxy, you can also run the server in background and detach it from the
terminal so that you don't need to start the server every time. To do this, in terminal, run command::

    nohup run_server xpd ~/xpd_server.ini &

If you have put the "xpd_server.ini" in default folder, run this instead::

    nohup run_server xpd &

You will find the message from the server in file "nohup.out".

If you would like to terminate the background process, in terminal, run command::

    kill <job ID>

The ``<job ID>`` is a number that shows up after you run the command ``nohup run_server xpd &``.

How to do the calibration?
--------------------------

When you run the command below in ``bsui`` of xpdacq, you will the xpd server responds and gives you a window of
diffraction image.

.. ipython::

   In [1]: run_calibration()

You will finish the calibration in this window. Please see the `tutorials <http://www.python.org/>`_ to learn
how to use it. When you are at the last step of the tutorials and you are going to save the geometry in a PONI
file, please save the file at exact where it is first shown in the finder window after you click the button.
Please do not change the folder and file name of the PONI file.
