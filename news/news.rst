**Added:**

* Add new callbacks in the `callback` package for the analysis, serialization and visualization for the new data structure from the new xpdacq.

* Add `FileNameRender` to compose file name according to the user's request and put filename in starts and events.

* Add `Analayzer` to process the data to XRD and PDF and save the processed data in the pyFAI standard and pdfgetx standard file and do calbration if necessary.

* Add `DarkSubtraction` to do the dark subtraction of the image in place.

* Add `AnalysisPipeline` that contains the `Analyzer`, `DarkSubtraction` and `Publisher`.

* Add `PlotterBase` as the basic class of the plotters.

* Add `ImagePlotter` to plot the image with or without masks and save image in files.

* Add `WaterfallPlotter` to plot the 1d array in a waterfall plot and save the figure in a file at the end.

* Add `ScalarPlotter` to plot the scalar array as a function of time or other dimensions and save the figure in a file at the end.

* Add `VisualizationPipeline` that contains the `ImagePlotter`, `WaterfallPlotter` and `ScalarPlotter`.

* Add `SerializerBase` as the basic class of the serializers.

* Add `TiffSerializer` to serialize the images in tiff files.

* Add `CSVSerializer` to serialize the scalar data, time stamp and the filename of outputs in csv files.

* Add `YamlSerializer` to serialize the start document in a yaml file using the `safe_dump`.

* Add `NumpySerializer` to serialize the masks in npy files.

* Add `SerializationPipeline` that contians `TiffSerializer`, `CSVSerializer`, `YamlSerializer` and `NumpySerializer`.

**Changed:**

* Make the `callbacks` package contain all the callback classes, including the servers.

* Make the servers able to process the event data from more than one detectors and mutliple different calibrations in one run.

* Make `run_server` command start the analysis, serialization and visualization servers separately in three children processes at the same time.

* Use logging package to stream logs from three processes to `sys.stdout`.

* Change the sections and some keys in the configuration so that users can adjust the `ANALYSIS` section in the configuration using `user_config` key in the start doc.

* Cache the calibration data for the integration and the binners for the masking using `lru_cache`. The cache is valid through the whole session unless it is updated.

* Change the filename pattern of the output files to avoid duplicated file names from different detector images.

* Make the time in the output event streams and the time stamps in the file names the sames as the time in the input event streams. The time that users see will be the same as the time that the data is measured instead of the time that the analysis code runs.

* Allow users to include any measured scalar data in the filename using the `user_config` keyword.

* Allow users to tune whether or not to save the figures, save any kind of data, visualize any kind of data, do the pdfgetx processing or do auto masking.

* Allower users to tune any configuration for auto masking, pyFAI integration and the pdfgetx.

**Deprecated:**

* Deprecate the old callbacks and servers for the old data structure from the old xpdacq.

* Deprecate the dependencies of the suitcase packages.

**Removed:**

* Remove `servers` package and `analyzer` package.

**Fixed:**

* Fix the wrong assignment of the `chi_max` and `chi_argmax`.

**Security:**

* <news item>
