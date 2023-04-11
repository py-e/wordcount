Unit Tests
-------

In the 'unit-tests' branch initial test cases were:
 | - Mocked, to isolate from external dependencies (reading/writing file system in our case).  To make test cases independent (deterministic) and run really fast.
 | - Splitted, one test is for one thing only (when the test fails, no debugging is needed to locate the problem).
 | - Named expressly, human readable naming schema help to understand the purpose of the test case just at glance, tests grouped by naming convention.


Integration Tests
-------

Integration test suites created for three available commands in edit mode:

- print the base ('l1'; 'l1:wo'),
- add words to the base ('l1 add:word wood'),
- remove words ('l1 rem:word wood')

| With the right design we can work with arguments and return values in the integration tests.
| But functions of the SUT might not satisfy single responsibility principle, so we need to create tests in a hard way: simulate the input and catch the output (print statements).
| So some workarounds implemented to make testing possible.

Comments added in BDD scenarios format (GIVEN/WHEN/THEN) to help reader understand what's going on.


Pytest
-------

| Unit Tests and Integration Tests (initially unittest framework) were rewritten using pytest framework.
| Advantages:
| - Parameterization - re-usage of one function instead of many functions. Test cases are more readable.
| - Fixtures - explicit dependencies in tests what provides data or state setup to the tests.
| - Built-in fixtures - some commonly needed utils out of the box.
| - Hooks - allow to customize framework and create new features.
| - Native assert instead of unittest assert methods, no required classes.
| As result we have less testing code, this code is more readable. Almost every piece of the framework can be changed what creates a rich ecosystem with big number of helpful plugins.
| 
| Please find more details in 'pytest' branch.


Launch examples (unittest):
-------

The whole file::

	python unittest_unit_tests.py
	python unittest_integration_tests.py

The class
(as unittest module, option -b to hide stdout from Code Under Test)::

	python -m unittest -b unittest_unit_tests.UT
	python -m unittest -b unittest_unit_tests.UTMockReadTxt

Single test case::

	python -m unittest -b unittest_unit_tests.UT.test_cleanupWordBeginning
	python -m unittest -b unittest_integration_tests.ITEditBase.test_add_words


Launch examples (pytest):
-------

The whole file::

	pytest pytest_unit_tests.py
	pytest pytest_integration_tests.py

One test::

	pytest pytest_integration_tests.py::test_count_words

One nodeid::

	pytest_integration_tests.py::test_print_base[1_word]

Example of launching with marks, in 'pytest' branch ('integration-tests' dir). To launch tests with both @smoke and @integration marks::

	pytest -m "smoke and integration" pytest_integration_tests.py

