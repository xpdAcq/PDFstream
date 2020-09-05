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
