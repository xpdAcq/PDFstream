Run Servers in One Command
==========================

Start the server
----------------

I assume that you have written a configuration file and the path to it is "~/xpd_server.ini". If you haven't, here is an example of the configuration file.

.. literalinclude:: _static/pdf_beamline.ini
   :text:

You will find more details about the parameters in the other chapters of the servers. Here, I only show how to use it start a server.

In terminal, run the command::

    run_server ~/xpd_server.ini

The server will start in terminal.

If you would like to terminate the server, press ``CTRL + C``.

(Recommended) Put the configuration file in default folder
----------------------------------------------------------

If you are tired of typing the path to the configuration file, you can put the .ini file in the default folder,
the software will find the configuration file for the server according to the name parameter in the
configuration file.

To know where the default configuration folder is, run the command::

    print_server_config_dir

You will find the path to the directory. Put the .ini file in that directory and then you can just run::

    run_server xpd_server

The server will start.

(Optional) Run the server in a detached background process
----------------------------------------------------------

Similar to what you have done with the proxy, you can also run the server in background and detach it from the terminal so that you don't need to start the server every time. To do this, in terminal, run command::

    nohup run_server ~/xpd_server.ini &

If you have put the "xpd_server.ini" in default folder, run this instead::

    nohup run_server xpd_server &

You will find the message from the server in file "nohup.out".

If you would like to terminate the background process, in terminal, run command::

    kill <job ID>

The ``<job ID>`` is a number that shows up after you run the command ``nohup run_server xpd &``.

You can also use other command like `tmux` to make a terminal session detached.
