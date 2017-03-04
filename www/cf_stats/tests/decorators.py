import os
import unittest


def slow_test(f):
    def inner(*args, **kwargs):
        expected_key = 'RUN_SLOW_TESTS'
        if expected_key not in os.environ:
            message = "Slow tests are skipped since '{s}' is not present in env variables".format(s=expected_key)
            raise unittest.SkipTest(message)
        return f(*args, **kwargs)
    return inner
