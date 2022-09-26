Beamline Scientists Documents
=============================

If you are a beamline scientist or a user who is conducting experiment at the beamline and you are using the bluesky to collect the data, here is the tutorial to setup a server that can process the data in real time.

There are three servers for data processing, visualization and exporting. They can be started in one command. They all listen to the data stream from one proxy. Usually, this proxy is running on a workstation at the beamline all the time.

I will introduce how to start the servers, and then show their functionalities.

.. toctree::
   :maxdepth: 1

   run_server
   configuration
   replay_analysis
   xpd_server
   xpdvis_server
   xpdsave_server
   zmq_proxy
   test
