import event_model
import numpy as np
import pandas as pd

from .serializerbase import SerializerBase


class CSVSerializer(SerializerBase):

    def __init__(self, folder: str = "scalar_data", **kwargs):
        super().__init__(folder)
        self._streamnames = {}  # maps descriptor uids to stream_names
        self._files = {}  # maps stream_name to file
        self._templated_file_prefix = ''
        self._start_found = False
        self._has_header = set()  # a set of uids to tell a file has a header
        kwargs.setdefault('header', True)
        kwargs.setdefault('index_label', 'time')
        kwargs.setdefault('mode', 'a')
        self._initial_header_kwarg = kwargs['header']  # to set the headers
        self._kwargs = kwargs

    def start(self, doc):
        '''Extracts `start` document information for formatting file_prefix.

        This method checks that only one `start` document is seen and formats
        `file_prefix` based on the contents of the `start` document.

        Parameters:
        -----------
        doc : dict
            RunStart document
        '''
        # raise an error if this is the second `start` document seen.
        super().start(doc)
        if self._start_found:
            raise RuntimeError(
                "The serializer in suitcase.csv expects documents from one "
                "run only. Two `start` documents where sent to it")
        else:
            self._start_found = True
        # format self._file_prefix
        self._templated_file_prefix = doc["filename"]
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
        streamname = doc.get('name')
        if streamname in ("primary", "baseline"):
            self._streamnames[doc['uid']] = streamname
        return doc

    def event_page(self, doc):
        '''Add event page document information to a ".csv" file.

        This method adds event_page document information to a ".csv" file,
        creating it if nesecary.

        .. warning::

            All non 1D 'tabular' data is explicitly ignored.

        .. note::

            The data in Events might be structured as an Event, an EventPage,
            or a "bulk event" (deprecated). The DocumentRouter base class takes
            care of first transforming the other repsentations into an
            EventPage and then routing them through here, so no further action
            is required in this class. We can assume we will always receive an
            EventPage.

        Parameters:
        -----------
        doc : dict
            EventPage document
        '''
        if doc['descriptor'] not in self._streamnames:
            return doc
        event_model.verify_filled(doc)
        streamname = self._streamnames[doc['descriptor']]
        valid_data = {}
        for field in doc['data']:
            # check that the data is 1D, if not ignore it
            if np.asarray(doc['data'][field]).ndim == 1:
                # create a file for this stream and field if required
                if streamname not in self._files.keys():
                    filename = (f'{self._templated_file_prefix}_'
                                f'{streamname}.csv')
                    self._files[streamname] = self._directory.joinpath(filename)
                # add the valid data to the valid_data dict
                valid_data[field] = doc['data'][field]
        if valid_data:
            event_data = pd.DataFrame(
                valid_data, index=doc[self._kwargs['index_label']])
            event_data['seq_num'] = doc['seq_num']

            if self._initial_header_kwarg:
                self._kwargs['header'] = streamname not in self._has_header

            filepath = self._files[streamname]
            event_data.to_csv(filepath, **self._kwargs)
            self._has_header.add(streamname)
        return doc

    def close(self):
        '''Close all of the files opened by this Serializer.
        '''
        for f in self._files.values():
            f.close()
        return

    def __enter__(self):
        return self
