====================
PDFstream Change Log
====================

.. current developments

v0.4.3
====================

**Added:**

* Add the functionality to export files in xpdan style file structure for the xpd server

* More messages from the server including what is running and the errors from pyFAI calibration

**Changed:**

* Average cli check if the directory exits, make it if not.

* AnalysisStream injects the pdfstream version into the start document.

**Fixed:**

* Fix the bug that the plot setting doesn't work in cli.

* Fix the bug about calibration in xpd server.



v0.4.2
====================

**Fixed:**

* Fix the bug that the background subtraction and dark substrate do not work in the integration



v0.4.1
====================

**Added:**

* The XPD server will publish the data to a proxy

**Changed:**

* The section name of the configuration of XPD server is changed.



v0.4.0
====================

**Added:**

* The base objects to process data from bluesky runs.

* The objects to process the XRD data to PDF data from bluesky runs.

* The functions to replay the analysis.



v0.3.2
====================

**Added:**

* Make callback safe for the Exporter and Visualizer in the XPDRouter.

* Add a DataFrameExporter to export data in dataframe

* Make calibration callback identify special calibrant name 'Ni_calib'

**Changed:**

* Export 1d array in dataframe data instead of the numpy array

* Optimize the layout of figures for visualization callbacks

**Fixed:**

* Fix the bugs of xpd server when it is used with xpdacq.



v0.3.1
====================

**Fixed:**

* Fix the bug that pdfstream has import error if the diffpy.pdfgetx is not in environment



v0.3.0
====================

**Added:**

* `databroker`, `bluesky` are added in the dependencies

* A server to process the streaming x-ray diffraction data to PDF

* A server to decompose processed PDF to a linear combination of other PDFs

* The functions to query the necessary data from the databroker

**Changed:**

* Starting from 0.3.0, the package will be released on `nsls2forge` channel on conda.


v0.2.2
====================

**Changed:**

* Starting from 0.2.2, the package will be released on `diffpy` channel on conda.



v0.2.1
====================



v0.2.0
====================

**Added:**

* `integrate` allows user to supply their own mask

* Add `transform` cli, a simple interface to transform the .chi file to PDF.

* Tutorials for users to use the tools in `pdfstream`.

* `integrate` and `transform` will create the output folder if it does not exists.

**Changed:**

* `load_data` is vended from diffpy. `load_array` accepts `min_rows` and key word arguments.

* `write_out` is renamed to `write_pdfgetter`.

* All the code using `diffpy.pdfgetx` is in the transformation subpackage. Users can choose whether to install the diffpy.pdfgetx.

**Removed:**

* IMPORTANT: modeling, parsers, calibration sub-packages are removed.

* IMPORTANT: remove the dependency on xpdtools



v0.1.3
====================

**Added:**

* Set values and bounds for the variables in the recipe.

**Fixed:**

* Fix the bug that mask is not applied to image in the integration.



v0.1.2
====================

**Added:**

* Add the ``parsers`` that parses the information in FitRecipe to mongo-friendly dictionary.

* Add options in ``multi_phase`` that users can set what parameters they would like to refine.

* Add the function ``create`` to create a recipe based on the data and model.

* Add the function ``initialize`` to populate recipe with variables. Users can choose differnet modes of constraints.

* Add examples for the modeling.

**Changed:**

* CLI ``visualize`` takes list argument ``legends`` instead of string ``legend``. Users can use legends for multiple curves.

**Removed:**

* Remove the codes not frequently used.

**Fixed:**

* Fix bugs in the modeling.



v0.1.1
====================



v0.1.0
====================

**Added:**

* Azimuthal integration of diffraction image with auto masking and background subtraction.

* Calculate the average of multiple diffraction image frames.

* Visualization of pair distribution function (PDF) or other 1D data.

* Visualization of the modeling results of 1D PDF data.

* Easy-to-use tools to create *DiffPy-CMI* recipe to model PDF and run optimization.

* Simple csv-file-based database to save the modeling results.

* A command line interface (CLI) for all the functionality.
