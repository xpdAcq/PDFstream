import matplotlib.pyplot as plt
import pytest

import pdfstream.visualization.main as vis


@pytest.mark.parametrize(
    'data_keys,kwargs', [
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'legends': ['Ni0', 'Ni1']}),
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'stack': False}),
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'xy_kwargs': {'color': 'black'}, 'texts': ['Ni0', 'Ni1']}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'texts': ['Ni0', 'Ni1']}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'stack': False}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'xy_kwargs': {'color': 'black'}})
    ]
)
def test_waterfall(db, data_keys, kwargs):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    vis.waterfall((db[k] for k in data_keys), ax=ax, **kwargs)
    plt.show(block=False)


@pytest.mark.parametrize(
    'data_key,kwargs', [
        ('Ni_gr', {'mode': 'line', 'text': 'Ni', 'xy_kwargs': {'color': 'black'}}),
        ('Ni_gr', {'mode': 'line', 'legend': 'Ni', 'xy_kwargs': {'color': 'black'}}),
        ('Ni_fgr', {'mode': 'fit', 'text': 'Ni', 'xy_kwargs': {'color': 'black'}})
    ]
)
def test_visualize(db, data_key, kwargs):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    vis.visualize(db[data_key], ax=ax, **kwargs)
    plt.show(block=False)
