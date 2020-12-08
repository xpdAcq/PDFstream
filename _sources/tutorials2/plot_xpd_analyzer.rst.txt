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
    run = db['9d320500-b3c8-47a2-8554-ca63fa092c17']








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
      * time                                 (time) float64 1.582e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        pe1_image                            (time, dim_0, dim_1, dim_2) uint16 0...
        pe1_stats1_total                     (time) float64 4.41e+08
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
        pe1:pe1_tiff_file_name               (time) &lt;U23 &#x27;92b6b929-d904-42f4-9017&#x27;
        pe1:pe1_tiff_file_path               (time) &lt;U23 &#x27;G:\\pe1_data\\2020\\02\...
        pe1:pe1_tiff_file_path_exists        (time) int64 1
        pe1:pe1_tiff_file_template           (time) &lt;U15 &#x27;%s%s_%6.6d.tiff&#x27;
        pe1:pe1_tiff_file_write_mode         (time) int64 1
        pe1:pe1_tiff_full_file_name          (time) &lt;U58 &#x27;G:\\pe1_data\\2020\\02\...
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
        pe1:pe1_proc_num_filter              (time) int64 50
        pe1:pe1_proc_num_filter_recip        (time) float64 0.02
        pe1:pe1_proc_num_filtered            (time) int64 2
        pe1:pe1_proc_o_offset                (time) float64 0.0
        pe1:pe1_proc_o_scale                 (time) float64 1.0
        pe1:pe1_proc_offset                  (time) float64 0.0
        pe1:pe1_proc_roffset                 (time) float64 0.0
        pe1:pe1_proc_scale                   (time) float64 1.0
        pe1:pe1_proc_scale_flat_field        (time) float64 255.0
        pe1:pe1_proc_valid_background        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_proc_valid_flat_field        (time) &lt;U7 &#x27;Invalid&#x27;
        pe1:pe1_images_per_set               (time) float64 50.0
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
        uid                                  (time) &lt;U36 &#x27;ad3b7a7f-6564-4157-933f...</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-65de49e6-0b04-449e-aaae-e6e12cb1d841' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-65de49e6-0b04-449e-aaae-e6e12cb1d841' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 1</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 2</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 17</li><li><span>dim_4</span>: 3</li><li><span>dim_5</span>: 40</li><li><span>dim_6</span>: 2</li><li><span>dim_7</span>: 19</li><li><span>dim_8</span>: 3</li><li><span>dim_9</span>: 14</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-fa945fc4-837d-49ed-9bf0-7e6c475a24fb' class='xr-section-summary-in' type='checkbox'  checked><label for='section-fa945fc4-837d-49ed-9bf0-7e6c475a24fb' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.582e+09</div><input id='attrs-5a48cf9a-09d5-4390-aa58-eea6d34319ae' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5a48cf9a-09d5-4390-aa58-eea6d34319ae' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-44a7012f-e1f4-4285-866b-eb5f3680ace8' class='xr-var-data-in' type='checkbox'><label for='data-44a7012f-e1f4-4285-866b-eb5f3680ace8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.581814e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-02cd42ac-ba73-4204-9a00-c614d31bc9ad' class='xr-section-summary-in' type='checkbox'  ><label for='section-02cd42ac-ba73-4204-9a00-c614d31bc9ad' class='xr-section-summary' >Data variables: <span>(98)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>pe1_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1, dim_2)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-949208b1-32f6-4864-8812-9be807d1daa2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-949208b1-32f6-4864-8812-9be807d1daa2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f3981573-5a3f-438c-a055-7a18af450f88' class='xr-var-data-in' type='checkbox'><label for='data-f3981573-5a3f-438c-a055-7a18af450f88' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[[   0,    0,    0, ...,    0,    0,    0],
             [4594, 4576, 4587, ..., 4123, 4172, 4122],
             [4635, 4600, 4624, ..., 4318, 4231, 4216],
             ...,
             [4335, 4315, 4312, ..., 4540, 4511, 4529],
             [4229, 4257, 4251, ..., 4458, 4474, 4525],
             [   0,    0,    0, ...,    0,    0,    0]]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1_stats1_total</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.41e+08</div><input id='attrs-47a91036-804a-4023-9e8a-24c4ed38d95e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-47a91036-804a-4023-9e8a-24c4ed38d95e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9379c397-e6bd-4895-aa10-aaa6288c92f4' class='xr-var-data-in' type='checkbox'><label for='data-9379c397-e6bd-4895-aa10-aaa6288c92f4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([4.41031435e+08])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_period</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1</div><input id='attrs-1dfd9c12-c6b5-4668-a63e-48895056c024' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1dfd9c12-c6b5-4668-a63e-48895056c024' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-17cb5f67-9bfe-4cfb-bb5b-f70a03ba592e' class='xr-var-data-in' type='checkbox'><label for='data-17cb5f67-9bfe-4cfb-bb5b-f70a03ba592e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.2</div><input id='attrs-9137a772-ad07-4472-8d60-5fd4f787a215' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9137a772-ad07-4472-8d60-5fd4f787a215' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bdefc426-222c-4248-a282-0c4048da3b44' class='xr-var-data-in' type='checkbox'><label for='data-bdefc426-222c-4248-a282-0c4048da3b44' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_x</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-a0c1c863-bb12-42d5-aa98-4c923677dc2f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a0c1c863-bb12-42d5-aa98-4c923677dc2f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c0931aa0-48cb-4fdc-aaf2-4beee12b33a9' class='xr-var-data-in' type='checkbox'><label for='data-c0931aa0-48cb-4fdc-aaf2-4beee12b33a9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_y</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-e52e5bb2-479e-4320-a98d-3e0bee6afc28' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e52e5bb2-479e-4320-a98d-3e0bee6afc28' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2f631805-0f19-4533-aa8d-c520eee3a8cc' class='xr-var-data-in' type='checkbox'><label for='data-2f631805-0f19-4533-aa8d-c520eee3a8cc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_image_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-ddd592c6-05ca-4db7-9a58-60c8666f5fec' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ddd592c6-05ca-4db7-9a58-60c8666f5fec' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-43966709-d3af-42f4-ab0d-b8ec4e640e0d' class='xr-var-data-in' type='checkbox'><label for='data-43966709-d3af-42f4-ab0d-b8ec4e640e0d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_manufacturer</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Perkin Elmer&#x27;</div><input id='attrs-ecb5b7c6-4a7b-4499-9b8d-ab4ba64198fb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ecb5b7c6-4a7b-4499-9b8d-ab4ba64198fb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b1ecbd7b-81a6-4a07-958d-20000b9aad6b' class='xr-var-data-in' type='checkbox'><label for='data-b1ecbd7b-81a6-4a07-958d-20000b9aad6b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin Elmer&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_model</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;XRD [0820/1620/1621] xN&#x27;</div><input id='attrs-4d976d0c-ea61-49f4-ae6b-4d2410ff5f93' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4d976d0c-ea61-49f4-ae6b-4d2410ff5f93' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-54ea1132-ed47-4b49-a29d-1eb142eff263' class='xr-var-data-in' type='checkbox'><label for='data-54ea1132-ed47-4b49-a29d-1eb142eff263' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;XRD [0820/1620/1621] xN&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_num_exposures</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-bb603384-58f1-472d-ba45-57bb0dc308bd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bb603384-58f1-472d-ba45-57bb0dc308bd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ab17b494-23be-4ed8-a124-a7ba02492236' class='xr-var-data-in' type='checkbox'><label for='data-ab17b494-23be-4ed8-a124-a7ba02492236' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_trigger_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-919cf8de-31c6-48ec-bfca-1dfa70ba08ea' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-919cf8de-31c6-48ec-bfca-1dfa70ba08ea' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-dcf2ab4f-ab4a-4eba-a40f-9bf4b27c430e' class='xr-var-data-in' type='checkbox'><label for='data-dcf2ab4f-ab4a-4eba-a40f-9bf4b27c430e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_configuration_names</span></div><div class='xr-var-dims'>(time, dim_3)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_tiff_configuration_names&#x27; ....</div><input id='attrs-a0041693-5c47-4bc0-b43c-fff65bab855a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a0041693-5c47-4bc0-b43c-fff65bab855a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-db0395bf-adb4-4a50-96a5-5189d8cdfe83' class='xr-var-data-in' type='checkbox'><label for='data-db0395bf-adb4-4a50-96a5-5189d8cdfe83' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_tiff_configuration_names&#x27;, &#x27;pe1_tiff_port_name&#x27;,
            &#x27;pe1_tiff_asyn_pipeline_config&#x27;, &#x27;pe1_tiff_blocking_callbacks&#x27;,
            &#x27;pe1_tiff_enable&#x27;, &#x27;pe1_tiff_nd_array_port&#x27;,
            &#x27;pe1_tiff_plugin_type&#x27;, &#x27;pe1_tiff_auto_increment&#x27;,
            &#x27;pe1_tiff_auto_save&#x27;, &#x27;pe1_tiff_file_format&#x27;,
            &#x27;pe1_tiff_file_name&#x27;, &#x27;pe1_tiff_file_path&#x27;,
            &#x27;pe1_tiff_file_path_exists&#x27;, &#x27;pe1_tiff_file_template&#x27;,
            &#x27;pe1_tiff_file_write_mode&#x27;, &#x27;pe1_tiff_full_file_name&#x27;,
            &#x27;pe1_tiff_num_capture&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;FileTIFF1&#x27;</div><input id='attrs-34655178-89a4-4421-a95e-053608b3c6d8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-34655178-89a4-4421-a95e-053608b3c6d8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-73950372-3ee4-4078-ab00-f5ce5c3e1697' class='xr-var-data-in' type='checkbox'><label for='data-73950372-3ee4-4078-ab00-f5ce5c3e1697' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;FileTIFF1&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_4)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-baeeed2a-9b8f-476d-9525-7b1502591a71' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-baeeed2a-9b8f-476d-9525-7b1502591a71' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a0389c85-3943-49b2-9530-c0da5f9d8cef' class='xr-var-data-in' type='checkbox'><label for='data-a0389c85-3943-49b2-9530-c0da5f9d8cef' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;,
            &#x27;pe1_tiff_configuration_names&#x27;]], dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-7a615815-8d71-4b21-95ff-fba7f36da7c2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7a615815-8d71-4b21-95ff-fba7f36da7c2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-03f157ea-d93c-4792-8a45-5aa767cc5806' class='xr-var-data-in' type='checkbox'><label for='data-03f157ea-d93c-4792-8a45-5aa767cc5806' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-7944f51e-4652-4cdc-9943-e50639586738' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7944f51e-4652-4cdc-9943-e50639586738' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a3054931-9a76-41fd-a91a-3e95ae1eec73' class='xr-var-data-in' type='checkbox'><label for='data-a3054931-9a76-41fd-a91a-3e95ae1eec73' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-f3601fd4-5bb7-4e30-896f-28f1c86f89d8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f3601fd4-5bb7-4e30-896f-28f1c86f89d8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-05c95f64-9757-4fba-9a30-600ce593430b' class='xr-var-data-in' type='checkbox'><label for='data-05c95f64-9757-4fba-9a30-600ce593430b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U10</div><div class='xr-var-preview xr-preview'>&#x27;NDFileTIFF&#x27;</div><input id='attrs-8830f9e0-af58-4d1c-b2ae-416a95a99ae9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8830f9e0-af58-4d1c-b2ae-416a95a99ae9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-26f8d825-0b0e-42b6-bc2b-ce04f84c3a73' class='xr-var-data-in' type='checkbox'><label for='data-26f8d825-0b0e-42b6-bc2b-ce04f84c3a73' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDFileTIFF&#x27;], dtype=&#x27;&lt;U10&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_increment</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-28686dcf-25a0-4ab0-bc20-20494f44d643' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-28686dcf-25a0-4ab0-bc20-20494f44d643' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1e850d2a-5c54-48a5-a8f0-c296a6471d07' class='xr-var-data-in' type='checkbox'><label for='data-1e850d2a-5c54-48a5-a8f0-c296a6471d07' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_save</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-b93821a4-d10c-463a-bf0f-76294a09f78b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b93821a4-d10c-463a-bf0f-76294a09f78b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fb19027e-0ac2-4900-8940-8a507b5f65f2' class='xr-var-data-in' type='checkbox'><label for='data-fb19027e-0ac2-4900-8940-8a507b5f65f2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_format</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-a5464f52-8f99-4699-a0c5-714dd2642479' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a5464f52-8f99-4699-a0c5-714dd2642479' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b5a3c297-cf56-4bcb-b728-8877a217e607' class='xr-var-data-in' type='checkbox'><label for='data-b5a3c297-cf56-4bcb-b728-8877a217e607' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;92b6b929-d904-42f4-9017&#x27;</div><input id='attrs-9cbc32db-7e9e-47af-afb5-4e9e15a6ba72' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9cbc32db-7e9e-47af-afb5-4e9e15a6ba72' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-95498cea-1408-4ee4-911e-e6b4dd3e4623' class='xr-var-data-in' type='checkbox'><label for='data-95498cea-1408-4ee4-911e-e6b4dd3e4623' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;92b6b929-d904-42f4-9017&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;</div><input id='attrs-06e48c43-2670-4a4f-bcbd-d41ca3593a43' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-06e48c43-2670-4a4f-bcbd-d41ca3593a43' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-11a401f8-ae31-415e-8770-e57152819bc3' class='xr-var-data-in' type='checkbox'><label for='data-11a401f8-ae31-415e-8770-e57152819bc3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path_exists</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-e4e3a500-bb9c-4733-b877-1bb43bade8c2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e4e3a500-bb9c-4733-b877-1bb43bade8c2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4d92b088-8cc1-4921-813e-e93f37a40968' class='xr-var-data-in' type='checkbox'><label for='data-4d92b088-8cc1-4921-813e-e93f37a40968' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_template</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;%s%s_%6.6d.tiff&#x27;</div><input id='attrs-8c39bb9a-3005-49ed-a0f9-e9fe10c30017' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8c39bb9a-3005-49ed-a0f9-e9fe10c30017' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-29b44b97-0e72-4c71-8727-177380b474e4' class='xr-var-data-in' type='checkbox'><label for='data-29b44b97-0e72-4c71-8727-177380b474e4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;%s%s_%6.6d.tiff&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_write_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-3db5b122-0395-4bac-b020-4f6d928d1e7f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3db5b122-0395-4bac-b020-4f6d928d1e7f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c0c92daa-9c5a-4c59-9313-6b2bd8f0e69b' class='xr-var-data-in' type='checkbox'><label for='data-c0c92daa-9c5a-4c59-9313-6b2bd8f0e69b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_full_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U58</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\92b...</div><input id='attrs-c2718ece-06a2-4a6b-8200-936223f92b86' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c2718ece-06a2-4a6b-8200-936223f92b86' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6dbd7317-ff21-4ff2-a20d-91d4675e6ab6' class='xr-var-data-in' type='checkbox'><label for='data-6dbd7317-ff21-4ff2-a20d-91d4675e6ab6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\92b6b929-d904-42f4-9017_000000.tiff&#x27;],
          dtype=&#x27;&lt;U58&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_num_capture</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-982543ef-34ea-4223-8fc5-5c57b791e945' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-982543ef-34ea-4223-8fc5-5c57b791e945' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9e59cb71-e146-4b60-9c30-fdafa38a821b' class='xr-var-data-in' type='checkbox'><label for='data-9e59cb71-e146-4b60-9c30-fdafa38a821b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_configuration_names</span></div><div class='xr-var-dims'>(time, dim_5)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_proc_configuration_names&#x27; ....</div><input id='attrs-7a1795ce-49d2-4e1b-a38e-b136b8144475' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7a1795ce-49d2-4e1b-a38e-b136b8144475' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-260c516a-1cb0-4d50-a893-a1cb73ffde53' class='xr-var-data-in' type='checkbox'><label for='data-260c516a-1cb0-4d50-a893-a1cb73ffde53' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_proc_configuration_names&#x27;, &#x27;pe1_proc_port_name&#x27;,
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
          dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-be0fd637-de6e-4ae0-b236-6cc0fd04a269' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-be0fd637-de6e-4ae0-b236-6cc0fd04a269' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3399127e-8c02-452b-b49a-205b6736a19c' class='xr-var-data-in' type='checkbox'><label for='data-3399127e-8c02-452b-b49a-205b6736a19c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-d70fadd7-4363-4cb0-b8ad-5e65fe711089' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d70fadd7-4363-4cb0-b8ad-5e65fe711089' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3ae0ef3d-3a6b-45b8-8829-dfaaff8b721d' class='xr-var-data-in' type='checkbox'><label for='data-3ae0ef3d-3a6b-45b8-8829-dfaaff8b721d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-bc7fe8d6-bbad-481c-8472-bd201c11bb9a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bc7fe8d6-bbad-481c-8472-bd201c11bb9a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e52a5153-5460-41f3-83b5-6bfe1f2fe60b' class='xr-var-data-in' type='checkbox'><label for='data-e52a5153-5460-41f3-83b5-6bfe1f2fe60b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;UInt16&#x27;</div><input id='attrs-9013b939-304d-42a8-9dbf-71bdf0faeaa6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9013b939-304d-42a8-9dbf-71bdf0faeaa6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-53a568a1-6a3f-4b3f-905f-f2b3618f1e74' class='xr-var-data-in' type='checkbox'><label for='data-53a568a1-6a3f-4b3f-905f-f2b3618f1e74' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;UInt16&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-cd620d7e-1777-422a-be4e-6f6bd032a56d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cd620d7e-1777-422a-be4e-6f6bd032a56d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-79075ca1-f818-4e57-ab96-68ae2377438d' class='xr-var-data-in' type='checkbox'><label for='data-79075ca1-f818-4e57-ab96-68ae2377438d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-f9d25750-bdbf-4a15-a4f3-4282931b553f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f9d25750-bdbf-4a15-a4f3-4282931b553f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1b7dce03-d0ef-4f86-8a91-73d0ade49d6c' class='xr-var-data-in' type='checkbox'><label for='data-1b7dce03-d0ef-4f86-8a91-73d0ade49d6c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginProcess&#x27;</div><input id='attrs-7a9cc862-b812-4513-90ae-c2e1fd079a97' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7a9cc862-b812-4513-90ae-c2e1fd079a97' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d868d8c3-b9ab-4210-9b07-8122156c35ac' class='xr-var-data-in' type='checkbox'><label for='data-d868d8c3-b9ab-4210-9b07-8122156c35ac' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginProcess&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;Done&#x27;</div><input id='attrs-f373460d-cce1-468f-b71c-fda7ee639317' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f373460d-cce1-468f-b71c-fda7ee639317' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-170c482f-0cf3-410d-b6e3-c3809a4830bc' class='xr-var-data-in' type='checkbox'><label for='data-170c482f-0cf3-410d-b6e3-c3809a4830bc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Done&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_reset_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-044600a9-752f-4946-8b49-23fb016dcb11' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-044600a9-752f-4946-8b49-23fb016dcb11' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9c74d049-7d72-4c84-be67-caa0a01d5670' class='xr-var-data-in' type='checkbox'><label for='data-9c74d049-7d72-4c84-be67-caa0a01d5670' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_copy_to_filter_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-5250e281-da53-49b3-a602-d7580b78784d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5250e281-da53-49b3-a602-d7580b78784d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9c4cfdb8-8071-4830-85ca-99b941eae00d' class='xr-var-data-in' type='checkbox'><label for='data-9c4cfdb8-8071-4830-85ca-99b941eae00d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-e0b79a2f-c223-45bc-a4da-4a26b40eb0af' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e0b79a2f-c223-45bc-a4da-4a26b40eb0af' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3e7efc3b-da98-452e-8c67-972bbbe1b9dc' class='xr-var-data-in' type='checkbox'><label for='data-3e7efc3b-da98-452e-8c67-972bbbe1b9dc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_difference_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-e84f83a4-0fd5-4e55-a1e6-4788783298c0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e84f83a4-0fd5-4e55-a1e6-4788783298c0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b6efa40f-8f7e-4493-9cc6-cf99677d1f98' class='xr-var-data-in' type='checkbox'><label for='data-b6efa40f-8f7e-4493-9cc6-cf99677d1f98' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-e6229c23-646d-4dc2-927b-995edd95ae2c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e6229c23-646d-4dc2-927b-995edd95ae2c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-58adf611-3077-41f7-8a25-ac08485f4afa' class='xr-var-data-in' type='checkbox'><label for='data-58adf611-3077-41f7-8a25-ac08485f4afa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-10b34f1b-6dd4-4eb6-b780-c4adaf53fd88' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-10b34f1b-6dd4-4eb6-b780-c4adaf53fd88' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d6bea798-d176-4da6-9119-d3971cfd3644' class='xr-var-data-in' type='checkbox'><label for='data-d6bea798-d176-4da6-9119-d3971cfd3644' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-0e669d9b-0b69-45b7-8d2b-441235fc653f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0e669d9b-0b69-45b7-8d2b-441235fc653f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9869c46e-c704-4ea7-94ea-51af05e03738' class='xr-var-data-in' type='checkbox'><label for='data-9869c46e-c704-4ea7-94ea-51af05e03738' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-11dbc6b4-0342-4e00-af15-19bb70cb0e4d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-11dbc6b4-0342-4e00-af15-19bb70cb0e4d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-294be102-068e-45ad-b05f-6527111c7b48' class='xr-var-data-in' type='checkbox'><label for='data-294be102-068e-45ad-b05f-6527111c7b48' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-cabc1ae8-f9f9-4288-b5fd-3a9779ba27b0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cabc1ae8-f9f9-4288-b5fd-3a9779ba27b0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6a1d512a-a640-4ef5-bf5c-eec5b4f7c126' class='xr-var-data-in' type='checkbox'><label for='data-6a1d512a-a640-4ef5-bf5c-eec5b4f7c126' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-6c9e9626-54cc-4c7c-a411-cfcb649f5667' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6c9e9626-54cc-4c7c-a411-cfcb649f5667' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ae30f1f7-2195-4a2e-9138-64fbaf98dae5' class='xr-var-data-in' type='checkbox'><label for='data-ae30f1f7-2195-4a2e-9138-64fbaf98dae5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_foffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-a796d999-09ed-44f4-a629-0770193b78d6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a796d999-09ed-44f4-a629-0770193b78d6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-41fe30a8-a7a9-4bd6-9688-4e7ce6cadc0b' class='xr-var-data-in' type='checkbox'><label for='data-41fe30a8-a7a9-4bd6-9688-4e7ce6cadc0b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_fscale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-7e33b3b5-fae2-44b0-a40d-7b248a4a024a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7e33b3b5-fae2-44b0-a40d-7b248a4a024a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-640d34d1-ecd3-4d16-9293-d6cacb28f881' class='xr-var-data-in' type='checkbox'><label for='data-640d34d1-ecd3-4d16-9293-d6cacb28f881' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Array N only&#x27;</div><input id='attrs-ce9f7eaa-a638-4179-9d14-fbead449adba' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ce9f7eaa-a638-4179-9d14-fbead449adba' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cdc40f12-2fc1-4887-b601-0a3068574312' class='xr-var-data-in' type='checkbox'><label for='data-cdc40f12-2fc1-4887-b601-0a3068574312' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Array N only&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Average&#x27;</div><input id='attrs-bfa4dfb8-b816-42b1-ba7b-7eb7ed1b12bc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bfa4dfb8-b816-42b1-ba7b-7eb7ed1b12bc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e1bd9247-4447-414f-a8f4-bbe1582d54f5' class='xr-var-data-in' type='checkbox'><label for='data-e1bd9247-4447-414f-a8f4-bbe1582d54f5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Average&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-0e7e8930-c169-4327-a49e-f036c34761a8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0e7e8930-c169-4327-a49e-f036c34761a8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-66b8ce97-8c56-4746-9181-1df33e16131a' class='xr-var-data-in' type='checkbox'><label for='data-66b8ce97-8c56-4746-9181-1df33e16131a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>100.0</div><input id='attrs-f3ba9407-7eb3-4c83-90c3-dc5d6e082bcf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f3ba9407-7eb3-4c83-90c3-dc5d6e082bcf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-86fe4465-1ecc-45c6-8171-ee6f8c606b0b' class='xr-var-data-in' type='checkbox'><label for='data-86fe4465-1ecc-45c6-8171-ee6f8c606b0b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([100.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-91115dfd-b102-47cb-aab1-1ce5829b2bac' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-91115dfd-b102-47cb-aab1-1ce5829b2bac' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-51dc77c5-b0d4-4a56-8631-dba4f3d18c92' class='xr-var-data-in' type='checkbox'><label for='data-51dc77c5-b0d4-4a56-8631-dba4f3d18c92' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>50</div><input id='attrs-dc0eaccc-fa7c-4d66-a8ce-6f65b19eb20e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dc0eaccc-fa7c-4d66-a8ce-6f65b19eb20e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5e644362-aba1-41c3-afeb-e336bd78b5ca' class='xr-var-data-in' type='checkbox'><label for='data-5e644362-aba1-41c3-afeb-e336bd78b5ca' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter_recip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.02</div><input id='attrs-4d860b74-70f8-4505-a054-37077fe7be04' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4d860b74-70f8-4505-a054-37077fe7be04' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-010d9b65-80bb-4b9e-aaeb-deb1e4893ff1' class='xr-var-data-in' type='checkbox'><label for='data-010d9b65-80bb-4b9e-aaeb-deb1e4893ff1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.02])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filtered</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-d1899330-fcec-4b2b-8f5b-673e9e5e67d2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d1899330-fcec-4b2b-8f5b-673e9e5e67d2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-314dca73-cbc0-45c7-870d-1b90b566f0c0' class='xr-var-data-in' type='checkbox'><label for='data-314dca73-cbc0-45c7-870d-1b90b566f0c0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-6bf44405-cabc-4765-8c12-9db96157a549' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6bf44405-cabc-4765-8c12-9db96157a549' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d6df7c55-8d15-403f-a208-36f408a2e9cd' class='xr-var-data-in' type='checkbox'><label for='data-d6df7c55-8d15-403f-a208-36f408a2e9cd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-f5553f3b-756e-45fe-901e-9d4133a34e6a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f5553f3b-756e-45fe-901e-9d4133a34e6a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-998c1f1d-ae16-401a-a748-1513a505bc2c' class='xr-var-data-in' type='checkbox'><label for='data-998c1f1d-ae16-401a-a748-1513a505bc2c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-c640b8e6-db7e-41be-93fd-374c7ccd88b6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c640b8e6-db7e-41be-93fd-374c7ccd88b6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-37e97661-d19c-4c9c-b606-c8f3a142faf4' class='xr-var-data-in' type='checkbox'><label for='data-37e97661-d19c-4c9c-b606-c8f3a142faf4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_roffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-5803cc01-2f9e-490a-805f-19c20db818ad' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5803cc01-2f9e-490a-805f-19c20db818ad' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ce979327-d66f-4be1-82fa-578ced2a604f' class='xr-var-data-in' type='checkbox'><label for='data-ce979327-d66f-4be1-82fa-578ced2a604f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-ae589bf6-639d-4e7d-8044-99fd58e555d9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ae589bf6-639d-4e7d-8044-99fd58e555d9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5e38dbc0-6176-485d-9b76-234ea1e1d68c' class='xr-var-data-in' type='checkbox'><label for='data-5e38dbc0-6176-485d-9b76-234ea1e1d68c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-92dbbf16-72e9-4464-b3aa-91e84046be2c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-92dbbf16-72e9-4464-b3aa-91e84046be2c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-660cc136-d64b-4c2b-9004-5dc97c3597c6' class='xr-var-data-in' type='checkbox'><label for='data-660cc136-d64b-4c2b-9004-5dc97c3597c6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-60df8148-9963-42af-91e3-b296b3f5218d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-60df8148-9963-42af-91e3-b296b3f5218d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9716b618-665f-47e9-a95a-60b0ea60ec4b' class='xr-var-data-in' type='checkbox'><label for='data-9716b618-665f-47e9-a95a-60b0ea60ec4b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-c4b62128-1abf-4edc-9ccc-5034c005b79a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c4b62128-1abf-4edc-9ccc-5034c005b79a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b878cb54-3b85-492e-857e-469b12237aa7' class='xr-var-data-in' type='checkbox'><label for='data-b878cb54-3b85-492e-857e-469b12237aa7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_images_per_set</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>50.0</div><input id='attrs-813029ba-247c-4291-b0a4-227e0a157645' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-813029ba-247c-4291-b0a4-227e0a157645' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-729edb40-37c3-485e-9b35-f7e0aee260b7' class='xr-var-data-in' type='checkbox'><label for='data-729edb40-37c3-485e-9b35-f7e0aee260b7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_number_of_sets</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-e4f54935-2600-42b8-922b-82bb24c1abad' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e4f54935-2600-42b8-922b-82bb24c1abad' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-31af7ad8-6186-406a-bae4-7490a22385f3' class='xr-var-data-in' type='checkbox'><label for='data-31af7ad8-6186-406a-bae4-7490a22385f3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_pixel_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0002</div><input id='attrs-00e110a1-8738-47a1-923b-617070459607' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-00e110a1-8738-47a1-923b-617070459607' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-313452bb-bf4b-406b-b63a-ceaf2656d533' class='xr-var-data-in' type='checkbox'><label for='data-313452bb-bf4b-406b-b63a-ceaf2656d533' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.0002])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_detector_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Perkin&#x27;</div><input id='attrs-f1a933c8-397d-4698-a50a-bbdfe4afacf4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f1a933c8-397d-4698-a50a-bbdfe4afacf4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-37f51c63-8719-41dd-9e4b-24a1996addd6' class='xr-var-data-in' type='checkbox'><label for='data-37f51c63-8719-41dd-9e4b-24a1996addd6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>&lt;U31</div><div class='xr-var-preview xr-preview'>&#x27;pe1_stats1_configuration_names&#x27;...</div><input id='attrs-8277ad5a-a04c-4788-9782-1929f5cee236' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8277ad5a-a04c-4788-9782-1929f5cee236' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2164d9e3-a143-4751-aa9c-6c4156afd8f5' class='xr-var-data-in' type='checkbox'><label for='data-2164d9e3-a143-4751-aa9c-6c4156afd8f5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_stats1_configuration_names&#x27;, &#x27;pe1_stats1_port_name&#x27;,
            &#x27;pe1_stats1_asyn_pipeline_config&#x27;,
            &#x27;pe1_stats1_blocking_callbacks&#x27;, &#x27;pe1_stats1_enable&#x27;,
            &#x27;pe1_stats1_nd_array_port&#x27;, &#x27;pe1_stats1_plugin_type&#x27;,
            &#x27;pe1_stats1_bgd_width&#x27;, &#x27;pe1_stats1_centroid_threshold&#x27;,
            &#x27;pe1_stats1_compute_centroid&#x27;, &#x27;pe1_stats1_compute_histogram&#x27;,
            &#x27;pe1_stats1_compute_profiles&#x27;, &#x27;pe1_stats1_compute_statistics&#x27;,
            &#x27;pe1_stats1_hist_max&#x27;, &#x27;pe1_stats1_hist_min&#x27;,
            &#x27;pe1_stats1_hist_size&#x27;, &#x27;pe1_stats1_profile_cursor&#x27;,
            &#x27;pe1_stats1_profile_size&#x27;, &#x27;pe1_stats1_ts_num_points&#x27;]],
          dtype=&#x27;&lt;U31&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;STATS1&#x27;</div><input id='attrs-e0a72e65-e12b-49f9-96f6-24776719a649' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e0a72e65-e12b-49f9-96f6-24776719a649' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b1c88bca-5319-411c-a958-e3fe6325aa85' class='xr-var-data-in' type='checkbox'><label for='data-b1c88bca-5319-411c-a958-e3fe6325aa85' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;STATS1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>&lt;U30</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-6457a226-435d-4142-acb6-aca5100c1779' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6457a226-435d-4142-acb6-aca5100c1779' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bab73fa3-aaa6-400a-a74d-78eed4c49afe' class='xr-var-data-in' type='checkbox'><label for='data-bab73fa3-aaa6-400a-a74d-78eed4c49afe' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;,
            &#x27;pe1_stats1_configuration_names&#x27;]], dtype=&#x27;&lt;U30&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-65d71f24-873f-4d62-8fe6-683101bf03f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-65d71f24-873f-4d62-8fe6-683101bf03f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-eeb57f51-36f7-46db-94a3-ffe46b2b6104' class='xr-var-data-in' type='checkbox'><label for='data-eeb57f51-36f7-46db-94a3-ffe46b2b6104' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-a4ed9110-9f60-4d64-be19-9a9cd4d4556a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a4ed9110-9f60-4d64-be19-9a9cd4d4556a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0e328e31-9fd0-40eb-8da9-63882388d24c' class='xr-var-data-in' type='checkbox'><label for='data-0e328e31-9fd0-40eb-8da9-63882388d24c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-678c232f-9716-41ac-a3b8-13fd88fbfa2d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-678c232f-9716-41ac-a3b8-13fd88fbfa2d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-85be3cfc-3f1e-4651-a2d4-a5107d4ec24b' class='xr-var-data-in' type='checkbox'><label for='data-85be3cfc-3f1e-4651-a2d4-a5107d4ec24b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U13</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginStats&#x27;</div><input id='attrs-4bc3dd0f-c263-4c88-a595-730e19602ae5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4bc3dd0f-c263-4c88-a595-730e19602ae5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-43b261f3-e170-4559-860c-7e489f6b5689' class='xr-var-data-in' type='checkbox'><label for='data-43b261f3-e170-4559-860c-7e489f6b5689' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginStats&#x27;], dtype=&#x27;&lt;U13&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_bgd_width</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-007df3db-24f1-46db-8128-39f1ef974819' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-007df3db-24f1-46db-8128-39f1ef974819' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4d1d0c9f-756b-4462-9b8c-c61472baa804' class='xr-var-data-in' type='checkbox'><label for='data-4d1d0c9f-756b-4462-9b8c-c61472baa804' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_centroid_threshold</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-d99e40be-b994-4c99-ae50-b2400913b5e7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d99e40be-b994-4c99-ae50-b2400913b5e7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0feb8557-e3db-474f-9564-19c7a68e31ec' class='xr-var-data-in' type='checkbox'><label for='data-0feb8557-e3db-474f-9564-19c7a68e31ec' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_centroid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-84744148-5292-4a8d-b59a-13b650423515' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-84744148-5292-4a8d-b59a-13b650423515' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8098b749-dc53-4228-b7c2-7efe759ca79b' class='xr-var-data-in' type='checkbox'><label for='data-8098b749-dc53-4228-b7c2-7efe759ca79b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_histogram</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-b2eaa828-6b83-4a2a-bb85-9cc55691e1a5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b2eaa828-6b83-4a2a-bb85-9cc55691e1a5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1e4023df-dbe3-46ee-8d0c-c3f9194cec0f' class='xr-var-data-in' type='checkbox'><label for='data-1e4023df-dbe3-46ee-8d0c-c3f9194cec0f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_profiles</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-f6266f99-189a-47af-91bf-a589c8de3f40' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f6266f99-189a-47af-91bf-a589c8de3f40' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-66adf453-8700-4067-ba1a-9532f7239771' class='xr-var-data-in' type='checkbox'><label for='data-66adf453-8700-4067-ba1a-9532f7239771' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_statistics</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-769e6632-8e75-4e08-a0cd-e55720110db1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-769e6632-8e75-4e08-a0cd-e55720110db1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b2a25ff9-824e-42a9-b263-e68414dc4efc' class='xr-var-data-in' type='checkbox'><label for='data-b2a25ff9-824e-42a9-b263-e68414dc4efc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-5dbe101a-7653-44f0-87d5-432dc7a41916' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5dbe101a-7653-44f0-87d5-432dc7a41916' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8f96ba14-fea8-46c8-983b-8e32a0d10270' class='xr-var-data-in' type='checkbox'><label for='data-8f96ba14-fea8-46c8-983b-8e32a0d10270' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_min</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-aedf3b56-6769-4ec6-b562-ce3b84c05b2a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-aedf3b56-6769-4ec6-b562-ce3b84c05b2a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b27de8c2-b34e-4e21-bff9-1517d5c24390' class='xr-var-data-in' type='checkbox'><label for='data-b27de8c2-b34e-4e21-bff9-1517d5c24390' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>256</div><input id='attrs-406041e2-73d1-4207-82aa-ce78696f6f0f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-406041e2-73d1-4207-82aa-ce78696f6f0f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8ecf2ea8-82bc-46b7-b951-8d37dfaa1296' class='xr-var-data-in' type='checkbox'><label for='data-8ecf2ea8-82bc-46b7-b951-8d37dfaa1296' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([256])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_ts_num_points</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2048</div><input id='attrs-f27394fb-09a2-429e-8dcc-44a45abd48f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f27394fb-09a2-429e-8dcc-44a45abd48f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c7796a9d-b15f-4f4d-a83c-87984a0087d3' class='xr-var-data-in' type='checkbox'><label for='data-c7796a9d-b15f-4f4d-a83c-87984a0087d3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2048])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_roi1_configuration_names&#x27; ....</div><input id='attrs-bd2a2862-4cd4-4256-8897-db1aafb498a6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bd2a2862-4cd4-4256-8897-db1aafb498a6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-02afe6d4-cfa6-44f8-b1d7-2a07556abf38' class='xr-var-data-in' type='checkbox'><label for='data-02afe6d4-cfa6-44f8-b1d7-2a07556abf38' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_roi1_configuration_names&#x27;, &#x27;pe1_roi1_port_name&#x27;,
            &#x27;pe1_roi1_asyn_pipeline_config&#x27;, &#x27;pe1_roi1_blocking_callbacks&#x27;,
            &#x27;pe1_roi1_enable&#x27;, &#x27;pe1_roi1_nd_array_port&#x27;,
            &#x27;pe1_roi1_plugin_type&#x27;, &#x27;pe1_roi1_bin_&#x27;,
            &#x27;pe1_roi1_data_type_out&#x27;, &#x27;pe1_roi1_enable_scale&#x27;,
            &#x27;pe1_roi1_roi_enable&#x27;, &#x27;pe1_roi1_min_xyz&#x27;, &#x27;pe1_roi1_name_&#x27;,
            &#x27;pe1_roi1_size&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-baeff5ec-29b4-4b5a-b01d-420cd4ba4d62' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-baeff5ec-29b4-4b5a-b01d-420cd4ba4d62' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d43d1166-59f3-4a69-8698-413669113cc0' class='xr-var-data-in' type='checkbox'><label for='data-d43d1166-59f3-4a69-8698-413669113cc0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-cf03a36d-73d7-4280-af42-caf954583f79' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cf03a36d-73d7-4280-af42-caf954583f79' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fdeb0dcf-4dee-4bc3-8a57-9b46f05ade1e' class='xr-var-data-in' type='checkbox'><label for='data-fdeb0dcf-4dee-4bc3-8a57-9b46f05ade1e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-dd9aeb0a-bb49-499a-bec9-fcf08168f26d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dd9aeb0a-bb49-499a-bec9-fcf08168f26d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-61c930f9-a6b8-42ed-971c-21ad082db2ae' class='xr-var-data-in' type='checkbox'><label for='data-61c930f9-a6b8-42ed-971c-21ad082db2ae' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-3b4c3fe2-701a-45de-8fe8-8d9cd0a1d459' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3b4c3fe2-701a-45de-8fe8-8d9cd0a1d459' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f5bccac1-dcbb-41e0-a679-f5ed76c02253' class='xr-var-data-in' type='checkbox'><label for='data-f5bccac1-dcbb-41e0-a679-f5ed76c02253' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-f2924046-417e-4105-b34b-cba0dbaa9e68' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f2924046-417e-4105-b34b-cba0dbaa9e68' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ee07ad9d-c733-4a82-9419-cb0c2ba05a9a' class='xr-var-data-in' type='checkbox'><label for='data-ee07ad9d-c733-4a82-9419-cb0c2ba05a9a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U11</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginROI&#x27;</div><input id='attrs-82309aac-d04a-4f29-9e4c-fa6a685a5ba3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-82309aac-d04a-4f29-9e4c-fa6a685a5ba3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-54265c8d-95c4-45ab-b76e-2a83d81830d6' class='xr-var-data-in' type='checkbox'><label for='data-54265c8d-95c4-45ab-b76e-2a83d81830d6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginROI&#x27;], dtype=&#x27;&lt;U11&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-2dc94965-88d9-4f14-a28f-04731651ebb8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2dc94965-88d9-4f14-a28f-04731651ebb8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6d9cde7f-d090-46ff-813e-8443b7603135' class='xr-var-data-in' type='checkbox'><label for='data-6d9cde7f-d090-46ff-813e-8443b7603135' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-16bd7fda-0cad-4003-b52e-ad61ae6e007c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-16bd7fda-0cad-4003-b52e-ad61ae6e007c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4ff2ac1d-44c9-4560-a988-29d56b506023' class='xr-var-data-in' type='checkbox'><label for='data-4ff2ac1d-44c9-4560-a988-29d56b506023' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_name_</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U1</div><div class='xr-var-preview xr-preview'>&#x27;&#x27;</div><input id='attrs-27aa22c7-7f36-447e-8458-fe57fcf85765' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-27aa22c7-7f36-447e-8458-fe57fcf85765' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-72d7f7bc-8e58-4f5d-b9e1-85ff595b30a2' class='xr-var-data-in' type='checkbox'><label for='data-72d7f7bc-8e58-4f5d-b9e1-85ff595b30a2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;&#x27;], dtype=&#x27;&lt;U1&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-4177748b-e6b9-4e12-8002-818ce8d09c02' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4177748b-e6b9-4e12-8002-818ce8d09c02' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-59284e90-871f-4749-b67e-25d8a50e06cf' class='xr-var-data-in' type='checkbox'><label for='data-59284e90-871f-4749-b67e-25d8a50e06cf' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;ad3b7a7f-6564-4157-933f-c3bae9e...</div><input id='attrs-adcf7a0f-25ca-408e-a9ad-09e2d7faaa99' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-adcf7a0f-25ca-408e-a9ad-09e2d7faaa99' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1c46f660-597f-4d50-b378-4253cd57ed6a' class='xr-var-data-in' type='checkbox'><label for='data-1c46f660-597f-4d50-b378-4253cd57ed6a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ad3b7a7f-6564-4157-933f-c3bae9e9e876&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-1cd9bd33-cc3b-43ef-aeac-2a61c2d77c11' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-1cd9bd33-cc3b-43ef-aeac-2a61c2d77c11' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

The data is processed by the analyzer is the diffraction image.


.. code-block:: default


    import matplotlib.pyplot as plt

    image = raw_data["pe1_image"]
    image.plot(vmin=0, vmax=image.mean() + 2. * image.std())
    plt.show()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_001.png
    :alt: time = 1581814176.5086372
    :class: sphx-glr-single-img





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
    Dimensions:       (dim_0: 2048, dim_1: 2048, dim_10: 692, dim_11: 692, dim_12: 692, dim_13: 692, dim_14: 3001, dim_15: 3001, dim_2: 2048, dim_3: 2048, dim_4: 2048, dim_5: 2048, dim_6: 1024, dim_7: 1024, dim_8: 755, dim_9: 755, time: 1)
    Coordinates:
      * time          (time) float64 1.607e+09
    Dimensions without coordinates: dim_0, dim_1, dim_10, dim_11, dim_12, dim_13, dim_14, dim_15, dim_2, dim_3, dim_4, dim_5, dim_6, dim_7, dim_8, dim_9
    Data variables:
        dk_sub_image  (time, dim_0, dim_1) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        bg_sub_image  (time, dim_2, dim_3) uint16 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0
        mask          (time, dim_4, dim_5) int64 1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1
        chi_Q         (time, dim_6) float64 0.0253 0.05714 0.08897 ... 32.56 32.59
        chi_I         (time, dim_7) float32 17.449076 15.25509 17.243057 ... 0.0 0.0
        chi_max       (time) float32 21331.768
        chi_argmax    (time) float64 3.081
        iq_Q          (time, dim_8) float64 0.0 0.03183 0.06366 ... 23.94 23.97 24.0
        iq_I          (time, dim_9) float64 17.45 17.0 15.66 ... 74.84 74.1 73.68
        sq_Q          (time, dim_10) float64 0.0 0.03183 0.06366 ... 21.96 21.99
        sq_S          (time, dim_11) float64 1.441 1.42 1.399 ... 1.019 1.014 0.9995
        fq_Q          (time, dim_12) float64 0.0 0.03183 0.06366 ... 21.96 21.99
        fq_F          (time, dim_13) float64 0.0 0.01336 0.0254 ... 0.3035 -0.01125
        gr_r          (time, dim_14) float64 0.0 0.01 0.02 0.03 ... 29.98 29.99 30.0
        gr_G          (time, dim_15) float64 0.0 0.003567 0.006975 ... 1.4 1.455
        gr_max        (time) float64 7.417
        gr_argmax     (time) float64 6.59
        seq_num       (time) int64 1
        uid           (time) &lt;U36 &#x27;4be28b0c-e766-4ca6-b497-7400ab3100c0&#x27;</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-706fb62d-0d8a-4668-9680-a0a59fe7b12a' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-706fb62d-0d8a-4668-9680-a0a59fe7b12a' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 2048</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 692</li><li><span>dim_11</span>: 692</li><li><span>dim_12</span>: 692</li><li><span>dim_13</span>: 692</li><li><span>dim_14</span>: 3001</li><li><span>dim_15</span>: 3001</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 2048</li><li><span>dim_4</span>: 2048</li><li><span>dim_5</span>: 2048</li><li><span>dim_6</span>: 1024</li><li><span>dim_7</span>: 1024</li><li><span>dim_8</span>: 755</li><li><span>dim_9</span>: 755</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-0ccea316-12a3-4c45-9f3d-2ae1cfda8c08' class='xr-section-summary-in' type='checkbox'  checked><label for='section-0ccea316-12a3-4c45-9f3d-2ae1cfda8c08' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.607e+09</div><input id='attrs-c31c6c63-6f82-4c90-a317-0edd375d75f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c31c6c63-6f82-4c90-a317-0edd375d75f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ad9c83a1-ac75-4e1e-ae40-db7802fc5160' class='xr-var-data-in' type='checkbox'><label for='data-ad9c83a1-ac75-4e1e-ae40-db7802fc5160' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.607451e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-ef588a19-0117-4798-98ee-a9498fa56a6a' class='xr-section-summary-in' type='checkbox'  ><label for='section-ef588a19-0117-4798-98ee-a9498fa56a6a' class='xr-section-summary' >Data variables: <span>(19)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>dk_sub_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-f682af1b-88c7-40cb-baa0-e82d3de4b7ec' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f682af1b-88c7-40cb-baa0-e82d3de4b7ec' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5ac3c05b-aaef-4b0f-94ad-7a1991aca059' class='xr-var-data-in' type='checkbox'><label for='data-5ac3c05b-aaef-4b0f-94ad-7a1991aca059' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>bg_sub_image</span></div><div class='xr-var-dims'>(time, dim_2, dim_3)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-0f595b70-14c0-4bb7-add1-bd124f110e1c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0f595b70-14c0-4bb7-add1-bd124f110e1c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a22b98f1-c364-4bb8-8a05-f4b9c4afbf40' class='xr-var-data-in' type='checkbox'><label for='data-a22b98f1-c364-4bb8-8a05-f4b9c4afbf40' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>mask</span></div><div class='xr-var-dims'>(time, dim_4, dim_5)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1</div><input id='attrs-03ea5fcc-b415-499d-b5b5-9c5ad8786534' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-03ea5fcc-b415-499d-b5b5-9c5ad8786534' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4b74b102-2189-403c-a4ac-c29a3f06bb50' class='xr-var-data-in' type='checkbox'><label for='data-4b74b102-2189-403c-a4ac-c29a3f06bb50' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            ...,
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1]]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_Q</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0253 0.05714 ... 32.56 32.59</div><input id='attrs-8e79b9f6-743f-4dc0-91c2-f42da5503069' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8e79b9f6-743f-4dc0-91c2-f42da5503069' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a6baf3bd-20c6-4c04-8b3b-99bea10252e5' class='xr-var-data-in' type='checkbox'><label for='data-a6baf3bd-20c6-4c04-8b3b-99bea10252e5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[2.53048628e-02, 5.71350587e-02, 8.89652545e-02, ...,
            3.25239349e+01, 3.25557651e+01, 3.25875953e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_I</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>17.449076 15.25509 ... 0.0 0.0</div><input id='attrs-0c934adf-e4db-4351-853e-f13c8c8d3193' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0c934adf-e4db-4351-853e-f13c8c8d3193' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a6224aea-bc28-4969-a724-a40e22a133dc' class='xr-var-data-in' type='checkbox'><label for='data-a6224aea-bc28-4969-a724-a40e22a133dc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[17.449076, 15.25509 , 17.243057, ...,  0.      ,  0.      ,
             0.      ]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>21331.768</div><input id='attrs-0521e6ff-35d7-499c-abaa-72954875bf51' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0521e6ff-35d7-499c-abaa-72954875bf51' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e1503260-299c-409d-8fe7-d2bcf43b5cd9' class='xr-var-data-in' type='checkbox'><label for='data-e1503260-299c-409d-8fe7-d2bcf43b5cd9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([21331.768], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>3.081</div><input id='attrs-cc99047a-3d43-4847-8cc8-e72cdbf06c66' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cc99047a-3d43-4847-8cc8-e72cdbf06c66' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7e3c7d35-8e7f-4cb8-9137-8010d167c9c6' class='xr-var-data-in' type='checkbox'><label for='data-7e3c7d35-8e7f-4cb8-9137-8010d167c9c6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([3.08100367])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_Q</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 23.97 24.0</div><input id='attrs-ba7246f5-387a-4cc9-bf0e-7bf0fc79cf68' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ba7246f5-387a-4cc9-bf0e-7bf0fc79cf68' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-75505bf2-5a60-4a1d-aeb2-bf5feb6e0b26' class='xr-var-data-in' type='checkbox'><label for='data-75505bf2-5a60-4a1d-aeb2-bf5feb6e0b26' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536, 22.02649556, 22.05832575, 22.09015595,
            22.12198614, 22.15381634, 22.18564654, 22.21747673, 22.24930693,
            22.28113712, 22.31296732, 22.34479751, 22.37662771, 22.40845791,
            22.4402881 , 22.4721183 , 22.50394849, 22.53577869, 22.56760889,
            22.59943908, 22.63126928, 22.66309947, 22.69492967, 22.72675987,
            22.75859006, 22.79042026, 22.82225045, 22.85408065, 22.88591085,
            22.91774104, 22.94957124, 22.98140143, 23.01323163, 23.04506182,
            23.07689202, 23.10872222, 23.14055241, 23.17238261, 23.2042128 ,
            23.236043  , 23.2678732 , 23.29970339, 23.33153359, 23.36336378,
            23.39519398, 23.42702418, 23.45885437, 23.49068457, 23.52251476,
            23.55434496, 23.58617515, 23.61800535, 23.64983555, 23.68166574,
            23.71349594, 23.74532613, 23.77715633, 23.80898653, 23.84081672,
            23.87264692, 23.90447711, 23.93630731, 23.96813751, 23.9999677 ]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_I</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>17.45 17.0 15.66 ... 74.1 73.68</div><input id='attrs-e35bd393-5893-48dc-a8e6-920be6898000' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e35bd393-5893-48dc-a8e6-920be6898000' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f3006bdf-1763-40de-876c-98dd504d0bc2' class='xr-var-data-in' type='checkbox'><label for='data-f3006bdf-1763-40de-876c-98dd504d0bc2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.74490757e+01, 1.69992987e+01, 1.56626320e+01, 1.74703867e+01,
            1.82314899e+01, 1.77723650e+01, 1.79923798e+01, 1.86504720e+01,
            1.86278119e+01, 2.02567210e+01, 2.41870058e+01, 3.32590795e+01,
            4.91376314e+01, 7.30356792e+01, 9.84936908e+01, 1.18458734e+02,
            1.37275093e+02, 1.60926731e+02, 1.87243910e+02, 2.09734490e+02,
            2.20428456e+02, 2.29835892e+02, 2.37006081e+02, 2.43149251e+02,
            2.48993769e+02, 2.55153101e+02, 2.59127294e+02, 2.64476241e+02,
            2.68652539e+02, 2.72060140e+02, 2.76712961e+02, 2.82302800e+02,
            2.87209671e+02, 2.93951986e+02, 3.00859860e+02, 3.08066882e+02,
            3.16258739e+02, 3.23977231e+02, 3.30552314e+02, 3.38680625e+02,
            3.46476725e+02, 3.54501546e+02, 3.59268364e+02, 3.55397755e+02,
            3.46637764e+02, 3.36138057e+02, 3.25597659e+02, 3.16246679e+02,
            3.06201998e+02, 2.95923148e+02, 2.87079741e+02, 2.80166792e+02,
            2.74960669e+02, 2.71866420e+02, 2.69234512e+02, 2.67884610e+02,
            2.66130365e+02, 2.64776255e+02, 2.63726726e+02, 2.62212858e+02,
            2.58381261e+02, 2.53875055e+02, 2.49515595e+02, 2.44848096e+02,
            2.40525781e+02, 2.37253478e+02, 2.34127167e+02, 2.31202783e+02,
            2.28390219e+02, 2.26667417e+02, 2.25341003e+02, 2.23721918e+02,
            2.22190254e+02, 2.21914465e+02, 2.22466176e+02, 2.24527675e+02,
            2.27023414e+02, 2.29708290e+02, 2.32981781e+02, 2.36155545e+02,
    ...
            9.74582451e+01, 9.95953449e+01, 1.00558303e+02, 9.95161601e+01,
            9.74455144e+01, 9.52782035e+01, 9.36979739e+01, 9.26285455e+01,
            9.20636392e+01, 9.18108913e+01, 9.24163763e+01, 9.38463873e+01,
            9.56380139e+01, 9.68500311e+01, 9.57089248e+01, 9.31999562e+01,
            9.17490841e+01, 9.17065724e+01, 9.32667132e+01, 9.55807180e+01,
            9.62349107e+01, 9.39821180e+01, 9.08120928e+01, 8.85367548e+01,
            8.75534450e+01, 8.69651889e+01, 8.66846185e+01, 8.63809746e+01,
            8.63784877e+01, 8.64525122e+01, 8.66992378e+01, 8.66280788e+01,
            8.62216662e+01, 8.54948699e+01, 8.53092902e+01, 8.53419303e+01,
            8.59511670e+01, 8.72290927e+01, 8.85321548e+01, 8.94252400e+01,
            8.90326335e+01, 8.71715986e+01, 8.48951726e+01, 8.34520534e+01,
            8.28345377e+01, 8.26872545e+01, 8.29400187e+01, 8.35994634e+01,
            8.39557361e+01, 8.36291483e+01, 8.25534566e+01, 8.20855279e+01,
            8.26846879e+01, 8.38482739e+01, 8.53235981e+01, 8.55899325e+01,
            8.41952229e+01, 8.20712543e+01, 8.03228259e+01, 7.93475595e+01,
            7.86968165e+01, 7.81825859e+01, 7.78836842e+01, 7.80504384e+01,
            7.81602998e+01, 7.78745627e+01, 7.75449953e+01, 7.73764532e+01,
            7.73500989e+01, 7.77641318e+01, 7.88876575e+01, 8.01621440e+01,
            8.06063787e+01, 7.95783767e+01, 7.80683545e+01, 7.64007970e+01,
            7.48447155e+01, 7.40994861e+01, 7.36818762e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_Q</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-eecf92ea-d7cb-45cf-a273-612f8e1ba8a9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-eecf92ea-d7cb-45cf-a273-612f8e1ba8a9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4a98d37e-13e3-4892-9c39-4fb6db04b475' class='xr-var-data-in' type='checkbox'><label for='data-4a98d37e-13e3-4892-9c39-4fb6db04b475' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            18.93896655, 18.97079675, 19.00262695, 19.03445714, 19.06628734,
            19.09811753, 19.12994773, 19.16177793, 19.19360812, 19.22543832,
            19.25726851, 19.28909871, 19.32092891, 19.3527591 , 19.3845893 ,
            19.41641949, 19.44824969, 19.48007988, 19.51191008, 19.54374028,
            19.57557047, 19.60740067, 19.63923086, 19.67106106, 19.70289126,
            19.73472145, 19.76655165, 19.79838184, 19.83021204, 19.86204224,
            19.89387243, 19.92570263, 19.95753282, 19.98936302, 20.02119321,
            20.05302341, 20.08485361, 20.1166838 , 20.148514  , 20.18034419,
            20.21217439, 20.24400459, 20.27583478, 20.30766498, 20.33949517,
            20.37132537, 20.40315557, 20.43498576, 20.46681596, 20.49864615,
            20.53047635, 20.56230655, 20.59413674, 20.62596694, 20.65779713,
            20.68962733, 20.72145752, 20.75328772, 20.78511792, 20.81694811,
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_S</span></div><div class='xr-var-dims'>(time, dim_11)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.441 1.42 1.399 ... 1.014 0.9995</div><input id='attrs-891d628f-8d3f-4bcc-ab41-899c8b0888de' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-891d628f-8d3f-4bcc-ab41-899c8b0888de' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2b3d1830-b2c4-4a26-98bf-bb91ab99ea93' class='xr-var-data-in' type='checkbox'><label for='data-2b3d1830-b2c4-4a26-98bf-bb91ab99ea93' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.44081866, 1.41981957, 1.39906439, 1.37918811, 1.35951973,
            1.34002596, 1.32100367, 1.30240962, 1.28405999, 1.26632305,
            1.24929995, 1.23344626, 1.2190332 , 1.20626319, 1.19409556,
            1.18138043, 1.16881716, 1.15738424, 1.14673059, 1.13578413,
            1.12320851, 1.11073121, 1.09818604, 1.08576812, 1.07359461,
            1.0617655 , 1.04984921, 1.03844949, 1.02712475, 1.01593813,
            1.00523673, 0.99496631, 0.98483846, 0.97529748, 0.96604566,
            0.95710431, 0.94859614, 0.94025376, 0.93194827, 0.92417391,
            0.91658006, 0.90926811, 0.90157293, 0.89244777, 0.88257606,
            0.87254518, 0.86267617, 0.85320734, 0.84376577, 0.83443641,
            0.82555113, 0.81721333, 0.80938256, 0.80214693, 0.79517008,
            0.78862283, 0.78215207, 0.77592404, 0.76991721, 0.76396392,
            0.75765499, 0.75133653, 0.74518394, 0.73909356, 0.7332078 ,
            0.72768543, 0.72232276, 0.71713077, 0.71208699, 0.7074183 ,
            0.70296468, 0.69856206, 0.69429746, 0.69045133, 0.68692431,
            0.68388661, 0.6810788 , 0.67844031, 0.67607082, 0.67379743,
            0.6716424 , 0.66968651, 0.66804367, 0.66669048, 0.66559618,
            0.66467602, 0.66406079, 0.66372731, 0.66415789, 0.66613362,
            0.67066807, 0.6802721 , 0.70308678, 0.77184812, 1.03740991,
            2.04527338, 4.48513999, 6.63947769, 5.20172815, 2.35408837,
    ...
            0.95604705, 0.9608355 , 0.97390518, 1.00217805, 1.04258786,
            1.07878673, 1.09810373, 1.1034093 , 1.0816646 , 1.03393221,
            0.98897848, 0.96868041, 0.96270436, 0.960861  , 0.96240767,
            0.97294368, 0.99394702, 1.01700675, 1.02282207, 1.00223255,
            0.97631878, 0.96403137, 0.96488497, 0.97781867, 0.99977995,
            1.01749416, 1.01058087, 0.98596325, 0.96634679, 0.95838788,
            0.95555419, 0.95408012, 0.95406125, 0.9546458 , 0.95779567,
            0.96062807, 0.96592607, 0.97321322, 0.97653979, 0.97596385,
            0.97378001, 0.9781229 , 0.99511825, 1.03065644, 1.08220202,
            1.11863088, 1.1127029 , 1.07823281, 1.04348347, 1.0134038 ,
            0.99134974, 0.98292983, 0.98073362, 0.98122166, 0.98529243,
            0.99812924, 1.01400698, 1.02347691, 1.01567839, 0.99909043,
            0.99000914, 0.99295082, 1.00671051, 1.03091632, 1.05208522,
            1.05712293, 1.04544024, 1.02847238, 1.00801862, 0.9911789 ,
            0.9822223 , 0.97927628, 0.97952865, 0.98164694, 0.98755204,
            0.9943492 , 0.99752411, 0.99207041, 0.98411696, 0.9815523 ,
            0.98510601, 0.99546581, 1.01092193, 1.01909779, 1.01467583,
            1.00370828, 0.99204683, 0.98404261, 0.9792457 , 0.97764904,
            0.97804693, 0.98398864, 0.99531282, 1.00906291, 1.01911829,
            1.01382084, 0.99948833]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_Q</span></div><div class='xr-var-dims'>(time, dim_12)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-7aad8b60-5f23-4bed-aeb8-f2e9ba527b0c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7aad8b60-5f23-4bed-aeb8-f2e9ba527b0c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5cc446af-ec02-4413-a8c3-777d64658d40' class='xr-var-data-in' type='checkbox'><label for='data-5cc446af-ec02-4413-a8c3-777d64658d40' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
             0.15915098,  0.19098118,  0.22281137,  0.25464157,  0.28647176,
             0.31830196,  0.35013215,  0.38196235,  0.41379255,  0.44562274,
             0.47745294,  0.50928313,  0.54111333,  0.57294353,  0.60477372,
             0.63660392,  0.66843411,  0.70026431,  0.73209451,  0.7639247 ,
             0.7957549 ,  0.82758509,  0.85941529,  0.89124548,  0.92307568,
             0.95490588,  0.98673607,  1.01856627,  1.05039646,  1.08222666,
             1.11405686,  1.14588705,  1.17771725,  1.20954744,  1.24137764,
             1.27320784,  1.30503803,  1.33686823,  1.36869842,  1.40052862,
             1.43235882,  1.46418901,  1.49601921,  1.5278494 ,  1.5596796 ,
             1.59150979,  1.62333999,  1.65517019,  1.68700038,  1.71883058,
             1.75066077,  1.78249097,  1.81432117,  1.84615136,  1.87798156,
             1.90981175,  1.94164195,  1.97347215,  2.00530234,  2.03713254,
             2.06896273,  2.10079293,  2.13262312,  2.16445332,  2.19628352,
             2.22811371,  2.25994391,  2.2917741 ,  2.3236043 ,  2.3554345 ,
             2.38726469,  2.41909489,  2.45092508,  2.48275528,  2.51458548,
             2.54641567,  2.57824587,  2.61007606,  2.64190626,  2.67373645,
             2.70556665,  2.73739685,  2.76922704,  2.80105724,  2.83288743,
             2.86471763,  2.89654783,  2.92837802,  2.96020822,  2.99203841,
             3.02386861,  3.05569881,  3.087529  ,  3.1193592 ,  3.15118939,
    ...
            18.93896655, 18.97079675, 19.00262695, 19.03445714, 19.06628734,
            19.09811753, 19.12994773, 19.16177793, 19.19360812, 19.22543832,
            19.25726851, 19.28909871, 19.32092891, 19.3527591 , 19.3845893 ,
            19.41641949, 19.44824969, 19.48007988, 19.51191008, 19.54374028,
            19.57557047, 19.60740067, 19.63923086, 19.67106106, 19.70289126,
            19.73472145, 19.76655165, 19.79838184, 19.83021204, 19.86204224,
            19.89387243, 19.92570263, 19.95753282, 19.98936302, 20.02119321,
            20.05302341, 20.08485361, 20.1166838 , 20.148514  , 20.18034419,
            20.21217439, 20.24400459, 20.27583478, 20.30766498, 20.33949517,
            20.37132537, 20.40315557, 20.43498576, 20.46681596, 20.49864615,
            20.53047635, 20.56230655, 20.59413674, 20.62596694, 20.65779713,
            20.68962733, 20.72145752, 20.75328772, 20.78511792, 20.81694811,
            20.84877831, 20.8806085 , 20.9124387 , 20.9442689 , 20.97609909,
            21.00792929, 21.03975948, 21.07158968, 21.10341988, 21.13525007,
            21.16708027, 21.19891046, 21.23074066, 21.26257085, 21.29440105,
            21.32623125, 21.35806144, 21.38989164, 21.42172183, 21.45355203,
            21.48538223, 21.51721242, 21.54904262, 21.58087281, 21.61270301,
            21.64453321, 21.6763634 , 21.7081936 , 21.74002379, 21.77185399,
            21.80368418, 21.83551438, 21.86734458, 21.89917477, 21.93100497,
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_F</span></div><div class='xr-var-dims'>(time, dim_13)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01336 ... 0.3035 -0.01125</div><input id='attrs-559b3bf8-cd6a-4b61-ab35-1b421cc4b3b5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-559b3bf8-cd6a-4b61-ab35-1b421cc4b3b5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3cdd578f-69e6-4914-8d26-b6e36542ab68' class='xr-var-data-in' type='checkbox'><label for='data-3cdd578f-69e6-4914-8d26-b6e36542ab68' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.00000000e+00,  1.33629391e-02,  2.54045954e-02,
             3.62088950e-02,  4.57743343e-02,  5.41154638e-02,
             6.13056589e-02,  6.73803015e-02,  7.23334823e-02,
             7.62940329e-02,  7.93526608e-02,  8.17370412e-02,
             8.36624360e-02,  8.53501688e-02,  8.64933963e-02,
             8.66006176e-02,  8.59757348e-02,  8.51627097e-02,
             8.40683431e-02,  8.21186759e-02,  7.84350187e-02,
             7.40165180e-02,  6.87561784e-02,  6.27903716e-02,
             5.62207429e-02,  4.91502014e-02,  4.12544627e-02,
             3.30440770e-02,  2.41748150e-02,  1.47120962e-02,
             5.00058434e-03, -4.96692403e-03, -1.54430380e-02,
            -2.59474382e-02, -3.67462968e-02, -4.77882392e-02,
            -5.89030154e-02, -7.03641739e-02, -8.23117904e-02,
            -9.41288150e-02, -1.06210922e-01, -1.18408565e-01,
            -1.31584024e-01, -1.47206571e-01, -1.64455595e-01,
            -1.82561031e-01, -2.01068042e-01, -2.19604632e-01,
            -2.38702380e-01, -2.58226155e-01, -2.77637090e-01,
            -2.96724903e-01, -3.15504311e-01, -3.33778201e-01,
            -3.52067924e-01, -3.70049715e-01, -3.88311959e-01,
            -4.06545757e-01, -4.24767648e-01, -4.43271399e-01,
    ...
            -4.72688425e-01, -4.85057684e-01, -5.29962934e-01,
            -4.42880122e-01, -9.89815414e-02,  6.22560762e-01,
             1.67194749e+00,  2.41666826e+00,  2.29949473e+00,
             1.59868632e+00,  8.89968226e-01,  2.74759667e-01,
            -1.77593889e-01, -3.51001991e-01, -3.96774531e-01,
            -3.87321521e-01, -3.03825923e-01, -3.87052387e-02,
             2.90244954e-01,  4.87223120e-01,  3.25877140e-01,
            -1.89344236e-02, -2.08297292e-01, -1.47191084e-01,
             1.40333078e-01,  6.47519697e-01,  1.09254479e+00,
             1.20003453e+00,  9.56051825e-01,  5.99958380e-01,
             1.69220264e-01, -1.86436116e-01, -3.76302033e-01,
            -4.39320237e-01, -4.34621895e-01, -3.90233279e-01,
            -2.65071758e-01, -1.20510201e-01, -5.28801902e-02,
            -1.69613113e-01, -3.40242116e-01, -3.95768588e-01,
            -3.20003121e-01, -9.75630791e-02,  2.35357129e-01,
             4.12146918e-01,  3.17184350e-01,  8.02640466e-02,
            -1.72395852e-01, -3.46406194e-01, -4.51198969e-01,
            -4.86621825e-01, -4.78657784e-01, -3.49616217e-01,
            -1.02496196e-01,  1.98470188e-01,  4.19283288e-01,
             3.03544788e-01, -1.12540794e-02]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_r</span></div><div class='xr-var-dims'>(time, dim_14)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01 0.02 ... 29.98 29.99 30.0</div><input id='attrs-5fd8b17d-eb1d-4101-b560-a31655494534' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5fd8b17d-eb1d-4101-b560-a31655494534' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9b3e2cee-b4ef-4a0b-af83-50204407859c' class='xr-var-data-in' type='checkbox'><label for='data-9b3e2cee-b4ef-4a0b-af83-50204407859c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.000e+00, 1.000e-02, 2.000e-02, ..., 2.998e+01, 2.999e+01,
            3.000e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_G</span></div><div class='xr-var-dims'>(time, dim_15)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.003567 0.006975 ... 1.4 1.455</div><input id='attrs-5475c1d5-73c2-4421-80e9-472382e009c0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5475c1d5-73c2-4421-80e9-472382e009c0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-230c4fb9-1ace-4b70-aeb5-5869e0e7e93c' class='xr-var-data-in' type='checkbox'><label for='data-230c4fb9-1ace-4b70-aeb5-5869e0e7e93c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.        , 0.0035669 , 0.00697492, ..., 1.33294076, 1.39995837,
            1.45483018]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>7.417</div><input id='attrs-8c677603-7688-440a-80ba-f7ceb60308c7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8c677603-7688-440a-80ba-f7ceb60308c7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e58c0c73-2333-4094-a028-ce11a760a793' class='xr-var-data-in' type='checkbox'><label for='data-e58c0c73-2333-4094-a028-ce11a760a793' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([7.41703315])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>6.59</div><input id='attrs-f0ba7025-4665-4e9d-bcbd-5c6ddec5d8c8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f0ba7025-4665-4e9d-bcbd-5c6ddec5d8c8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-78aa4b36-7eee-4de5-9420-cfce32e3c162' class='xr-var-data-in' type='checkbox'><label for='data-78aa4b36-7eee-4de5-9420-cfce32e3c162' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([6.59])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-db718363-7e41-4518-8e60-2e62faa5132d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-db718363-7e41-4518-8e60-2e62faa5132d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-190bffe0-a2ab-47e4-aea8-c42b574075dc' class='xr-var-data-in' type='checkbox'><label for='data-190bffe0-a2ab-47e4-aea8-c42b574075dc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;4be28b0c-e766-4ca6-b497-7400ab3...</div><input id='attrs-fc87ec70-4149-424b-8518-5e523ba2f566' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fc87ec70-4149-424b-8518-5e523ba2f566' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0a68fe8f-97d2-4aa5-8ba6-088c63f167c0' class='xr-var-data-in' type='checkbox'><label for='data-0a68fe8f-97d2-4aa5-8ba6-088c63f167c0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;4be28b0c-e766-4ca6-b497-7400ab3100c0&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-991e2cba-9fe5-4374-9b4a-7ec70000b16d' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-991e2cba-9fe5-4374-9b4a-7ec70000b16d' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
    <br />
    <br />

We plot the some of the important data to give a sense of what the processed data looks like.
First, we plot the masked dark subtracted image.


.. code-block:: default


    import numpy as np

    image2 = np.ma.masked_array(an_data["dk_sub_image"], an_data["mask"])
    image2 = np.ma.squeeze(image2)
    plt.matshow(image2, vmin=0., vmax=image2.mean() + 2. * image2.std())
    plt.colorbar()
    plt.show()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_002.png
    :alt: plot xpd analyzer
    :class: sphx-glr-single-img





Second, we show the XRD data obtained from the dark subtracted image above.


.. code-block:: default


    chi = np.stack((an_data["chi_Q"], an_data["chi_I"])).squeeze()
    plt.plot(*chi)
    plt.show()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_003.png
    :alt: plot xpd analyzer
    :class: sphx-glr-single-img





Finally, it is the PDF data transferred from XRD data.


.. code-block:: default


    gr = np.stack((an_data["gr_r"], an_data["gr_G"])).squeeze()
    plt.plot(*gr)
    plt.show()




.. image:: /tutorials2/images/sphx_glr_plot_xpd_analyzer_004.png
    :alt: plot xpd analyzer
    :class: sphx-glr-single-img





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
You don't need to create another analyzer if you tune the configuration other than "BASIC" and "FUNCTIONALITY".

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

If you would like see the figures of processed data at the same time of data processing
, run the code below to turn on the functionality.


.. code-block:: default


    config["FUNCTIONALITY"]["visualize_data"] = "True"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The detail of what the figures will be like is introduced in :ref:`xpd-server-figures`.

Send to a server
^^^^^^^^^^^^^^^^

We can even send the streaming processed data to a server in an internal network.
To make it, we need to turn the functionality on.


.. code-block:: default


    config["FUNCTIONALITY"]["send_messages"] = "True"








Then, we need to build the analyzer again ``analyzer = XPDAnalyzer(config)`` to make the functionality
take effect and rerun the analysis ``analyzer.analyze(run)``.
The server specified in the configuration will receive message from our analyzer.

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

   **Total running time of the script:** ( 0 minutes  10.693 seconds)


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
