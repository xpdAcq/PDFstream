#!/usr/bin/env python
import sys

import pytest

if __name__ == "__main__":
    # show local variables from every test function
    args = ['--showlocals']
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    print("pytest arguments: {}".format(args))
    # call pytest and exit with the return code from pytest so that
    # travis will fail correctly if tests fail
    a = args.copy() + ["pdfstream/tests"]
    result = pytest.main(a)
    sys.exit(result)
