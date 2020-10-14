import itertools
from bluesky.callbacks import CallbackBase


class StripDepVar(CallbackBase):
    """Strip the dependent variables from a data stream. This creates a
    stream with only the independent variables, allowing the stream to be
    merged with other dependent variables (including analyzed data)"""

    def __init__(self):
        super().__init__()
        self.independent_vars = set()

    def start(self, doc):
        self.independent_vars = set(
            itertools.chain.from_iterable(
                [n for n, s in doc.get("hints", {}).get("dimensions", [])]
            )
        )

    def descriptor(self, doc):
        new_doc = dict(doc)

        # Step 1 determine which configuration and object keys to keep
        throw_out_keys = set()
        for k, v in new_doc["object_keys"].items():
            # If they share any keys then keep this component, it serves up
            # independent vars
            if not self.independent_vars & set(v):
                throw_out_keys.add(k)

        for k in ["hints", "configuration", "object_keys"]:
            new_doc[k] = dict(doc[k])
            for key in throw_out_keys:
                new_doc[k].pop(key, None)

        for k in self.independent_vars ^ set(new_doc["data_keys"]):
            new_doc["data_keys"].pop(k, None)
        return new_doc

    def event(self, doc):
        # make copies
        new_doc = dict(doc)
        new_doc["data"] = dict(doc["data"])
        new_doc["timestamps"] = dict(doc["timestamps"])
        data_keys = set(new_doc["data"].keys())
        # all the things not in
        for key in self.independent_vars ^ data_keys:
            new_doc["data"].pop(key, None)
            new_doc["timestamps"].pop(key, None)
            new_doc.get("filled", {}).pop(key, None)
        return new_doc
