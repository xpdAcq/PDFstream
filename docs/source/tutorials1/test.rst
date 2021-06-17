Test at the beamline
====================

Installation
------------

In terminal, run::

    git clone https://github.com/xpdAcq/PDFstream.git

Create the environment::

    conda create -f env-test.yaml
    conda activate test_pdfstream

Install the diffpy.pdfgetx::

    python -m pip install <diffpy.pdfgetx-xxxx-xx-xx.whl>

The repo `PDFstream` will be cloned. Then, install `PDFstream` from the repo::

    python -m pip install -e ./PDFstream --no-deps --ignore-installed


Run servers
-----------

The configuration files are inside the `PDFstream/pdfstream/data/config_files/` folder::

    cd PDFstream/pdfstream/data/config_files/

Run the xpd server::

    run_server xpd_server_pdf_beamline.ini

Run the xpdvis server::

    run_server xpdvis_server_pdf_beamline.ini

Run the xpdsave server::

    run_server xpdsave_server_pdf_beamline.ini

The order is not important here. The servers should be running in different terminal sessions.
