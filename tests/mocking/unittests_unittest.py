import sys
import os
import shutil
import unittest
from unittest.mock import patch, mock_open

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import count_words


class UT(unittest.TestCase):
    """
    Unit tests draft.
    First approach: launch evident tests for every function as test_<function_name>.
    """

    def test_cleanup_beginning(self):
        """count_words.cleanup_beginning(word)"""
        word = 'recursion'
        word_to_cleanup = '-15:'+word
        ret = count_words.cleanup_beginning(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

    def test_cleanup_end(self):
        """count_words.cleanup_end(word)"""
        word = 'recursion'
        word_to_cleanup = word+'-#7;'
        ret = count_words.cleanup_end(word_to_cleanup)
        self.assertEqual(word, ret, f'"{word}" is expected after cleanup')

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

    def test_sort_and_exclude(self):
        """count_words.sort_and_exclude(words, exclude=None)

        Sort by frequency
        Data format:  key: word; value: [frequency, list, variants, index]
        """
        def check_results():
            for e, key in enumerate(ret_sorted_words):
                self.assertEqual(expected_order[e], key, f'Expected: {expected_order[e]}')
                self.assertEqual(e+1, ret_sorted_words[key][3], f'Expected index: {e+1}')

        words = {'one':     [1, '(in top 100)', '', ''],
                 'ten':     [10, '(from 100 to 1000)', '', ''],
                 'fifteen': [15, '', '(1 with s: fifteens)', ''],
                 'two':     [2, '(in top 100)', '', ''],
                 'eighty':  [80, '(l1)', '', ''],
                 'twice':   [2, '(from 100 to 1000)', '', '']}

        # 1 - Sort only
        expected_order = ['eighty', 'fifteen', 'ten', 'two', 'twice', 'one']
        ret_sorted_words = count_words.sort_and_exclude(words)
        check_results()

        # 2 - Sort & exclude
        expected_order = ['fifteen', 'ten', 'twice']
        ret_sorted_words = count_words.sort_and_exclude(words, ['(in top 100)', '(l1)'])
        check_results()

    """
    print_sorted_by_number(words)
    Launch sort_and_exclude and print results
    """

    def test_add_to_counter(self):
        """
        count_words.add_to_counter(w, words_counter, l1, l2)
        """
        word3 = 'word'
        word2 = 'test'
        word1 = 'prerequisite'
        l1 = [word3, word2, 'debug']
        l2 = [word1, 'snippet']
        words_counter = {}
        for word in (word3, word1, word3, word2, word3, word2):
            count_words.add_to_counter(word, words_counter, l1, l2)
        self.assertEqual(3, words_counter[word3][0], f'"{word3}" was added three times')
        self.assertEqual(2, words_counter[word2][0], f'"{word2}" was added two times')
        self.assertEqual(1, words_counter[word1][0], f'"{word1}" was added once')

    """
    recount_variants(words, variants)
    Launched in count_forms(), count_apostrophes()
    """

    def test_count_apostrophes(self):
        """
        count_words.count_apostrophes(words)

        Checking ending: "'s"
        """
        words = {'moss': [1, '', '', ''], "moss's": [1, '', '', '']}
        count_words.count_apostrophes(words)
        self.assertEqual(1, len(words), "2 forms collapsed to 1: moss <- moss's")
        self.assertEqual(2, words['moss'][0], "2 forms collapsed to 1: moss <- moss's")

    def test_count_forms(self):
        """
        count_words.count_forms(words)

        Checking endings: 's', 'es', 'ed', 'd', 'ing'
        """
        words = {'word': [1, '(from 100 to 1000)', '', ''], 'words': [1, '', '', ''], 'worded': [1, '', '', ''],
                 'wording': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '4 forms collapsed to 1: word <- words, worded, wording')
        self.assertEqual(4, words['word'][0], '4 forms collapsed to 1: word <- words, worded, wording')

        words = {'moss': [1, '', '', ''], 'mosses': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '2 forms collapsed to 1: moss <- mosses')
        self.assertEqual(2, words['moss'][0], '2 forms collapsed to 1: moss <- mosses')

        words = {'observe': [1, '', '', ''], 'observed': [1, '', '', '']}
        count_words.count_forms(words)
        self.assertEqual(1, len(words), '2 forms collapsed to 1: observe <- observed')
        self.assertEqual(2, words['observe'][0], '2 forms collapsed to 1: observe <- observed')

    """
    print_sizes(sizes)
    print statements
    """

    def test_size_of_words(self):
        """
        size_of_words(words)
        """
        words = {'a': [1, '(in top 100)', '', 1],
                 'two': [1, '(in top 100)', '', 2],
                 'dot': [1, '', '', 3],
                 'ten': [1, '(from 100 to 1000)', '', 4],
                 'objectification': [1, '', '', 5]}
        expected_sizes = {1: [['a'], 1], 3: [['two', 'dot', 'ten'], 3], 15: [['objectification'], 1]}
        ret_sizes = count_words.size_of_words(words)
        self.assertCountEqual(expected_sizes, ret_sizes, f'Expected: {expected_sizes}')

    def test_get_words_by_indexes(self):
        """
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add):
        """
        list_words = ['one', 'two', 'three']
        words_to_add = set()

        # 1 - words added
        indexes_to_add = {2, 3}
        # expected_words = [word for e, word in enumerate(list_words, 1) if e in indexes_to_add]  # Not readable...
        expected_words = ['two', 'three']
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertCountEqual(expected_words, words_to_add,
                              f'Expected: {len(expected_words)} words added: {expected_words}')

        # 2 - out of range (0 not in range: 1, 2, 3)
        indexes_to_add = {0}
        count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        self.assertCountEqual(expected_words, words_to_add, f'Expected: nothing added')

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
    Unit tests draft.
    First approach: launch evident tests for every function as test_<function_name>.
    Test suite with mocking read file functionality.
    """

    def test_mock_read_text(self):
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


class IntegrationTestsWriteRead(unittest.TestCase):
    """
    Integration tests draft.
    First approach: launch evident tests for every function as test_<function_name>.
    Test suite with file write/read functionality.
    """

    @staticmethod
    def create_txt(base, files):
        base_dir = os.path.join(count_words.PATH_TO_BASE, base)
        all_words = []
        file_paths = []
        for file in files:
            file_name = file[0][0] + '.txt'
            file_path = os.path.join(base_dir, file_name)
            file_paths.append(file_path)
            with open(file_path, 'w') as f:
                for word in file:
                    all_words.append(word)
                    f.write(word + '\n')
        return all_words, file_paths

    @staticmethod
    def remove_txt(file_paths):
        for file in file_paths:
            os.remove(file)

    @classmethod
    def setUpClass(cls) -> None:
        # For test launches: relocate SCRIPT_DIR from root to /tests
        count_words.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        count_words.PATH_TO_BASE = os.path.join(count_words.SCRIPT_DIR, 'db', 'txt')
        # Create db hierarchy in /tests
        for dirs in (('db',), ('db', 'txt'), ('db', 'txt', 'l1'), ('db', 'txt', 'l2')):
            path_now = count_words.SCRIPT_DIR
            for d in dirs:
                path_now = os.path.join(path_now, d)
            if not os.path.isdir(path_now):
                os.mkdir(path_now)

    @classmethod
    def tearDownClass(cls) -> None:
        dir_path = os.path.join(count_words.SCRIPT_DIR, 'db')
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

    def test_count_words(self):
        """
        count_words.count_words(text)

        Kind of integration test: write/read file system.
        Text for test: some words with symbols to clean up, and some not words.
        One word in l2 base.
        """
        word4 = {'word': 'word',            'variants': ('word', '-&7word', 'word")', 'word")')}
        word3 = {'word': 'test',            'variants': ('-=test=-', 'test....', r'\test/')}
        word2 = {'word': "prerequisite's",  'variants': ('prerequisite`s', 'prerequisite’s')}
        not_words = ('75', '#*!')
        text = ' '.join([word3['variants'][0], word4['variants'][0], not_words[0], word4['variants'][1],
                         word2['variants'][0], word3['variants'][1], word2['variants'][1],
                         word4['variants'][2], word3['variants'][2], word4['variants'][3], not_words[1]])

        base = 'l2'
        files = ([word2['word']],)
        _, file_paths = IntegrationTestsWriteRead.create_txt(base, files)

        expected_words_counter = {word3['word']: [3, '(from 100 to 1000)', '', ''],
                                  word4['word']: [4, '(from 100 to 1000)', '', ''],
                                  word2['word']: [2, '(l2)', '', '']}
        try:
            ret_words_counter, ret_not_words = count_words.count_words(text)
            self.assertCountEqual(expected_words_counter, ret_words_counter, f'Expected: {expected_words_counter}')
            self.assertCountEqual(not_words, ret_not_words, f'Expected: {not_words}')
        finally:
            IntegrationTestsWriteRead.remove_txt(file_paths)

    def test_get_sorted_list_from_base(self):
        """
        count_words.get_sorted_list_from_base(base, first_letters):

        Kind of integration test: write/read file system.
        """
        base = 'l1'
        files = (['hello', 'hi'], ['goodbye'], ['bye'])
        all_words, file_paths = IntegrationTestsWriteRead.create_txt(base, files)
        try:
            # 1 - all words
            expected_sorted_words = sorted(all_words)
            sorted_words_from_base = count_words.get_sorted_list_from_base(base)
            self.assertListEqual(expected_sorted_words, sorted_words_from_base)

            # 2 - by first letters
            first_letters = 'he'
            expected_sorted_words = ['hello']
            sorted_words_from_base = count_words.get_sorted_list_from_base(base, first_letters=first_letters)
            self.assertListEqual(expected_sorted_words, sorted_words_from_base)
        finally:
            IntegrationTestsWriteRead.remove_txt(file_paths)

    """
    print_base(base, first_letters='')
    get_sorted_list_from_base
    print statements
    """

    def test_write_read_base(self):
        """count_words.write_to_base, count_words.word_in_base"""
        base = 'l1'
        word_for_test = 'hello'
        file_to_remove_after = os.path.join(count_words.PATH_TO_BASE, base, 'h.txt')
        try:
            count_words.write_to_base(base, word_for_test)
            ret = count_words.word_in_base(base, word_for_test)
            self.assertTrue(ret, f'"{word_for_test}" is not found in base')
        finally:
            os.remove(file_to_remove_after)

    def test_rem_from_txt(self):
        """
        count_words.rem_from_txt(base, word):

        Kind of integration test: write/read file system.
        """
        base = 'l1'
        files = (['hello', 'hi'],)
        _, file_paths = IntegrationTestsWriteRead.create_txt(base, files)
        try:
            word_to_remove = 'hello'
            ret_word = count_words.rem_from_txt(base, word_to_remove)
            self.assertEqual(word_to_remove, ret_word, f'Expected removed word: {word_to_remove}')

            expected_after_remove = 'hi'
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    after_remove = f.read()
                self.assertEqual(expected_after_remove, after_remove.replace('\n', ''),
                                 f'Expected after remove: {expected_after_remove}')
        finally:
            IntegrationTestsWriteRead.remove_txt(file_paths)

    """
    rem_words(base, str_words)
    launch test_rem_from_txt for word in words
    """


if __name__ == '__main__':
    unittest.main(buffer=True)
