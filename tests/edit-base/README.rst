Integration tests (for edit mode functionality of the application)

| Notice, for now functions of the SUT are not ideal in terms of design.
| For example, if we look at the edit_base function (starting point) it does not satisfy the single responsibility principle, inside the function placed both input and command detection. Of course it's better to refactor the code, make decomposition so one function processes the input and return the value which is sent to the next function as an argument.
| With the right design we can work with arguments and return values in the integration tests.
| But let's pretend we cannot change the design, so we need to create tests in a hard way: simulate the input and catch the print statements.
| So some workarounds were implemented to make testing possible.

Comments in BDD scenarios format (GIVEN/WHEN/THEN) seem reasonable and help to understand what’s going on.

Run application in edit mode:
python count_words.py -e

Integration test suites created for three available commands:

- print the base ('l1'; 'l1:wo'),
- add words to the base ('l1 add:word wood'),
- remove words ('l1 rem:word wood')

Launch examples:

Run all integration tests::

    python unittest_integration_tests.py

Run one test::

    python -m unittest unittest_integration_tests.ITEditBase.test_add_words -b
