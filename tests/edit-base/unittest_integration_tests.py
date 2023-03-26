import sys
import os
import io
import shutil
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import count_words


class SetupsIT(unittest.TestCase):
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

        # Reset stdout redirect
        sys.stdout = sys.__stdout__
        # Applied at the class level (was set at the method level)
        # Test level issue for reset: if test is failed, unittest need to get sys.stdout.getvalue()
        # No attribute 'getvalue' in '_io.TextIOWrapper' object (sys.__stdout__)


class ITWriteRead(SetupsIT):
    """
    Tests functions with file write/read functionality.
    """

    def test_count_words(self):
        """
        count_words.count_words(text)

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
        _, file_paths = SetupsIT.create_txt(base, files)

        expected_words_counter = {word3['word']: [3, '(from 100 to 1000)', '', ''],
                                  word4['word']: [4, '(from 100 to 1000)', '', ''],
                                  word2['word']: [2, '(l2)', '', '']}
        try:
            ret_words_counter, ret_not_words = count_words.count_words(text)
            self.assertCountEqual(expected_words_counter, ret_words_counter, f'Expected: {expected_words_counter}')
            self.assertCountEqual(not_words, ret_not_words, f'Expected: {not_words}')
        finally:
            SetupsIT.remove_txt(file_paths)

    def test_get_sorted_list_from_base(self):
        """
        count_words.get_sorted_list_from_base(base, first_letters)

        Check that function return sorted words in both cases (all, by first letters)
        """
        base = 'l1'
        files = (['hello', 'hi'], ['goodbye'], ['bye'])
        all_words, file_paths = SetupsIT.create_txt(base, files)
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
            SetupsIT.remove_txt(file_paths)

    """
    print_base(base, first_letters='')
    get_sorted_list_from_base
    print statements
    """

    def test_write_read_base(self):
        """
        count_words.write_to_base(base, word_for_test)
        count_words.word_in_base(base, word_for_test)

        Simple test: write word to the db, then read it.
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

        Remove word from base, check that only one correct word was removed from the file.
        """
        base = 'l1'
        files = (['hello', 'hi', 'hyphen'],)
        _, file_paths = SetupsIT.create_txt(base, files)
        try:
            word_to_remove = files[0][1]    # 'hi'
            ret_word = count_words.rem_from_txt(base, word_to_remove)
            self.assertEqual(word_to_remove, ret_word, f'Expected removed word: {word_to_remove}')

            expected_after_remove = files[0][0] + files[0][2]   # 'hello' + 'hyphen'
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    after_remove = f.read()
                self.assertEqual(expected_after_remove, after_remove.replace('\n', ''),
                                 f'Expected after remove: {expected_after_remove}')
        finally:
            SetupsIT.remove_txt(file_paths)

    """
    rem_words(base, str_words)
    launch test_rem_from_txt for word in words
    """


class ITEditBase(SetupsIT):
    """
    Integration tests suite.
    Interfaces between functions for actions:
    - get data from the base
    - add data to the base
    - remove data from the base
    """

    captured_output = ''
    input_counter = [0]

    def mock_input_l1_q(self, inp_message, counter=input_counter):
        """
        To override input two times: 'l1' (print l1 base) and 'q' (quit).
        Capture print output after 'l1' command.
        """
        counter[0] += 1
        if counter[0] == 1:
            self.captured_output = io.StringIO()
            sys.stdout = self.captured_output        # Redirect stdout
            return 'l1'
        elif counter[0] == 2:
            return 'q'

    def test_print_base_one_word(self):
        """
        Add one word to the base
        edit_base() -> print_base('l1')
        Check that content of the base is printed correct
        """
        self.input_counter[0] = 0
        count_words.input = self.mock_input_l1_q
        base = 'l1'
        files = (('word',),)
        expected_val = '1 word'
        _, file_paths = SetupsIT.create_txt(base, files)
        count_words.edit_base()
        captured_val = self.captured_output.getvalue()
        captured_val = captured_val.replace('\n', '')
        try:
            self.assertEqual(expected_val, captured_val, f'Expected: {expected_val}')
        finally:
            SetupsIT.remove_txt(file_paths)

    def test_print_base_many_words(self):
        """
        Add three words to the base (two files)
        edit_base() -> print_base('l1')
        Check that content of the base is printed correct
        """
        self.input_counter[0] = 0
        count_words.input = self.mock_input_l1_q
        base = 'l1'
        files = (('word', 'world'), ('sword',))

        list_of_words = [w for f in files for w in f]
        list_of_words.sort()
        numbered_list_of_words = [str(e) + ' ' + l for e, l in enumerate(list_of_words, 1)]
        expected_val = ''.join(numbered_list_of_words)  # like: '1 sword2 word3 world'

        _, file_paths = SetupsIT.create_txt(base, files)
        count_words.edit_base()
        captured_val = self.captured_output.getvalue()
        captured_val = captured_val.replace('\n', '')
        print(captured_val)
        try:
            self.assertEqual(expected_val, captured_val, f'Expected: {expected_val}')
        finally:
            SetupsIT.remove_txt(file_paths)

    def test_print_base_empty(self):
        """
        No words in the base
        edit_base() -> print_base('l1')
        Check that nothing is printed, no errors
        """
        self.input_counter[0] = 0
        count_words.input = self.mock_input_l1_q
        base = 'l1'
        expected_val = ''
        count_words.edit_base()
        captured_val = self.captured_output.getvalue()
        captured_val = captured_val.replace('\n', '')
        print(captured_val)
        self.assertEqual(expected_val, captured_val, f'Expected: no print')


if __name__ == '__main__':
    unittest.main(buffer=True)
