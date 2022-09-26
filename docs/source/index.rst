PDFstream Documentation
=======================

Welcome to the Documentation of PDFstream. PDFstream is a software used at the 28-ID beamline to conduct automatic data processing for the streaming x-ray scattering data. It help users do the data processing and analysis so that users can directly take publishable XRD and PDF data home without clicking a mouse. It also provides the CLI interface to do the same data processing and analysis for users when they take the data home and would like to do fine tuning of the parameters.

I designed the software based on the `bluesky event model <https://blueskyproject.io/event-model/>`_. It is a architecture for streaming data. Simply speaking, the data stream is a stream of the `(name, document)` pair with a schemas for the document in this architecture. The PDFstream provides the data pipelines that this stream will flow in and flow out. At each processing step, the document is read, processed, and updated. I equipped the data pipelines on 0MQ servers so that the data stream will flow in from the network and flow out to the network.

A typical example of the PDFstream data pipeline is the data analysis pipeline. A data stream containing the x-ray diffraction images flow into the pipeline, and a data stream of XRD and PDF data flows out of the pipeline.

Although I designed the software especially for the 28-ID beamline for their automatic PDF measurement, it can also be used in other beamlines or at labs as long as the input data stream following the very flexible schemas.


.. toctree::
   :maxdepth: 2

   installation
   tutorials0/index
   tutorials1/index
   changelog
   min_versions
