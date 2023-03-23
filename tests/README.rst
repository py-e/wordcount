Unit Tests
-------

.. role:: grey

In this branch initial test cases were:
 | - Mocked, to isolate from external dependencies (reading/writing file system in our case).  To make test cases independent (deterministic) and run really fast. :grey:`(Check mocking/README.rst for more details)`
 | - Splitted, one test is for one thing only (when the test fails, no debugging is needed to locate the problem). :grey:`(Check splitting/README.rst for more details)`
 | - Named expressly, human readable naming schema help to understand the purpose of the test case just at glance, tests grouped by naming convention. :grey:`(Check naming/README.rst for more details)`



Launch examples:

The whole file::

	python unittests_unittest.py

The class
(as unittest module, option -b to hide stdout from Code Under Test)::

	python -m unittest -b unittests_unittest.UT
	python -m unittest -b unittests_unittest.UTMockReadTxt

Single test case::

	python -m unittest -b unittests_unittest.UT.test_cleanupWordBeginning

