Splitting unit tests
-------
After mocking tests in tests/mocking, tests do not rely on any external resources (thus they are independent and run really fast).

Here in tests/splitting we split tests.
Each unit test should be small and test only one thing (when the test fails, no debugging is needed to locate the problem).
For each function we can simply implement a bunch of similar-looking tests to validate all possible cases.
