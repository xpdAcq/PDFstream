"""XPD Analyzer
============

This analyzer processes the x-ray powder diffraction images and yields pair distribution function data.
It is basically a wrapper of the core of the XPD server and thus its functionality is the same as the XPD server.
The only difference is that the XPD server receives data from the messages sent by a proxy
while the analyzer takes data from a database entry.
If you would like to know what the analyzer does and what input and output look like,
please see :ref:`xpd-server-functionalities`.

The sections below show how to use the XPD analyzer in Ipython.
"""

# %%
# Create an analyzer
# ^^^^^^^^^^^^^^^^^^
#
# To create an ``XPDAnalyzer``, you need to create a ``XPDAnalyzerConfig`` first.
# The ``XPDAnalyzerConfig`` is an object that holds the configuration of the analyzer.

from pdfstream.analyzers.xpd_analyzer import XPDAnalyzerConfig, XPDAnalyzer

config = XPDAnalyzerConfig(allow_no_value=True)

# %%
# The ``allow_no_value`` is an optional argument.
# Please see the document of `configparser <https://docs.python.org/3/library/configparser.html>`_ for details of
# the arguments.
# It is the parent class of the ``XPDAnalyzerConfig``.
#
# Then, we will load the configuration parameters into the ``config``.
# We can use a .ini file, a python string or a python dictionary.

config.read("../source/_static/xpd_analyzer.ini")

# %%
# Here, we use a .ini file as an example.
# The content of the file is shown below and the meaning of the parameters is described in the comments.
# Please read through it and change it according to your needs.
#
# .. include:: ../_static/xpd_analyzer.ini
#    :literal:
#
# Now, we have a ``config`` loaded with parameters.
# We use it to create an analyzer.

analyzer = XPDAnalyzer(config)

# %%
# Get data from databroker
# ^^^^^^^^^^^^^^^^^^^^^^^^
#
# The input data of the analyzer is a ``BlueskyRun``, the data entry retrieved by from a databroker catalog.
# Below is an example showing the process of retrieving one run from a catalog according to its unique ID.

db = config.raw_db
run = db['9d320500-b3c8-47a2-8554-ca63fa092c17']

# %%
# Here, ``db`` is a databroker catalog loaded according to your configuration.
# Please visit `databroker user documents <https://blueskyproject.io/databroker/v2/user/index.html>`_ for details
# about what you can do with the ``db`` and ``run``.
# The data inside this run is show below.

raw_data = run.primary.read()
raw_data

# %%
# The data is processed by the analyzer is the diffraction image.

import matplotlib.pyplot as plt

image = raw_data["pe1_image"]
image.plot(vmin=0, vmax=image.mean() + 2. * image.std())
plt.show()

# %%
# In both ways, we need to use string values even if the ``qmax`` is actually a number.
#
# After we run either line of the code above, the analyzer will use ``qmax = 20`` in the data processing.
#
# Process the data
# ^^^^^^^^^^^^^^^^
#
# We use the analyzer to process the data.

analyzer.analyze(run)

# %%
# Get processed data from databroker
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# The data is dumped into databroker ``an_db`` by the analyzer.
# We retrieve the last run in the database and it should be the processed data from our analyzer.

an_db = config.an_db
an_run = an_db[-1]

# %%
# Here, we show the processed data in an xarray.

an_data = an_run.primary.read()
an_data

# %%
# We plot the some of the important data to give a sense of what the processed data looks like.
# First, we plot the masked dark subtracted image.

import numpy as np

image2 = np.ma.masked_array(an_data["dk_sub_image"], an_data["mask"])
image2 = np.ma.squeeze(image2)
plt.matshow(image2, vmin=0., vmax=image2.mean() + 2. * image2.std())
plt.colorbar()
plt.show()

# %%
# Second, we show the XRD data obtained from the dark subtracted image above.

chi = np.stack((an_data["chi_Q"], an_data["chi_I"])).squeeze()
plt.plot(*chi)
plt.show()

# %%
# Finally, it is the PDF data transferred from XRD data.

gr = np.stack((an_data["gr_r"], an_data["gr_G"])).squeeze()
plt.plot(*gr)
plt.show()

# %%
# Change settings
# ^^^^^^^^^^^^^^^
#
# We can change all the settings for the analyzer except the visualization settings
# before or after the analyzer is created.
# For example, we think that the ``qmax`` in section ``TRANSFORMATION SETTING``
# is slightly larger than the ideal and thus we decrease it to 20 inverse angstrom.

config.set("TRANSFORMATION SETTING", "qmax", '20')

# %%
# We can also use another way.

config["TRANSFORMATION SETTING"]["qmax"] = '20'

# %%
# Then, we just need to run ``analyzer.analyze(run)``.
# You don't need to create another analyzer if you tune the configuration other than "BASIC" and "FUNCTIONALITY".

# %%
# Export the processed data to files
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Besides saving the metadata and data in the database, we can also export them in files at the same time.
# For example, we run the code blow to let the analyzer export the processed data into the ``~/my_folder``.

config["FUNCTIONALITY"]["export_files"] = "True"
config["FILE SYSTEM"]["tiff_base"] = "~/my_folder"

# %%
# Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
# take effect and rerun the analysis ``analyzer.analyze(run)``.
# The detail of what the data will be like is introduced in :ref:`xpd-server-data`.

# %%
# Live visualization
# ^^^^^^^^^^^^^^^^^^
#
# If you would like see the figures of processed data at the same time of data processing
# , run the code below to turn on the functionality.

config["FUNCTIONALITY"]["visualize_data"] = "True"

# %%
# Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
# take effect and rerun the analysis ``analyzer.analyze(run)``.
# The detail of what the figures will be like is introduced in :ref:`xpd-server-figures`.

# %%
# Replay the data processing
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# We can replay the analysis process according to the metadata and data in the analysis run.

from pdfstream.analyzers.xpd_analyzer import replay

config2, analyzer2 = replay(an_run)

# %%
# The ``confgi2`` and ``analyzer2`` have the same settings as the ``config`` and ``analyzer``
# except the databases.
# It is because we uses two special temporary databases for the demonstration.
# You will not encounter the problem if you are using permanent database in catalog.
