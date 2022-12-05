Mocking
-------
- To mock reading from a txt file we use 'patch' and 'mock_open' from unittest.mock

.. code:: python

    with patch('count_words.open'.format(__name__),
               new=mock_open(read_data=mock_file_content)) as _file:
        ret = count_words.get_text(fake_file_path)
        _file.assert_called_once_with(fake_file_path, encoding='utf-8')

'open' (builtin function) from the tested file (count_words.py) is patched with a 'new' object (mock_open).

We can check that open was launched just once with the parameters provided:
_file.assert_called_once_with(fake_file_path, encoding='utf-8')


- Example patching of 'glob'
As decorator:

.. code:: python

    @patch('count_words.glob.glob', return_value=['some/path'])

As context manager:

.. code:: python

    with patch('count_words.glob.glob', return_value=['some/path']):


Integration testing
-------
Seems it make sense to leave some write/read tests as integration tests.
