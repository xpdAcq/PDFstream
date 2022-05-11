import event_model
import numpy
import time


class DarkSubtractionError(Exception):

    pass


class DarkSubtraction(event_model.DocumentRouter):
    """Document router to do in-place background subtraction.

    Expects that the events are filled.

    The values in `(light_stream_name, field)` are replaced with ::

        np.clip(light - np.clip(dark - pedestal, 0), 0)


    Adds the key f'{self.field}_is_background_subtracted' to the
    'light_stream_name' stream and a configuration key for the
    pedestal value.


    .. warning

       This mutates the document stream in-place!


    Parameters
    ----------
    field : str
        The name of the field to do the background subtraction on.

        This field must contain the light-field values in the
        'light-stream' and the background images in the 'dark-stream'

    light_stream_name : str, optional
         The stream that contains the exposed images that need to be
         background subtracted.

         defaults to 'primary'

    dark_stream_name : str, optional
         The stream that contains the background dark images.

         defaults to 'dark'

    pedestal : int, optional
         Pedestal to add to the data to make sure subtracted result does not
         fall below 0.

         This is actually pre subtracted from the dark frame for efficiency.

         Defaults to 0.
    """
    def __init__(self,
                 field,
                 light_stream_name='primary',
                 dark_stream_name='dark',
                 pedestal=0):
        self.field = field
        self.light_stream_name = light_stream_name
        self.dark_stream_name = dark_stream_name
        self.pedestal = pedestal
        self.clear_cache()

    def clear_cache(self):
        self.light_descriptor = None
        self.dark_descriptor = None
        self.dark_frame = None
        return

    def start(self, doc):
        self.clear_cache()
        return doc

    def descriptor(self, doc):
        if self.field not in doc["data_keys"]:
            return doc
        if doc['name'] == self.light_stream_name:
            self.light_descriptor = doc['uid']
            # add flag that we did the background subtraction
            doc['data_keys'][f'{self.field}_is_background_subtracted'] = {
                'source': 'DarkSubtraction',
                'dtype': 'number',
                'shape': [],
                'precsion': 0,
                'object_name': f'{self.field}_DarkSubtraction'}
            doc['configuration'][f'{self.field}_DarkSubtraction'] = {
                'data': {'pedestal': self.pedestal},
                'timestamps': {'pedestal': time.time()},
                'data_keys': {
                    'pedestal': {
                        'source': 'DarkSubtraction',
                        'dtype': 'number',
                        'shape': [],
                        'precsion': 0,
                    }
                }
            }
            doc['object_keys'][f'{self.field}_DarkSubtraction'] = [
                f'{self.field}_is_background_subtracted']
        elif doc['name'] == self.dark_stream_name:
            self.dark_descriptor = doc['uid']
        return doc

    def event(self, doc):
        if self.field not in doc["data"]:
            return doc
        if doc['descriptor'] == self.dark_descriptor:
            self.dark_frame = doc['data'][self.field][0]
            self.dark_frame -= self.pedestal
            numpy.clip(self.dark_frame, a_min=0, a_max=None, out=self.dark_frame)
        elif doc['descriptor'] == self.light_descriptor:
            if self.dark_frame is None:
                raise DarkSubtractionError(
                    "DarkSubtraction has not received a 'dark' Event yet, so "
                    "it has nothing to subtract.")
            light = numpy.asarray(doc['data'][self.field])
            subtracted = self.subtract(light, self.dark_frame)
            doc['data'][self.field] = subtracted
            doc['data'][f'{self.field}_is_background_subtracted'] = [True]
            doc['timestamps'][f'{self.field}_is_background_subtracted'] = [time.time()]
        return doc

    def event_page(self, doc):
        return self.event(doc)

    def stop(self, doc):
        return doc

    @staticmethod
    def subtract(light, dark):
        return numpy.clip(light - dark, a_min=0, a_max=None).astype(light.dtype)
