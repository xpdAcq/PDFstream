ZMQ Proxy
=========

The proxy works like a bridge between your data acquisition program and the server.
It receives the data from the data acquisition and send it to the server.

Start the proxy
^^^^^^^^^^^^^^^

Before you start the server, you need to start the proxy first. The proxy is a server that transfers the message
from the bluesky RunEngine to the server. Without proxy, the server cannot receive any data from the experiments.

To start a proxy, in terminal, run the following command::

    bluesky-0MQ-proxy 5567 5568

The ``5567`` is the port where the proxy receives the message and the ``5568`` is the port where the proxy sends
the message to. You can change the values according to the machine you are using.

Please remember the two ports because they are needed when you set up the server. Please also remember the
address of the machine where you run the proxy if you are running server on a different machine.

If you would like to terminate the proxy, press ``CTRL + C`` in the terminal.

Run the proxy in background
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are tired of running the command very time, you can run the proxy in background and detach it with the
terminal::

    nohup bluesky-0MQ-proxy 5567 5568 &

You will find some text showing up, press ``CTRL + C`` to end it. It won't terminate the proxy. Then, close the
terminal and the proxy will keep running in the background.

To terminate this proxy, in terminal, run command::

    kill <job ID>

The ``<job ID>`` is a number that shows up after you run the command ``nohup bluesky-0MQ-proxy 5567 5568 &``.
