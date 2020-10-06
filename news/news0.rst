**Added:**

* `integrate` allows user to supply their own mask

* Add `transform` cli, a simple interface to transform the .chi file to PDF.

**Changed:**

* `load_data` is vended from diffpy. `load_array` accepts `min_rows` and key word arguments.

* `write_out` is renamed to `write_pdfgetter`.

* All the code using `diffpy.pdfgetx` is in the transformation subpackage. Users can choose whether to install the diffpy.pdfgetx.

**Deprecated:**

* <news item>

**Removed:**

* IMPORTANT: modeling, parsers, calibration sub-packages are removed.

* IMPORTANT: remove the dependency on xpdtools

**Fixed:**

* <news item>

**Security:**

* <news item>
