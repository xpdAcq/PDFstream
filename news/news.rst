**Added:**

* Add AreaDetectorTiffHandler for the xpd and lsq servers.

**Changed:**

* The image data can be any array with dimensions N as long as N >= 2. The first N - 2 dimensions will be averaged.

* Simplify the configuration for the servers.

**Deprecated:**

* Deprecate the background subtraction functionality because of the stability.

**Removed:**

* <news item>

**Fixed:**

* Use v1 databroker interface for the query of dark images info due to the broken xarray conversion in v2 databroker.

* Fix the bug that server cannot deal with the data for which the background measurement failed.

**Security:**

* <news item>
