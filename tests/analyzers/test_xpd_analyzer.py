from pkg_resources import resource_filename

import pdfstream.analyzers.xpd_analyzer as mod

fn = resource_filename("tests", "configs/xpd_server.ini")


def test_XPDAnalyzer(db_with_img_and_bg_img, tmpdir):
    raw_db = db_with_img_and_bg_img
    config = mod.XPDAnalyzerConfig()
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    config.read(fn)
    analyzer = mod.XPDAnalyzer(config)
    run = raw_db[-1]
    analyzer.analyze(run)
