====================
pdfstream Change Log
====================

.. current developments

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
