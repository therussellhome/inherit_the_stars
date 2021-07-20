#!/usr/bin/python3


"""
This file is for running the stars unit tests
and computing direct-test coverage

It overrides some deep methods inside the
unittest and coverage libraries giving it the
potential to be fragile
"""


import unittest
import pathlib
import sys

""" Coverage object """
cov = None

""" File currently under test """
coverage_filter = None

""" Root directory """
root = pathlib.Path(__file__).parent

""" Override taking credit for lines to filter out by which test is running """
def add_lines(self, line_data):
    global coverage_filter
    for f in line_data:
        if f.replace('\\', '/').split('/')[-1][:-3] == coverage_filter or not coverage_filter:
            self.add_lines_real({f: line_data[f]})

""" Override the test case run method to capture the file under test """
def test_run(self, result=None):
    global cov, coverage_filter, root
    coverage_filter = self.__class__.__module__[16:]
    self.run_real(result)
    if cov:
        cov.get_data()
    coverage_filter = None
unittest.TestCase.run_real = unittest.TestCase.run
unittest.TestCase.run = test_run

# Put restricted coverage tracking into place and run the tests
try:
    import coverage
    test_search = 'test_*.py'
    if len(sys.argv) > 1:
        test_search = 'test_' + sys.argv[1] + '.py'
    cov = coverage.Coverage(data_file=None, source=['stars'])
    cov.start()
    # Run test
    tests = unittest.TestLoader().discover(root / 'stars' / 'test', test_search, root)
    cov.get_data()
    # Install filter overrides
    cov._data.__class__.add_lines_real = cov._data.__class__.add_lines
    cov._data.__class__.add_lines = add_lines
    unittest.TextTestRunner(buffer=True, tb_locals=True).run(tests)
    # Print results
    cov.stop()
    print()
    if len(sys.argv) > 1:
        cov.report(show_missing=True, skip_covered=False, include=['stars/' + sys.argv[1] + '.py'])
    else:
        cov.report(show_missing=True, skip_covered=True, omit=['stars/ui/*', 'stars/test/*'])
# No coverage module so just run the tests
except Exception as e:
    tests = unittest.TestLoader().discover(root / 'stars' / 'test', 'test_*.py', root)
    unittest.TextTestRunner(buffer=True, tb_locals=True).run(tests)
