Hook example - read parameters from csv
-------

| If we need to separate code and test data, we can move parameters of the tests to its own files (csv format seems appropriate).
| To achieve this a pytest hook called pytest_generate_tests() is used (from collection hooks).
| For each test_name we load test_name.csv.

| csv format info:
| delimiter: semicolon (comma is used in base_files column)
| Rows
| - first row: indirect marker for parameter (two values: None/'indirect')
| - second row: header (parameter names, first item is not parameter name but id)
| - the rest is test data

To get base_files value right as tuple instead of str, ast module is used.

Custom exception with extended message is provided for the case when a csv file is not found.


This hook (local plugin) is created just as an example, of course it makes sense to look at the available plugins (for pytest parameterization in PyPI) first.
