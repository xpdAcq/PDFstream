Replay Analysis
===============

If somehow the server doesn't output expected results because of some incident, I will show how to replay the same analysis here. You will need to run the following script in python, IPython or jupyter notebooks. This script shows how to send the data from the database to the running server.

.. literalinclude :: ../_static/replay.py
   :language: python

If you don't have the servers running, and you would like to use the data pipeline directly in a script, I recommend using the data pipeline. This is the component in the server to do the data processing. It is a bit more work but give you more freedom to program your own software.

.. literalinclude :: ../_static/pipeline.py
   :language: python
