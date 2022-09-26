from pdfstream.callbacks.config import Config
from pdfstream.callbacks.analysispipeline import AnalysisPipeline
from pdfstream.callbacks.visualizationpipeline import VisualizationPipeline
from pdfstream.callbacks.serializationpipeline import SerializationPipeline


# create the configuration, key words are optional
config = Config()
# read the configuration file
config.read_a_file("~/.config/acq/xpd_server.ini")
# create three pipelines
analyze = AnalysisPipeline(config)
visualize = VisualizationPipeline(config)
serialize = SerializationPipeline(config)
# choose a blue sky run in the database, here use the latest as an example
run = db[-1]
# pipe the data stream into the pipelines
for name, doc in run.documents():
    name, doc = analyze(name, doc)
    visualize(name, doc)
    serialize(name, doc)
