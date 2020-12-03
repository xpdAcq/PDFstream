from configparser import ConfigParser

from bluesky.callbacks.core import CallbackBase
from databroker.core import BlueskyRun


class AnalyzerConfig(ConfigParser):
    """The base class of configuration of analyzers."""

    def read_run(self, run: BlueskyRun, source="<BlueskyRun>"):
        """Read the configuration from the analysis result in a bluesky run."""
        # see schemas for the key of configuration
        config_dct = run.metadata["start"]["an_config"]
        return self.read_dict(config_dct, source=source)


class Analyzer(CallbackBase):
    """The base class of analyzers."""

    def analyze(self, run: BlueskyRun):
        """Analyze the data in a bluesky run."""
        for name, doc in run.canonical(fill="yes"):
            # inject the original_db
            if name == "start":
                doc = doc.to_dict()
                doc["original_db"] = run.catalog_object.name
            self.__call__(name, doc)
