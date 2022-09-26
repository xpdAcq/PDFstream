Configuration of Servers
========================

This package uses a two level configuration systems. The ground layer is the default configuration and upon it, there are multiple user configuration.

Default Configuration
---------------------

The first level is the default settings for a server. This is static through the life time of the service process and applied to every data stream it receives.

This is determined by a configuration file. The three servers all use the same configuration as their default configuration settings. Below is an example file.

.. literalinclude:: _static/pdf_beamline.ini
   :text:

This is usually set up by the beamline scientist or the developer.

Below is an introduction about `MEATDATA` section. It is a section defining the important key names in the start document. These are all default settings and usually not need to be changed.

* composition_str: the key to get a string of sample composition, used in PDFGetter.
* sample_name: the key of a string of sample name, used in naming.
* user_config: the key of user configuration in the start document, used to update the document.
* pyfai_calib_kwargs: the key to start the pyFAI-calib2, used to identify whether to start a pyFAI calibration session.

Now, we come to the most important part `ANALYSIS`. These will determine most of the behavior of data processing and serialization.

* detectors: the names of the detectors, used to create the data key names for processed data.
* image_fields: the names of the detector image data, used to find out the image data in the data keys.
* image_dtype: the data type of the image to be saved, all images will be converted to this type.
* fill: whether or not to use a filler to fill in the external data.
* auto_mask: whether or not to do the auto masking.
* alpha: the number of standard deviation to be considered as valid.
* edge: the number of pixels to be masked at the edges.
* lower_thresh: the lower limit for the valid pixels, used to mask the deal pixels.
* upper_thresh (optional): the upper limit for the valid pixels, used to mask the hot pixels.
* npt: number of the data points in the output XRD data.
* correctsolidangle: whether or not to correct solid angle in the pyFAI.
* polarization_factor: polarization correction factor in the pyFAI.
* method: method for the integration in the pyFAI, must be three comma separated value or just one value.
* normalization_factor: the normalization factor used in pyFAI.
* pdfgetx: whether or not to run diffpy.pdfgetx to get PDF data, if False, only XRD will be output.
* rpoly: polynomial correction order in the pdfgetx.
* qmaxinst: maximum Q to do the polynomial correction in the pdfgetx.
* qmax: maximum Q to do the Fourier transformation in the pdfgetx.
* qmin: minimum Q to do the Fourier transformation in the pdfgetx.
* rmin: minimum in r axis to calculate the PDF.
* rmax: maximum in r axis to calculate the PDF.
* rstep: interval of axis to calculate the PDF.
* composition: the default composition if it is not provided by the start document.
* exports: what data to save.
* tiff_base: the root directory to save data.
* directory: a python format string of directory name template 
* file_prefix: a python format string of file name prefix template.
* hints (optional): additional signal names to be added in the file name.
* save_plots: whether to save the plots or not.
* is_test: whether to run the server in a test mode, used by developer to debug.

The `Visualizer` is the the settings of visualization. This currently only contains one key to specify what to visualize.

The proxy settings have been introduced in the chapter before.

User Configuration
------------------

User configuration, or in other word, experiment specific configuration is read from the start document of an even stream. It is recorded in the key `user_config`. Users can add the `user_config` in the metadata when they run the `xrun` or `RE` in the IPython session.

The user_config is a dictionary of key value pairs. These keys are the same as the ones in the `ANALYSIS` section in the configuration file. Their values are used to update the values in the default settings. This update is only applied for one specific bluesky run and won't affect the following runs.

In this way, users can tune all the parameters in the data processing and serialization. Currently, we don't allow users to tune the visualization settings.

Here, we introduce some use cases to customize the data processing.

Example Use Cases
-----------------

For example, I would like to use a new location to save the data from one experiment. This new location is "./new_tiff_base". Then, I will give the user configuration.

.. code-block: python

   xrun(0, 0, user_config={"tiff_base": "./new_tiff_base"})


It will change the configuration of `tiff_base` to `"./new_tiff_base"` for this run. Note that this is only one time change. If I don't give this option in the next run, the data will be saved in the default location.

Another example is that I would like to add a specific data in the filename, like "temperature_setpoint". I will add it as a string.

.. code-block: python

   xrun(0, 0, user_config={"hints": "temperature_setpoint"})


Note that there must be the same name as the signal name in your temperature controller ophyd device. If I have more than one key, for example, "temperature_setpoint" and "heat_rate", I will use comma-separate values.

.. code-block: python

   xrun(0, 0, user_config={"hints": "temperature_setpoint,heat_rate"})


Note that all values of the configuration must be a string, just like what I wrote in the configuration file.
