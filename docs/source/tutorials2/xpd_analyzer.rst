XPD Analyzer
============

This analyzer processes the x-ray powder diffraction images and yields pair distribution function data.
It is basically a wrapper of the core of the XPD server and thus its functionality is the same as the XPD server.
The only difference is that the XPD server receives data from the messages sent by a proxy
while the analyzer takes data from a database entry.
If you would like to know what the analyzer does and what input and output look like,
please see :ref:`xpd_server`.

The sections below show how to use the XPD analyzer in Ipython.


Get data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^

The input data of the analyzer can be a ``BlueskyRun``.
It can be retrieved by from a databroker ``catalog``.
Below is an example showing the process of retrieving one run from a catalog according to its unique ID.
For details, please visit `databroker user documents <https://blueskyproject.io/databroker/v2/user/index.html>`_.

.. ipython::

    In [1]: from databroker import catalog

    In [2]: db = catalog['example']

    In [5]: run = db['a3e64b70-c5b9-4437-80ea-ea6a7198d397']

Here, We show the metadata of this run.

.. ipython::

    In [6]: run.metadata['start']

Create the analysis database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here, we create a temporary database and use it to store the processed data from the analyzer.
You can use the database catalog on your machine instead of creating a temporary one.
How to create a database catalog is written in the
`databroker administrator documents <https://blueskyproject.io/databroker/v2/administrator/index.html>`_.

.. ipython::

    In [18]: import databroker

    In [19]: an_db = databroker.v2.temp()

Create an analyzer
^^^^^^^^^^^^^^^^^^

To create an ``XPDAnalyzer``, you need to create a ``XPDAnalyzerConfig`` first.
The ``XPDAnalyzerConfig`` is a object that holds the configuration of the analyzer.
Here, we create an empty ``XPDAnalyzerConfig``.

.. ipython::

    In [7]: from pdfstream.analyzers.xpd_analyzer import XPDAnalyzerConfig, XPDAnalyzer

    In [8]: config = XPDAnalyzerConfig(allow_no_value=True)

The ``allow_no_value`` is an optional argument.
Please see the document of `configparser <https://docs.python.org/3/library/configparser.html>`_ for details of
the arguments.
It is the parent class of the ``XPDAnalyzerConfig``.

Then, we will load the configuration parameters into the ``config``.
We can use a .ini file, a python string or a python dictionary.

.. ipython::

    In [11]: config.read("./source/_static/xpd_analyzer.ini")

Here, we use a .ini file as an example.
The content of the file is shown below and the meaning of the parameters is described in the comments.
Please read through it and change it according to your needs.

.. include:: ../_static/xpd_analyzer.ini
   :literal:

Now, we have a ``config`` loaded with parameters.
We use it to create an analyzer.

Because we use the temporary database in the example here, we have to manually add it to ``config``.
You don't need to do the step below if you are not using the temporary database.

.. ipython::

    In [20]: config.an_db = an_db

Finally, we use this ``config`` to create an ``analyzer``.

.. ipython::

    In [21]: analyzer = XPDAnalyzer(config)

Change settings
^^^^^^^^^^^^^^^

We can change all the settings for the analyzer except the visualization settings
before or after the analyzer is created.
For example, we think that the ``qmax`` in section ``TRANSFORMATION SETTING``
is slightly larger than the ideal and thus we decrease it to 20 inverse angstrom.

.. ipython::

    In [22]: config.set("TRANSFORMATION SETTING", "qmax", '20')

We can also use another way.

.. ipython::

    In [24]: config["TRANSFORMATION SETTING"]["qmax"] = '20'

In both ways, we need to use string values even if the ``qmax`` is actually a number.

After we run either line of the code above, the analyzer will use ``qmax = 20`` in the data processing.

Process the data
^^^^^^^^^^^^^^^^

We use the analyzer to process the data.

.. ipython::

    @savefig
    In [29]: analyzer.analyze(run)

Export the processed data to files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Instead of saving the metadata and data in the database, we can also export them in files.
By setting ``export_files = True`` and specify ``tiff_base`` parameter in the configuration,
we will export the processed data into the ``tiff_base``.
The detail of what the data will be like is introduced in :ref:`xpd_server`.

Get processed data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data is dumped into databroker ``an_db`` by the analyzer.
We retrieve the last run in the database and it should be the processed data from our analyzer.

.. ipython::

    In [30]: an_run = an_db[-1]

    In [31]: an_run.metadata['start']

This is the processed data.
We notice that the metadata is the same as the input raw data except one additional key ``an_config``.
This is the dictionary of configuration used in the data processing.

Here, we show the processed data in an xarray.

.. ipython::

    In [32]: an_run.primary.read()

You can play with it in the way you like.

Create a configuration from the processed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can load configuration from a run.

.. ipython::

    In [33]: config2 = XPDAnalyzerConfig()

    In [34]: config2.read_run(an_run)

Because the we used the temporary database,
the ``an_run`` does record the information of ``an_db``
and thus the ``config2`` does not know what database to use for ``an_db``.
We need to specify it manually.

.. ipython::

    In [34]: config2.an_db = an_db

You don't need this step if you were using a permanent database when you processed the data.

We create an analyzer.
This analyzer is exactly the same as the one used to obtain the data in ``an_run``.

.. ipython::

    In [21]: analyzer2 = XPDAnalyzer(config2)

You can use it to process other data so that the data will be processed in the same way as the ``an_run``.
