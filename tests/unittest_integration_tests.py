import io
import os
import sys
import glob
import shutil
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    @staticmethod
    def remove_all_txt():
        paths_to_bases = (os.path.join(count_words.PATH_TO_BASE, 'l1'),
                          os.path.join(count_words.PATH_TO_BASE, 'l2'))
        for path in paths_to_bases:
            shutil.rmtree(path)
            os.mkdir(path)

    @classmethod
    def setUpClass(cls):
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
    def tearDownClass(cls):
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
        word_to_remove = files[0][1]  # 'hi'
        _, file_paths = SetupsIT.create_txt(base, files)
        try:
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

    base = 'l1'
    captured_output = ''
    input_counter = [0]

    def setUp(self):
        self.input_counter[0] = 0
        count_words.input = self.mock_input

    def tearDown(self):
        SetupsIT.remove_all_txt()

    def set_base(self, files):
        _, file_paths = SetupsIT.create_txt(self.base, files)
        return file_paths

    def get_base(self):
        db_txt_files = glob.glob(os.path.join(count_words.PATH_TO_BASE, self.base, '[a-z].txt'))
        list_from_txt = []
        for file in db_txt_files:
            with open(file) as f:
                for line in f:
                    list_from_txt.append(line.replace('\n', ''))
        return list_from_txt

    def mock_input(self, inp_message, counter=input_counter):
        """
        To override input two times: command (like 'l1') and 'q' (quit).
        Capture print output after command (first input).
        """
        counter[0] += 1
        if counter[0] == 1:
            self.captured_output = io.StringIO()
            sys.stdout = self.captured_output        # Redirect stdout
            return self.input_command
        elif counter[0] == 2:
            return 'q'

    def launch_and_assert(self, expected_val):
        count_words.edit_base()
        captured_val = self.captured_output.getvalue()
        captured_val = captured_val.replace('\n', '')
        self.assertEqual(expected_val, captured_val, f'Expected: {expected_val}')

    def launch_and_assert_list(self, expected_list):
        count_words.edit_base()
        captured_val = self.captured_output.getvalue()
        captured_list = captured_val.split('\n')
        captured_list = list(filter(None, captured_list))
        self.assertCountEqual(expected_list, captured_list, f'Expected: {expected_list}')

    # Test cases: get data from the base (print base)

    def test_print_base_one_word(self):
        """Print base with one word
        edit_base(); print_base('l1'); get_sorted_list_from_base('l1', ''); get_words_from_txt('l1')"""
        # GIVEN one word (word) in the base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name> (l1)
        # THEN correct data is printed: <num word> (1 word)
        self.set_base((('word',),))
        self.input_command = self.base
        self.launch_and_assert(expected_val='1 word')

    def test_print_base_many_words(self):
        """Print base: three words (two files)
        edit_base(); print_base('l1'); get_sorted_list_from_base('l1', ''); get_words_from_txt('l1')"""
        # GIVEN three words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name> (l1)
        # THEN correct data is printed: 3 items <num word> sorted alphabetically
        self.set_base((('word', 'world'), ('sword',)))
        self.input_command = self.base
        self.launch_and_assert(expected_val='1 sword2 word3 world')

    def test_print_base_empty(self):
        """Print empty base
        edit_base(); print_base('l1'); get_sorted_list_from_base('l1', ''); get_words_from_txt('l1')"""
        # GIVEN base is empty AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name> (l1)
        # THEN correct data is printed: correct message, no errors
        self.input_command = self.base
        self.launch_and_assert(expected_val=f'Base {self.base} is empty for now')

    def test_print_base_by_letter(self):
        """Print words starting with letter (two such words from three in 2 files)
        edit_base(); print_base('l1', 'w'); get_sorted_list_from_base('l1', 'w')"""
        # GIVEN three words in the base (files: w.txt - 2, s.txt - 1) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name:letter> (l1:w)
        # THEN correct data is printed: 2 items <num word> starting with the letter (w)
        self.set_base((('word', 'world'), ('sword',)))
        self.input_command = self.base+':w'
        self.launch_and_assert(expected_val='1 word2 world')

    def test_print_base_by_few_letters(self):
        """Print words starting with some letters (two such words from five in 2 files)
        edit_base(); print_base('l1', 'woo'); get_sorted_list_from_base('l1', 'woo')"""
        # GIVEN five words in the base (files: w.txt - 4, s.txt - 1) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name:letters> (l1:woo)
        # THEN correct data is printed: 2 items <num word> starting with the letters (woo)
        self.set_base((('wolf', 'wood', 'wool', 'wrong'), ('sword',)))
        self.input_command = self.base+':woo'
        self.launch_and_assert(expected_val='1 wood2 wool')

    def test_print_base_by_letter_not_found(self):
        """Print message: words not found (by letter)
        edit_base(); print_base('l1', 'f'); get_sorted_list_from_base('l1', 'f')"""
        # GIVEN three words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name:letter> (l1:f)
        # THEN correct message is printed: <No words found>
        self.set_base((('word', 'world'), ('sword',)))
        self.input_command = self.base+':f'
        self.launch_and_assert(expected_val=f'No words in {self.base} starting with: f')

    def test_print_base_by_letter_wrong_symbol(self):
        """Print message: words not found (by non-letter character)
        edit_base(); print_base('l1', '5'); get_sorted_list_from_base('l1', '5')"""
        # GIVEN three words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name:letter> (l1:5)
        # THEN correct message is printed: <No words found>, no errors
        self.set_base((('word', 'world'), ('sword',)))
        self.input_command = self.base+':5'
        self.launch_and_assert(expected_val=f'No words in {self.base} starting with: 5')

    def test_print_base_by_letter_second_symbol_wrong(self):
        """No message for case: correct first letter (w), but next symbol is not letter ('*')
        edit_base(); print_base('l1', 'w*'); get_sorted_list_from_base('l1', 'w*')"""
        # GIVEN three words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name:letter> (l1:w*)
        # THEN prompt reappears: No message shown
        self.set_base((('word', 'world'), ('sword',)))
        self.input_command = self.base+':w*'
        self.launch_and_assert(expected_val='')

    # Test cases: add data to the base

    def test_add_word_to_empty(self):
        """Add word to empty base
        edit_base(); add_to_base('l1', 'framework', words=None); write_to_base('l1', 'framework')"""
        word = 'framework'
        # GIVEN base is empty AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:framework)
        # THEN correct message is printed: <word added>
        # AND base contains the word
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'{word}, added to ({self.base})')
        self.assertCountEqual((word,), self.get_base())

    def test_add_try_word_from_1000(self):
        """Word from top1000 not added, message for user
        edit_base(); add_to_base('l1', 'word', words=None)"""
        word = 'word'
        # GIVEN base is empty AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:word)
        # THEN correct message is printed: <word in top1000>
        # AND base is still empty
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'{word}, already in (from 100 to 1000)')
        self.assertCountEqual('', self.get_base())

    def test_add_word_file_exist(self):
        """Add new word to base, txt file (first letter) exist
        edit_base(); add_to_base('l1', 'framework', words=None); write_to_base('l1', 'framework')"""
        word = 'framework'
        words_initial_base = (('frame', 'frost'),)
        words_expected_base = [word] + [i for w in words_initial_base for i in w]   # ['framework', 'frame', 'frost']
        # GIVEN 3 words in the base (file: f.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:framework)
        # THEN correct message is printed: <word added>
        # AND base contains all 3 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'{word}, added to ({self.base})')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_add_words(self):
        """Add new words to base. Some txt files (first letter) exist, and some not.
        edit_base(); add_to_base('l1', 'cake sweetie caramel candy', words=None); write_to_base('l1', 'sweetie')"""
        words = 'cake workshop sweetie caramel candy'
        messages_expected = [f'cake, already in (from 100 to 1000)',
                             f'workshop, found in ({self.base})',
                             f'sweetie, added to ({self.base})',
                             f'caramel, added to ({self.base})',
                             f'candy, added to ({self.base})']
        words_initial_base = (('workload', 'workshop'), ('software',))
        words_expected_base = words.split(' ')[2:] + [i for w in words_initial_base for i in w] # ['sweetie', 'caramel', 'candy', 'workload', 'workshop', 'software']
        # GIVEN 3 words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:cake workshop sweetie caramel candy)
        # THEN correct messages are printed: <word added/already in/found in>
        # AND base contains 6 words (3 initial & 3 added)
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'+words
        self.launch_and_assert_list(expected_list=messages_expected)
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_add_existing_word(self):
        """Add word to base, but this word already in the base
        edit_base(); add_to_base('l1', 'frame', words=None)"""
        word = 'frame'
        words_initial_base = (('frame', 'frost'),)
        words_expected_base = [i for w in words_initial_base for i in w]    # ['frame', 'frost']
        # GIVEN 2 words in the base (file: f.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:frame)
        # THEN correct message is printed: <word found in the base>
        # AND base contains initial 2 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'{word}, found in ({self.base})')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_add_without_data(self):
        """Add command without any word
        edit_base(); add_to_base('l1', '', words=None)"""
        words_initial_base = (('frame', 'frost'),)
        words_expected_base = [i for w in words_initial_base for i in w]    # ['frame', 'frost']
        # GIVEN 2 words in the base (file: f.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:)
        # THEN prompt reappears: No message shown
        # AND base contains initial 2 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'
        self.launch_and_assert(expected_val='')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_add_try_number(self):
        """Add command with number
        edit_base(); add_to_base('l1', '5', words=None)"""
        word = '5'
        words_initial_base = (('frame', 'frost'),)
        words_expected_base = [i for w in words_initial_base for i in w]    # ['frame', 'frost']
        # GIVEN 2 words in the base (file: f.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:5)
        # THEN correct message is printed: <seems a digit>
        # AND base contains initial 2 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'seems a digit: {{{word}}}')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_add_try_non_letter_first(self):
        """Add command: non-letter first symbol
        edit_base(); add_to_base('l1', '%w', words=None); is_letter_first('%w')"""
        word = '%w'
        words_initial_base = (('word', 'world'), ('sword',))
        words_expected_base = [i for w in words_initial_base for i in w]    # ['word', 'world', 'sword']
        # GIVEN 3 words in the base (files: w.txt, s.txt) AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name add:word> (l1 add:%w)
        # THEN correct message is printed: <skipped>
        # AND base contains initial 3 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' add:'+word
        self.launch_and_assert(expected_val=f'{word} - skipped, word should start with a letter')
        self.assertCountEqual(words_expected_base, self.get_base())

    # Test cases: remove data from the base

    def test_remove_word(self):
        """Remove word from the base (with one word)
        edit_base(); rem_words('l1', 'framework'); rem_from_txt('l1', 'framework')"""
        word = 'framework'
        words_initial_base = (('framework',),)
        # GIVEN 1 word in base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name rem:word> (l1 rem:framework)
        # THEN correct message is printed: <removed>
        # AND base is empty now
        self.set_base(words_initial_base)
        self.input_command = self.base+' rem:'+word
        self.launch_and_assert(expected_val=f'removed from ({self.base}): {word}')
        self.assertCountEqual('', self.get_base())

    def test_remove_words(self):
        """Remove words from the base (some removed and some not found)
        edit_base(); rem_words('l1', 'workshop software processor'); rem_from_txt('l1', 'workshop')"""
        words = 'workshop software processor'
        words_initial_base = (('workload', 'workshop'), ('software',))
        messages_expected = f'processor is not found in {self.base}removed from ({self.base}): workshop, software'
        words_expected_base = ('workload',)
        # GIVEN 3 words in base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name rem:words> (l1 rem:workshop software processor)
        # THEN correct messages are printed: <not found/removed>
        # AND 1 word in base now
        self.set_base(words_initial_base)
        self.input_command = self.base+' rem:'+words
        self.launch_and_assert(expected_val=messages_expected)
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_remove_try_wrong_symbol(self):
        """Remove command: non-letter symbol
        edit_base(); rem_words('l1', '?'); rem_from_txt('l1', '?')"""
        word = '?'
        words_initial_base = (('workload', 'workshop'), ('software',))
        words_expected_base = [i for w in words_initial_base for i in w]    # ['workload', 'workshop', 'software']
        # GIVEN 3 words in base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name rem:words> (l1 rem:?)
        # THEN correct messages are printed: <not found>
        # AND base still contains all 3 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' rem:'+word
        self.launch_and_assert(expected_val=f'{word} is not found in {self.base}')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_remove_try_without_data(self):
        """Remove command: without any word
        edit_base(); rem_words('l1', '')"""
        words_initial_base = (('workload', 'workshop'), ('software',))
        words_expected_base = [i for w in words_initial_base for i in w]    # ['workload', 'workshop', 'software']
        # GIVEN 3 words in base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name rem:words> (l1 rem:)
        # THEN prompt reappears: No message shown
        # AND base still contains all 3 words
        self.set_base(words_initial_base)
        self.input_command = self.base+' rem:'
        self.launch_and_assert(expected_val='')
        self.assertCountEqual(words_expected_base, self.get_base())

    def test_remove_try_empty_base(self):
        """Remove command: but the base is empty
        edit_base(); rem_words('l1', 'framework'); rem_from_txt('l1', 'framework')"""
        word = 'framework'
        # GIVEN no words in base AND app in edit mode (start func: edit_base())
        # WHEN command sent: <base_name rem:words> (l1 rem:framework)
        # THEN prompt reappears: <not found>
        # AND base is empty
        self.input_command = self.base+' rem:framework'
        self.launch_and_assert(expected_val=f'{word} is not found in {self.base}')
        self.assertCountEqual('', self.get_base())


if __name__ == '__main__':
    unittest.main(buffer=True)
