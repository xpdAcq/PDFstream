XPD Analyzer
============

This analyzer processes the x-ray powder diffraction images and yields pair distribution function data.
It is basically a wrapper of the core of the XPD server and thus its functionality is the same as the XPD server.
The only difference is that the XPD server receives data from the messages sent by a proxy
while the analyzer takes data from a database entry.
If you would like to know what the analyzer does and what input and output look like,
please see :ref:`xpd_server`.
