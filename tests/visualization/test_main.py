import matplotlib.pyplot as plt
import pytest

import pdfstream.visualization.main as vis


@pytest.mark.parametrize(
    'keys,kwargs', [
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'legends': ['Ni0', 'Ni1'], 'label': 'gr'}),
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'stack': False}),
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'xy_kwargs': {'color': 'black'}, 'texts': ['Ni0', 'Ni1']}),
        (['Ni_gr', 'Ni_gr'], {'mode': 'line', 'colors': ['r', 'g']}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'texts': ['Ni0', 'Ni1'], 'label': 'gr'}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'stack': False}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'xy_kwargs': {'color': 'black'}}),
        (['Ni_fgr', 'Ni_fgr'], {'mode': 'fit', 'colors': ['r', 'g']})
    ]
)
def test_waterfall(test_data, keys, kwargs):
    plt.figure()
    vis.waterfall((test_data[k] for k in keys), **kwargs)
    plt.show(block=False)
    plt.close()


def test_waterfall_error(test_data):
    plt.figure()
    with pytest.raises(ValueError):
        vis.waterfall(test_data['Ni_gr'], mode="unknown")


@pytest.mark.parametrize(
    'key,kwargs', [
        ('Ni_gr', {'mode': 'line', 'text': 'Ni', 'xy_kwargs': {'color': 'black'}}),
        ('Ni_gr', {'mode': 'line', 'legends': ['Ni'], 'xy_kwargs': {'color': 'black'}}),
        ('Ni_fgr', {'mode': 'fit', 'text': 'Ni', 'xy_kwargs': {'color': 'black'}})
    ]
)
def test_visualize(test_data, key, kwargs):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    vis.visualize(test_data[key], ax=ax, **kwargs)
    plt.show(block=False)
    plt.close()
