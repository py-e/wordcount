import sys
import os
import shutil
import unittest
from unittest.mock import patch, mock_open

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import count_words


class UT(unittest.TestCase):
    """
    Unit tests suite.
    Test cases for the functions in count_words.py.
    """

    def test_cleanupWordBeginning(self):
        """count_words.cleanup_beginning(word)"""
        word = 'recursion'
        word_to_cleanup = '-15:'+word
        ret = count_words.cleanup_beginning(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

    def test_cleanupWordBeginning_clean_word(self):
        """count_words.cleanup_beginning(word)
        Clean word"""
        word = 'recursion'
        ret = count_words.cleanup_beginning(word)
        self.assertEqual(word, ret, f'The same clean "{word}" is expected after cleanup')

    def test_cleanupWordBeginning_symbol_inside(self):
        """count_words.cleanup_beginning(word)
        Symbol inside (not at the beginning)"""
        word = 'recur-sion'
        ret = count_words.cleanup_beginning(word)
        self.assertEqual(word, ret, f'Not changed "{word}" is expected after cleanup')

    def test_cleanupWordBeginning_symbol_at_the_end(self):
        """count_words.cleanup_beginning(word)
        Symbol at the end (not at the beginning)"""
        word = 'recursion'
        word_to_cleanup = word+'-#7;'
        ret = count_words.cleanup_beginning(word_to_cleanup)
        self.assertEqual(word_to_cleanup, ret, f'"{word_to_cleanup}" not clean at the end is expected after cleanup')

    def test_cleanupWordEnd(self):
        """count_words.cleanup_end(word)"""
        word = 'recursion'
        word_to_cleanup = word+'-#7;'
        ret = count_words.cleanup_end(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

    def test_cleanupWordEnd_clean_word(self):
        """count_words.cleanup_end(word)
        Clean word"""
        word = 'recursion'
        ret = count_words.cleanup_end(word)
        self.assertEqual(word, ret, f'The same clean "{word}" is expected after cleanup')

    def test_cleanupWordEnd_symbol_inside(self):
        """count_words.cleanup_end(word)
        Symbol inside (not at the end)"""
        word = 'recur-sion'
        ret = count_words.cleanup_end(word)
        self.assertEqual(word, ret, f'Not changed "{word}" is expected after cleanup')

    def test_cleanupWordEnd_symbol_at_the_end(self):
        """count_words.cleanup_end(word)
        Symbol at the beginning (not at the end)"""
        word = 'recursion'
        word_to_cleanup = '-15:'+word
        ret = count_words.cleanup_end(word_to_cleanup)
        self.assertEqual(word_to_cleanup, ret, f'"{word_to_cleanup}" not clean at the beginning is expected after cleanup')

    def test_cleanup_word(self):
        """count_words.cleanup_word(word)

        Sort of integration test: launch other modules (cleanup_beginning, cleanup_end)
        """
        word = 'recursion'
        word_to_cleanup = '-15:'+word+'-#7;'
        ret = count_words.cleanup_word(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

    """
    print_totals(words)
    print statements
    """

    def sort_and_exclude_helper(self):
        """
        Data format:  key: word; value: [frequency, list, variants, index]
        """
        def check_results(expected_order, ret_sorted_words):
            for e, key in enumerate(ret_sorted_words):
                self.assertEqual(expected_order[e], key, f'Expected: {expected_order[e]}')
                self.assertEqual(e + 1, ret_sorted_words[key][3], f'Expected index: {e + 1}')

        words = {'one':     [1, '(in top 100)', '', ''],
                 'ten':     [10, '(from 100 to 1000)', '', ''],
                 'fifteen': [15, '', '(1 with s: fifteens)', ''],
                 'two':     [2, '(in top 100)', '', ''],
                 'eighty':  [80, '(l1)', '', ''],
                 'twice':   [2, '(from 100 to 1000)', '', '']}
        return words, check_results

    def test_dataSortAndExclude_sort_only(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) only
        """
        words, check_results = self.sort_and_exclude_helper()
        expected_order = ['eighty', 'fifteen', 'ten', 'two', 'twice', 'one']
        ret_sorted_words = count_words.sort_and_exclude(words)
        check_results(expected_order, ret_sorted_words)

    def test_dataSortAndExclude_sort_and_exclude(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) & exclude
        """
        words, check_results = self.sort_and_exclude_helper()
        expected_order = ['fifteen', 'ten', 'twice']
        ret_sorted_words = count_words.sort_and_exclude(words, ['(in top 100)', '(l1)'])
        check_results(expected_order, ret_sorted_words)

    def test_dataSortAndExclude_sort_only_empty(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) only
        No words - return empty dict
        """
        words = {}
        ret_sorted_words = count_words.sort_and_exclude(words)
        self.assertEqual(words, ret_sorted_words, f'Expected: empty dict')

    def test_dataSortAndExclude_sort_and_exclude_empty(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) & exclude
        No words - return empty dict
        """
        words = {}
        ret_sorted_words = count_words.sort_and_exclude(words, ['(in top 100)', '(l1)'])
        self.assertEqual(words, ret_sorted_words, f'Expected: empty dict')

    def test_dataSortAndExclude_sort_only_wrong_type_int_instead_str(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) only
        int instead of str (word)
        """
        words = {1: [1, '', '', '']}
        ret_sorted_words = count_words.sort_and_exclude(words)
        self.assertEqual(words, ret_sorted_words, f'Expected: int returned')

    def test_dataSortAndExclude_sort_only_wrong_type_int_instead_list(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) only
        int instead of list
        """
        words = {'word': 1}
        try:
            ret_sorted_words = count_words.sort_and_exclude(words)
        except TypeError as e:
            exc_message = e
        finally:
            self.assertEqual("'int' object is not subscriptable", exc_message.args[0],
                             f'Expected: TypeError (int instead of list)')

    def test_dataSortAndExclude_wrong_exclude_value(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) & exclude
        Wrong (not existing) exclude value
        """
        words = {'word': [1, '', '', ''], 'and': [5, '', '', '']}
        expected_order = ['and', 'word']
        ret_sorted_words = count_words.sort_and_exclude(words, ['(no such value)'])
        self.assertListEqual(expected_order, list(ret_sorted_words))

    def test_dataSortAndExclude_wrong_signature(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort (by frequency) & exclude
        Wrong signature
        """
        words = {'word': [1, '', '', '']}
        try:
            ret_sorted_words = count_words.sort_and_exclude(words, ['(in top 100)', '(l1)'], 'unexpected value')
        except TypeError as e:
            self.assertEqual('sort_and_exclude() takes from 1 to 2 positional arguments but 3 were given', e.args[0])

    """
    print_sorted_by_number(words)
    Launch sort_and_exclude and print results
    """

    def test_countWord_from_top1000_once(self):
        """
        count_words.add_to_counter(w, words_counter, l1, l2)
        Add once (word in list)
        """
        word = 'word'
        l1 = [word, 'test', 'debug']
        l2 = ['prerequisite', 'snippet']
        words_counter = {}
        count_words.add_to_counter(word, words_counter, l1, l2)
        self.assertEqual(1, words_counter[word][0], f'"{word}" was added once')
        for key in words_counter:
            self.assertEqual(word, key, f'"{word}" was added')
            self.assertEqual('(from 100 to 1000)', words_counter[key][1], 'Expect: word in list')

    def test_countWord_from_top1000_twice(self):
        """
        count_words.add_to_counter(w, words_counter, l1, l2)
        Add two times (word in list)
        """
        word = 'word'
        l1 = [word, 'test', 'debug']
        l2 = ['prerequisite', 'snippet']
        words_counter = {}
        count_words.add_to_counter(word, words_counter, l1, l2)
        count_words.add_to_counter(word, words_counter, l1, l2)
        self.assertEqual(2, words_counter[word][0], f'"{word}" was added two times')
        for key in words_counter:
            self.assertEqual(word, key, f'"{word}" was added')
            self.assertEqual('(from 100 to 1000)', words_counter[key][1], 'Expect: word in list')

    def test_countWord_once(self):
        """
        count_words.add_to_counter(w, words_counter, l1, l2)
        Add once (word NOT in list)
        """
        word = 'wordnotinlist'
        l1 = ['test', 'debug']
        l2 = ['prerequisite', 'snippet']
        words_counter = {}
        count_words.add_to_counter(word, words_counter, l1, l2)
        self.assertEqual(1, words_counter[word][0], f'"{word}" was added once')
        for key in words_counter:
            self.assertEqual(word, key, f'"{word}" was added')
            self.assertEqual('', words_counter[key][1], 'Expect: word out of lists')

    """
    recount_variants(words, variants)
    Launched in count_forms(), count_apostrophes()
    """

    def test_count_apostrophes(self):
        """
        count_words.count_apostrophes(words)
        Kind of integration test: count_apostrophes launches recount_variants

        Checking ending: "'s"
        """
        words = {'moss': [1, '', '', ''], "moss's": [1, '', '', '']}
        count_words.count_apostrophes(words)
        self.assertEqual(1, len(words), "2 forms collapsed to 1: moss <- moss's")
        self.assertEqual(2, words['moss'][0], "2 - is expected number for: moss")

    def test_count_forms(self):
        """
        count_words.count_forms(words)
        Kind of integration test: count_forms launches recount_variants

        Checking endings: 's', 'es', 'ed', 'd', 'ing'
        """
        words = {'word': [1, '(from 100 to 1000)', '', ''], 'words': [1, '', '', ''], 'worded': [1, '', '', ''],
                 'wording': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '4 forms collapsed to 1: word <- words, worded, wording')
        self.assertEqual(4, words['word'][0], '4 - is expected number for: word')

        words = {'moss': [1, '', '', ''], 'mosses': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '2 forms collapsed to 1: moss <- mosses')
        self.assertEqual(2, words['moss'][0], '2 - is expected number for: moss <- mosses')

        words = {'observe': [1, '', '', ''], 'observed': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '2 forms collapsed to 1: observe <- observed')
        self.assertEqual(2, words['observe'][0], '2 - is expected number for: observe')

    """
    print_sizes(sizes)
    print statements
    """

    def test_sizeOfWords_1_word_1_symbol(self):
        """
        count_words.size_of_words(words)
        Simple test: one word counted
        """
        words = {'a': [1, '(in top 100)', '', 1]}
        expected_sizes = {1: [['a'], 1]}
        ret_sizes = count_words.size_of_words(words)
        self.assertEqual(expected_sizes, ret_sizes, f'Expected: {expected_sizes}')

    def test_sizeOfWords_2_words_3_symbols_each(self):
        """
        count_words.size_of_words(words)
        Check that two words of the same size (3) counted
        """
        words = {'dot': [2, '', '', 1],
                 'ten': [1, '(from 100 to 1000)', '', 2]}
        expected_sizes = {3: [['dot', 'ten'], 2]}
        ret_sizes = count_words.size_of_words(words)
        self.assertEqual(expected_sizes, ret_sizes, f'Expected: {expected_sizes}')

    def test_sizeOfWords_2_words_1_and_15_symbols(self):
        """
        count_words.size_of_words(words)
        Check that two words of the different size are counted
        """
        words = {'a': [1, '(in top 100)', '', 1],
                 'objectification': [1, '', '', 2]}
        expected_sizes = {1: [['a'], 1], 15: [['objectification'], 1]}
        ret_sizes = count_words.size_of_words(words)
        self.assertEqual(expected_sizes, ret_sizes, f'Expected: {expected_sizes}')

    def test_findWordInDataStructureByIndex_one_word(self):
        """
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add):
        Adding word by index (2 from list_words) to the set of words (words_to_add)
        """
        list_words = ['one', 'two', 'three']
        words_to_add = set()

        indexes_to_add = {2}
        # expected_words = [word for e, word in enumerate(list_words, 1) if e in indexes_to_add]  # Not readable...
        expected_words = ['two']
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertCountEqual(expected_words, words_to_add,
                              f'Expected word is added: {expected_words}')

    def test_findWordInDataStructureByIndex_two_words(self):
        """
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add):
        Adding words by multiple indexes (2, 3 from list_words) to the set of words (words_to_add)
        """
        list_words = ['one', 'two', 'three']
        words_to_add = set()

        indexes_to_add = {2, 3}
        # expected_words = [word for e, word in enumerate(list_words, 1) if e in indexes_to_add]  # Not readable...
        expected_words = ['two', 'three']
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertCountEqual(expected_words, words_to_add,
                              f'Expected: {len(expected_words)} words added: {expected_words}')

    def test_findWordInDataStructureByIndex_index_out_of_range(self):
        """
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add):
        Trying to add word, but index is out of range (0 not in range: 1, 2, 3)
        """
        list_words = ['one', 'two', 'three']
        words_to_add = set()

        indexes_to_add = {0}
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertFalse(words_to_add, f'Expected: nothing added')

    def test_findWordInDataStructureByIndex_index_not_int(self):
        """
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add):
        Trying to add word while index is not int
        """
        list_words = ['one', 'two', 'three']
        words_to_add = set()

        indexes_to_add = {0.5}
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertFalse(words_to_add, f'Expected: nothing added')

    """
    add_to_base(base, str_elements, words=None)
    Launch next functions:
    get_words_by_indexes
    word_in_base
    write_to_base
    """

    """
    main()
    Starting point
    """


class UTMockReadTxt(unittest.TestCase):
    """
    Unit tests suite with mocking read file functionality.
    Test cases for the functions (with data read from file) in count_words.py.
    """

    def test_mock_read_text_from_file(self):
        """count_words.get_text()"""
        mock_file_content = """hello unit test

                and more
                """
        fake_file_path = 'some/mock/path'
        with patch('count_words.open',
                   new=mock_open(read_data=mock_file_content)) as _file:
            ret = count_words.get_text(fake_file_path)
            _file.assert_called_once_with(fake_file_path, encoding='utf-8')

        expected_list_of_words = mock_file_content.split()
        # expected_list_of_words.append('opened')
        ret_list_of_words = ret.split()
        self.assertListEqual(expected_list_of_words, ret_list_of_words,
                             f'\nExpected words from file: {expected_list_of_words}')

    @patch('count_words.glob.glob', return_value=['path/to/c.txt'])
    def test_mock_get_words_from_txt(self, mock_glob):
        """
        count_words.get_words_from_txt(base)

        Check that all words from l2 base returned by the tested function.
        """
        base = 'l2'
        all_words = ['cell', 'cadmium']
        mock_file_content = 'cell\ncadmium\n'
        file_path = 'path/to/c.txt'

        with patch('count_words.open',
                   new=mock_open(read_data=mock_file_content)) as _file:
            ret = count_words.get_words_from_txt(base)
            _file.assert_called_once_with(file_path)

        self.assertCountEqual(all_words, ret, f'\nExpected words from the base: {all_words}')

    @staticmethod
    # https://gist.github.com/adammartinez271828/137ae25d0b817da2509c1a96ba37fc56
    def multi_mock_open(*file_contents):
        """Create a mock "open" that will mock open multiple files in sequence
        Args:
            *file_contents ([str]): a list of file contents to be returned by open
        Returns:
            (MagicMock) a mock opener that will return the contents of the first
                file when opened the first time, the second file when opened the
                second time, etc.
        """
        mock_files = [mock_open(read_data=content).return_value for content in file_contents]
        mock_opener = mock_open()
        mock_opener.side_effect = mock_files

        return mock_opener

    def test_mock_get_words_from_2_txt_files(self):
        """
        count_words.get_words_from_txt(base)

        Check that all words from l2 base returned by the tested function.
        """
        base = 'l2'
        files = (['cell', 'cadmium'], ['velocity'])

        base_dir = os.path.join(count_words.PATH_TO_BASE, base)
        input_words = []
        expected_words = []
        file_paths = []
        for file in files:
            file_name = file[0][0] + '.txt'
            file_path = os.path.join(base_dir, file_name)
            file_paths.append(file_path)
            words_in_file = ''
            for word in file:
                words_in_file += word+'\n'
                expected_words.append(word)
            input_words.append(words_in_file)

        with patch('count_words.glob.glob', return_value=file_paths):
            with patch('count_words.open',
                       new=UTMockReadTxt.multi_mock_open(*input_words)) as _file:
                ret = count_words.get_words_from_txt(base)

        self.assertCountEqual(expected_words, ret, f'\nExpected words from the base: {expected_words}')


if __name__ == '__main__':
    unittest.main(buffer=True)
