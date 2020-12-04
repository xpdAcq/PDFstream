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
        uid                                  (time) &lt;U36 &#x27;ad3b7a7f-6564-4157-933f...</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-7f165d7e-e4af-4bea-a060-837502bfd163' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-7f165d7e-e4af-4bea-a060-837502bfd163' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 1</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 2</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 17</li><li><span>dim_4</span>: 3</li><li><span>dim_5</span>: 40</li><li><span>dim_6</span>: 2</li><li><span>dim_7</span>: 19</li><li><span>dim_8</span>: 3</li><li><span>dim_9</span>: 14</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-1b66aa79-bbed-47e3-8eaa-761475422a35' class='xr-section-summary-in' type='checkbox'  checked><label for='section-1b66aa79-bbed-47e3-8eaa-761475422a35' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.582e+09</div><input id='attrs-a8d34942-bad9-408d-9ed5-23e3b066c47f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a8d34942-bad9-408d-9ed5-23e3b066c47f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c32d0791-7a13-4a90-89fd-9d4a0e51b288' class='xr-var-data-in' type='checkbox'><label for='data-c32d0791-7a13-4a90-89fd-9d4a0e51b288' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.581814e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-a1e0a29e-644e-496c-a705-fb4ddf0cb7b0' class='xr-section-summary-in' type='checkbox'  ><label for='section-a1e0a29e-644e-496c-a705-fb4ddf0cb7b0' class='xr-section-summary' >Data variables: <span>(98)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>pe1_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1, dim_2)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-bfb93132-e20f-44cd-91e3-4d0211f3d00a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bfb93132-e20f-44cd-91e3-4d0211f3d00a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4d415201-f32e-436b-b941-037fa8d8cc69' class='xr-var-data-in' type='checkbox'><label for='data-4d415201-f32e-436b-b941-037fa8d8cc69' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[[   0,    0,    0, ...,    0,    0,    0],
             [4594, 4576, 4587, ..., 4123, 4172, 4122],
             [4635, 4600, 4624, ..., 4318, 4231, 4216],
             ...,
             [4335, 4315, 4312, ..., 4540, 4511, 4529],
             [4229, 4257, 4251, ..., 4458, 4474, 4525],
             [   0,    0,    0, ...,    0,    0,    0]]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1_stats1_total</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>4.41e+08</div><input id='attrs-9066ddf3-1efd-4978-bd19-8729ab8b22df' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9066ddf3-1efd-4978-bd19-8729ab8b22df' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2ec21abc-13cd-4641-9ea2-f81caf5e25a9' class='xr-var-data-in' type='checkbox'><label for='data-2ec21abc-13cd-4641-9ea2-f81caf5e25a9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([4.41031435e+08])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_period</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1</div><input id='attrs-6fcf8076-cab6-4d1d-b053-f1c7cd1d016b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6fcf8076-cab6-4d1d-b053-f1c7cd1d016b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f715e228-e8af-40be-a656-0082f15aa513' class='xr-var-data-in' type='checkbox'><label for='data-f715e228-e8af-40be-a656-0082f15aa513' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_acquire_time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.2</div><input id='attrs-fe54954d-366d-4dd0-bf69-082efe15ba15' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fe54954d-366d-4dd0-bf69-082efe15ba15' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a42081fe-45bd-4a53-9491-f74c7d18650a' class='xr-var-data-in' type='checkbox'><label for='data-a42081fe-45bd-4a53-9491-f74c7d18650a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_x</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-10a034fc-6deb-43f8-a37d-3dc903ae1520' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-10a034fc-6deb-43f8-a37d-3dc903ae1520' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8fb05eb3-6c00-4c75-b27c-a2e676d2b946' class='xr-var-data-in' type='checkbox'><label for='data-8fb05eb3-6c00-4c75-b27c-a2e676d2b946' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_bin_y</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-fab4f21d-9ff8-44f9-b58f-d0b31887c2ea' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fab4f21d-9ff8-44f9-b58f-d0b31887c2ea' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e1f78b1b-93eb-491e-986f-80ae4b539aed' class='xr-var-data-in' type='checkbox'><label for='data-e1f78b1b-93eb-491e-986f-80ae4b539aed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_image_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-3ed22472-dd60-4cf3-8e59-f471a4e59b61' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3ed22472-dd60-4cf3-8e59-f471a4e59b61' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7193270a-8ea6-4360-a805-75f30e6e6ee6' class='xr-var-data-in' type='checkbox'><label for='data-7193270a-8ea6-4360-a805-75f30e6e6ee6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_manufacturer</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Perkin Elmer&#x27;</div><input id='attrs-995bf7fe-ea46-4197-a32d-48cd98df9173' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-995bf7fe-ea46-4197-a32d-48cd98df9173' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-511c9a4c-ffc6-4a9b-819e-028bb1f50e97' class='xr-var-data-in' type='checkbox'><label for='data-511c9a4c-ffc6-4a9b-819e-028bb1f50e97' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin Elmer&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_model</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;XRD [0820/1620/1621] xN&#x27;</div><input id='attrs-f26940b4-d77b-4cf1-8501-279ae3e71d8f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f26940b4-d77b-4cf1-8501-279ae3e71d8f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f7b4eb02-b02d-4406-91a8-a1077c685e4d' class='xr-var-data-in' type='checkbox'><label for='data-f7b4eb02-b02d-4406-91a8-a1077c685e4d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;XRD [0820/1620/1621] xN&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_num_exposures</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-a93489b5-0ca2-469d-bf98-2eb7c5355c2b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a93489b5-0ca2-469d-bf98-2eb7c5355c2b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b044196f-8bfa-4500-ad22-1fb53f0ba31b' class='xr-var-data-in' type='checkbox'><label for='data-b044196f-8bfa-4500-ad22-1fb53f0ba31b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_cam_trigger_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-e91ec7ec-851d-49f2-9e00-77a72e456568' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e91ec7ec-851d-49f2-9e00-77a72e456568' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-391af8e7-b095-44b7-a89e-5ab236101f5d' class='xr-var-data-in' type='checkbox'><label for='data-391af8e7-b095-44b7-a89e-5ab236101f5d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_configuration_names</span></div><div class='xr-var-dims'>(time, dim_3)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_tiff_configuration_names&#x27; ....</div><input id='attrs-16a493f1-a1fd-44ae-9596-813568ebdf2e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-16a493f1-a1fd-44ae-9596-813568ebdf2e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f3613e75-4bee-40a8-b629-40a06e2b4012' class='xr-var-data-in' type='checkbox'><label for='data-f3613e75-4bee-40a8-b629-40a06e2b4012' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_tiff_configuration_names&#x27;, &#x27;pe1_tiff_port_name&#x27;,
            &#x27;pe1_tiff_asyn_pipeline_config&#x27;, &#x27;pe1_tiff_blocking_callbacks&#x27;,
            &#x27;pe1_tiff_enable&#x27;, &#x27;pe1_tiff_nd_array_port&#x27;,
            &#x27;pe1_tiff_plugin_type&#x27;, &#x27;pe1_tiff_auto_increment&#x27;,
            &#x27;pe1_tiff_auto_save&#x27;, &#x27;pe1_tiff_file_format&#x27;,
            &#x27;pe1_tiff_file_name&#x27;, &#x27;pe1_tiff_file_path&#x27;,
            &#x27;pe1_tiff_file_path_exists&#x27;, &#x27;pe1_tiff_file_template&#x27;,
            &#x27;pe1_tiff_file_write_mode&#x27;, &#x27;pe1_tiff_full_file_name&#x27;,
            &#x27;pe1_tiff_num_capture&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;FileTIFF1&#x27;</div><input id='attrs-2981ac6b-98c1-4408-b797-52ebada6d301' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2981ac6b-98c1-4408-b797-52ebada6d301' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f8528033-b6d2-4589-b9e2-1aba62532b7b' class='xr-var-data-in' type='checkbox'><label for='data-f8528033-b6d2-4589-b9e2-1aba62532b7b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;FileTIFF1&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_4)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-f26d34f5-c003-41a3-922e-495c8f166a7d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f26d34f5-c003-41a3-922e-495c8f166a7d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b236d408-6f89-4c4c-ba16-633f6714412f' class='xr-var-data-in' type='checkbox'><label for='data-b236d408-6f89-4c4c-ba16-633f6714412f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;,
            &#x27;pe1_tiff_configuration_names&#x27;]], dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-ba55fadf-c732-4935-bb81-c7251c9708fe' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ba55fadf-c732-4935-bb81-c7251c9708fe' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d37f8c5b-94e6-41c9-a69f-fd3c94075f20' class='xr-var-data-in' type='checkbox'><label for='data-d37f8c5b-94e6-41c9-a69f-fd3c94075f20' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-58694ca5-691e-45ec-8db0-41675f3e65ed' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-58694ca5-691e-45ec-8db0-41675f3e65ed' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ff8fa662-b5b0-475c-a66a-f7b53fb9e7d3' class='xr-var-data-in' type='checkbox'><label for='data-ff8fa662-b5b0-475c-a66a-f7b53fb9e7d3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-b3b8a040-7c49-45b4-a68c-43c8780dee10' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b3b8a040-7c49-45b4-a68c-43c8780dee10' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8805ceda-5e2f-4760-b7b7-d9f54ba17e82' class='xr-var-data-in' type='checkbox'><label for='data-8805ceda-5e2f-4760-b7b7-d9f54ba17e82' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U10</div><div class='xr-var-preview xr-preview'>&#x27;NDFileTIFF&#x27;</div><input id='attrs-b7013aa5-1528-465d-ab4e-d5986adb6aef' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b7013aa5-1528-465d-ab4e-d5986adb6aef' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4555ad07-9b2d-45a9-bc83-bdb1cd11481e' class='xr-var-data-in' type='checkbox'><label for='data-4555ad07-9b2d-45a9-bc83-bdb1cd11481e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDFileTIFF&#x27;], dtype=&#x27;&lt;U10&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_increment</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-c5930f28-8046-4456-bdb3-529b4c2fd948' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c5930f28-8046-4456-bdb3-529b4c2fd948' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-af0a9cb7-1aad-45f9-b6bd-d13ad02bb509' class='xr-var-data-in' type='checkbox'><label for='data-af0a9cb7-1aad-45f9-b6bd-d13ad02bb509' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_auto_save</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-be59daf7-699d-4b72-b8d0-ec1eb759425b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-be59daf7-699d-4b72-b8d0-ec1eb759425b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-67a1fcd7-f992-40d8-b168-a9d38e88086c' class='xr-var-data-in' type='checkbox'><label for='data-67a1fcd7-f992-40d8-b168-a9d38e88086c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_format</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-b6f43039-0522-4f5a-8926-2cb7176ea188' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b6f43039-0522-4f5a-8926-2cb7176ea188' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4a397133-1463-4372-b8f6-b73454d22b0c' class='xr-var-data-in' type='checkbox'><label for='data-4a397133-1463-4372-b8f6-b73454d22b0c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;92b6b929-d904-42f4-9017&#x27;</div><input id='attrs-ab0172e9-5098-41ea-8e60-76e009b2a49c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ab0172e9-5098-41ea-8e60-76e009b2a49c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-26adcb78-7fdf-4122-b687-74dbd5dc8ba0' class='xr-var-data-in' type='checkbox'><label for='data-26adcb78-7fdf-4122-b687-74dbd5dc8ba0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;92b6b929-d904-42f4-9017&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U23</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;</div><input id='attrs-3188fdbf-4fe4-4f5d-b430-131c4a3be89c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3188fdbf-4fe4-4f5d-b430-131c4a3be89c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fd0a2f9c-50e9-4ae1-a365-dfaa650cb783' class='xr-var-data-in' type='checkbox'><label for='data-fd0a2f9c-50e9-4ae1-a365-dfaa650cb783' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\&#x27;], dtype=&#x27;&lt;U23&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_path_exists</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-3809a5c6-d5b2-4f0f-a4ef-4ad80cdb2bad' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3809a5c6-d5b2-4f0f-a4ef-4ad80cdb2bad' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-404ae1a8-f67a-420e-b84b-3004d6871b52' class='xr-var-data-in' type='checkbox'><label for='data-404ae1a8-f67a-420e-b84b-3004d6871b52' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_template</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;%s%s_%6.6d.tiff&#x27;</div><input id='attrs-6f103b01-2dca-4216-a1af-d4b45eb36851' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6f103b01-2dca-4216-a1af-d4b45eb36851' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9397b254-4d99-4bbd-810c-60fccc8b757d' class='xr-var-data-in' type='checkbox'><label for='data-9397b254-4d99-4bbd-810c-60fccc8b757d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;%s%s_%6.6d.tiff&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_file_write_mode</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-7622f598-74cd-405f-93bd-6606e10d0fc6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7622f598-74cd-405f-93bd-6606e10d0fc6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6380f878-1ad0-4475-85cd-0352a74d362d' class='xr-var-data-in' type='checkbox'><label for='data-6380f878-1ad0-4475-85cd-0352a74d362d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_full_file_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U58</div><div class='xr-var-preview xr-preview'>&#x27;G:\\pe1_data\\2020\\02\\15\\92b...</div><input id='attrs-8d911936-11ef-4515-aa38-84d0790164b7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8d911936-11ef-4515-aa38-84d0790164b7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8d44f1d6-8a40-4a8b-a53f-c1fac0cc78e9' class='xr-var-data-in' type='checkbox'><label for='data-8d44f1d6-8a40-4a8b-a53f-c1fac0cc78e9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;G:\\pe1_data\\2020\\02\\15\\92b6b929-d904-42f4-9017_000000.tiff&#x27;],
          dtype=&#x27;&lt;U58&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_tiff_num_capture</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-a2f9fb96-c9d2-4c95-8348-d59f9efb6ebd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a2f9fb96-c9d2-4c95-8348-d59f9efb6ebd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-db93832a-5413-4bf5-a4fc-c0d4d4bb663f' class='xr-var-data-in' type='checkbox'><label for='data-db93832a-5413-4bf5-a4fc-c0d4d4bb663f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_configuration_names</span></div><div class='xr-var-dims'>(time, dim_5)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_proc_configuration_names&#x27; ....</div><input id='attrs-f93ead5c-33bd-4b08-9c0c-5ae399b49180' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f93ead5c-33bd-4b08-9c0c-5ae399b49180' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-19a7059b-51d0-454b-bdba-8dd48623e15b' class='xr-var-data-in' type='checkbox'><label for='data-19a7059b-51d0-454b-bdba-8dd48623e15b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_proc_configuration_names&#x27;, &#x27;pe1_proc_port_name&#x27;,
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
          dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U5</div><div class='xr-var-preview xr-preview'>&#x27;PROC1&#x27;</div><input id='attrs-fccc084d-d30a-417a-97fa-32afd33ef2bc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fccc084d-d30a-417a-97fa-32afd33ef2bc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-359afb90-05ce-4496-9fe1-2c4eb12b9f52' class='xr-var-data-in' type='checkbox'><label for='data-359afb90-05ce-4496-9fe1-2c4eb12b9f52' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PROC1&#x27;], dtype=&#x27;&lt;U5&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-8b80a102-be47-4a7c-b896-bcd93a3318c1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8b80a102-be47-4a7c-b896-bcd93a3318c1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fec7d71c-cbee-4c39-bc26-d1a7b25153ff' class='xr-var-data-in' type='checkbox'><label for='data-fec7d71c-cbee-4c39-bc26-d1a7b25153ff' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_proc_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-e755626a-1e64-4111-bbc6-4871c97edb06' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e755626a-1e64-4111-bbc6-4871c97edb06' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4687e1c3-4884-4e80-9511-9c8ec12875d8' class='xr-var-data-in' type='checkbox'><label for='data-4687e1c3-4884-4e80-9511-9c8ec12875d8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;UInt16&#x27;</div><input id='attrs-b2765010-a162-44ee-83dd-cd3287cb31d0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b2765010-a162-44ee-83dd-cd3287cb31d0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8aaefe29-2e08-487b-9931-f66ae22a15c0' class='xr-var-data-in' type='checkbox'><label for='data-8aaefe29-2e08-487b-9931-f66ae22a15c0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;UInt16&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-a11f9992-3fd4-487a-b2ef-f20ef72611ce' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a11f9992-3fd4-487a-b2ef-f20ef72611ce' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-68fb9128-e37b-436f-a94f-066497b1b620' class='xr-var-data-in' type='checkbox'><label for='data-68fb9128-e37b-436f-a94f-066497b1b620' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-1366066e-524d-437d-8f6a-784de47f62cf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1366066e-524d-437d-8f6a-784de47f62cf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fa02304b-88d0-4af2-be21-b833cd5f39a8' class='xr-var-data-in' type='checkbox'><label for='data-fa02304b-88d0-4af2-be21-b833cd5f39a8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U15</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginProcess&#x27;</div><input id='attrs-a49284f4-97c3-4c74-ba4c-f50e49a04997' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a49284f4-97c3-4c74-ba4c-f50e49a04997' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ca3d431c-e1b2-4291-af8a-6faa1bb5af92' class='xr-var-data-in' type='checkbox'><label for='data-ca3d431c-e1b2-4291-af8a-6faa1bb5af92' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginProcess&#x27;], dtype=&#x27;&lt;U15&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;Done&#x27;</div><input id='attrs-3ff238db-a71c-49f4-af6e-314d28333ab0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-3ff238db-a71c-49f4-af6e-314d28333ab0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-39602c9d-3c7c-4566-b643-558ae2fc0b21' class='xr-var-data-in' type='checkbox'><label for='data-39602c9d-3c7c-4566-b643-558ae2fc0b21' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Done&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_auto_reset_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-fe22d386-6858-4178-8f60-2e73bc9bf500' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fe22d386-6858-4178-8f60-2e73bc9bf500' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-acfea3f8-a640-411c-93d2-ab755ea28c2e' class='xr-var-data-in' type='checkbox'><label for='data-acfea3f8-a640-411c-93d2-ab755ea28c2e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_copy_to_filter_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-0f0e170c-f32f-4eea-9dd8-bc904f2fac9d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0f0e170c-f32f-4eea-9dd8-bc904f2fac9d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-65282ce1-2464-4ac5-9bbc-4cee4ef1034e' class='xr-var-data-in' type='checkbox'><label for='data-65282ce1-2464-4ac5-9bbc-4cee4ef1034e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-252ece55-202e-4684-9315-1b2423401d2d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-252ece55-202e-4684-9315-1b2423401d2d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-be304ef4-062f-4e0a-8967-cca183e4b414' class='xr-var-data-in' type='checkbox'><label for='data-be304ef4-062f-4e0a-8967-cca183e4b414' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_difference_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-41f6d810-9f31-44f8-89bf-99f9bdc0a6a7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-41f6d810-9f31-44f8-89bf-99f9bdc0a6a7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-661fb609-3e5e-4bad-a48f-ea8514e48e40' class='xr-var-data-in' type='checkbox'><label for='data-661fb609-3e5e-4bad-a48f-ea8514e48e40' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-fe92f55e-3d26-419e-9706-a2b178d40881' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-fe92f55e-3d26-419e-9706-a2b178d40881' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-61765f89-3c91-4521-8864-55d1e776c5f1' class='xr-var-data-in' type='checkbox'><label for='data-61765f89-3c91-4521-8864-55d1e776c5f1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-33f7b3dd-0672-4820-bfa8-6c2200fa0ea2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-33f7b3dd-0672-4820-bfa8-6c2200fa0ea2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-85fde45f-ea65-4142-9ab0-5ebdd16a33db' class='xr-var-data-in' type='checkbox'><label for='data-85fde45f-ea65-4142-9ab0-5ebdd16a33db' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-dced738c-a620-4ef8-9165-f27b47b0c390' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dced738c-a620-4ef8-9165-f27b47b0c390' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-50f7a407-4ae4-499c-b20b-e6b4222cb528' class='xr-var-data-in' type='checkbox'><label for='data-50f7a407-4ae4-499c-b20b-e6b4222cb528' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-cf7581fc-947d-433b-81cf-18b9903aa9cc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cf7581fc-947d-433b-81cf-18b9903aa9cc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-97fa26b2-a12c-48a4-a7dc-db5c3741933e' class='xr-var-data-in' type='checkbox'><label for='data-97fa26b2-a12c-48a4-a7dc-db5c3741933e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-61f5e280-a51a-4437-8733-c7181edc4541' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-61f5e280-a51a-4437-8733-c7181edc4541' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6b4b07aa-f29a-4d6c-a66d-40b4d60d97a9' class='xr-var-data-in' type='checkbox'><label for='data-6b4b07aa-f29a-4d6c-a66d-40b4d60d97a9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_enable_offset_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-dec8d1fd-2cc1-490f-8531-714d749bad4a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dec8d1fd-2cc1-490f-8531-714d749bad4a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d8f204b4-e637-4aec-8ec3-8dc7803139a2' class='xr-var-data-in' type='checkbox'><label for='data-d8f204b4-e637-4aec-8ec3-8dc7803139a2' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_foffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-718065dd-b157-4bd8-8cb9-a8171fa85223' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-718065dd-b157-4bd8-8cb9-a8171fa85223' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3fb3481d-1f43-4db6-9a4c-9f3689ed67e9' class='xr-var-data-in' type='checkbox'><label for='data-3fb3481d-1f43-4db6-9a4c-9f3689ed67e9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_fscale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-c4cf7a3a-393f-46e2-a895-8d98c819005b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c4cf7a3a-393f-46e2-a895-8d98c819005b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-92e92391-0477-4b6a-a99e-f19a5938f20f' class='xr-var-data-in' type='checkbox'><label for='data-92e92391-0477-4b6a-a99e-f19a5938f20f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U12</div><div class='xr-var-preview xr-preview'>&#x27;Array N only&#x27;</div><input id='attrs-e63feaf5-f900-42ed-a8e5-70aa21bc9f42' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e63feaf5-f900-42ed-a8e5-70aa21bc9f42' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e7a26e64-cb50-4c50-a64a-ae37caf367bc' class='xr-var-data-in' type='checkbox'><label for='data-e7a26e64-cb50-4c50-a64a-ae37caf367bc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Array N only&#x27;], dtype=&#x27;&lt;U12&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Average&#x27;</div><input id='attrs-557d5d7e-3df0-42ae-9e15-ec33ab386c49' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-557d5d7e-3df0-42ae-9e15-ec33ab386c49' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a7980a78-6d47-4e4d-98ac-10e79ccc000b' class='xr-var-data-in' type='checkbox'><label for='data-a7980a78-6d47-4e4d-98ac-10e79ccc000b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Average&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_filter_type_seq</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>0</div><input id='attrs-105efb2b-9d88-4f7c-95ec-bc0cd11ef0f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-105efb2b-9d88-4f7c-95ec-bc0cd11ef0f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f71e76d2-15cf-4b7d-9df1-cf505b53b813' class='xr-var-data-in' type='checkbox'><label for='data-f71e76d2-15cf-4b7d-9df1-cf505b53b813' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_high_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>100.0</div><input id='attrs-6dda3cb0-2f09-499a-b0d2-68bcdc5065f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6dda3cb0-2f09-499a-b0d2-68bcdc5065f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9619a7ae-7eb0-4855-88f5-8340f49a6674' class='xr-var-data-in' type='checkbox'><label for='data-9619a7ae-7eb0-4855-88f5-8340f49a6674' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([100.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_low_clip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-930a69ac-5e56-4dd3-9b82-b9d9530fd9e2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-930a69ac-5e56-4dd3-9b82-b9d9530fd9e2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5c259245-51d6-43c2-a390-e7d160de13bd' class='xr-var-data-in' type='checkbox'><label for='data-5c259245-51d6-43c2-a390-e7d160de13bd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>50</div><input id='attrs-e1d35b57-7a7c-48c5-a127-fea3e2205cb9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e1d35b57-7a7c-48c5-a127-fea3e2205cb9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-1cc1ce6f-894a-4813-93c3-e42e734b11fc' class='xr-var-data-in' type='checkbox'><label for='data-1cc1ce6f-894a-4813-93c3-e42e734b11fc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filter_recip</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.02</div><input id='attrs-922a7446-414f-43a6-af70-f3e72fced5bf' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-922a7446-414f-43a6-af70-f3e72fced5bf' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5c927636-fd89-4026-8464-8f214b85280a' class='xr-var-data-in' type='checkbox'><label for='data-5c927636-fd89-4026-8464-8f214b85280a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.02])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_num_filtered</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2</div><input id='attrs-0a23c2c7-29b5-462e-ac38-058b58c6e88f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0a23c2c7-29b5-462e-ac38-058b58c6e88f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e4d24188-91fd-4129-892d-46f6f7388e59' class='xr-var-data-in' type='checkbox'><label for='data-e4d24188-91fd-4129-892d-46f6f7388e59' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-dc68a573-e003-44c6-b4d7-44872e6da947' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dc68a573-e003-44c6-b4d7-44872e6da947' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e09cdbe9-00ac-4568-b716-140f62495ba9' class='xr-var-data-in' type='checkbox'><label for='data-e09cdbe9-00ac-4568-b716-140f62495ba9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_o_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-cc3df08c-37b5-422e-b1d8-59f1983663b1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cc3df08c-37b5-422e-b1d8-59f1983663b1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b60242f8-0d3e-4bb5-af84-19052699d4f6' class='xr-var-data-in' type='checkbox'><label for='data-b60242f8-0d3e-4bb5-af84-19052699d4f6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_offset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-e5033243-c059-48ab-951e-445c1c06660f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e5033243-c059-48ab-951e-445c1c06660f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7ef6ae87-8884-4c7b-852d-5377e9e7096a' class='xr-var-data-in' type='checkbox'><label for='data-7ef6ae87-8884-4c7b-852d-5377e9e7096a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_roffset</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-5c0cc361-bacb-4b19-ae41-d45b232eb8a1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5c0cc361-bacb-4b19-ae41-d45b232eb8a1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2d0f3433-d497-4bfd-8209-fb0ad43dc4b1' class='xr-var-data-in' type='checkbox'><label for='data-2d0f3433-d497-4bfd-8209-fb0ad43dc4b1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-5a86ff75-43e9-4068-9b69-1a4496233279' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5a86ff75-43e9-4068-9b69-1a4496233279' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b89515ac-b29a-498a-b887-09000194a4d3' class='xr-var-data-in' type='checkbox'><label for='data-b89515ac-b29a-498a-b887-09000194a4d3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_scale_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-f03920a0-b51c-4c83-ac74-5fac9deac3e2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-f03920a0-b51c-4c83-ac74-5fac9deac3e2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-926970e8-07a8-4bb7-a64e-c85da8999bce' class='xr-var-data-in' type='checkbox'><label for='data-926970e8-07a8-4bb7-a64e-c85da8999bce' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_background</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-44afb336-77bf-42af-994a-71e6574c753e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-44afb336-77bf-42af-994a-71e6574c753e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fff37dcc-e600-4f12-8458-9ec12c6f9346' class='xr-var-data-in' type='checkbox'><label for='data-fff37dcc-e600-4f12-8458-9ec12c6f9346' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_proc_valid_flat_field</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Invalid&#x27;</div><input id='attrs-337c2bb6-b47f-46b2-81f0-16ada239f314' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-337c2bb6-b47f-46b2-81f0-16ada239f314' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b371101a-f5cb-4d53-9234-63f6d89be1ea' class='xr-var-data-in' type='checkbox'><label for='data-b371101a-f5cb-4d53-9234-63f6d89be1ea' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Invalid&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_images_per_set</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>50.0</div><input id='attrs-90883d84-1f03-4e4b-a977-7f1f877505d7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-90883d84-1f03-4e4b-a977-7f1f877505d7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7a90847b-2651-4a51-8746-827af5251bcf' class='xr-var-data-in' type='checkbox'><label for='data-7a90847b-2651-4a51-8746-827af5251bcf' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([50.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_number_of_sets</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-aa4ed26d-217f-4c06-991a-ac9885bccad8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-aa4ed26d-217f-4c06-991a-ac9885bccad8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-bcb5e891-a326-4b0d-ad2d-8635499be26a' class='xr-var-data-in' type='checkbox'><label for='data-bcb5e891-a326-4b0d-ad2d-8635499be26a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_pixel_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0002</div><input id='attrs-01f457f7-7b6c-4cf2-a922-4ac727f65ac2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-01f457f7-7b6c-4cf2-a922-4ac727f65ac2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-39a9f337-af9d-4e1b-bece-bf3c20d2f500' class='xr-var-data-in' type='checkbox'><label for='data-39a9f337-af9d-4e1b-bece-bf3c20d2f500' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.0002])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_detector_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Perkin&#x27;</div><input id='attrs-ac262c43-a4fa-45f9-976e-7099f5c0ff92' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ac262c43-a4fa-45f9-976e-7099f5c0ff92' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f1678083-4fc0-489f-912b-9aaa4c4442a0' class='xr-var-data-in' type='checkbox'><label for='data-f1678083-4fc0-489f-912b-9aaa4c4442a0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Perkin&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>&lt;U31</div><div class='xr-var-preview xr-preview'>&#x27;pe1_stats1_configuration_names&#x27;...</div><input id='attrs-93447a1d-c66d-4b1b-832a-24127970c270' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-93447a1d-c66d-4b1b-832a-24127970c270' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e731f50f-4973-4716-b039-8f60ef1eee17' class='xr-var-data-in' type='checkbox'><label for='data-e731f50f-4973-4716-b039-8f60ef1eee17' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_stats1_configuration_names&#x27;, &#x27;pe1_stats1_port_name&#x27;,
            &#x27;pe1_stats1_asyn_pipeline_config&#x27;,
            &#x27;pe1_stats1_blocking_callbacks&#x27;, &#x27;pe1_stats1_enable&#x27;,
            &#x27;pe1_stats1_nd_array_port&#x27;, &#x27;pe1_stats1_plugin_type&#x27;,
            &#x27;pe1_stats1_bgd_width&#x27;, &#x27;pe1_stats1_centroid_threshold&#x27;,
            &#x27;pe1_stats1_compute_centroid&#x27;, &#x27;pe1_stats1_compute_histogram&#x27;,
            &#x27;pe1_stats1_compute_profiles&#x27;, &#x27;pe1_stats1_compute_statistics&#x27;,
            &#x27;pe1_stats1_hist_max&#x27;, &#x27;pe1_stats1_hist_min&#x27;,
            &#x27;pe1_stats1_hist_size&#x27;, &#x27;pe1_stats1_profile_cursor&#x27;,
            &#x27;pe1_stats1_profile_size&#x27;, &#x27;pe1_stats1_ts_num_points&#x27;]],
          dtype=&#x27;&lt;U31&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;STATS1&#x27;</div><input id='attrs-6428a7a0-4afc-48ae-8ec4-94a9365be3e3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6428a7a0-4afc-48ae-8ec4-94a9365be3e3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a1cfd6a2-f1c9-45ba-9179-548c65cbaf36' class='xr-var-data-in' type='checkbox'><label for='data-a1cfd6a2-f1c9-45ba-9179-548c65cbaf36' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;STATS1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>&lt;U30</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; .....</div><input id='attrs-23a0de16-b47a-44c8-9543-9e64f699fcbd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-23a0de16-b47a-44c8-9543-9e64f699fcbd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-14b3a9d3-9719-4400-b5d9-b6957f8a39fa' class='xr-var-data-in' type='checkbox'><label for='data-14b3a9d3-9719-4400-b5d9-b6957f8a39fa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;,
            &#x27;pe1_stats1_configuration_names&#x27;]], dtype=&#x27;&lt;U30&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-dff75fe8-3b49-4455-906f-1e2abef1595e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dff75fe8-3b49-4455-906f-1e2abef1595e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c2519619-a494-4a9b-9d36-afd42b5401e1' class='xr-var-data-in' type='checkbox'><label for='data-c2519619-a494-4a9b-9d36-afd42b5401e1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-9f29bdf7-f392-4c50-88df-468dfc0f0fae' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9f29bdf7-f392-4c50-88df-468dfc0f0fae' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7f170d09-946a-4e79-a551-a675af3d6e5f' class='xr-var-data-in' type='checkbox'><label for='data-7f170d09-946a-4e79-a551-a675af3d6e5f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-1ab67245-2530-4027-8edf-2d152ef6f24b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1ab67245-2530-4027-8edf-2d152ef6f24b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5bb01da6-5d67-4515-8c16-621511650d81' class='xr-var-data-in' type='checkbox'><label for='data-5bb01da6-5d67-4515-8c16-621511650d81' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U13</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginStats&#x27;</div><input id='attrs-957a58f8-d4ce-419e-b3a5-e96af973ac2f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-957a58f8-d4ce-419e-b3a5-e96af973ac2f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-81db7751-6819-4554-94e1-299409042eaa' class='xr-var-data-in' type='checkbox'><label for='data-81db7751-6819-4554-94e1-299409042eaa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginStats&#x27;], dtype=&#x27;&lt;U13&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_bgd_width</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-bd95ff78-df63-4698-a132-45d179b1f819' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-bd95ff78-df63-4698-a132-45d179b1f819' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f2566a81-375d-4d60-995c-24247b992c33' class='xr-var-data-in' type='checkbox'><label for='data-f2566a81-375d-4d60-995c-24247b992c33' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_centroid_threshold</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.0</div><input id='attrs-15775fdf-c554-4743-9be3-34aaef5242dd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-15775fdf-c554-4743-9be3-34aaef5242dd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e0c1ebd5-f68f-4c5f-98f5-a9282253f3f3' class='xr-var-data-in' type='checkbox'><label for='data-e0c1ebd5-f68f-4c5f-98f5-a9282253f3f3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_centroid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-9ac6366c-3814-4ebb-b8f0-8bdf1c06c1f3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9ac6366c-3814-4ebb-b8f0-8bdf1c06c1f3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-5aba5bfd-46b3-4d4e-bde0-78af24ef5d28' class='xr-var-data-in' type='checkbox'><label for='data-5aba5bfd-46b3-4d4e-bde0-78af24ef5d28' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_histogram</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-9f1ead18-add4-4f1e-88ac-a5578d3388c3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9f1ead18-add4-4f1e-88ac-a5578d3388c3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f2e2af04-543e-45ec-be58-b21216460f23' class='xr-var-data-in' type='checkbox'><label for='data-f2e2af04-543e-45ec-be58-b21216460f23' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_profiles</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U2</div><div class='xr-var-preview xr-preview'>&#x27;No&#x27;</div><input id='attrs-4b72cc49-d3f2-4d58-acc5-f11b373f0713' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4b72cc49-d3f2-4d58-acc5-f11b373f0713' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-06a7b97f-975d-4bad-9644-3f970088845d' class='xr-var-data-in' type='checkbox'><label for='data-06a7b97f-975d-4bad-9644-3f970088845d' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;No&#x27;], dtype=&#x27;&lt;U2&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_compute_statistics</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-d8a33d9d-6207-417d-80ac-be2b6418f443' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d8a33d9d-6207-417d-80ac-be2b6418f443' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8569773d-d886-4073-a2c5-05138bf6addc' class='xr-var-data-in' type='checkbox'><label for='data-8569773d-d886-4073-a2c5-05138bf6addc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>255.0</div><input id='attrs-d9c79d73-8cfa-4a0d-b454-b703cc450838' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d9c79d73-8cfa-4a0d-b454-b703cc450838' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ff60935a-dfd7-46da-b86b-dbdffa8effb1' class='xr-var-data-in' type='checkbox'><label for='data-ff60935a-dfd7-46da-b86b-dbdffa8effb1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([255.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_min</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-c4e2d7d3-4829-417c-be8e-8b7b96ce78b4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c4e2d7d3-4829-417c-be8e-8b7b96ce78b4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ee91b7dd-04af-4f28-8693-599701515be3' class='xr-var-data-in' type='checkbox'><label for='data-ee91b7dd-04af-4f28-8693-599701515be3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_hist_size</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>256</div><input id='attrs-df3ba34f-8c02-4f67-8a93-34d37e6d92a0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-df3ba34f-8c02-4f67-8a93-34d37e6d92a0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-814fe463-bbdd-4d23-807a-a932cb584248' class='xr-var-data-in' type='checkbox'><label for='data-814fe463-bbdd-4d23-807a-a932cb584248' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([256])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_stats1_ts_num_points</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>2048</div><input id='attrs-60613768-2863-4d89-aac8-9fd683d1dcb7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-60613768-2863-4d89-aac8-9fd683d1dcb7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7677a52f-cb55-4253-9b8e-944afbef4cef' class='xr-var-data-in' type='checkbox'><label for='data-7677a52f-cb55-4253-9b8e-944afbef4cef' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([2048])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_configuration_names</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>&lt;U29</div><div class='xr-var-preview xr-preview'>&#x27;pe1_roi1_configuration_names&#x27; ....</div><input id='attrs-334961a1-77b6-4620-abec-a2f57eff6b1f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-334961a1-77b6-4620-abec-a2f57eff6b1f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ccb8bb28-11c6-47e6-b517-7173cbe26d90' class='xr-var-data-in' type='checkbox'><label for='data-ccb8bb28-11c6-47e6-b517-7173cbe26d90' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_roi1_configuration_names&#x27;, &#x27;pe1_roi1_port_name&#x27;,
            &#x27;pe1_roi1_asyn_pipeline_config&#x27;, &#x27;pe1_roi1_blocking_callbacks&#x27;,
            &#x27;pe1_roi1_enable&#x27;, &#x27;pe1_roi1_nd_array_port&#x27;,
            &#x27;pe1_roi1_plugin_type&#x27;, &#x27;pe1_roi1_bin_&#x27;,
            &#x27;pe1_roi1_data_type_out&#x27;, &#x27;pe1_roi1_enable_scale&#x27;,
            &#x27;pe1_roi1_roi_enable&#x27;, &#x27;pe1_roi1_min_xyz&#x27;, &#x27;pe1_roi1_name_&#x27;,
            &#x27;pe1_roi1_size&#x27;]], dtype=&#x27;&lt;U29&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_port_name</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U4</div><div class='xr-var-preview xr-preview'>&#x27;ROI1&#x27;</div><input id='attrs-c046aa76-0ceb-4382-b6af-43139c407628' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c046aa76-0ceb-4382-b6af-43139c407628' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3ba53635-bbb5-4e9e-9276-a22f4b15eebd' class='xr-var-data-in' type='checkbox'><label for='data-3ba53635-bbb5-4e9e-9276-a22f4b15eebd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ROI1&#x27;], dtype=&#x27;&lt;U4&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_asyn_pipeline_config</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>&lt;U28</div><div class='xr-var-preview xr-preview'>&#x27;pe1_cam_configuration_names&#x27; &#x27;p...</div><input id='attrs-cd4a409c-4c40-46d6-8eb8-b7c4ae75462e' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-cd4a409c-4c40-46d6-8eb8-b7c4ae75462e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-09163d17-a49e-4eb4-9940-1a9824eb301e' class='xr-var-data-in' type='checkbox'><label for='data-09163d17-a49e-4eb4-9940-1a9824eb301e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[&#x27;pe1_cam_configuration_names&#x27;, &#x27;pe1_roi1_configuration_names&#x27;]],
          dtype=&#x27;&lt;U28&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_blocking_callbacks</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U3</div><div class='xr-var-preview xr-preview'>&#x27;Yes&#x27;</div><input id='attrs-0505b18f-0364-40b7-8ee9-c06fa7a88921' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0505b18f-0364-40b7-8ee9-c06fa7a88921' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c55d487d-f0ff-49ef-82a1-d052c91ae5f0' class='xr-var-data-in' type='checkbox'><label for='data-c55d487d-f0ff-49ef-82a1-d052c91ae5f0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Yes&#x27;], dtype=&#x27;&lt;U3&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;Enable&#x27;</div><input id='attrs-5b2813c0-bec4-47f6-9af9-6b07bf7c182a' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5b2813c0-bec4-47f6-9af9-6b07bf7c182a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6086a83a-79e7-432e-bab7-e644aa5cc0aa' class='xr-var-data-in' type='checkbox'><label for='data-6086a83a-79e7-432e-bab7-e644aa5cc0aa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Enable&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_nd_array_port</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U6</div><div class='xr-var-preview xr-preview'>&#x27;PEDET1&#x27;</div><input id='attrs-7c3d1f28-df20-4333-8d55-4fd4de7113e8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7c3d1f28-df20-4333-8d55-4fd4de7113e8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e19a5d78-a8d7-4236-9751-d4c8c6ccb0b9' class='xr-var-data-in' type='checkbox'><label for='data-e19a5d78-a8d7-4236-9751-d4c8c6ccb0b9' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;PEDET1&#x27;], dtype=&#x27;&lt;U6&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_plugin_type</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U11</div><div class='xr-var-preview xr-preview'>&#x27;NDPluginROI&#x27;</div><input id='attrs-efb54e32-82f0-4a61-b562-c01689abee12' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-efb54e32-82f0-4a61-b562-c01689abee12' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-dc526b57-b14c-4b4f-8cd5-9286f442e645' class='xr-var-data-in' type='checkbox'><label for='data-dc526b57-b14c-4b4f-8cd5-9286f442e645' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;NDPluginROI&#x27;], dtype=&#x27;&lt;U11&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_data_type_out</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>&#x27;Automatic&#x27;</div><input id='attrs-a7af1b19-dea0-4bd5-ae95-c1db3ce8c4f6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a7af1b19-dea0-4bd5-ae95-c1db3ce8c4f6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e6fee5b0-5543-43e0-96b3-e06abb5c3bfd' class='xr-var-data-in' type='checkbox'><label for='data-e6fee5b0-5543-43e0-96b3-e06abb5c3bfd' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Automatic&#x27;], dtype=&#x27;&lt;U9&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_enable_scale</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U7</div><div class='xr-var-preview xr-preview'>&#x27;Disable&#x27;</div><input id='attrs-b34689a3-ec0a-43d7-b879-51c61c47a5cb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b34689a3-ec0a-43d7-b879-51c61c47a5cb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fddcdf69-c71d-45bb-a176-c7e4baf38855' class='xr-var-data-in' type='checkbox'><label for='data-fddcdf69-c71d-45bb-a176-c7e4baf38855' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;Disable&#x27;], dtype=&#x27;&lt;U7&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>pe1:pe1_roi1_name_</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U1</div><div class='xr-var-preview xr-preview'>&#x27;&#x27;</div><input id='attrs-29c34b00-b3d5-407c-bf75-2e09d2d96da3' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-29c34b00-b3d5-407c-bf75-2e09d2d96da3' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3e126b90-c3c4-4622-a1e6-ede32c8090f4' class='xr-var-data-in' type='checkbox'><label for='data-3e126b90-c3c4-4622-a1e6-ede32c8090f4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;&#x27;], dtype=&#x27;&lt;U1&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-6626f0e1-e88f-477c-b8e6-66d1b305cba8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6626f0e1-e88f-477c-b8e6-66d1b305cba8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6a20982c-4e19-49ba-8e24-cef4ab172ef5' class='xr-var-data-in' type='checkbox'><label for='data-6a20982c-4e19-49ba-8e24-cef4ab172ef5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;ad3b7a7f-6564-4157-933f-c3bae9e...</div><input id='attrs-1116806e-df47-49b5-acea-481707bbd564' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1116806e-df47-49b5-acea-481707bbd564' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c5a8befe-a4fd-477b-b8ac-ac58da200a13' class='xr-var-data-in' type='checkbox'><label for='data-c5a8befe-a4fd-477b-b8ac-ac58da200a13' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;ad3b7a7f-6564-4157-933f-c3bae9e9e876&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-65e70a1a-3430-4f0f-95a3-45aa3ecbda80' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-65e70a1a-3430-4f0f-95a3-45aa3ecbda80' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
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
        uid           (time) &lt;U36 &#x27;0eb4e35f-86db-428e-ad78-bc3d448c9f9d&#x27;</pre><div class='xr-wrap' hidden><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-4279db4c-0927-4e1e-a943-aa5b837bb09c' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-4279db4c-0927-4e1e-a943-aa5b837bb09c' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>dim_0</span>: 2048</li><li><span>dim_1</span>: 2048</li><li><span>dim_10</span>: 692</li><li><span>dim_11</span>: 692</li><li><span>dim_12</span>: 692</li><li><span>dim_13</span>: 692</li><li><span>dim_14</span>: 3001</li><li><span>dim_15</span>: 3001</li><li><span>dim_2</span>: 2048</li><li><span>dim_3</span>: 2048</li><li><span>dim_4</span>: 2048</li><li><span>dim_5</span>: 2048</li><li><span>dim_6</span>: 1024</li><li><span>dim_7</span>: 1024</li><li><span>dim_8</span>: 755</li><li><span>dim_9</span>: 755</li><li><span class='xr-has-index'>time</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-9a865517-b5f6-49bb-af77-7edef9103a57' class='xr-section-summary-in' type='checkbox'  checked><label for='section-9a865517-b5f6-49bb-af77-7edef9103a57' class='xr-section-summary' >Coordinates: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.607e+09</div><input id='attrs-2f07aa11-b77b-4f9d-9303-d1a2515d09e0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2f07aa11-b77b-4f9d-9303-d1a2515d09e0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-97bb411f-b979-4019-8d9a-07b27def74e4' class='xr-var-data-in' type='checkbox'><label for='data-97bb411f-b979-4019-8d9a-07b27def74e4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1.607102e+09])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-6a56ea14-9e30-4ac8-9129-50c1def24294' class='xr-section-summary-in' type='checkbox'  ><label for='section-6a56ea14-9e30-4ac8-9129-50c1def24294' class='xr-section-summary' >Data variables: <span>(19)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>dk_sub_image</span></div><div class='xr-var-dims'>(time, dim_0, dim_1)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-5182cde0-80d0-447d-b358-f26967f99329' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5182cde0-80d0-447d-b358-f26967f99329' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-af839a05-bfd0-4d93-8648-bb82572db5a6' class='xr-var-data-in' type='checkbox'><label for='data-af839a05-bfd0-4d93-8648-bb82572db5a6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>bg_sub_image</span></div><div class='xr-var-dims'>(time, dim_2, dim_3)</div><div class='xr-var-dtype'>uint16</div><div class='xr-var-preview xr-preview'>0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0</div><input id='attrs-a30627e6-d1e8-4173-93ec-52f06366a771' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a30627e6-d1e8-4173-93ec-52f06366a771' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-30f11ef1-85fd-4a9a-b20f-0892c58e16a5' class='xr-var-data-in' type='checkbox'><label for='data-30f11ef1-85fd-4a9a-b20f-0892c58e16a5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[    0,     0,     0, ...,     0,     0,     0],
            [    9,     1,     6, ...,     6,     4, 65534],
            [    4,    11,     4, ...,     6,     5,     2],
            ...,
            [    6, 65529,     4, ...,     7,     3, 65533],
            [    3,     2, 65533, ...,     7, 65535,     0],
            [    0,     0,     0, ...,     0,     0,     0]]], dtype=uint16)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>mask</span></div><div class='xr-var-dims'>(time, dim_4, dim_5)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1 1 1 1 1 1 1 1 ... 1 1 1 1 1 1 1 1</div><input id='attrs-2cc9c3df-8131-4ef1-b63b-55bf07e0a77c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-2cc9c3df-8131-4ef1-b63b-55bf07e0a77c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-c3e0d0d7-4f1a-43b4-a553-6ee27c32e45c' class='xr-var-data-in' type='checkbox'><label for='data-c3e0d0d7-4f1a-43b4-a553-6ee27c32e45c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            ...,
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1],
            [1, 1, 1, ..., 1, 1, 1]]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_Q</span></div><div class='xr-var-dims'>(time, dim_6)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0253 0.05714 ... 32.56 32.59</div><input id='attrs-5ac9dfd0-3047-4a60-b0c7-f7a08bcb4d7d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-5ac9dfd0-3047-4a60-b0c7-f7a08bcb4d7d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f27c2cca-99f1-48fb-b5d8-b9137b01b5a8' class='xr-var-data-in' type='checkbox'><label for='data-f27c2cca-99f1-48fb-b5d8-b9137b01b5a8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[2.53048628e-02, 5.71350587e-02, 8.89652545e-02, ...,
            3.25239349e+01, 3.25557651e+01, 3.25875953e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_I</span></div><div class='xr-var-dims'>(time, dim_7)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>17.449076 15.25509 ... 0.0 0.0</div><input id='attrs-c11d66fa-7945-4d87-80c3-ae6cba243d85' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-c11d66fa-7945-4d87-80c3-ae6cba243d85' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-2e4be466-0817-4882-8dee-d48c3b032717' class='xr-var-data-in' type='checkbox'><label for='data-2e4be466-0817-4882-8dee-d48c3b032717' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[17.449076, 15.25509 , 17.243057, ...,  0.      ,  0.      ,
             0.      ]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>21331.768</div><input id='attrs-13152ae6-5d32-40a8-b1b6-827a574df5ac' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-13152ae6-5d32-40a8-b1b6-827a574df5ac' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-71e257c3-21f1-458b-b27e-b38d93a24f1f' class='xr-var-data-in' type='checkbox'><label for='data-71e257c3-21f1-458b-b27e-b38d93a24f1f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([21331.768], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>3.081</div><input id='attrs-7284634c-80de-48da-a671-be0f7d1cc0ef' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7284634c-80de-48da-a671-be0f7d1cc0ef' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-70ba6588-c9dd-49e7-ab32-0ef2ac5a1eed' class='xr-var-data-in' type='checkbox'><label for='data-70ba6588-c9dd-49e7-ab32-0ef2ac5a1eed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([3.08100367])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_Q</span></div><div class='xr-var-dims'>(time, dim_8)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 23.97 24.0</div><input id='attrs-8b850b7e-4da0-4481-8758-0371a11216e9' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-8b850b7e-4da0-4481-8758-0371a11216e9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0dd372f8-a358-4769-a01b-1b8301e05c65' class='xr-var-data-in' type='checkbox'><label for='data-0dd372f8-a358-4769-a01b-1b8301e05c65' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
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
            23.87264692, 23.90447711, 23.93630731, 23.96813751, 23.9999677 ]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>iq_I</span></div><div class='xr-var-dims'>(time, dim_9)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>17.45 17.0 15.66 ... 74.1 73.68</div><input id='attrs-79cde8ec-b7dd-4453-9c8e-1309d589f8b7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-79cde8ec-b7dd-4453-9c8e-1309d589f8b7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6dec69c0-b5a8-453d-b7f6-a0873c80a59f' class='xr-var-data-in' type='checkbox'><label for='data-6dec69c0-b5a8-453d-b7f6-a0873c80a59f' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.74490757e+01, 1.69992987e+01, 1.56626320e+01, 1.74703867e+01,
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
            7.48447155e+01, 7.40994861e+01, 7.36818762e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_Q</span></div><div class='xr-var-dims'>(time, dim_10)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-693ac8f2-4fc6-4c34-90f7-1da335e2b806' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-693ac8f2-4fc6-4c34-90f7-1da335e2b806' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b861e943-fff5-4d2c-a394-be2048438a74' class='xr-var-data-in' type='checkbox'><label for='data-b861e943-fff5-4d2c-a394-be2048438a74' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
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
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>sq_S</span></div><div class='xr-var-dims'>(time, dim_11)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>1.441 1.42 1.399 ... 1.014 0.9995</div><input id='attrs-545885d1-2b55-421b-9f55-bf2b38455f76' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-545885d1-2b55-421b-9f55-bf2b38455f76' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-06e2c2dd-d282-43a0-a39e-1eada09aa7a6' class='xr-var-data-in' type='checkbox'><label for='data-06e2c2dd-d282-43a0-a39e-1eada09aa7a6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[1.44081866, 1.41981957, 1.39906439, 1.37918811, 1.35951973,
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
            1.01382084, 0.99948833]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_Q</span></div><div class='xr-var-dims'>(time, dim_12)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.03183 0.06366 ... 21.96 21.99</div><input id='attrs-6c60eb50-db9e-41c1-87df-0f7a8c44aecc' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6c60eb50-db9e-41c1-87df-0f7a8c44aecc' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7a75c044-656c-405d-9926-92d1ea843ea0' class='xr-var-data-in' type='checkbox'><label for='data-7a75c044-656c-405d-9926-92d1ea843ea0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.        ,  0.0318302 ,  0.06366039,  0.09549059,  0.12732078,
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
            21.96283516, 21.99466536]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>fq_F</span></div><div class='xr-var-dims'>(time, dim_13)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01336 ... 0.3035 -0.01125</div><input id='attrs-69ce0ad7-3ad9-4dfa-9332-316688966aeb' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-69ce0ad7-3ad9-4dfa-9332-316688966aeb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6deaafcd-c5b7-4bd2-bad1-59689cccb412' class='xr-var-data-in' type='checkbox'><label for='data-6deaafcd-c5b7-4bd2-bad1-59689cccb412' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[ 0.00000000e+00,  1.33629391e-02,  2.54045954e-02,
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
             3.03544788e-01, -1.12540794e-02]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_r</span></div><div class='xr-var-dims'>(time, dim_14)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.01 0.02 ... 29.98 29.99 30.0</div><input id='attrs-a25bd52c-3051-44c2-b5a6-1a6958d46909' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a25bd52c-3051-44c2-b5a6-1a6958d46909' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-33b21d7a-52f9-49ee-86c3-0100f995eb7b' class='xr-var-data-in' type='checkbox'><label for='data-33b21d7a-52f9-49ee-86c3-0100f995eb7b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.000e+00, 1.000e-02, 2.000e-02, ..., 2.998e+01, 2.999e+01,
            3.000e+01]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_G</span></div><div class='xr-var-dims'>(time, dim_15)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.003567 0.006975 ... 1.4 1.455</div><input id='attrs-e5c1b949-ae17-4ef8-b15f-c35662422ad5' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e5c1b949-ae17-4ef8-b15f-c35662422ad5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7d7559b9-3b1a-4e3a-8b8a-f4c4c195939c' class='xr-var-data-in' type='checkbox'><label for='data-7d7559b9-3b1a-4e3a-8b8a-f4c4c195939c' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[0.        , 0.0035669 , 0.00697492, ..., 1.33294076, 1.39995837,
            1.45483018]])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_max</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>7.417</div><input id='attrs-22c9ebb7-1f52-426d-9f71-4a4d677cadf1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-22c9ebb7-1f52-426d-9f71-4a4d677cadf1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3d6e349f-dc8a-4bc8-a41e-6b51ca930902' class='xr-var-data-in' type='checkbox'><label for='data-3d6e349f-dc8a-4bc8-a41e-6b51ca930902' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([7.41703315])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>gr_argmax</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>6.59</div><input id='attrs-b74ed4e4-3d71-49b8-85f4-4ef3337a3479' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b74ed4e4-3d71-49b8-85f4-4ef3337a3479' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e00bc86b-1749-4c78-94eb-330c67bc7153' class='xr-var-data-in' type='checkbox'><label for='data-e00bc86b-1749-4c78-94eb-330c67bc7153' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([6.59])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>seq_num</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>int64</div><div class='xr-var-preview xr-preview'>1</div><input id='attrs-1a9dbddd-3bae-4369-ba9b-64082f8f79c4' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-1a9dbddd-3bae-4369-ba9b-64082f8f79c4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8f903fd0-27cd-4dba-a02d-62bcb2a11c69' class='xr-var-data-in' type='checkbox'><label for='data-8f903fd0-27cd-4dba-a02d-62bcb2a11c69' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([1])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>uid</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>&lt;U36</div><div class='xr-var-preview xr-preview'>&#x27;0eb4e35f-86db-428e-ad78-bc3d448...</div><input id='attrs-83cf618e-3161-4224-ad38-99879e42557f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-83cf618e-3161-4224-ad38-99879e42557f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7ab4e91a-c85e-4432-9764-b754d3440bad' class='xr-var-data-in' type='checkbox'><label for='data-7ab4e91a-c85e-4432-9764-b754d3440bad' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([&#x27;0eb4e35f-86db-428e-ad78-bc3d448c9f9d&#x27;], dtype=&#x27;&lt;U36&#x27;)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-a4366088-e02d-4e2a-a450-288b6fa78550' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-a4366088-e02d-4e2a-a450-288b6fa78550' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>
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

   **Total running time of the script:** ( 0 minutes  10.265 seconds)


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
