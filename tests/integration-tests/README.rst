Pytest - Integration Tests
-------

Advantages of pytest are the same as described in Unit Tests (see README.rst in /unit-tests directory)

It is worth noting usage of built-in fixtures:

- tmp_path - for temporary directory for test's files
- monkeypatch - to mock builtins.input
In unittest we need to create our own utils (of course patterns can be found).

Seems chain of fixtures, when the fixture function accepts another fixture(s) as parameter(s) is great for integration tests.
It helps to move what you had to do to get ready for the test outside the test itself, organize it in a logical not repeatable (but inheritance) way.

Hooks - are huge possibilities for framework update. Just one example for now in the /hook_csv_parameters directory, parameters from csv file assigned to the test at the collection stage.

In /helper_functions_in_conftest directory: two examples of helper functions (moved from file with tests to conftest.py)
