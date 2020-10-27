import asyncio
import sys

_QT_KICKER_INSTALLED = {}


def install_qt_kicker(loop=None, update_rate=0.03):
    """Install a periodic callback to integrate Qt and asyncio event loops.

    If a version of the Qt bindings are not already imported, this function
    will do nothing.

    It is safe to call this function multiple times.

    Parameters
    ----------
    loop : event loop, optional
    update_rate : number
        Seconds between periodic updates. Default is 0.03.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    global _QT_KICKER_INSTALLED
    if loop in _QT_KICKER_INSTALLED:
        return
    if not any(p in sys.modules for p in ['PyQt4', 'pyside', 'PyQt5']):
        return
    import matplotlib.backends.backend_qt5
    from matplotlib.backends.backend_qt5 import _create_qApp
    from matplotlib._pylab_helpers import Gcf

    _create_qApp()
    qApp = matplotlib.backends.backend_qt5.qApp

    try:
        _draw_all = Gcf.draw_all  # mpl version >= 1.5
    except AttributeError:
        # slower, but backward-compatible
        def _draw_all():
            for f_mgr in Gcf.get_all_fig_managers():
                f_mgr.canvas.draw_idle()

    def _qt_kicker():
        # The RunEngine Event Loop interferes with the qt event loop. Here we
        # kick it to keep it going.
        _draw_all()

        qApp.processEvents()
        loop.call_later(update_rate, _qt_kicker)

    _QT_KICKER_INSTALLED[loop] = loop.call_soon(_qt_kicker)
