Data Processing Server
======================

The data processing server received the data stream of raw x-ray scattering data from the proxy server, conduction data reduction on the data, send out the XRD and PDF data back to the proxy server.

Proxy Settings
--------------

The inbound and outbound address of the proxy and the data prefix of the input and output data are set in the section below in the configuration file.

.. code-block: text

    [PROXY]
    inbound_address = xf28id1-ca1:5577
    outbound_address = xf28id1-ca1:5578
    raw_data_prefix = raw
    analyzed_data_prefix = an

This follows the convention from XpdAn, the previous software for the servers at the beamline.

Two Modes
---------

The data reduction has two modes: (1) calibration mode (2) collection mode. The two modes have mostly the same but differs in whether to start a interactive calibration session. Which mode to run is determined the key word `pyfai_calib_kwargs` in the start document. If there is the key word, it is calibration model, other wise it is collection mode.

I will introduce the collection mode as an example. The calibration mode only adds an interactive pyFAI-calib2 session but doesn't change other operations. In the collection mode, the server conducts several tasks depending on what document it receives and what event stream it is if it receives a event document. These task are described below.

Document Mutation
-----------------

The server only mutates the documents instead creating new ones. Thus, the uid is the same as the input document. Here, I will introduce how it mutates the documents.

Start
^^^^^

The server will read some keys in the start document and add two new keys in it. Below are the keys that the server will read and how they will be used.

* sample_name (required): make the name of the directory and a part of the file names.
* uid (required): make a part of the file names.
* time (required): make a part of the file names.
* composition_str (required): use it to normalize the I(Q) to get the PDF.
* pyfai_calib_kwargs (optional): start a pyFAI-calib2 session if this key appears.
* user_config (optional): use the user configuration to tune the settings.

Below are the keys that will be added by the server into start document.

* directory: used to make the directory.
* filename: used as a template to create the file names.

The data processing server will save the original start document instead of the mutated ones in `yaml` files.

Descriptor
^^^^^^^^^^

The server doesn't use any information from the descriptor. It only adds the keys of processed data in the descriptor. These keys all starts with the name of the detector because they are all associated with a detector image. If there are more than one detector there will be more than one set of keys. Here, I will use detector `pe1` as an example name.

* pe1_mask: the 2D mask binary array, 0 means good pixel and 1 means bad pixels.
* pe1_chi_2theta: the two theta grid for XRD data.
* pe1_chi_Q: the momentum transfer grid for XRD data.
* pe1_chi_I: the XRD intensity data.
* pe1_iq_Q: the momentum transfer grid for I(Q) data of diffpy.pdfgetx.
* pe1_iq_I: the intensity data for I(Q) data of diffpy.pdfgetx.
* pe1_sq_Q: the momentum transfer grid for S(Q) data of diffpy.pdfgetx.
* pe1_sq_I: the intensity data for S(Q) data of diffpy.pdfgetx.
* pe1_fq_Q: the momentum transfer grid for F(Q) data of diffpy.pdfgetx.
* pe1_fq_I: the intensity data for F(Q) data of diffpy.pdfgetx.
* pe1_gr_Q: the momentum transfer grid for PDF data of diffpy.pdfgetx.
* pe1_gr_I: the intensity data for PDF data of diffpy.pdfgetx.
* pe1_chi_argmax: the Q value at the highest peak in PDF.
* pe1_chi_max: the I value at the highest peak in PDF.s
* pe1_gr_argmax: the r value at the highest peak in PDF.
* pe1_gr_max: the G value at the highest peak in PDF.

Event
^^^^^

The server fills in all the external references with the real data. It then finds the image data in the event document and then map it to a scikitbeam binner, pyFAI integrator. It uses the scikitbeam binner to bin the intensity and throw out the invalid pixels and then gives the data to the pyFAI integrator to integrate the image along the arcs to get the XRD. Then, it uses the PDFGetter to transfer the XRD to PDF.

The server will add these processed data with the keys stated in the previous section. The data is added either a scalar or a numpy array. These keys have been shown in the previous section so I won't show it again here. In these data, all of the light weight data is saved to disk during the processing. These data includes the XRD data, PDF data, calibration data, and intermediate data S(Q), F(Q).

In the process below, the scikitbeam binner may be a little necessary. Currently, I am working on substitute it with thy pyFAI integrator to accelerate the auto masking.

Stop
^^^^

The server will not mutate the stop document.