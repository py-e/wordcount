Naming unit tests
-------
The intent of a unit test should be clear, so we can use human readable naming schema where the test name describes what we want to test.
Test cases can be grouped into Test Groups or Test Suites.
Let's group our tests by CamelCase naming (to distinguish from other words describing the test), one group is related to one function.

Example, tests for cleanup_beginning function which remove symbols (not letters) only at the beginning of the word, like '("robots' -> 'robots':

.. list-table::
   :widths: 25 25 50

   * - test_cleanupWordBeginning
     - main functionality check, processing
     - input: '-15:recursion', expected output: 'recursion'
   * - test_cleanupWordBeginning_clean_word
     - no processing
     - input: 'recursion', expected output: 'recursion'
   * - test_cleanupWordBeginning_symbol_inside
     - no processing
     - input: 'recur-sion', expected output: 'recur-sion'
   * - test_cleanupWordBeginning_symbol_at_the_end
     - no processing
     - input: 'recursion-#7;', expected output: 'recursion-#7;'
