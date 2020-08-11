#!/usr/bin/env python
import sys

import pytest


def run_tests():
    """Run the tests using pytest."""
    # show local variables from every test function
    args = ['--showlocals']
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    print("pytest arguments: {}".format(args))
    # call pytest and exit with the return code from pytest so that
    # travis will fail correctly if tests fail
    a = args.copy() + ["tests"]
    result = pytest.main(a)
    sys.exit(result)


if __name__ == "__main__":
    run_tests()
