====================
PDFstream Change Log
====================

.. current developments

v0.3.0
====================

**Added:**

* `databroker`, `bluesky`, `shed` are added in the dependencies

* A pipeline to process the streaming x-ray diffraction data

* The functions to query the necessary data from the databroker

* The wrappers of the data processing functions that can be used in pipeline.



v0.2.2
====================

**Changed:**

* Starting from 0.2.2, the package willl be released in `diffpy` channel on conda.



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
