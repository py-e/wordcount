import sys
import os
import shutil
import unittest
from unittest.mock import patch, mock_open

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import count_words


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
        count_words.get_sorted_list_from_base(base, first_letters)

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
        """
        count_words.write_to_base(base, word_for_test)
        count_words.word_in_base(base, word_for_test)

        Kind of integration test: write/read file system.
        """
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
        count_words.rem_from_txt(base, word)

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
