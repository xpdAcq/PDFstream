import pdfstream.utils.wrappers as wrappers


def test_report_stage(capsys):
    def func():
        return

    wrapped_func = wrappers.report_stage(func)
    wrapped_func()
    captured = capsys.readouterr()
    assert captured.out == "start func\nfinish func\n"


def test_take_in_namespace():
    def func(arg0, **kwargs):
        return locals()

    wrapped_func = wrappers.take_in_namespace(func)
    assert wrapped_func({'arg0': 0, 'arg1': 1}) == {'arg0': 0, 'arg1': 1}
