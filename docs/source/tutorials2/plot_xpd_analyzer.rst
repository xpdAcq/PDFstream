.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_tutorials2_plot_xpd_analyzer.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_tutorials2_plot_xpd_analyzer.py:

XPD Analyzer
============

This analyzer processes the x-ray powder diffraction images and yields pair distribution function data.
It is basically a wrapper of the core of the XPD server and thus its functionality is the same as the XPD server.
The only difference is that the XPD server receives data from the messages sent by a proxy
while the analyzer takes data from a database entry.
If you would like to know what the analyzer does and what input and output look like,
please see :ref:`xpd-server-functionalities`.

The sections below show how to use the XPD analyzer in Ipython.

Create an analyzer
^^^^^^^^^^^^^^^^^^

To create an ``XPDAnalyzer``, you need to create a ``XPDAnalyzerConfig`` first.
The ``XPDAnalyzerConfig`` is an object that holds the configuration of the analyzer.


.. code-block:: default


    from pdfstream.analyzers.xpd_analyzer import XPDAnalyzerConfig, XPDAnalyzer
    config = XPDAnalyzerConfig(allow_no_value=True)








The ``allow_no_value`` is an optional argument.
Please see the document of `configparser <https://docs.python.org/3/library/configparser.html>`_ for details of
the arguments.
It is the parent class of the ``XPDAnalyzerConfig``.

Then, we will load the configuration parameters into the ``config``.
We can use a .ini file, a python string or a python dictionary.


.. code-block:: default


    config.read("../source/_static/xpd_analyzer.ini")





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    ['../source/_static/xpd_analyzer.ini']



Here, we use a .ini file as an example.
The content of the file is shown below and the meaning of the parameters is described in the comments.
Please read through it and change it according to your needs.

.. include:: ../_static/xpd_analyzer.ini
   :literal:

Now, we have a ``config`` loaded with parameters.
We use it to create an analyzer.


.. code-block:: default


    analyzer = XPDAnalyzer(config)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Warning: a temporary db is created for an db. It will be destroy at the end of the session.




Get data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^

The input data of the analyzer is a ``BlueskyRun``, the data entry retrieved by from a databroker catalog.
Below is an example showing the process of retrieving one run from a catalog according to its unique ID.


.. code-block:: default


    db = config.raw_db
    run = db['a3e64b70-c5b9-4437-80ea-ea6a7198d397']








Here, ``db`` is a databroker catalog loaded according to your configuration.
Please visit `databroker user documents <https://blueskyproject.io/databroker/v2/user/index.html>`_ for details
about what you can do with the ``db`` and ``run``.
The data inside this run is show below.


.. code-block:: default


    raw_data = run.primary.read()
    raw_data






.. raw:: html

    <div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
    <defs>
    <symbol id="icon-database" viewBox="0 0 32 32">
    <path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
    <path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    <path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    </symbol>
    <symbol id="icon-file-text2" viewBox="0 0 32 32">
    <path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
    <path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    </symbol>
    </defs>
    </svg>
    <style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
     *
     */

    :root {
      --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
      --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
      --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
      --xr-border-color: var(--jp-border-color2, #e0e0e0);
      --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
      --xr-background-color: var(--jp-layout-color0, white);
      --xr-background-color-row-even: var(--jp-layout-color1, white);
      --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
    }

    html[theme=dark],
    body.vscode-dark {
      --xr-font-color0: rgba(255, 255, 255, 1);
      --xr-font-color2: rgba(255, 255, 255, 0.54);
      --xr-font-color3: rgba(255, 255, 255, 0.38);
      --xr-border-color: #1F1F1F;
      --xr-disabled-color: #515151;
      --xr-background-color: #111111;
      --xr-background-color-row-even: #111111;
      --xr-background-color-row-odd: #313131;
    }

    .xr-wrap {
      display: block;
      min-width: 300px;
      max-width: 700px;
    }

    .xr-text-repr-fallback {
      /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
      display: none;
    }

    .xr-header {
      padding-top: 6px;
      padding-bottom: 6px;
      margin-bottom: 4px;
      border-bottom: solid 1px var(--xr-border-color);
    }

    .xr-header > div,
    .xr-header > ul {
      display: inline;
      margin-top: 0;
      margin-bottom: 0;
    }

    .xr-obj-type,
    .xr-array-name {
      margin-left: 2px;
      margin-right: 10px;
    }

    .xr-obj-type {
      color: var(--xr-font-color2);
    }

    .xr-sections {
      padding-left: 0 !important;
      display: grid;
      grid-template-columns: 150px auto auto 1fr 20px 20px;
    }

    .xr-section-item {
      display: contents;
    }

    .xr-section-item input {
      display: none;
    }

    .xr-section-item input + label {
      color: var(--xr-disabled-color);
    }

    .xr-section-item input:enabled + label {
      cursor: pointer;
      color: var(--xr-font-color2);
    }

    .xr-section-item input:enabled + label:hover {
      color: var(--xr-font-color0);
    }

    .xr-section-summary {
      grid-column: 1;
      color: var(--xr-font-color2);
      font-weight: 500;
    }

    .xr-section-summary > span {
      display: inline-block;
      padding-left: 0.5em;
    }

    .xr-section-summary-in:disabled + label {
      color: var(--xr-font-color2);
    }

    .xr-section-summary-in + label:before {
      display: inline-block;
      content: '►';
      font-size: 11px;
      width: 15px;
      text-align: center;
    }

    .xr-section-summary-in:disabled + label:before {
      color: var(--xr-disabled-color);
    }

    .xr-section-summary-in:checked + label:before {
      content: '▼';
    }

    .xr-section-summary-in:checked + label > span {
      display: none;
    }

    .xr-section-summary,
    .xr-section-inline-details {
      padding-top: 4px;
      padding-bottom: 4px;
    }

    .xr-section-inline-details {
      grid-column: 2 / -1;
    }

    .xr-section-details {
      display: none;
      grid-column: 1 / -1;
      margin-bottom: 5px;
    }

    .xr-section-summary-in:checked ~ .xr-section-details {
      display: contents;
    }

    .xr-array-wrap {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 20px auto;
    }

    .xr-array-wrap > label {
      grid-column: 1;
      vertical-align: top;
    }

    .xr-preview {
      color: var(--xr-font-color3);
    }

    .xr-array-preview,
    .xr-array-data {
      padding: 0 5px !important;
      grid-column: 2;
    }

    .xr-array-data,
    .xr-array-in:checked ~ .xr-array-preview {
      display: none;
    }

    .xr-array-in:checked ~ .xr-array-data,
    .xr-array-preview {
      display: inline-block;
    }

    .xr-dim-list {
      display: inline-block !important;
      list-style: none;
      padding: 0 !important;
      margin: 0;
    }

    .xr-dim-list li {
      display: inline-block;
      padding: 0;
      margin: 0;
    }

    .xr-dim-list:before {
      content: '(';
    }

    .xr-dim-list:after {
      content: ')';
    }

    .xr-dim-list li:not(:last-child):after {
      content: ',';
      padding-right: 5px;
    }

    .xr-has-index {
      font-weight: bold;
    }

    .xr-var-list,
    .xr-var-item {
      display: contents;
    }

    .xr-var-item > div,
    .xr-var-item label,
    .xr-var-item > .xr-var-name span {
      background-color: var(--xr-background-color-row-even);
      margin-bottom: 0;
    }

    .xr-var-item > .xr-var-name:hover span {
      padding-right: 5px;
    }

    .xr-var-list > li:nth-child(odd) > div,
    .xr-var-list > li:nth-child(odd) > label,
    .xr-var-list > li:nth-child(odd) > .xr-var-name span {
      background-color: var(--xr-background-color-row-odd);
    }

    .xr-var-name {
      grid-column: 1;
    }

    .xr-var-dims {
      grid-column: 2;
    }

    .xr-var-dtype {
      grid-column: 3;
      text-align: right;
      color: var(--xr-font-color2);
    }

    .xr-var-preview {
      grid-column: 4;
    }

    .xr-var-name,
    .xr-var-dims,
    .xr-var-dtype,
    .xr-preview,
    .xr-attrs dt {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 10px;
    }

    .xr-var-name:hover,
    .xr-var-dims:hover,
    .xr-var-dtype:hover,
    .xr-attrs dt:hover {
      overflow: visible;
      width: auto;
      z-index: 1;
    }

    .xr-var-attrs,
    .xr-var-data {
      display: none;
      background-color: var(--xr-background-color) !important;
      padding-bottom: 5px !important;
    }

    .xr-var-attrs-in:checked ~ .xr-var-attrs,
    .xr-var-data-in:checked ~ .xr-var-data {
      display: block;
    }

    .xr-var-data > table {
      float: right;
    }

    .xr-var-name span,
    .xr-var-data,
    .xr-attrs {
      padding-left: 25px !important;
    }

    .xr-attrs,
    .xr-var-attrs,
    .xr-var-data {
      grid-column: 1 / -1;
    }

    dl.xr-attrs {
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 125px auto;
    }

    .xr-attrs dt, dd {
      padding: 0;
      margin: 0;
      float: left;
      padding-right: 10px;
      width: auto;
    }

    .xr-attrs dt {
      font-weight: normal;
      grid-column: 1;
    }

    .xr-attrs dt:hover span {
      display: inline-block;
      background: var(--xr-background-color);
      padding-right: 10px;
    }

    .xr-attrs dd {
      grid-column: 2;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .xr-icon-database,
    .xr-icon-file-text2 {
      display: inline-block;
      vertical-align: middle;
      width: 1em;
      height: 1.5em !important;
      stroke-width: 0;
      stroke: currentColor;
      fill: currentColor;
    }
    </style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
    Dimensions:                              (dim_0: 1, dim_1: 2048, dim_10: 2, dim_2: 2048, dim_3: 17, dim_4: 3, dim_5: 40, dim_6: 2, dim_7: 19, dim_8: 3, dim_9: 14, time: 1)
    Coordinates:
      * time                                 (time) float64 1.599e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        pe1_image                            (time, dim_0, dim_1, dim_2) uint16 0...
        pe1_stats1_total                     (time) float64 4.747e+08
        pe1:pe1_cam_acquire_period           (time) float64 0.1
        pe1:pe1_cam_acquire_time             (time) float64 0.2
        pe1:pe1_cam_bin_x                    (time) int64 1
        pe1:pe1_cam_bin_y                    (time) int64 1
        pe1:pe1_cam_image_mode               (time) int64 2
        pe1:pe1_cam_manufacturer             (time) &lt;U12 &#x27;Perkin Elmer&#x27;
        pe1:pe1_cam_model                    (time) &lt;U23 &#x27;XRD [0820/1620/1621] xN&#x27;
        pe1:pe1_cam_num_exposures            (time) int64 1
        pe1:pe1_cam_trigger_mode             (time) int64 0
        pe1:pe1_tiff_configuration_names     (time, dim_3) &lt;U29 &#x27;pe1_tiff_configu...
        pe1:pe1_tiff_port_name               (time) &lt;U9 &#x27;FileTIFF1&#x27;
        pe1:pe1_tiff_asyn_pipeline_config    (time, dim_4) &lt;U28 &#x27;pe1_cam_configur...
        pe1:pe1_tiff_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_tiff_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_tiff_nd_array_port           (time) &lt;U5 &#x27;PROC1&#x27;
        pe1:pe1_tiff_plugin_type             (time) &lt;U10 &#x27;NDFileTIFF&#x27;
        pe1:pe1_tiff_auto_increment          (time) int64 1
        pe1:pe1_tiff_auto_save               (time) int64 0
        pe1:pe1_tiff_file_format             (time) int64 0
        pe1:pe1_tiff_file_name               (time) &lt;U23 &#x27;e45a79a2-205f-47ed-8535&#x27;
        pe1:pe1_tiff_file_path               (time) &lt;U23 &#x27;G:\\pe1_data\\2020\\08\...
        pe1:pe1_tiff_file_path_exists        (time) int64 1
        pe1:pe1_tiff_file_template           (time) &lt;U15 &#x27;%s%s_%6.6d.tiff&#x27;
        pe1:pe1_tiff_file_write_mode         (time) int64 1
        pe1:pe1_tiff_full_file_name          (time) &lt;U58 &#x27;G:\\pe1_data\\2020\\08\...
        pe1:pe1_tiff_num_capture             (time) int64 1
        pe1:pe1_proc_configuration_names     (time, dim_5) &lt;U29 &#x27;pe1_proc_configu...
        pe1:pe1_proc_port_name               (time) &lt;U5 &#x27;PROC1&#x27;
        pe1:pe1_proc_asyn_pipeline_config    (time, dim_6) &lt;U28 &#x27;pe1_cam_configur...
        pe1:pe1_proc_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_proc_data_type               (time) &lt;U6 &#x27;UInt16&#x27;
        pe1:pe1_proc_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_proc_nd_array_port           (time) &lt;U6 &#x27;PEDET1&#x27;
        pe1:pe1_proc_plugin_type             (time) &lt;U15 &#x27;NDPluginProcess&#x27;
        pe1:pe1_proc_auto_offset_scale       (time) &lt;U4 &#x27;Done&#x27;
        pe1:pe1_proc_auto_reset_filter       (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_proc_copy_to_filter_seq      (time) int64 0
        pe1:pe1_proc_data_type_out           (time) &lt;U9 &#x27;Automatic&#x27;
        pe1:pe1_proc_difference_seq          (time) int64 0
        pe1:pe1_proc_enable_background       (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_filter           (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_proc_enable_flat_field       (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_high_clip        (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_low_clip         (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_enable_offset_scale     (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_proc_foffset                 (time) float64 0.0
        pe1:pe1_proc_fscale                  (time) float64 1.0
        pe1:pe1_proc_filter_callbacks        (time) &lt;U12 &#x27;Array N only&#x27;
        pe1:pe1_proc_filter_type             (time) &lt;U7 &#x27;Average&#x27;
        pe1:pe1_proc_filter_type_seq         (time) int64 0
        pe1:pe1_proc_high_clip               (time) float64 100.0
        pe1:pe1_proc_low_clip                (time) float64 0.0
        pe1:pe1_proc_num_filter              (time) int64 25
        pe1:pe1_proc_num_filter_recip        (time) float64 0.04
        pe1:pe1_proc_num_filtered            (time) int64 1
        pe1:pe1_proc_o_offset                (time) float64 0.0
        pe1:pe1_proc_o_scale                 (time) float64 1.0
        pe1:pe1_proc_offset                  (time) float64 0.0
        pe1:pe1_proc_roffset                 (time) float64 0.0
        pe1:pe1_proc_scale                   (time) float64 1.0
        pe1:pe1_proc_scale_flat_field        (time) float64 255.0
        pe1:pe1_proc_valid_background        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_proc_valid_flat_field        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_images_per_set               (time) float64 25.0
        pe1:pe1_number_of_sets               (time) int64 1
        pe1:pe1_pixel_size                   (time) float64 0.0002
        pe1:pe1_detector_type                (time) &lt;U6 &#x27;Perkin&#x27;
        pe1:pe1_stats1_configuration_names   (time, dim_7) &lt;U31 &#x27;pe1_stats1_confi...
        pe1:pe1_stats1_port_name             (time) &lt;U6 &#x27;STATS1&#x27;
        pe1:pe1_stats1_asyn_pipeline_config  (time, dim_8) &lt;U30 &#x27;pe1_cam_configur...
        pe1:pe1_stats1_blocking_callbacks    (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_stats1_enable                (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_stats1_nd_array_port         (time) &lt;U4 &#x27;ROI1&#x27;
        pe1:pe1_stats1_plugin_type           (time) &lt;U13 &#x27;NDPluginStats&#x27;
        pe1:pe1_stats1_bgd_width             (time) int64 1
        pe1:pe1_stats1_centroid_threshold    (time) float64 1.0
        pe1:pe1_stats1_compute_centroid      (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_histogram     (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_profiles      (time) &lt;U2 &#x27;No&#x27;
        pe1:pe1_stats1_compute_statistics    (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_stats1_hist_max              (time) float64 255.0
        pe1:pe1_stats1_hist_min              (time) float64 0.0
        pe1:pe1_stats1_hist_size             (time) int64 256
        pe1:pe1_stats1_ts_num_points         (time) int64 2048
        pe1:pe1_roi1_configuration_names     (time, dim_9) &lt;U29 &#x27;pe1_roi1_configu...
        pe1:pe1_roi1_port_name               (time) &lt;U4 &#x27;ROI1&#x27;
        pe1:pe1_roi1_asyn_pipeline_config    (time, dim_10) &lt;U28 &#x27;pe1_cam_configu...
        pe1:pe1_roi1_blocking_callbacks      (time) &lt;U3 &#x27;Yes&#x27;
        pe1:pe1_roi1_enable                  (time) &lt;U6 &#x27;Enable&#x27;
        pe1:pe1_roi1_nd_array_port           (time) &lt;U6 &#x27;PEDET1&#x27;
        pe1:pe1_roi1_plugin_type             (time) &lt;U11 &#x27;NDPluginROI&#x27;
        pe1:pe1_roi1_data_type_out           (time) &lt;U9 &#x27;Automatic&#x27;
        pe1:pe1_roi1_enable_scale            (time) &lt;U7 &#x27;Disable&#x27;
        pe1:pe1_roi1_name_                   (time) &lt;U1 &#x27;&#x27;
        seq_num                              (time) int64 1
        uid                                  (time) &lt;U36 &#x27;6a7a00e2-2a64-4284-9d67...</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-42b56436-3c1d-4cb8-9e60-fd2856b12dda' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-42b56436-3c1d-4cb8-9e60-fd2856b12dda' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 1</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 2</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 17</li><li><span>dim_4</span>: 3</li><li><span>dim_5</span>: 40</li><li><span>dim_6</span>: 2</li><li><span>dim_7</span>: 19</li><li><span>dim_8</span>: 3</li><li><span>dim_9</span>: 14</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-37231e9c-d831-4d51-8887-a1d76597d673' class='xr-section-summary-in' type='checkbox'  checked><label for='section-37231e9c-d831-4d51-8887-a1d76597d673' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.599e+09</div><input id='attrs-faf57017-159f-4979-a6f7-98246c652c5f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-faf57017-159f-4979-a6f7-98246c652c5f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0292acbf-e08a-4d16-b100-028a00828518' class='xr-var-data-in' type='checkbox'><label for='data-0292acbf-e08a-4d16-b100-028a00828518' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.598891e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-51d03a81-6224-48dc-b8cd-d92e7828e7f3' class='xr-section-summary-in' type='checkbox'  ><label for='section-51d03a81-6224-48dc-b8cd-d92e7828e7f3' class='xr-section-summary' >Data variables: <span>(98)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>pe1_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1, dim_2)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-3e25b97d-7efa-40f2-8946-409b368ba2ac' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3e25b97d-7efa-40f2-8946-409b368ba2ac' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-971b8963-bec1-4468-8e93-0a14f2a3ca9f' class='xr-var-data-in' type='checkbox'><label for='data-971b8963-bec1-4468-8e93-0a14f2a3ca9f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[[   0,    0,    0, ...,    0,    0,    0],
             [4906, 4913, 4929, ..., 4726, 4783, 4734],
             [4938, 4922, 4962, ..., 4886, 4789, 4768],
             ...,
             [4898, 4880, 4873, ..., 4971, 4943, 4914],
             [4848, 4867, 4868, ..., 4903, 4918, 4929],
             [   0,    0,    0, ...,    0,    0,    0]]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1_stats1_total</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.747e+08</div><input id='attrs-ec9fc673-6de0-4ea1-a2bf-13906c249aa4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ec9fc673-6de0-4ea1-a2bf-13906c249aa4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f447cda0-ea5c-4758-ae51-a098ce531265' class='xr-var-data-in' type='checkbox'><label for='data-f447cda0-ea5c-4758-ae51-a098ce531265' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([4.7474451e+08])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_period</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1</div><input id='attrs-b17bccc1-b441-4d2c-8869-7cdcd0068348' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b17bccc1-b441-4d2c-8869-7cdcd0068348' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7d05e55c-fdc4-431f-9338-2ad4a2a625a0' class='xr-var-data-in' type='checkbox'><label for='data-7d05e55c-fdc4-431f-9338-2ad4a2a625a0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.2</div><input id='attrs-e945e238-9a89-4233-897e-c34db26bb4d8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e945e238-9a89-4233-897e-c34db26bb4d8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e905f77c-0abe-4d38-bc5c-09049e109ffd' class='xr-var-data-in' type='checkbox'><label for='data-e905f77c-0abe-4d38-bc5c-09049e109ffd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_x</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-2ec360d9-42ee-4d78-a514-39bf82023ebf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2ec360d9-42ee-4d78-a514-39bf82023ebf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fe9bef09-9bbd-47c3-bac8-da4112d50d7c' class='xr-var-data-in' type='checkbox'><label for='data-fe9bef09-9bbd-47c3-bac8-da4112d50d7c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_y</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-0ffc0be2-bf86-43b6-b9b5-131bf477f805' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0ffc0be2-bf86-43b6-b9b5-131bf477f805' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9db5d8ac-e329-41b4-98dd-18ed7c088fca' class='xr-var-data-in' type='checkbox'><label for='data-9db5d8ac-e329-41b4-98dd-18ed7c088fca' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_image_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-03b61c56-389e-41b0-b38a-ab30d01ec09d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-03b61c56-389e-41b0-b38a-ab30d01ec09d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-54ee4e2b-b9a1-4480-a09d-f88d75bc767a' class='xr-var-data-in' type='checkbox'><label for='data-54ee4e2b-b9a1-4480-a09d-f88d75bc767a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_manufacturer</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Perkin Elmer&#x27;</div><input id='attrs-efcc3a07-f767-416e-842e-ab7bdd5a840c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-efcc3a07-f767-416e-842e-ab7bdd5a840c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ec48e820-a498-42a7-a281-7e6800d18a3f' class='xr-var-data-in' type='checkbox'><label for='data-ec48e820-a498-42a7-a281-7e6800d18a3f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin Elmer&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_model</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;XRD [0820/1620/1621] xN&#x27;</div><input id='attrs-1b78693f-b0c1-4587-b55c-b188dc6afb2a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1b78693f-b0c1-4587-b55c-b188dc6afb2a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0c9c0a02-8803-42d5-9a0e-71d144761e66' class='xr-var-data-in' type='checkbox'><label for='data-0c9c0a02-8803-42d5-9a0e-71d144761e66' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;XRD [0820/1620/1621] xN&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_num_exposures</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-e27102ae-df53-42c8-987a-5c05eac1cca4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e27102ae-df53-42c8-987a-5c05eac1cca4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ead7b088-48e4-42c0-9b6f-f1f53f43e06e' class='xr-var-data-in' type='checkbox'><label for='data-ead7b088-48e4-42c0-9b6f-f1f53f43e06e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_trigger_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-2377514f-12bf-4d30-9e34-e768749a0b45' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2377514f-12bf-4d30-9e34-e768749a0b45' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5a77b634-b838-4237-ba6e-c3c74dabb27e' class='xr-var-data-in' type='checkbox'><label for='data-5a77b634-b838-4237-ba6e-c3c74dabb27e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_configuration_names</span></div><div class='xr-var-dims'>(time, dim_3)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_tiff_configuration_names&#x27; ....</div><input id='attrs-3e465f51-4952-4e96-b41d-530b6bb551cd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3e465f51-4952-4e96-b41d-530b6bb551cd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d6f73f93-f29b-49df-863f-6ea9d33c0218' class='xr-var-data-in' type='checkbox'><label for='data-d6f73f93-f29b-49df-863f-6ea9d33c0218' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_tiff_configuration_names&#x27;, &#x27;pe1_tiff_port_name&#x27;,
            &#x27;pe1_tiff_asyn_pipeline_config&#x27;, &#x27;pe1_tiff_blocking_callbacks&#x27;,
            &#x27;pe1_tiff_enable&#x27;, &#x27;pe1_tiff_nd_array_port&#x27;,
            &#x27;pe1_tiff_plugin_type&#x27;, &#x27;pe1_tiff_auto_increment&#x27;,
            &#x27;pe1_tiff_auto_save&#x27;, &#x27;pe1_tiff_file_format&#x27;,
            &#x27;pe1_tiff_file_name&#x27;, &#x27;pe1_tiff_file_path&#x27;,
            &#x27;pe1_tiff_file_path_exists&#x27;, &#x27;pe1_tiff_file_template&#x27;,
            &#x27;pe1_tiff_file_write_mode&#x27;, &#x27;pe1_tiff_full_file_name&#x27;,
            &#x27;pe1_tiff_num_capture&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;FileTIFF1&#x27;</div><input id='attrs-c089205d-af05-44e2-9649-4163acbdaf6b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c089205d-af05-44e2-9649-4163acbdaf6b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2e6d8a3e-4059-4c22-b848-a01748294ffb' class='xr-var-data-in' type='checkbox'><label for='data-2e6d8a3e-4059-4c22-b848-a01748294ffb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;FileTIFF1&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_4)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-fa9e1d22-3983-4550-bc04-5b9472903bad' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fa9e1d22-3983-4550-bc04-5b9472903bad' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ffdf5af3-989b-4e49-9529-81dc17035037' class='xr-var-data-in' type='checkbox'><label for='data-ffdf5af3-989b-4e49-9529-81dc17035037' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;,
            &#x27;pe1_tiff_configuration_names&#x27;]], dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-e17dfc12-a5e5-4ca1-abad-501a21b749cd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e17dfc12-a5e5-4ca1-abad-501a21b749cd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-85dde61b-5670-433f-8d17-4269b5d052f2' class='xr-var-data-in' type='checkbox'><label for='data-85dde61b-5670-433f-8d17-4269b5d052f2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-acb1c6b7-d455-4168-bc6d-94697f612045' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-acb1c6b7-d455-4168-bc6d-94697f612045' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-32c276b7-ab10-4914-aabb-b8d9d5827947' class='xr-var-data-in' type='checkbox'><label for='data-32c276b7-ab10-4914-aabb-b8d9d5827947' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-e77e40fa-93fc-491b-98ad-98b93ddef93d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e77e40fa-93fc-491b-98ad-98b93ddef93d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-660eeb8d-50f9-414f-b7f0-8f3e7156d1ff' class='xr-var-data-in' type='checkbox'><label for='data-660eeb8d-50f9-414f-b7f0-8f3e7156d1ff' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U10</div><div class='xr-var-preview xr-preview'>&#x27;NDFileTIFF&#x27;</div><input id='attrs-f62eb497-e3dd-4849-afe5-7b382b460b4d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f62eb497-e3dd-4849-afe5-7b382b460b4d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0d681a62-73bc-424b-92b5-050502ae6091' class='xr-var-data-in' type='checkbox'><label for='data-0d681a62-73bc-424b-92b5-050502ae6091' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDFileTIFF&#x27;], dtype=&#x27;&lt;U10&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_increment</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-82f45d8a-a19a-4aba-b7a6-5f827a050944' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-82f45d8a-a19a-4aba-b7a6-5f827a050944' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4f7d1b25-387f-4800-a058-21f3714ac294' class='xr-var-data-in' type='checkbox'><label for='data-4f7d1b25-387f-4800-a058-21f3714ac294' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_save</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-83abd536-a7ea-4682-8e18-af92c2bcf91f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-83abd536-a7ea-4682-8e18-af92c2bcf91f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-236d030e-1b10-402e-b507-8a3debdec216' class='xr-var-data-in' type='checkbox'><label for='data-236d030e-1b10-402e-b507-8a3debdec216' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_format</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-5bd1cc7f-8035-44e3-b088-72a909915888' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5bd1cc7f-8035-44e3-b088-72a909915888' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e7605cfb-4ab8-4a77-b941-dc3e38dcdd0f' class='xr-var-data-in' type='checkbox'><label for='data-e7605cfb-4ab8-4a77-b941-dc3e38dcdd0f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;e45a79a2-205f-47ed-8535&#x27;</div><input id='attrs-107fe3fb-dc69-4b5d-b4b6-ea71462cbc2b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-107fe3fb-dc69-4b5d-b4b6-ea71462cbc2b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-811c568c-54c8-4bc4-b7ab-8a5617ad6371' class='xr-var-data-in' type='checkbox'><label for='data-811c568c-54c8-4bc4-b7ab-8a5617ad6371' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;e45a79a2-205f-47ed-8535&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\08\\31\\&#x27;</div><input id='attrs-c6b1afbd-8331-4d0c-a4ff-f0ed53d1bb34' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c6b1afbd-8331-4d0c-a4ff-f0ed53d1bb34' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cd7ebb58-af05-4a8a-aa0b-13df1f077ad5' class='xr-var-data-in' type='checkbox'><label for='data-cd7ebb58-af05-4a8a-aa0b-13df1f077ad5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\08\\31\\&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path_exists</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-a93a4597-bc38-4641-b00e-36be75592d20' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a93a4597-bc38-4641-b00e-36be75592d20' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-60216222-8671-4a0e-878b-1c7cd932796f' class='xr-var-data-in' type='checkbox'><label for='data-60216222-8671-4a0e-878b-1c7cd932796f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_template</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;%s%s_%6.6d.tiff&#x27;</div><input id='attrs-6593963e-2688-4da2-ab76-3a1cee73339a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6593963e-2688-4da2-ab76-3a1cee73339a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-00d2bf55-6c4b-4767-9741-6ff6b8b4169e' class='xr-var-data-in' type='checkbox'><label for='data-00d2bf55-6c4b-4767-9741-6ff6b8b4169e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;%s%s_%6.6d.tiff&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_write_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-292aaf76-8a07-4190-86d8-c743c3fcc4dd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-292aaf76-8a07-4190-86d8-c743c3fcc4dd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f3eb7d25-fdfc-45cf-bfc7-230f48679483' class='xr-var-data-in' type='checkbox'><label for='data-f3eb7d25-fdfc-45cf-bfc7-230f48679483' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_full_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U58</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\08\\31\\e45...</div><input id='attrs-bf384d52-1242-4eda-9028-906bc17a453f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bf384d52-1242-4eda-9028-906bc17a453f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7318bfa1-1a0d-48f1-b32f-854feb1d1d8c' class='xr-var-data-in' type='checkbox'><label for='data-7318bfa1-1a0d-48f1-b32f-854feb1d1d8c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\08\\31\\e45a79a2-205f-47ed-8535_000000.tiff&#x27;],
          dtype=&#x27;&lt;U58&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_num_capture</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-cd594056-31c1-4694-99e8-4eb67fb6c4b4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cd594056-31c1-4694-99e8-4eb67fb6c4b4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7d1e59dd-d219-4e25-a446-e7a42f2f84be' class='xr-var-data-in' type='checkbox'><label for='data-7d1e59dd-d219-4e25-a446-e7a42f2f84be' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_configuration_names</span></div><div class='xr-var-dims'>(time, dim_5)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_proc_configuration_names&#x27; ....</div><input id='attrs-894dccdc-c4f9-45a0-977b-3ff3730b100a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-894dccdc-c4f9-45a0-977b-3ff3730b100a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5f46b558-9225-47e3-86a2-47b374919b09' class='xr-var-data-in' type='checkbox'><label for='data-5f46b558-9225-47e3-86a2-47b374919b09' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_proc_configuration_names&#x27;, &#x27;pe1_proc_port_name&#x27;,
            &#x27;pe1_proc_asyn_pipeline_config&#x27;, &#x27;pe1_proc_blocking_callbacks&#x27;,
            &#x27;pe1_proc_data_type&#x27;, &#x27;pe1_proc_enable&#x27;,
            &#x27;pe1_proc_nd_array_port&#x27;, &#x27;pe1_proc_plugin_type&#x27;,
            &#x27;pe1_proc_auto_offset_scale&#x27;, &#x27;pe1_proc_auto_reset_filter&#x27;,
            &#x27;pe1_proc_copy_to_filter_seq&#x27;, &#x27;pe1_proc_data_type_out&#x27;,
            &#x27;pe1_proc_difference_seq&#x27;, &#x27;pe1_proc_enable_background&#x27;,
            &#x27;pe1_proc_enable_filter&#x27;, &#x27;pe1_proc_enable_flat_field&#x27;,
            &#x27;pe1_proc_enable_high_clip&#x27;, &#x27;pe1_proc_enable_low_clip&#x27;,
            &#x27;pe1_proc_enable_offset_scale&#x27;, &#x27;pe1_proc_fc&#x27;,
            &#x27;pe1_proc_foffset&#x27;, &#x27;pe1_proc_fscale&#x27;,
            &#x27;pe1_proc_filter_callbacks&#x27;, &#x27;pe1_proc_filter_type&#x27;,
            &#x27;pe1_proc_filter_type_seq&#x27;, &#x27;pe1_proc_high_clip&#x27;,
            &#x27;pe1_proc_low_clip&#x27;, &#x27;pe1_proc_num_filter&#x27;,
            &#x27;pe1_proc_num_filter_recip&#x27;, &#x27;pe1_proc_num_filtered&#x27;,
            &#x27;pe1_proc_oc&#x27;, &#x27;pe1_proc_o_offset&#x27;, &#x27;pe1_proc_o_scale&#x27;,
            &#x27;pe1_proc_offset&#x27;, &#x27;pe1_proc_rc&#x27;, &#x27;pe1_proc_roffset&#x27;,
            &#x27;pe1_proc_scale&#x27;, &#x27;pe1_proc_scale_flat_field&#x27;,
            &#x27;pe1_proc_valid_background&#x27;, &#x27;pe1_proc_valid_flat_field&#x27;]],
          dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-6c92a2ed-7bba-4c2f-bd3d-77fc798e98a0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6c92a2ed-7bba-4c2f-bd3d-77fc798e98a0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8f0955ec-1bf4-4991-a94d-6900fafa461c' class='xr-var-data-in' type='checkbox'><label for='data-8f0955ec-1bf4-4991-a94d-6900fafa461c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-f920bdee-a05f-48f0-bc48-84d48a27d878' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f920bdee-a05f-48f0-bc48-84d48a27d878' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b57ed3a6-8704-43a7-9a9e-21f2442043bb' class='xr-var-data-in' type='checkbox'><label for='data-b57ed3a6-8704-43a7-9a9e-21f2442043bb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-35b5584d-be4f-4d2d-98cc-3534e0154075' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-35b5584d-be4f-4d2d-98cc-3534e0154075' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5ce610cc-1e81-4e26-bb93-d41b6312ca87' class='xr-var-data-in' type='checkbox'><label for='data-5ce610cc-1e81-4e26-bb93-d41b6312ca87' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;UInt16&#x27;</div><input id='attrs-ea46401a-fa08-4a8e-b509-4ccaf9378e12' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ea46401a-fa08-4a8e-b509-4ccaf9378e12' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ac164d41-4eab-44c0-9802-b2a61c52327f' class='xr-var-data-in' type='checkbox'><label for='data-ac164d41-4eab-44c0-9802-b2a61c52327f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;UInt16&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-af348667-6661-4c15-bd68-827bc33aec0f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-af348667-6661-4c15-bd68-827bc33aec0f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9b147ac4-30f0-47e8-9be8-ab3ab56f1b6e' class='xr-var-data-in' type='checkbox'><label for='data-9b147ac4-30f0-47e8-9be8-ab3ab56f1b6e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-20993f99-3b32-4a20-b225-b33d48f64f28' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-20993f99-3b32-4a20-b225-b33d48f64f28' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d8e5bda4-de83-44f2-98bd-a9c80b379fba' class='xr-var-data-in' type='checkbox'><label for='data-d8e5bda4-de83-44f2-98bd-a9c80b379fba' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginProcess&#x27;</div><input id='attrs-75c4fecd-6942-4733-b6e1-0e966477b761' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-75c4fecd-6942-4733-b6e1-0e966477b761' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6f61ea86-b711-4ba5-94f9-bd23d6ba70c0' class='xr-var-data-in' type='checkbox'><label for='data-6f61ea86-b711-4ba5-94f9-bd23d6ba70c0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginProcess&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;Done&#x27;</div><input id='attrs-e6575bcf-83d4-4a35-b4ef-271348f7e404' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e6575bcf-83d4-4a35-b4ef-271348f7e404' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-676c3f1c-9d80-4e5b-9a97-2fafb05dc159' class='xr-var-data-in' type='checkbox'><label for='data-676c3f1c-9d80-4e5b-9a97-2fafb05dc159' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Done&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_reset_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-02c77d18-c62b-4c04-8aab-2322553548b0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-02c77d18-c62b-4c04-8aab-2322553548b0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-361094d6-06bd-4bf7-a6d3-38ca98763ed8' class='xr-var-data-in' type='checkbox'><label for='data-361094d6-06bd-4bf7-a6d3-38ca98763ed8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_copy_to_filter_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-41de41bb-1911-4691-9891-53d6d0420509' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-41de41bb-1911-4691-9891-53d6d0420509' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ba76a1f3-c955-4d0a-84d9-f6bce8a34997' class='xr-var-data-in' type='checkbox'><label for='data-ba76a1f3-c955-4d0a-84d9-f6bce8a34997' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-d9237b77-627c-43be-b3d5-a7c92ec5e33b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d9237b77-627c-43be-b3d5-a7c92ec5e33b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fecf77f1-c6bf-40c1-a984-cf8a082156ec' class='xr-var-data-in' type='checkbox'><label for='data-fecf77f1-c6bf-40c1-a984-cf8a082156ec' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_difference_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-44b94edb-f59e-4482-9b84-3549f1fb8a84' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-44b94edb-f59e-4482-9b84-3549f1fb8a84' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-43be3593-b536-49f1-8bb6-334fea73765f' class='xr-var-data-in' type='checkbox'><label for='data-43be3593-b536-49f1-8bb6-334fea73765f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-f3d8e0e9-5375-4a94-a61f-eec95f88a892' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f3d8e0e9-5375-4a94-a61f-eec95f88a892' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3e8208d5-c6e9-468a-865d-0f42ab007f7c' class='xr-var-data-in' type='checkbox'><label for='data-3e8208d5-c6e9-468a-865d-0f42ab007f7c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-e436a478-6a6a-4254-bd14-7ee85362be81' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e436a478-6a6a-4254-bd14-7ee85362be81' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-00f88a4c-365b-4cc4-b323-c4d99f6c909b' class='xr-var-data-in' type='checkbox'><label for='data-00f88a4c-365b-4cc4-b323-c4d99f6c909b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-9ca77bd8-693c-488b-bac4-70f661a6eee9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9ca77bd8-693c-488b-bac4-70f661a6eee9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9a51998e-6e13-4bef-ba52-911f7014c719' class='xr-var-data-in' type='checkbox'><label for='data-9a51998e-6e13-4bef-ba52-911f7014c719' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-4c118224-1d5a-445b-8802-d4099978694b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4c118224-1d5a-445b-8802-d4099978694b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f47a18cb-7fa3-4b40-a0ae-d06fc94a2d3d' class='xr-var-data-in' type='checkbox'><label for='data-f47a18cb-7fa3-4b40-a0ae-d06fc94a2d3d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-0c0b6c9f-7196-47a3-923c-9748c2d62473' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0c0b6c9f-7196-47a3-923c-9748c2d62473' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-aec4d4a2-f9cb-4c65-a2a0-506faa70cb05' class='xr-var-data-in' type='checkbox'><label for='data-aec4d4a2-f9cb-4c65-a2a0-506faa70cb05' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-22e3b38c-e321-41ea-8c24-4ee0e6e41169' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-22e3b38c-e321-41ea-8c24-4ee0e6e41169' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-10866fa1-07ca-49e2-9f24-d87c8a3e83b8' class='xr-var-data-in' type='checkbox'><label for='data-10866fa1-07ca-49e2-9f24-d87c8a3e83b8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_foffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-cd8e0f44-b250-4ee6-9215-c8a2a78b90fd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cd8e0f44-b250-4ee6-9215-c8a2a78b90fd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c22a473c-2e9a-487f-b8e4-c295e89538fa' class='xr-var-data-in' type='checkbox'><label for='data-c22a473c-2e9a-487f-b8e4-c295e89538fa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_fscale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-323ce22a-68e1-444f-806c-306cdbac5c28' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-323ce22a-68e1-444f-806c-306cdbac5c28' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-63670ae2-8379-4ce2-8410-f73ea7a855cd' class='xr-var-data-in' type='checkbox'><label for='data-63670ae2-8379-4ce2-8410-f73ea7a855cd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Array N only&#x27;</div><input id='attrs-38a4ee1e-2b29-4c75-a927-5de2a3da03c6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-38a4ee1e-2b29-4c75-a927-5de2a3da03c6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9dc4e5b4-3d97-4f48-9dac-c05443ae584b' class='xr-var-data-in' type='checkbox'><label for='data-9dc4e5b4-3d97-4f48-9dac-c05443ae584b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Array N only&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Average&#x27;</div><input id='attrs-0c07d291-341f-4b29-a413-5a2363c42390' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0c07d291-341f-4b29-a413-5a2363c42390' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ae71bf59-6f9f-4ed7-83b2-a50a7840635a' class='xr-var-data-in' type='checkbox'><label for='data-ae71bf59-6f9f-4ed7-83b2-a50a7840635a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Average&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-19491eb6-5364-40e4-ae00-cca071797d41' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-19491eb6-5364-40e4-ae00-cca071797d41' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ca8b2b98-a4cc-486e-906b-8d49c85c39a3' class='xr-var-data-in' type='checkbox'><label for='data-ca8b2b98-a4cc-486e-906b-8d49c85c39a3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>100.0</div><input id='attrs-1a51cb0b-3b33-4d77-ab38-fcfbdcc78a31' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1a51cb0b-3b33-4d77-ab38-fcfbdcc78a31' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-492676d3-923a-4f87-a987-42f845c1d212' class='xr-var-data-in' type='checkbox'><label for='data-492676d3-923a-4f87-a987-42f845c1d212' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([100.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-8e2e1ac5-2198-4ae6-b6b2-6ef6ec7e30b9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8e2e1ac5-2198-4ae6-b6b2-6ef6ec7e30b9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bee1c371-60fd-419a-b875-5c16b174a1eb' class='xr-var-data-in' type='checkbox'><label for='data-bee1c371-60fd-419a-b875-5c16b174a1eb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>25</div><input id='attrs-e7e1f4e2-6ca2-420e-adeb-c12012b3272e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e7e1f4e2-6ca2-420e-adeb-c12012b3272e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-74204d36-b900-41d4-85d3-37332b0defac' class='xr-var-data-in' type='checkbox'><label for='data-74204d36-b900-41d4-85d3-37332b0defac' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([25])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter_recip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.04</div><input id='attrs-b0080ac3-40ee-4b20-b937-dcbf61644c38' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b0080ac3-40ee-4b20-b937-dcbf61644c38' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a0c065f6-3bdf-4fe5-be49-9696cb8af6b4' class='xr-var-data-in' type='checkbox'><label for='data-a0c065f6-3bdf-4fe5-be49-9696cb8af6b4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.04])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filtered</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-23ff119c-e88c-4fcf-a950-1172d3619ea9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-23ff119c-e88c-4fcf-a950-1172d3619ea9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b7a958a8-8ff8-4ee7-ac09-aba12a3d9abb' class='xr-var-data-in' type='checkbox'><label for='data-b7a958a8-8ff8-4ee7-ac09-aba12a3d9abb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-4c8587b4-e366-4e34-a030-7dce722c3288' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4c8587b4-e366-4e34-a030-7dce722c3288' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2fcf0b52-17fb-40e4-abda-2cb3503f2c0c' class='xr-var-data-in' type='checkbox'><label for='data-2fcf0b52-17fb-40e4-abda-2cb3503f2c0c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-2442b40b-b510-47bf-a752-a1c36534f8d9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2442b40b-b510-47bf-a752-a1c36534f8d9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bc7f9c80-3d2a-4672-a238-442dc41c401e' class='xr-var-data-in' type='checkbox'><label for='data-bc7f9c80-3d2a-4672-a238-442dc41c401e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-8141751a-712a-43ef-8dea-e71c78292218' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8141751a-712a-43ef-8dea-e71c78292218' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-aebecd9b-e932-499e-9bfc-ff5540e1682a' class='xr-var-data-in' type='checkbox'><label for='data-aebecd9b-e932-499e-9bfc-ff5540e1682a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_roffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-cfc599b4-da24-415e-8e69-70deb6acde44' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cfc599b4-da24-415e-8e69-70deb6acde44' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a25fc9c0-1539-434d-8f37-b8496670f85e' class='xr-var-data-in' type='checkbox'><label for='data-a25fc9c0-1539-434d-8f37-b8496670f85e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-d1d65447-dfb2-42f4-955a-e8129b01941e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d1d65447-dfb2-42f4-955a-e8129b01941e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-239ddab7-f94b-42af-aae7-140ab8e45d33' class='xr-var-data-in' type='checkbox'><label for='data-239ddab7-f94b-42af-aae7-140ab8e45d33' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-c9362f27-c530-4bbe-a5e7-bbdc5390c4a4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c9362f27-c530-4bbe-a5e7-bbdc5390c4a4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d4c19536-2af9-4d30-9d85-01a864287429' class='xr-var-data-in' type='checkbox'><label for='data-d4c19536-2af9-4d30-9d85-01a864287429' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-169e97c6-b590-4097-8af3-bdc14599f326' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-169e97c6-b590-4097-8af3-bdc14599f326' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8bb5fef7-60fc-462b-b653-7b4a2d967203' class='xr-var-data-in' type='checkbox'><label for='data-8bb5fef7-60fc-462b-b653-7b4a2d967203' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-5f6d1f6f-aa13-4efe-89b9-dabcf5aab7e7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5f6d1f6f-aa13-4efe-89b9-dabcf5aab7e7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fac0c1ce-d6dd-43bb-9ef8-2a84c89b8af3' class='xr-var-data-in' type='checkbox'><label for='data-fac0c1ce-d6dd-43bb-9ef8-2a84c89b8af3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_images_per_set</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>25.0</div><input id='attrs-2d966647-9d74-4681-b7ba-75b4b6ab1916' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2d966647-9d74-4681-b7ba-75b4b6ab1916' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cbeb8e8b-c213-4964-b7dc-3b48a391e027' class='xr-var-data-in' type='checkbox'><label for='data-cbeb8e8b-c213-4964-b7dc-3b48a391e027' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([25.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_number_of_sets</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-ef29c7c8-525d-43f9-82ad-bedfe4d68784' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ef29c7c8-525d-43f9-82ad-bedfe4d68784' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-51756a11-9b38-441a-b65d-d49668097ecd' class='xr-var-data-in' type='checkbox'><label for='data-51756a11-9b38-441a-b65d-d49668097ecd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_pixel_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0002</div><input id='attrs-2832e874-1e80-4352-ac30-f80d5261d285' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2832e874-1e80-4352-ac30-f80d5261d285' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-44b00593-db82-4307-afab-9ea986445794' class='xr-var-data-in' type='checkbox'><label for='data-44b00593-db82-4307-afab-9ea986445794' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.0002])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_detector_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Perkin&#x27;</div><input id='attrs-ad199702-ac9c-4375-90a5-c8db3b9b8662' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ad199702-ac9c-4375-90a5-c8db3b9b8662' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-acb727a5-daa5-495e-988e-0c895613c006' class='xr-var-data-in' type='checkbox'><label for='data-acb727a5-daa5-495e-988e-0c895613c006' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>&lt;U31</div><div class='xr-var-preview xr-preview'>&#x27;pe1_stats1_configuration_names&#x27;...</div><input id='attrs-aea327e7-8b06-44ed-b015-02a2de90924e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-aea327e7-8b06-44ed-b015-02a2de90924e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5fc11aaa-622b-446c-be55-d57247ab5e5d' class='xr-var-data-in' type='checkbox'><label for='data-5fc11aaa-622b-446c-be55-d57247ab5e5d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_stats1_configuration_names&#x27;, &#x27;pe1_stats1_port_name&#x27;,
            &#x27;pe1_stats1_asyn_pipeline_config&#x27;,
            &#x27;pe1_stats1_blocking_callbacks&#x27;, &#x27;pe1_stats1_enable&#x27;,
            &#x27;pe1_stats1_nd_array_port&#x27;, &#x27;pe1_stats1_plugin_type&#x27;,
            &#x27;pe1_stats1_bgd_width&#x27;, &#x27;pe1_stats1_centroid_threshold&#x27;,
            &#x27;pe1_stats1_compute_centroid&#x27;, &#x27;pe1_stats1_compute_histogram&#x27;,
            &#x27;pe1_stats1_compute_profiles&#x27;, &#x27;pe1_stats1_compute_statistics&#x27;,
            &#x27;pe1_stats1_hist_max&#x27;, &#x27;pe1_stats1_hist_min&#x27;,
            &#x27;pe1_stats1_hist_size&#x27;, &#x27;pe1_stats1_profile_cursor&#x27;,
            &#x27;pe1_stats1_profile_size&#x27;, &#x27;pe1_stats1_ts_num_points&#x27;]],
          dtype=&#x27;&lt;U31&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;STATS1&#x27;</div><input id='attrs-990aa0bd-06b7-431e-8345-7c437af971d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-990aa0bd-06b7-431e-8345-7c437af971d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5638de94-d2f8-4bd7-a289-3007518faa16' class='xr-var-data-in' type='checkbox'><label for='data-5638de94-d2f8-4bd7-a289-3007518faa16' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;STATS1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>&lt;U30</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-5eff555a-bb4e-4016-bef8-8a7f21777be0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5eff555a-bb4e-4016-bef8-8a7f21777be0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-361895f6-c885-40c1-a4a3-ee23de98dc38' class='xr-var-data-in' type='checkbox'><label for='data-361895f6-c885-40c1-a4a3-ee23de98dc38' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;,
            &#x27;pe1_stats1_configuration_names&#x27;]], dtype=&#x27;&lt;U30&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-44b320ae-e1f3-452c-b7f2-78a84cfbc097' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-44b320ae-e1f3-452c-b7f2-78a84cfbc097' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-46eb5710-f8b1-47c0-8b9b-33aa7549ca12' class='xr-var-data-in' type='checkbox'><label for='data-46eb5710-f8b1-47c0-8b9b-33aa7549ca12' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-409a4936-66bc-462f-a652-1aea1a56a3a3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-409a4936-66bc-462f-a652-1aea1a56a3a3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ce62a8e9-f80a-4fff-8726-3558994ff2d0' class='xr-var-data-in' type='checkbox'><label for='data-ce62a8e9-f80a-4fff-8726-3558994ff2d0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-136dd7e8-22dc-470a-a92f-ee0a76c0d9c2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-136dd7e8-22dc-470a-a92f-ee0a76c0d9c2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8d92f38b-b48e-4cf1-bc1f-1fb7f9515e07' class='xr-var-data-in' type='checkbox'><label for='data-8d92f38b-b48e-4cf1-bc1f-1fb7f9515e07' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U13</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginStats&#x27;</div><input id='attrs-1e59cb28-8821-4766-bf84-d29f3ab7960e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1e59cb28-8821-4766-bf84-d29f3ab7960e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1bf657fd-7428-4b2c-adeb-fe1fe111b3e9' class='xr-var-data-in' type='checkbox'><label for='data-1bf657fd-7428-4b2c-adeb-fe1fe111b3e9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginStats&#x27;], dtype=&#x27;&lt;U13&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_bgd_width</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-9fff225e-54ad-40bf-bc10-f4f5e077b91a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9fff225e-54ad-40bf-bc10-f4f5e077b91a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5ed1a8af-141d-4eb6-ab49-e620d3267b5b' class='xr-var-data-in' type='checkbox'><label for='data-5ed1a8af-141d-4eb6-ab49-e620d3267b5b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_centroid_threshold</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-30d733d6-8d4c-48fa-a67e-85b957f9dfc3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-30d733d6-8d4c-48fa-a67e-85b957f9dfc3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9aea3506-e2a8-471f-8ea4-9c6d27b9e7ed' class='xr-var-data-in' type='checkbox'><label for='data-9aea3506-e2a8-471f-8ea4-9c6d27b9e7ed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_centroid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-6b33d6f3-e938-49d0-ae79-374140d4d6f2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6b33d6f3-e938-49d0-ae79-374140d4d6f2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3bceef41-12a7-4490-bc3c-71eea4638fff' class='xr-var-data-in' type='checkbox'><label for='data-3bceef41-12a7-4490-bc3c-71eea4638fff' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_histogram</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-07f36f08-a956-4b13-95ea-e5bfe840be2d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-07f36f08-a956-4b13-95ea-e5bfe840be2d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fca976b7-a934-4517-ac4e-32a0a635737b' class='xr-var-data-in' type='checkbox'><label for='data-fca976b7-a934-4517-ac4e-32a0a635737b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_profiles</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-f456ff59-bb44-42d2-9b88-47e212056069' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f456ff59-bb44-42d2-9b88-47e212056069' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f85c4a93-788e-416b-81e1-1198a5b9c0c5' class='xr-var-data-in' type='checkbox'><label for='data-f85c4a93-788e-416b-81e1-1198a5b9c0c5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_statistics</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-2d0daf3b-b8ad-4758-9d91-4442c7dd7c47' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2d0daf3b-b8ad-4758-9d91-4442c7dd7c47' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8ca9cfaf-b112-4aa1-9bc7-d8618d17e95e' class='xr-var-data-in' type='checkbox'><label for='data-8ca9cfaf-b112-4aa1-9bc7-d8618d17e95e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-66b80052-a320-486b-b8a7-97475f1dc552' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-66b80052-a320-486b-b8a7-97475f1dc552' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-12fb6022-b74d-4908-82c5-4dc2a8c6f384' class='xr-var-data-in' type='checkbox'><label for='data-12fb6022-b74d-4908-82c5-4dc2a8c6f384' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_min</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-e18b2d6e-d0a2-45b3-b729-971a333c636e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e18b2d6e-d0a2-45b3-b729-971a333c636e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5113c519-8d7b-43ef-a8dc-d0a00f7a7e45' class='xr-var-data-in' type='checkbox'><label for='data-5113c519-8d7b-43ef-a8dc-d0a00f7a7e45' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>256</div><input id='attrs-736d647e-9a80-4b47-a2c0-1909266edf3a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-736d647e-9a80-4b47-a2c0-1909266edf3a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-37c02914-b678-4b56-9c55-c3900ff03424' class='xr-var-data-in' type='checkbox'><label for='data-37c02914-b678-4b56-9c55-c3900ff03424' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([256])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_ts_num_points</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2048</div><input id='attrs-6647f161-11c3-45b9-a933-c91cabf5b9a1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6647f161-11c3-45b9-a933-c91cabf5b9a1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2b8b47e9-d396-4ae9-a14b-a253c0ef057a' class='xr-var-data-in' type='checkbox'><label for='data-2b8b47e9-d396-4ae9-a14b-a253c0ef057a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2048])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_roi1_configuration_names&#x27; ....</div><input id='attrs-f57bfdee-1203-4779-9707-af29f1b95625' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f57bfdee-1203-4779-9707-af29f1b95625' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-db6b00ac-9068-4721-8947-81e66b41b779' class='xr-var-data-in' type='checkbox'><label for='data-db6b00ac-9068-4721-8947-81e66b41b779' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_roi1_configuration_names&#x27;, &#x27;pe1_roi1_port_name&#x27;,
            &#x27;pe1_roi1_asyn_pipeline_config&#x27;, &#x27;pe1_roi1_blocking_callbacks&#x27;,
            &#x27;pe1_roi1_enable&#x27;, &#x27;pe1_roi1_nd_array_port&#x27;,
            &#x27;pe1_roi1_plugin_type&#x27;, &#x27;pe1_roi1_bin_&#x27;,
            &#x27;pe1_roi1_data_type_out&#x27;, &#x27;pe1_roi1_enable_scale&#x27;,
            &#x27;pe1_roi1_roi_enable&#x27;, &#x27;pe1_roi1_min_xyz&#x27;, &#x27;pe1_roi1_name_&#x27;,
            &#x27;pe1_roi1_size&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-be1c8b1d-a6dc-45c1-b475-d4ddc9cc55ac' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-be1c8b1d-a6dc-45c1-b475-d4ddc9cc55ac' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e7369e86-9f45-49a8-92d1-352c5b2e925e' class='xr-var-data-in' type='checkbox'><label for='data-e7369e86-9f45-49a8-92d1-352c5b2e925e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-9ea2e42d-b0c6-4874-b175-55c35cc73aeb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9ea2e42d-b0c6-4874-b175-55c35cc73aeb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1b35b50b-8a97-439e-b208-a1174e26f150' class='xr-var-data-in' type='checkbox'><label for='data-1b35b50b-8a97-439e-b208-a1174e26f150' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-5b6fa35d-c055-45c2-b069-307e81da11db' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5b6fa35d-c055-45c2-b069-307e81da11db' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-98170786-7848-49e2-a351-c30fbaf7ae63' class='xr-var-data-in' type='checkbox'><label for='data-98170786-7848-49e2-a351-c30fbaf7ae63' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-9bd047f5-1bf7-45fa-af05-39e98f293c5d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9bd047f5-1bf7-45fa-af05-39e98f293c5d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-60cb84c0-431a-43ca-abd4-721534168748' class='xr-var-data-in' type='checkbox'><label for='data-60cb84c0-431a-43ca-abd4-721534168748' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-14fa7381-5051-4f09-bc2c-792925b2bec1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-14fa7381-5051-4f09-bc2c-792925b2bec1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5239da8e-e0c5-47af-933a-090f3b57ee05' class='xr-var-data-in' type='checkbox'><label for='data-5239da8e-e0c5-47af-933a-090f3b57ee05' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U11</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginROI&#x27;</div><input id='attrs-1f6ffe2b-9ba2-4c6d-ad20-840876492a2a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1f6ffe2b-9ba2-4c6d-ad20-840876492a2a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7b206600-060a-492a-97b8-0f5048bba4e9' class='xr-var-data-in' type='checkbox'><label for='data-7b206600-060a-492a-97b8-0f5048bba4e9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginROI&#x27;], dtype=&#x27;&lt;U11&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-70f3ff7c-cd02-42d4-be4e-e0dfb62bac75' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-70f3ff7c-cd02-42d4-be4e-e0dfb62bac75' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1e925140-0c90-40dd-97aa-0c12e925721b' class='xr-var-data-in' type='checkbox'><label for='data-1e925140-0c90-40dd-97aa-0c12e925721b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-8d15675c-9827-47ff-8d74-f2337aeb4586' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8d15675c-9827-47ff-8d74-f2337aeb4586' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8071ba8f-3b2a-4208-b6c7-5b57887b886a' class='xr-var-data-in' type='checkbox'><label for='data-8071ba8f-3b2a-4208-b6c7-5b57887b886a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_name_</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U1</div><div class='xr-var-preview xr-preview'>&#x27;&#x27;</div><input id='attrs-0054a0e9-810a-4015-8b2d-724af7326995' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0054a0e9-810a-4015-8b2d-724af7326995' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-dab5613f-dbf3-4a1b-96f2-ec773d8c7dcb' class='xr-var-data-in' type='checkbox'><label for='data-dab5613f-dbf3-4a1b-96f2-ec773d8c7dcb' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;&#x27;], dtype=&#x27;&lt;U1&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-9b3ba4cb-5cc7-477c-9285-4b0bf87af513' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9b3ba4cb-5cc7-477c-9285-4b0bf87af513' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8ef243ad-f86c-41a0-a435-36499ab1b929' class='xr-var-data-in' type='checkbox'><label for='data-8ef243ad-f86c-41a0-a435-36499ab1b929' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;6a7a00e2-2a64-4284-9d67-e499ab6...</div><input id='attrs-88c95385-e2aa-4cc1-8e01-aae908d76abf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-88c95385-e2aa-4cc1-8e01-aae908d76abf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-476f9842-9316-4f56-81f5-90424dda9b38' class='xr-var-data-in' type='checkbox'><label for='data-476f9842-9316-4f56-81f5-90424dda9b38' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;6a7a00e2-2a64-4284-9d67-e499ab682eea&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-5351b828-1035-40c9-a5ea-5008293b2e3e' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-5351b828-1035-40c9-a5ea-5008293b2e3e' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

The data is processed by the analyzer is the diffraction image.


.. code-block:: default


    raw_data["pe1_image"][0].plot()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_001.png
    :alt: time = 1598890768.1880767
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    <matplotlib.collections.QuadMesh object at 0x7fc5f3b140d0>



In both ways, we need to use string values even if the ``qmax`` is actually a number.

After we run either line of the code above, the analyzer will use ``qmax = 20`` in the data processing.

Process the data
^^^^^^^^^^^^^^^^

We use the analyzer to process the data.


.. code-block:: default


    analyzer.analyze(run)








Get processed data from databroker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data is dumped into databroker ``an_db`` by the analyzer.
We retrieve the last run in the database and it should be the processed data from our analyzer.


.. code-block:: default


    an_db = config.an_db
    an_run = an_db[-1]








Here, we show the processed data in an xarray.


.. code-block:: default


    an_data = an_run.primary.read()
    an_data






.. raw:: html

    <div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
    <defs>
    <symbol id="icon-database" viewBox="0 0 32 32">
    <path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
    <path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    <path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
    </symbol>
    <symbol id="icon-file-text2" viewBox="0 0 32 32">
    <path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
    <path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    <path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
    </symbol>
    </defs>
    </svg>
    <style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
     *
     */

    :root {
      --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
      --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
      --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
      --xr-border-color: var(--jp-border-color2, #e0e0e0);
      --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
      --xr-background-color: var(--jp-layout-color0, white);
      --xr-background-color-row-even: var(--jp-layout-color1, white);
      --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
    }

    html[theme=dark],
    body.vscode-dark {
      --xr-font-color0: rgba(255, 255, 255, 1);
      --xr-font-color2: rgba(255, 255, 255, 0.54);
      --xr-font-color3: rgba(255, 255, 255, 0.38);
      --xr-border-color: #1F1F1F;
      --xr-disabled-color: #515151;
      --xr-background-color: #111111;
      --xr-background-color-row-even: #111111;
      --xr-background-color-row-odd: #313131;
    }

    .xr-wrap {
      display: block;
      min-width: 300px;
      max-width: 700px;
    }

    .xr-text-repr-fallback {
      /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
      display: none;
    }

    .xr-header {
      padding-top: 6px;
      padding-bottom: 6px;
      margin-bottom: 4px;
      border-bottom: solid 1px var(--xr-border-color);
    }

    .xr-header > div,
    .xr-header > ul {
      display: inline;
      margin-top: 0;
      margin-bottom: 0;
    }

    .xr-obj-type,
    .xr-array-name {
      margin-left: 2px;
      margin-right: 10px;
    }

    .xr-obj-type {
      color: var(--xr-font-color2);
    }

    .xr-sections {
      padding-left: 0 !important;
      display: grid;
      grid-template-columns: 150px auto auto 1fr 20px 20px;
    }

    .xr-section-item {
      display: contents;
    }

    .xr-section-item input {
      display: none;
    }

    .xr-section-item input + label {
      color: var(--xr-disabled-color);
    }

    .xr-section-item input:enabled + label {
      cursor: pointer;
      color: var(--xr-font-color2);
    }

    .xr-section-item input:enabled + label:hover {
      color: var(--xr-font-color0);
    }

    .xr-section-summary {
      grid-column: 1;
      color: var(--xr-font-color2);
      font-weight: 500;
    }

    .xr-section-summary > span {
      display: inline-block;
      padding-left: 0.5em;
    }

    .xr-section-summary-in:disabled + label {
      color: var(--xr-font-color2);
    }

    .xr-section-summary-in + label:before {
      display: inline-block;
      content: '►';
      font-size: 11px;
      width: 15px;
      text-align: center;
    }

    .xr-section-summary-in:disabled + label:before {
      color: var(--xr-disabled-color);
    }

    .xr-section-summary-in:checked + label:before {
      content: '▼';
    }

    .xr-section-summary-in:checked + label > span {
      display: none;
    }

    .xr-section-summary,
    .xr-section-inline-details {
      padding-top: 4px;
      padding-bottom: 4px;
    }

    .xr-section-inline-details {
      grid-column: 2 / -1;
    }

    .xr-section-details {
      display: none;
      grid-column: 1 / -1;
      margin-bottom: 5px;
    }

    .xr-section-summary-in:checked ~ .xr-section-details {
      display: contents;
    }

    .xr-array-wrap {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 20px auto;
    }

    .xr-array-wrap > label {
      grid-column: 1;
      vertical-align: top;
    }

    .xr-preview {
      color: var(--xr-font-color3);
    }

    .xr-array-preview,
    .xr-array-data {
      padding: 0 5px !important;
      grid-column: 2;
    }

    .xr-array-data,
    .xr-array-in:checked ~ .xr-array-preview {
      display: none;
    }

    .xr-array-in:checked ~ .xr-array-data,
    .xr-array-preview {
      display: inline-block;
    }

    .xr-dim-list {
      display: inline-block !important;
      list-style: none;
      padding: 0 !important;
      margin: 0;
    }

    .xr-dim-list li {
      display: inline-block;
      padding: 0;
      margin: 0;
    }

    .xr-dim-list:before {
      content: '(';
    }

    .xr-dim-list:after {
      content: ')';
    }

    .xr-dim-list li:not(:last-child):after {
      content: ',';
      padding-right: 5px;
    }

    .xr-has-index {
      font-weight: bold;
    }

    .xr-var-list,
    .xr-var-item {
      display: contents;
    }

    .xr-var-item > div,
    .xr-var-item label,
    .xr-var-item > .xr-var-name span {
      background-color: var(--xr-background-color-row-even);
      margin-bottom: 0;
    }

    .xr-var-item > .xr-var-name:hover span {
      padding-right: 5px;
    }

    .xr-var-list > li:nth-child(odd) > div,
    .xr-var-list > li:nth-child(odd) > label,
    .xr-var-list > li:nth-child(odd) > .xr-var-name span {
      background-color: var(--xr-background-color-row-odd);
    }

    .xr-var-name {
      grid-column: 1;
    }

    .xr-var-dims {
      grid-column: 2;
    }

    .xr-var-dtype {
      grid-column: 3;
      text-align: right;
      color: var(--xr-font-color2);
    }

    .xr-var-preview {
      grid-column: 4;
    }

    .xr-var-name,
    .xr-var-dims,
    .xr-var-dtype,
    .xr-preview,
    .xr-attrs dt {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 10px;
    }

    .xr-var-name:hover,
    .xr-var-dims:hover,
    .xr-var-dtype:hover,
    .xr-attrs dt:hover {
      overflow: visible;
      width: auto;
      z-index: 1;
    }

    .xr-var-attrs,
    .xr-var-data {
      display: none;
      background-color: var(--xr-background-color) !important;
      padding-bottom: 5px !important;
    }

    .xr-var-attrs-in:checked ~ .xr-var-attrs,
    .xr-var-data-in:checked ~ .xr-var-data {
      display: block;
    }

    .xr-var-data > table {
      float: right;
    }

    .xr-var-name span,
    .xr-var-data,
    .xr-attrs {
      padding-left: 25px !important;
    }

    .xr-attrs,
    .xr-var-attrs,
    .xr-var-data {
      grid-column: 1 / -1;
    }

    dl.xr-attrs {
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: 125px auto;
    }

    .xr-attrs dt, dd {
      padding: 0;
      margin: 0;
      float: left;
      padding-right: 10px;
      width: auto;
    }

    .xr-attrs dt {
      font-weight: normal;
      grid-column: 1;
    }

    .xr-attrs dt:hover span {
      display: inline-block;
      background: var(--xr-background-color);
      padding-right: 10px;
    }

    .xr-attrs dd {
      grid-column: 2;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .xr-icon-database,
    .xr-icon-file-text2 {
      display: inline-block;
      vertical-align: middle;
      width: 1em;
      height: 1.5em !important;
      stroke-width: 0;
      stroke: currentColor;
      fill: currentColor;
    }
    </style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
    Dimensions:       (dim_0: 2048, dim_1: 2048, dim_10: 770, dim_11: 770, dim_12: 770, dim_13: 770, dim_14: 3001, dim_15: 3001, dim_2: 2048, dim_3: 2048, dim_4: 2048, dim_5: 2048, dim_6: 1024, dim_7: 1024, dim_8: 839, dim_9: 839, time: 1)
    Coordinates:
      * time          (time) float64 1.607e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_11, dim_12, dim_13, dim_14, dim_15, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        dk_sub_image  (time, dim_0, dim_1) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        bg_sub_image  (time, dim_2, dim_3) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        mask          (time, dim_4, dim_5) int64 1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1
        chi_Q         (time, dim_6) float64 0.02664 0.05525 0.08385 ... 29.26 29.29
        chi_I         (time, dim_7) float32 85.86265 84.71822 86.26226 ... 0.0 0.0
        chi_max       (time) float32 5094.0054
        chi_argmax    (time) float64 1.371
        iq_Q          (time, dim_8) float64 0.0 0.02861 0.05721 ... 23.94 23.97
        iq_I          (time, dim_9) float64 85.86 85.78 84.82 ... 199.3 198.9 198.4
        sq_Q          (time, dim_10) float64 0.0 0.02861 0.05721 ... 21.97 22.0
        sq_S          (time, dim_11) float64 0.0111 0.02154 ... 0.9974 0.9996
        fq_Q          (time, dim_12) float64 0.0 0.02861 0.05721 ... 21.97 22.0
        fq_F          (time, dim_13) float64 -0.0 -0.02799 ... -0.057 -0.009531
        gr_r          (time, dim_14) float64 0.0 0.01 0.02 0.03 ... 29.98 29.99 30.0
        gr_G          (time, dim_15) float64 0.0 -0.002569 ... -0.004487 -0.004957
        gr_max        (time) float64 0.5124
        gr_argmax     (time) float64 1.43
        seq_num       (time) int64 1
        uid           (time) &lt;U36 &#x27;100654f6-12d9-48e2-a04c-613bcc30e658&#x27;</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-8ba95db0-bb96-4d16-a7dd-1821dc505813' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-8ba95db0-bb96-4d16-a7dd-1821dc505813' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 2048</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 770</li><li><span>dim_11</span>: 770</li><li><span>dim_12</span>: 770</li><li><span>dim_13</span>: 770</li><li><span>dim_14</span>: 3001</li><li><span>dim_15</span>: 3001</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 2048</li><li><span>dim_4</span>: 2048</li><li><span>dim_5</span>: 2048</li><li><span>dim_6</span>: 1024</li><li><span>dim_7</span>: 1024</li><li><span>dim_8</span>: 839</li><li><span>dim_9</span>: 839</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-a0f41e27-732c-4110-99b1-6871e1af91c2' class='xr-section-summary-in' type='checkbox'  checked><label for='section-a0f41e27-732c-4110-99b1-6871e1af91c2' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.607e+09</div><input id='attrs-d70858e7-3c8f-4a84-8640-8c0384f78231' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d70858e7-3c8f-4a84-8640-8c0384f78231' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-764e8c00-524c-4ff9-b374-7f2dae126cd0' class='xr-var-data-in' type='checkbox'><label for='data-764e8c00-524c-4ff9-b374-7f2dae126cd0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.607037e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-b4d85a05-e97f-480e-8d72-b459fc77a132' class='xr-section-summary-in' type='checkbox'  ><label for='section-b4d85a05-e97f-480e-8d72-b459fc77a132' class='xr-section-summary' >Data variables: <span>(19)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>dk_sub_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-e52a6465-b12f-4e9e-9a6c-e939a793cc2f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e52a6465-b12f-4e9e-9a6c-e939a793cc2f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9f90c5e8-c51e-4a6a-bde6-29c0deb8fe3a' class='xr-var-data-in' type='checkbox'><label for='data-9f90c5e8-c51e-4a6a-bde6-29c0deb8fe3a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[ 0,  0,  0, ...,  0,  0,  0],
            [14, 14, 31, ..., 26, 11,  3],
            [20, 18, 31, ..., 34, 25, 10],
            ...,
            [26, 31, 28, ..., 40, 30, 11],
            [18, 29, 27, ..., 29, 23,  8],
            [ 0,  0,  0, ...,  0,  0,  0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>bg_sub_image</span></div><div class='xr-var-dims'>(time, dim_2, dim_3)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-a3355b65-8892-491f-b577-6f245fa73731' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a3355b65-8892-491f-b577-6f245fa73731' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3b17a4f7-5acc-475c-8ab2-c70e6d991300' class='xr-var-data-in' type='checkbox'><label for='data-3b17a4f7-5acc-475c-8ab2-c70e6d991300' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[ 0,  0,  0, ...,  0,  0,  0],
            [14, 14, 31, ..., 26, 11,  3],
            [20, 18, 31, ..., 34, 25, 10],
            ...,
            [26, 31, 28, ..., 40, 30, 11],
            [18, 29, 27, ..., 29, 23,  8],
            [ 0,  0,  0, ...,  0,  0,  0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>mask</span></div><div class='xr-var-dims'>(time, dim_4, dim_5)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1</div><input id='attrs-b5165481-cc9c-4919-bf5b-9d0fee3ddcd6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b5165481-cc9c-4919-bf5b-9d0fee3ddcd6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2e55c0b7-92a6-41cd-b298-bd650bd35b0a' class='xr-var-data-in' type='checkbox'><label for='data-2e55c0b7-92a6-41cd-b298-bd650bd35b0a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            ...,
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1]]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_Q</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.02664 0.05525 ... 29.26 29.29</div><input id='attrs-a35f63ca-abb7-404b-a5c1-450ca1ae10af' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a35f63ca-abb7-404b-a5c1-450ca1ae10af' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c2836055-3921-4b6f-8bd7-a70c8d8c2fe8' class='xr-var-data-in' type='checkbox'><label for='data-c2836055-3921-4b6f-8bd7-a70c8d8c2fe8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[2.66397920e-02, 5.52467933e-02, 8.38537946e-02, ...,
            2.92343881e+01, 2.92629951e+01, 2.92916021e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_I</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>85.86265 84.71822 ... 0.0 0.0</div><input id='attrs-6d4ec9f3-cb78-426b-b43a-f5b8bf3dd6c8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6d4ec9f3-cb78-426b-b43a-f5b8bf3dd6c8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ea28fc29-40cf-49b6-82a0-1103c509a719' class='xr-var-data-in' type='checkbox'><label for='data-ea28fc29-40cf-49b6-82a0-1103c509a719' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[85.86265, 84.71822, 86.26226, ...,  0.     ,  0.     ,  0.     ]],
          dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>5094.0054</div><input id='attrs-c642bcec-dbbc-45f0-922c-8da5b9e0ad41' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c642bcec-dbbc-45f0-922c-8da5b9e0ad41' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-885639c6-0898-4920-b429-d0a23fab021d' class='xr-var-data-in' type='checkbox'><label for='data-885639c6-0898-4920-b429-d0a23fab021d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([5094.0054], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.371</div><input id='attrs-f4784fe6-99b8-4ebf-af4e-6660b4bcefcf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f4784fe6-99b8-4ebf-af4e-6660b4bcefcf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fdfb8512-1f2e-4896-b7db-3c1f500a4203' class='xr-var-data-in' type='checkbox'><label for='data-fdfb8512-1f2e-4896-b7db-3c1f500a4203' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.37116885])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_Q</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.02861 0.05721 ... 23.94 23.97</div><input id='attrs-017110c0-241c-4e74-9abc-90e29e7936dc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-017110c0-241c-4e74-9abc-90e29e7936dc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-501ec965-6e8f-467b-bd28-15608d40c7c7' class='xr-var-data-in' type='checkbox'><label for='data-501ec965-6e8f-467b-bd28-15608d40c7c7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.028607  ,  0.057214  ,  0.085821  ,  0.11442801,
             0.14303501,  0.17164201,  0.20024901,  0.22885601,  0.25746301,
             0.28607001,  0.31467701,  0.34328402,  0.37189102,  0.40049802,
             0.42910502,  0.45771202,  0.48631902,  0.51492602,  0.54353302,
             0.57214003,  0.60074703,  0.62935403,  0.65796103,  0.68656803,
             0.71517503,  0.74378203,  0.77238903,  0.80099604,  0.82960304,
             0.85821004,  0.88681704,  0.91542404,  0.94403104,  0.97263804,
             1.00124504,  1.02985205,  1.05845905,  1.08706605,  1.11567305,
             1.14428005,  1.17288705,  1.20149405,  1.23010105,  1.25870806,
             1.28731506,  1.31592206,  1.34452906,  1.37313606,  1.40174306,
             1.43035006,  1.45895706,  1.48756407,  1.51617107,  1.54477807,
             1.57338507,  1.60199207,  1.63059907,  1.65920607,  1.68781308,
             1.71642008,  1.74502708,  1.77363408,  1.80224108,  1.83084808,
             1.85945508,  1.88806208,  1.91666909,  1.94527609,  1.97388309,
             2.00249009,  2.03109709,  2.05970409,  2.08831109,  2.11691809,
             2.1455251 ,  2.1741321 ,  2.2027391 ,  2.2313461 ,  2.2599531 ,
             2.2885601 ,  2.3171671 ,  2.3457741 ,  2.37438111,  2.40298811,
             2.43159511,  2.46020211,  2.48880911,  2.51741611,  2.54602311,
             2.57463011,  2.60323712,  2.63184412,  2.66045112,  2.68905812,
             2.71766512,  2.74627212,  2.77487912,  2.80348612,  2.83209313,
    ...
            21.16918094, 21.19778794, 21.22639494, 21.25500194, 21.28360895,
            21.31221595, 21.34082295, 21.36942995, 21.39803695, 21.42664395,
            21.45525095, 21.48385795, 21.51246496, 21.54107196, 21.56967896,
            21.59828596, 21.62689296, 21.65549996, 21.68410696, 21.71271396,
            21.74132097, 21.76992797, 21.79853497, 21.82714197, 21.85574897,
            21.88435597, 21.91296297, 21.94156998, 21.97017698, 21.99878398,
            22.02739098, 22.05599798, 22.08460498, 22.11321198, 22.14181898,
            22.17042599, 22.19903299, 22.22763999, 22.25624699, 22.28485399,
            22.31346099, 22.34206799, 22.37067499, 22.399282  , 22.427889  ,
            22.456496  , 22.485103  , 22.51371   , 22.542317  , 22.570924  ,
            22.599531  , 22.62813801, 22.65674501, 22.68535201, 22.71395901,
            22.74256601, 22.77117301, 22.79978001, 22.82838701, 22.85699402,
            22.88560102, 22.91420802, 22.94281502, 22.97142202, 23.00002902,
            23.02863602, 23.05724302, 23.08585003, 23.11445703, 23.14306403,
            23.17167103, 23.20027803, 23.22888503, 23.25749203, 23.28609903,
            23.31470604, 23.34331304, 23.37192004, 23.40052704, 23.42913404,
            23.45774104, 23.48634804, 23.51495504, 23.54356205, 23.57216905,
            23.60077605, 23.62938305, 23.65799005, 23.68659705, 23.71520405,
            23.74381106, 23.77241806, 23.80102506, 23.82963206, 23.85823906,
            23.88684606, 23.91545306, 23.94406006, 23.97266707]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_I</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>85.86 85.78 84.82 ... 198.9 198.4</div><input id='attrs-6df30a9c-5fce-461b-a06a-fc1ea253ce77' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6df30a9c-5fce-461b-a06a-fc1ea253ce77' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-76dd852a-741d-4211-968d-1a2f57e78428' class='xr-var-data-in' type='checkbox'><label for='data-76dd852a-741d-4211-968d-1a2f57e78428' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[  85.86264801,   85.78394971,   84.8244019 ,   86.46644727,
              89.34330399,   91.16086609,   96.4154137 ,  115.54391051,
             176.62410716,  345.18678367,  647.43122376,  932.44093501,
            1313.16691337, 1765.56211688, 2182.56199716, 2542.71615282,
            2807.16213533, 3062.76194799, 3238.45037934, 3376.45557215,
            3482.54219454, 3568.18170169, 3645.90891288, 3682.06444507,
            3709.22949374, 3751.35527982, 3767.73134598, 3800.52227287,
            3835.64682394, 3868.40440136, 3921.18617649, 3959.6199192 ,
            4014.22033744, 4066.24532368, 4108.30486257, 4159.8033555 ,
            4187.08437729, 4235.98867744, 4282.02384505, 4326.44352957,
            4409.15203201, 4489.16798746, 4599.64093646, 4713.94518743,
            4825.69695646, 4943.7819105 , 5020.63037133, 5080.02277588,
            5092.30426812, 5065.57820207, 5008.71749655, 4908.0086016 ,
            4798.84040419, 4662.35388865, 4531.01751853, 4396.46480995,
            4260.23377028, 4136.83837594, 4010.99337725, 3898.04577054,
            3791.01840542, 3686.83393275, 3587.64832404, 3487.4649561 ,
            3392.79616631, 3297.8786927 , 3202.01790261, 3106.70179668,
            3012.55629638, 2921.73321496, 2830.1384727 , 2742.00096723,
            2661.09231239, 2585.76621481, 2515.21159264, 2452.30253918,
            2393.3229578 , 2339.72571512, 2289.49583787, 2242.2864227 ,
    ...
             239.65260655,  238.66988943,  238.09572151,  237.63101019,
             237.00702597,  236.48708947,  236.01300938,  235.76826145,
             234.8764283 ,  234.70297261,  234.21421446,  233.80372004,
             233.14543933,  232.56872353,  231.85845872,  231.32274348,
             230.85739325,  230.29859181,  229.75615887,  229.2090784 ,
             228.64502237,  228.09719725,  227.49982431,  227.00226353,
             226.43749585,  225.88993131,  225.31707648,  224.78181183,
             224.19820401,  223.65871944,  223.09957634,  222.47460789,
             221.93191353,  221.50112141,  221.05368658,  220.43546948,
             219.82120049,  219.202812  ,  218.62633519,  218.13205961,
             217.63153526,  217.12726463,  216.58476248,  216.01639125,
             215.54556089,  214.91247253,  214.32594079,  213.76780458,
             213.29829979,  212.6280319 ,  212.15589993,  211.63916679,
             211.06755722,  210.52170888,  210.01531189,  209.45566591,
             208.96977115,  208.30107905,  207.80803682,  207.24089918,
             206.78616905,  206.28220704,  205.75258257,  205.1500513 ,
             204.64763204,  204.21989936,  203.70039941,  203.11924655,
             202.62095737,  202.13544676,  201.79793683,  201.36487645,
             201.07956863,  200.64905335,  200.21432376,  199.72360676,
             199.34604828,  198.8886273 ,  198.41287737]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_Q</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.02861 0.05721 ... 21.97 22.0</div><input id='attrs-0f5e658f-2736-489f-9297-a033a21c3615' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0f5e658f-2736-489f-9297-a033a21c3615' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-117351d4-2cb2-4da0-92eb-a18b242f6364' class='xr-var-data-in' type='checkbox'><label for='data-117351d4-2cb2-4da0-92eb-a18b242f6364' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.028607  ,  0.057214  ,  0.085821  ,  0.11442801,
             0.14303501,  0.17164201,  0.20024901,  0.22885601,  0.25746301,
             0.28607001,  0.31467701,  0.34328402,  0.37189102,  0.40049802,
             0.42910502,  0.45771202,  0.48631902,  0.51492602,  0.54353302,
             0.57214003,  0.60074703,  0.62935403,  0.65796103,  0.68656803,
             0.71517503,  0.74378203,  0.77238903,  0.80099604,  0.82960304,
             0.85821004,  0.88681704,  0.91542404,  0.94403104,  0.97263804,
             1.00124504,  1.02985205,  1.05845905,  1.08706605,  1.11567305,
             1.14428005,  1.17288705,  1.20149405,  1.23010105,  1.25870806,
             1.28731506,  1.31592206,  1.34452906,  1.37313606,  1.40174306,
             1.43035006,  1.45895706,  1.48756407,  1.51617107,  1.54477807,
             1.57338507,  1.60199207,  1.63059907,  1.65920607,  1.68781308,
             1.71642008,  1.74502708,  1.77363408,  1.80224108,  1.83084808,
             1.85945508,  1.88806208,  1.91666909,  1.94527609,  1.97388309,
             2.00249009,  2.03109709,  2.05970409,  2.08831109,  2.11691809,
             2.1455251 ,  2.1741321 ,  2.2027391 ,  2.2313461 ,  2.2599531 ,
             2.2885601 ,  2.3171671 ,  2.3457741 ,  2.37438111,  2.40298811,
             2.43159511,  2.46020211,  2.48880911,  2.51741611,  2.54602311,
             2.57463011,  2.60323712,  2.63184412,  2.66045112,  2.68905812,
             2.71766512,  2.74627212,  2.77487912,  2.80348612,  2.83209313,
    ...
            19.16669085, 19.19529785, 19.22390485, 19.25251186, 19.28111886,
            19.30972586, 19.33833286, 19.36693986, 19.39554686, 19.42415386,
            19.45276086, 19.48136787, 19.50997487, 19.53858187, 19.56718887,
            19.59579587, 19.62440287, 19.65300987, 19.68161687, 19.71022388,
            19.73883088, 19.76743788, 19.79604488, 19.82465188, 19.85325888,
            19.88186588, 19.91047288, 19.93907989, 19.96768689, 19.99629389,
            20.02490089, 20.05350789, 20.08211489, 20.11072189, 20.13932889,
            20.1679359 , 20.1965429 , 20.2251499 , 20.2537569 , 20.2823639 ,
            20.3109709 , 20.3395779 , 20.36818491, 20.39679191, 20.42539891,
            20.45400591, 20.48261291, 20.51121991, 20.53982691, 20.56843391,
            20.59704092, 20.62564792, 20.65425492, 20.68286192, 20.71146892,
            20.74007592, 20.76868292, 20.79728992, 20.82589693, 20.85450393,
            20.88311093, 20.91171793, 20.94032493, 20.96893193, 20.99753893,
            21.02614593, 21.05475294, 21.08335994, 21.11196694, 21.14057394,
            21.16918094, 21.19778794, 21.22639494, 21.25500194, 21.28360895,
            21.31221595, 21.34082295, 21.36942995, 21.39803695, 21.42664395,
            21.45525095, 21.48385795, 21.51246496, 21.54107196, 21.56967896,
            21.59828596, 21.62689296, 21.65549996, 21.68410696, 21.71271396,
            21.74132097, 21.76992797, 21.79853497, 21.82714197, 21.85574897,
            21.88435597, 21.91296297, 21.94156998, 21.97017698, 21.99878398]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_S</span></div><div class='xr-var-dims'>(time, dim_11)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0111 0.02154 ... 0.9974 0.9996</div><input id='attrs-4e252891-adce-42df-a565-72b0a4e8f400' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4e252891-adce-42df-a565-72b0a4e8f400' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-60d5a554-78c7-45ac-b057-3eb7e6eef201' class='xr-var-data-in' type='checkbox'><label for='data-60d5a554-78c7-45ac-b057-3eb7e6eef201' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.01109677, 0.02154318, 0.03177837, 0.04225646, 0.0527998 ,
            0.0631094 , 0.07377312, 0.08615956, 0.10395912, 0.13580822,
            0.18523768, 0.23246804, 0.29243382, 0.36206215, 0.4272352 ,
            0.48509036, 0.53040011, 0.57470949, 0.6084722 , 0.63729118,
            0.66190364, 0.68382865, 0.70475021, 0.72004964, 0.7341411 ,
            0.75031902, 0.76296252, 0.77790243, 0.79319903, 0.80819654,
            0.82605906, 0.84194328, 0.8601814 , 0.87811819, 0.8946818 ,
            0.91266969, 0.92718811, 0.94491502, 0.96228571, 0.9794805 ,
            1.00246607, 1.02517992, 1.05263767, 1.08087097, 1.10891606,
            1.13814087, 1.16118029, 1.18163132, 1.1947772 , 1.20175654,
            1.20386066, 1.1987908 , 1.19211933, 1.18074657, 1.16989359,
            1.15819243, 1.14588193, 1.13537646, 1.12414287, 1.11476819,
            1.10610279, 1.09763494, 1.08974405, 1.08140001, 1.07373829,
            1.06575786, 1.05733118, 1.04871834, 1.04003144, 1.03166315,
            1.02287431, 1.01443874, 1.00706759, 1.00047939, 0.9945416 ,
            0.98981663, 0.98562408, 0.98225812, 0.97934928, 0.97684278,
            0.97432919, 0.97139854, 0.96918658, 0.96648153, 0.96404748,
            0.96179597, 0.95951265, 0.95789578, 0.95595645, 0.95451072,
            0.95363829, 0.95348177, 0.95409697, 0.95428549, 0.95521673,
            0.95644139, 0.95805918, 0.9602171 , 0.96234729, 0.96491356,
    ...
            1.00361859, 1.00306913, 1.0027782 , 1.00308618, 1.00272346,
            1.00262824, 1.00242651, 1.00196771, 1.00150248, 1.00186633,
            1.00186298, 1.001379  , 1.0013879 , 1.0017147 , 1.00149054,
            1.0010619 , 1.00092195, 1.00056945, 1.00068046, 1.00082213,
            1.0007892 , 1.00041706, 1.00009188, 1.00041915, 1.00024879,
            0.99958058, 0.99944494, 0.99965   , 0.99984578, 0.99989122,
            0.99946334, 0.99999727, 1.00004452, 0.99937605, 0.99924016,
            0.99937294, 0.99951736, 0.99953244, 0.99977679, 0.99982243,
            0.99991161, 0.99927458, 0.99936515, 0.99932191, 0.99954765,
            0.99949604, 0.99912709, 0.99918498, 0.99921381, 0.99922569,
            0.9989831 , 0.99939867, 0.99925333, 0.99885779, 0.99911824,
            0.99941786, 0.99938452, 0.99927402, 0.99920573, 0.99752927,
            0.99943755, 0.99940695, 1.00003288, 0.99978258, 0.99980578,
            0.99987117, 0.99971374, 0.99946135, 0.99945114, 0.99896247,
            0.99912419, 0.99940718, 0.99947919, 0.99904166, 0.99941912,
            0.99948171, 0.99948463, 0.99989051, 0.99990116, 0.99973332,
            0.99964355, 0.99991889, 1.00002578, 0.99965374, 0.99912199,
            0.99230647, 0.99443372, 0.99558865, 0.99701744, 0.99770213,
            0.99822224, 0.99610622, 0.99613105, 0.99673177, 0.99648532,
            0.99678772, 0.99733281, 0.99910711, 0.99740557, 0.99956675]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_Q</span></div><div class='xr-var-dims'>(time, dim_12)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.02861 0.05721 ... 21.97 22.0</div><input id='attrs-05a98ef8-1cd1-4fba-8d20-c159e393e65d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-05a98ef8-1cd1-4fba-8d20-c159e393e65d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d2f470a8-9797-47e5-8932-d62ac294fb1b' class='xr-var-data-in' type='checkbox'><label for='data-d2f470a8-9797-47e5-8932-d62ac294fb1b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.028607  ,  0.057214  ,  0.085821  ,  0.11442801,
             0.14303501,  0.17164201,  0.20024901,  0.22885601,  0.25746301,
             0.28607001,  0.31467701,  0.34328402,  0.37189102,  0.40049802,
             0.42910502,  0.45771202,  0.48631902,  0.51492602,  0.54353302,
             0.57214003,  0.60074703,  0.62935403,  0.65796103,  0.68656803,
             0.71517503,  0.74378203,  0.77238903,  0.80099604,  0.82960304,
             0.85821004,  0.88681704,  0.91542404,  0.94403104,  0.97263804,
             1.00124504,  1.02985205,  1.05845905,  1.08706605,  1.11567305,
             1.14428005,  1.17288705,  1.20149405,  1.23010105,  1.25870806,
             1.28731506,  1.31592206,  1.34452906,  1.37313606,  1.40174306,
             1.43035006,  1.45895706,  1.48756407,  1.51617107,  1.54477807,
             1.57338507,  1.60199207,  1.63059907,  1.65920607,  1.68781308,
             1.71642008,  1.74502708,  1.77363408,  1.80224108,  1.83084808,
             1.85945508,  1.88806208,  1.91666909,  1.94527609,  1.97388309,
             2.00249009,  2.03109709,  2.05970409,  2.08831109,  2.11691809,
             2.1455251 ,  2.1741321 ,  2.2027391 ,  2.2313461 ,  2.2599531 ,
             2.2885601 ,  2.3171671 ,  2.3457741 ,  2.37438111,  2.40298811,
             2.43159511,  2.46020211,  2.48880911,  2.51741611,  2.54602311,
             2.57463011,  2.60323712,  2.63184412,  2.66045112,  2.68905812,
             2.71766512,  2.74627212,  2.77487912,  2.80348612,  2.83209313,
    ...
            19.16669085, 19.19529785, 19.22390485, 19.25251186, 19.28111886,
            19.30972586, 19.33833286, 19.36693986, 19.39554686, 19.42415386,
            19.45276086, 19.48136787, 19.50997487, 19.53858187, 19.56718887,
            19.59579587, 19.62440287, 19.65300987, 19.68161687, 19.71022388,
            19.73883088, 19.76743788, 19.79604488, 19.82465188, 19.85325888,
            19.88186588, 19.91047288, 19.93907989, 19.96768689, 19.99629389,
            20.02490089, 20.05350789, 20.08211489, 20.11072189, 20.13932889,
            20.1679359 , 20.1965429 , 20.2251499 , 20.2537569 , 20.2823639 ,
            20.3109709 , 20.3395779 , 20.36818491, 20.39679191, 20.42539891,
            20.45400591, 20.48261291, 20.51121991, 20.53982691, 20.56843391,
            20.59704092, 20.62564792, 20.65425492, 20.68286192, 20.71146892,
            20.74007592, 20.76868292, 20.79728992, 20.82589693, 20.85450393,
            20.88311093, 20.91171793, 20.94032493, 20.96893193, 20.99753893,
            21.02614593, 21.05475294, 21.08335994, 21.11196694, 21.14057394,
            21.16918094, 21.19778794, 21.22639494, 21.25500194, 21.28360895,
            21.31221595, 21.34082295, 21.36942995, 21.39803695, 21.42664395,
            21.45525095, 21.48385795, 21.51246496, 21.54107196, 21.56967896,
            21.59828596, 21.62689296, 21.65549996, 21.68410696, 21.71271396,
            21.74132097, 21.76992797, 21.79853497, 21.82714197, 21.85574897,
            21.88435597, 21.91296297, 21.94156998, 21.97017698, 21.99878398]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_F</span></div><div class='xr-var-dims'>(time, dim_13)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-0.0 -0.02799 ... -0.057 -0.009531</div><input id='attrs-7a87c9c2-144b-480a-9a54-d4b9bb09bc48' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7a87c9c2-144b-480a-9a54-d4b9bb09bc48' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a11ec80a-5e7e-4e09-8731-48f72da79c02' class='xr-var-data-in' type='checkbox'><label for='data-a11ec80a-5e7e-4e09-8731-48f72da79c02' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[-0.00000000e+00, -2.79907155e-02, -5.53958350e-02,
            -8.21945123e-02, -1.08386229e-01, -1.34008153e-01,
            -1.58979441e-01, -1.82995643e-01, -2.05064342e-01,
            -2.22497418e-01, -2.33079067e-01, -2.41524665e-01,
            -2.42896159e-01, -2.37243355e-01, -2.29391166e-01,
            -2.20950309e-01, -2.14941514e-01, -2.06826864e-01,
            -2.01607851e-01, -1.97144224e-01, -1.93438459e-01,
            -1.89938998e-01, -1.85816645e-01, -1.84196424e-01,
            -1.82530221e-01, -1.78565601e-01, -1.76304219e-01,
            -1.71545727e-01, -1.65646754e-01, -1.59120730e-01,
            -1.49277865e-01, -1.40167393e-01, -1.27993311e-01,
            -1.15060211e-01, -1.02436485e-01, -8.74390447e-02,
            -7.49854704e-02, -5.83051956e-02, -4.09979276e-02,
            -2.28930528e-02,  2.82187745e-03,  2.95331990e-02,
             6.32438487e-02,  9.94794662e-02,  1.37093522e-01,
             1.77830827e-01,  2.12100704e-01,  2.44208594e-01,
             2.67455591e-01,  2.82810835e-01,  2.91592113e-01,
             2.90027235e-01,  2.85789808e-01,  2.74042721e-01,
             2.62447892e-01,  2.48897601e-01,  2.33701697e-01,
             2.20744732e-01,  2.05978608e-01,  1.93707245e-01,
    ...
            -1.47546606e-02, -1.29307135e-02, -1.38309551e-02,
            -9.23947121e-03, -1.03079278e-02, -1.78794597e-02,
            -1.67171451e-02, -1.61482997e-02, -1.59262952e-02,
            -2.09451836e-02, -1.24028438e-02, -1.54219091e-02,
            -2.36242652e-02, -1.82624742e-02, -1.20735255e-02,
            -1.27827238e-02, -1.50984806e-02, -1.65413546e-02,
            -5.15257969e-02, -1.17458101e-02, -1.24017801e-02,
             6.88498405e-04, -4.55913082e-03, -4.07804211e-03,
            -2.70889734e-03, -6.02711842e-03, -1.13565739e-02,
            -1.15874942e-02, -2.19339726e-02, -1.85401112e-02,
            -1.25664870e-02, -1.10549743e-02, -2.03694515e-02,
            -1.23631985e-02, -1.10460138e-02, -1.09985064e-02,
            -2.33966989e-03, -2.11496670e-03, -5.71407123e-03,
            -7.64773246e-03, -1.74254824e-03,  5.54493858e-04,
            -7.45870454e-03, -1.89384285e-02, -1.66167095e-01,
            -1.20381363e-01, -9.55299812e-02, -6.46741319e-02,
            -4.98930615e-02, -3.86509338e-02, -8.47673709e-02,
            -8.43374449e-02, -7.13360939e-02, -7.68158585e-02,
            -7.02985709e-02, -5.84459637e-02, -1.95914855e-02,
            -5.70000493e-02, -9.53098372e-03]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_r</span></div><div class='xr-var-dims'>(time, dim_14)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01 0.02 ... 29.98 29.99 30.0</div><input id='attrs-b5bd84e4-cc1f-4c17-bf50-2f3b66e60f36' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b5bd84e4-cc1f-4c17-bf50-2f3b66e60f36' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ab2d9cd0-8459-4c0c-86ea-047de305c011' class='xr-var-data-in' type='checkbox'><label for='data-ab2d9cd0-8459-4c0c-86ea-047de305c011' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.000e+00, 1.000e-02, 2.000e-02, ..., 2.998e+01, 2.999e+01,
            3.000e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_G</span></div><div class='xr-var-dims'>(time, dim_15)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 -0.002569 ... -0.004957</div><input id='attrs-8548dd0d-60bf-462b-95d9-f07bd984b82e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8548dd0d-60bf-462b-95d9-f07bd984b82e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-87235e83-0fec-4d4f-9054-8b45c70ec4f8' class='xr-var-data-in' type='checkbox'><label for='data-87235e83-0fec-4d4f-9054-8b45c70ec4f8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        , -0.00256927, -0.00502088, ..., -0.00379451,
            -0.00448708, -0.00495651]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.5124</div><input id='attrs-41b449c8-18e8-444c-bbe9-d8f950730dc7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-41b449c8-18e8-444c-bbe9-d8f950730dc7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4e071c5a-f730-4a8e-bfcb-7fc85c34386b' class='xr-var-data-in' type='checkbox'><label for='data-4e071c5a-f730-4a8e-bfcb-7fc85c34386b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.5123865])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.43</div><input id='attrs-01c29fb6-1c64-44af-b67e-f59fe01a9ae5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-01c29fb6-1c64-44af-b67e-f59fe01a9ae5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a19e7c43-7a18-472d-bce9-a99f4faab263' class='xr-var-data-in' type='checkbox'><label for='data-a19e7c43-7a18-472d-bce9-a99f4faab263' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.43])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-acac5020-f9af-4642-8e3c-80eee65bf4a9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-acac5020-f9af-4642-8e3c-80eee65bf4a9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-467614da-a182-430e-bd3a-6de46963e42f' class='xr-var-data-in' type='checkbox'><label for='data-467614da-a182-430e-bd3a-6de46963e42f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;100654f6-12d9-48e2-a04c-613bcc3...</div><input id='attrs-83d41cc9-b1bc-4e0e-803f-a0aa65101860' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-83d41cc9-b1bc-4e0e-803f-a0aa65101860' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-48568dc1-b3d0-4e08-8101-89729f2a5825' class='xr-var-data-in' type='checkbox'><label for='data-48568dc1-b3d0-4e08-8101-89729f2a5825' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;100654f6-12d9-48e2-a04c-613bcc30e658&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-2109926e-d511-4bce-913e-df90e6b17802' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-2109926e-d511-4bce-913e-df90e6b17802' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

Here, we plot the most important part of data, that is, the reduced pair distribution function.


.. code-block:: default


    import matplotlib.pyplot as plt
    plt.plot(an_data["gr_r"][0], an_data["gr_G"][0])




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_002.png
    :alt: plot xpd analyzer
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    [<matplotlib.lines.Line2D object at 0x7fc5e0f68950>]



Change settings
^^^^^^^^^^^^^^^

We can change all the settings for the analyzer except the visualization settings
before or after the analyzer is created.
For example, we think that the ``qmax`` in section ``TRANSFORMATION SETTING``
is slightly larger than the ideal and thus we decrease it to 20 inverse angstrom.


.. code-block:: default


    config.set("TRANSFORMATION SETTING", "qmax", '20')








We can also use another way.


.. code-block:: default


    config["TRANSFORMATION SETTING"]["qmax"] = '20'








Then, we just need to run ``analyzer.analyze(run)``.

Export the processed data to files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Besides saving the metadata and data in the database, we can also export them in files at the same time.
For example, we run the code blow to let the analyzer export the processed data into the ``~/my_folder``.


.. code-block:: default


    config["FUNCTIONALITY"]["export_files"] = "True"
    config["FILE SYSTEM"]["tiff_base"] = "~/my_folder"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The detail of what the data will be like is introduced in :ref:`xpd-server-data`.

Live visualization
^^^^^^^^^^^^^^^^^^

If you would like live visualization of the processed data, run the code below to run on the functionality.


.. code-block:: default


    config["FUNCTIONALITY"]["visualize_data"] = "True"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The detail of what the figures will be like is introduced in :ref:`xpd-server-figures`.

Replay the data processing
^^^^^^^^^^^^^^^^^^^^^^^^^^

We can replay the analysis process according to the metadata and data in the analysis run.


.. code-block:: default


    from pdfstream.analyzers.xpd_analyzer import replay
    config2, analyzer2 = replay(an_run)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Warning: a temporary db is created for an db. It will be destroy at the end of the session.




The ``confgi2`` and ``analyzer2`` have the same settings as the ``config`` and ``analyzer``
except the databases.
It is because we uses two special temporary databases for the demonstration.
You will not encounter the problem if you are using permanent database in catalog.


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  8.939 seconds)


.. _sphx_glr_download_tutorials2_plot_xpd_analyzer.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_xpd_analyzer.py <plot_xpd_analyzer.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_xpd_analyzer.ipynb <plot_xpd_analyzer.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
