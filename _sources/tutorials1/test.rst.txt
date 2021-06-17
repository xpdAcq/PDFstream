===========================
Beamline Scientist Document
===========================

Test at the beamline
--------------------

In terminal, run::

    git clone https://github.com/xpdAcq/PDFstream.git

The repo `pdfstream` will be cloned. Then, install `pdfstream` from the repo::

    python -m pip install ./pdfstream --no-deps --ignore-installed --prefix ~/test_pdfstream

The directoty `~/test_pdfstream` is where the package will be installed.

Run the command line using environment variable `PYTHONPATH`::

    export PYTHONPATH=~/test_pdfstream/lib/python3.8/site-packages/:$PYTHONPATH

Run the server::

    run_server xpd ./pdfstream/pdfstream/data/config_files/xpd_server_pdf_beamline.ini

