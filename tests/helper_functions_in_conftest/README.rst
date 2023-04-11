Examples of utils in conftest.py
-------

| If we have some helper functions for our test functions, and at some moment we want to move helpers out of the file with tests, we can do it, at least in two ways:
| - Move to a separate python file (module) and import
| - Move to conftest.py (no need to import)

| In this directory two realizations of helpers in conftest.py provided:
| - Helper class (Utils) with static method (helper_function), and fixture (utils) which return this class.
| So, we include the fixture name (utils) in the parameter list of a test function, and then we can call helper function in the test:
| utils.helper_function()

| - Create a fixure (helper_function) with definition of a inner function, and return name of the inner function.
| So, we include the fixture name (helper_function) in the parameter list of a test function, and then we can call helper function (it's a reference to the inner function):
| helper_function()
