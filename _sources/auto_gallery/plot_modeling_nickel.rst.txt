.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_gallery_plot_modeling_nickel.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_gallery_plot_modeling_nickel.py:


Modeling of the PDF of Ni.
==========================

A simple example of how to model a PDF using a crystal structure and a characteristic function.


.. code-block:: default

    import pdfstream.io as io
    import pdfstream.modeling as M








load the data and meta data from data file to a data parser


.. code-block:: default

    data = io.load_parser(
        "data/Ni_damped.gr",
        {"qbroad": 0.04, "qdamp": 0.02}
    )







create a crystal object using the cif file


.. code-block:: default

    crystal = io.load_crystal("data/Ni.cif")







create a recipe whose "name" is "nickel"
the fitting target is the data we loaded from the data file
the fitting range is from 2.2 A to 22.2 A with 0.01 A as step
the equation is "f * G"
"f" is the spherical characteristic function
"G" is the PDF calculated from the Ni crystal we loaded from the cif file


.. code-block:: default

    recipe = M.create(
        "nickel",
        data,
        (2.2, 22.2, 0.01),
        "f * G",
        {"f": M.F.sphericalCF},
        {"G": crystal}
    )







initialize the recipe with the fitting parameters
different initialization mode can be chosen using the key words in the function


.. code-block:: default

    M.initialize(recipe)







set the initial value of "psize" parameter in "f"


.. code-block:: default

    recipe.f_psize.setValue(25.)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    <diffpy.srfit.fitbase.parameter.Parameter object at 0x7f81bf157390>



set the lower bound of "psize"


.. code-block:: default

    recipe.f_psize.boundRange(lb=0.)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    <diffpy.srfit.fitbase.parameter.Parameter object at 0x7f81bf157390>



define what parameter to refine in each step
the parameters will be freed and refined one by one according to the order in the list


.. code-block:: default

    STEPS = [
        ("G_scale", "f_psize"),
        "G_lat",
        ("G_adp", "G_delta2")
    ]







start optimization


.. code-block:: default

    M.optimize(recipe, STEPS)







view the fitted data


.. code-block:: default

    M.view_fits(recipe)



.. image:: /auto_gallery/images/sphx_glr_plot_modeling_nickel_001.png
    :alt: nickel
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    [<AxesSubplot:title={'center':'nickel'}>]



report the fitting results


.. code-block:: default

    M.report(recipe)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Some quantities invalid due to missing profile uncertainty
    Overall (Chi2 and Reduced Chi2 invalid)
    ------------------------------------------------------------------------------
    Residual       0.00375528
    Contributions  0.00375528
    Restraints     0.00000000
    Chi2           7.32084310
    Reduced Chi2   0.00366776
    Rw             0.06128031

    Variables (Uncertainties invalid)
    ------------------------------------------------------------------------------
    G_Ni0_Biso  3.95495218e-01 +/- 1.07578822e+00
    G_a         3.52405982e+00 +/- 5.31099006e-02
    G_delta2    1.36561354e+00 +/- 2.77932977e+01
    G_scale     3.44633237e-01 +/- 6.35484141e-01
    f_psize     2.48752027e+01 +/- 4.49898950e+01

    Variable Correlations greater than 25% (Correlations invalid)
    ------------------------------------------------------------------------------
    corr(f_psize, G_scale)       -0.5780
    corr(G_delta2, G_Ni0_Biso)   0.4449
    corr(f_psize, G_delta2)      0.4182
    corr(G_scale, G_delta2)      -0.3524
    corr(f_psize, G_Ni0_Biso)    0.3171
    corr(G_scale, G_Ni0_Biso)    0.3020

    <diffpy.srfit.fitbase.fitresults.FitResults object at 0x7f81bf31fd10>



uncomment the following line to save the recipe


.. code-block:: default

    M.save(recipe, "Ni_refined", "outputs")




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    (PosixPath('outputs/Ni_refined.res'), [PosixPath('outputs/Ni_refined_nickel.fgr')], [PosixPath('outputs/Ni_refined_nickel_G.cif')])



fitting result will be saved in .res file
the fitted data will be saved in .fgr file
the refined structure will be saved in .cif file


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.269 seconds)


.. _sphx_glr_download_auto_gallery_plot_modeling_nickel.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_modeling_nickel.py <plot_modeling_nickel.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_modeling_nickel.ipynb <plot_modeling_nickel.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
