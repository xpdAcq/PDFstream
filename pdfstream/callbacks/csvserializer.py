from suitcase.csv import Serializer


class CSVSerializer(Serializer):

    def __init__(self, directory: str):
        super().__init__(directory)

    def start(self, doc):
        '''Extracts `start` document information for formatting file_prefix.
        This method checks that only one `start` document is seen and formats
        `file_prefix` based on the contents of the `start` document.
        Parameters:
        -----------
        doc : dict
            RunStart document
        '''
        if self._start_found:
            raise RuntimeError(
                "The serializer in suitcase.csv expects documents from one "
                "run only. Two `start` documents where sent to it")
        else:
            self._start_found = True
        self._templated_file_prefix = doc["filename"] + "_"
        return doc

    def descriptor(self, doc):
        '''Use `descriptor` doc to map stream_names to descriptor uid's.

        This method usess the descriptor document information to map the
        stream_names to descriptor uid's.

        Parameters:
        -----------
        doc : dict
            EventDescriptor document
        '''
        # extract some useful info from the doc
        if doc["name"] in ("primary", "baseline"):
            super().descriptor(doc)
        return doc

    def event_page(self, doc):
        if doc["descriptor"] in self._streamnames:
            super().event_page(doc)
        return doc
    