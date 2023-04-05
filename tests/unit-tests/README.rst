Pytest - Unit Tests
-------

Unit tests rewritten for the pytest framework, and obvious benefits are:

- Less code - 484 lines (unittest file) vs 282 lines (pytest file).
- Parameterization - re-usage of one function instead of many functions.
- Fixtures - provides the separation of "getting ready for" and "cleaning up after" code from the test functions: to focus the test on what is actually testing, not on what is necessary to get ready for the test.
|
| **Example of the parameterization.**
| One function with parameters looks good. It's readable, new cases can be added right at the place.
| No need to create new test functions and repeat code (launch and assert) again and again.
| Nodeid of pytest, like test_cleanup_beginning[clean_word] as informative as test name in unittetst test_cleanupWordBeginning_clean_word. And can be easily extended in id value, without enlargement of the test function name.

.. code-block:: python

	# pytest
	# four lines with values 'send data', 'expected return data' and 'name' are self explaining
	# at first glance you can get the idea
	p_cleanup_beginning = (
		pytest.param('-15:recursion', 'recursion',      id='symbol_at_the_beginning'),
		pytest.param('recursion', 'recursion',          id='clean_word'),
		pytest.param('recur-sion', 'recur-sion',        id='symbol_inside'),
		pytest.param('recursion-#7;', 'recursion-#7;',  id='symbol_at_the_end'))
	@pytest.mark.parametrize('send, exp', p_cleanup_beginning)
	def test_cleanup_beginning(send, exp):
		ret = count_words.cleanup_beginning(send)
		assert exp == ret

.. code-block:: python

    # unittest
    # need to scroll down all four tests, look at the test name and variables
    # need more attention to get the idea
    def test_cleanupWordBeginning(self):
        word = 'recursion'
        word_to_cleanup = '-15:'+word
        ret = count_words.cleanup_beginning(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

    def test_cleanupWordBeginning_clean_word(self):
        word = 'recursion'
        ret = count_words.cleanup_beginning(word)
        self.assertEqual(word, ret, f'The same clean "{word}" is expected after cleanup')

    def test_cleanupWordBeginning_symbol_inside(self):
        word = 'recur-sion'
        ret = count_words.cleanup_beginning(word)
        self.assertEqual(word, ret, f'Not changed "{word}" is expected after cleanup')

    def test_cleanupWordBeginning_symbol_at_the_end(self):
        word = 'recursion'
        word_to_cleanup = word+'-#7;'
        ret = count_words.cleanup_beginning(word_to_cleanup)
        self.assertEqual(word_to_cleanup, ret, f'"{word_to_cleanup}" not clean at the end is expected after cleanup')



| **Example of moving preparation code to fixtures.**
| At the test itself we can find only things that are related: parameters, launch and assert.
| If we look through AAA (Arrange, Act and Assert) pattern, we can concentrate on Act and Assert. When we look at the test, no need to read code which create mocks for example, we just look at the input data in launch and output data in assert.

.. code-block:: python

    # pytest
    # there are just two lines of code inside test definition
    # ACT: launch of the SUT function with mock_file (parameter)
    # ASSERT: expected (parameter) and returned value of SUT function
    @pytest.mark.parametrize('mock_file, expected', [[
        """hello unit test

    and more""",
        'hello unit test  and more']],
                             indirect=['mock_file'],
                             ids=['file_with_5_words'])
    def test_mock_read_text_from_file(mock_file, expected):
        ret = count_words.get_text(mock_file)
        assert expected == ret


    @pytest.mark.parametrize('mock_file, expected', [[
        'cell\ncadmium\n',
        ['cell', 'cadmium']]],
                             indirect=['mock_file'],
                             ids=['file_2_words'])
    def test_mock_get_words_from_txt(mock_glob, mock_file, expected):
        ret = count_words.get_words_from_txt('l2')
        assert expected == ret

    FAKE_FILE_PATH = 'some/mock/path'
    @pytest.fixture
    def mock_file(request):
        with patch('count_words.open', new=mock_open(read_data=request.param)) as _file:
            yield FAKE_FILE_PATH

            # Additional check (that the object was called only one time)
            try:
                _file.assert_called_once_with(FAKE_FILE_PATH, encoding='utf-8')
            except AssertionError as e:
                if 'expected call not found' in str(e) and 'utf-8' in str(e):
                    _file.assert_called_once_with(FAKE_FILE_PATH)
                else:
                    raise e


    @pytest.fixture
    def mock_glob():
        with patch('count_words.glob.glob', return_value=[FAKE_FILE_PATH]) as _file:
            yield



.. code-block:: python

    # unittest
    # ARRANGE step: mocking is inside - need some time to understand what is going on
    # (of course it might be improved by helper functions)
    def test_mock_read_text_from_file(self):
        mock_file_content = """hello unit test

                and more
                """
        fake_file_path = 'some/mock/path'
        with patch('count_words.open',
                   new=mock_open(read_data=mock_file_content)) as _file:
            ret = count_words.get_text(fake_file_path)
            _file.assert_called_once_with(fake_file_path, encoding='utf-8')

        expected_list_of_words = mock_file_content.split()
        ret_list_of_words = ret.split()
        self.assertListEqual(expected_list_of_words, ret_list_of_words,
                             f'\nExpected words from file: {expected_list_of_words}')


    @patch('count_words.glob.glob', return_value=['path/to/c.txt'])
    def test_mock_get_words_from_txt(self, mock_glob):
        mock_file_content = 'cell\ncadmium\n'
        expected = ['cell', 'cadmium']
        file_path = 'path/to/c.txt'

        with patch('count_words.open',
                   new=mock_open(read_data=mock_file_content)) as _file:
            ret = count_words.get_words_from_txt('l2')
            _file.assert_called_once_with(file_path)

        self.assertCountEqual(expected, ret, f'\nExpected words from the base: {expected}')
