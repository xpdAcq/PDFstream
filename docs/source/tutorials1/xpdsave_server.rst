XPDSave Server
==============

The XPDSave server is the server that save the data from the XPD server. If users would like to separate the
data processing with the data exporting, they could run the XPDSave server together with the XPD server on
the same or different machine.

How to setup a XPDSave Server?
------------------------------

There are only two steps: first, write a configuration file or download one; start a server in terminal using
that file.

Write the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The server needs a .ini file. This file contains all the configuration to build a server. An example of the file
is shown below. Please read the comments in the file to know what are the meaning of the parameters.

.. include:: ../_static/xpdsave_server.ini
   :literal:

The parameters you can change are the values that behind the equity symbol in each row. Usually, you don't need
to change the file structure but if you would like to do that, you can find what file structure is supported
`here <https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_.

Start the server
^^^^^^^^^^^^^^^^

Assume that you have written a configuration file and the path to it is "~/xpd_server.ini".

In terminal, run the command::

    run_server ~/xpdsave_server.ini

The server will start in terminal.

If you would like to terminate the server, press ``CTRL + C``.

(Recommended) Put the configuration file in default folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are tired of typing the path to the configuration file, you can put the .ini file in the default folder,
the software will find the configuration file for the server according to the name parameter in the
configuration file.

To know where the default configuration folder is, run the command::

    print_server_config_dir

You will find the path to the directory. Put the .ini file in that directory and then you can just run::

    run_server xpdsave_server

The server will start.

(Optional) Run the server in a detached background process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to what you have done with the proxy, you can also run the server in background and detach it from the
terminal so that you don't need to start the server every time. To do this, in terminal, run command::

    nohup run_server ~/xpdsave_server.ini &

If you have put the "xpd_server.ini" in default folder, run this instead::

    nohup run_server xpdsave_server &

You will find the message from the server in file "nohup.out".

If you would like to terminate the background process, in terminal, run command::

    kill <job ID>

The ``<job ID>`` is a number that shows up after you run the command ``nohup run_server xpd &``.
