import sys
import os
import shutil
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import count_words


class UT(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # For test launches: relocate SCRIPT_DIR from root to /tests
        count_words.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        # Create db hierarchy in /tests
        for d in ('db', 'db/txt', 'db/txt/l1', 'db/txt/l2'):
            cls.dir_path = os.path.join(count_words.SCRIPT_DIR, d)
            if not os.path.isdir(cls.dir_path):
                os.mkdir(cls.dir_path)

    def test_read_text(self):
        """count_words.get_text()"""
        temp_file = os.path.join(count_words.SCRIPT_DIR, '_temp_text.txt')
        words_to_write = """hello unit test

        and more
        """
        words_number = len(words_to_write.split())
        with open(temp_file, 'w') as f:
            f.write(words_to_write)

        count_words.args.file = temp_file
        ret = count_words.get_text()
        ret_list = ret.split()
        self.assertEqual(words_number, len(ret_list), f'Should be {words_number} words')

        os.remove(temp_file)

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
        """count_words.cleanup_word(word)"""
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
        def check_results(expected_order, ret_sorted_words):
            for e, key in enumerate(ret_sorted_words):
                self.assertEqual(expected_order[e], key, f'Expected: {expected_order[e]}')
                self.assertEqual(e+1, ret_sorted_words[key][3], f'Expected number: {e+1}')

        words = {'one':     [1, '(in top 100)', '', ''],
                 'ten':     [10, '(from 100 to 1000)', '', ''],
                 'fifteen': [15, '', '(1 with s: fifteens)', ''],
                 'two':     [2, '(in top 100)', '', ''],
                 'eighty':  [80, '(l1)', '', ''],
                 'twice':   [2, '(from 100 to 1000)', '', '']}

        # 1 - Sort only
        expected_order = ['eighty', 'fifteen', 'ten', 'two', 'twice', 'one']
        ret_sorted_words = count_words.sort_and_exclude(words)
        check_results(expected_order, ret_sorted_words)

        # 2 - Sort & exclude
        expected_order = ['fifteen', 'ten', 'twice']
        ret_sorted_words = count_words.sort_and_exclude(words, ['(in top 100)', '(l1)'])
        check_results(expected_order, ret_sorted_words)

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

    def test_get_words_from_txt(self):
        """
        count_words.get_words_from_txt(base)

        Write files (c.txt, v.txt) to l2 dir.
        Check that all words from l2 base returned by the function.
        """
        l2_base_dir = __class__.dir_path
        files = (['cell', 'cadmium'], ['velocity'])
        all_words = []
        for file in files:
            file_name = file[0][0]+'.txt'
            file_path = os.path.join(l2_base_dir, file_name)
            with open(file_path, 'w') as f:
                for word in file:
                    all_words.append(word)
                    f.write(word+'\n')

        ret = count_words.get_words_from_txt('l2')
        self.assertCountEqual(all_words, ret, f'Expected words from the base: {all_words}')

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

        l2_base_dir = __class__.dir_path
        file_name = word2['word'][0] + '.txt'
        file_path = os.path.join(l2_base_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(word2['word'] + '\n')

        expected_words_counter = {word3['word']: [3, '(from 100 to 1000)', '', ''],
                                  word4['word']: [4, '(from 100 to 1000)', '', ''],
                                  word2['word']: [2, '(l2)', '', '']}
        ret_words_counter, ret_not_words = count_words.count_words(text)
        try:
            self.assertCountEqual(expected_words_counter, ret_words_counter, f'Expected: {expected_words_counter}')
            self.assertCountEqual(not_words, ret_not_words, f'Expected: {not_words}')
        finally:
            os.remove(file_path)

    """
    recount_variants(words, variants)
    Launched in count_forms(), count_apostrophes()
    """

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

    def test_count_apostrophes(self):
        """
        count_words.count_apostrophes(words)

        Checking ending: "'s"
        """
        words = {'moss': [1, '', '', ''], "moss's": [1, '', '', '']}
        count_words.count_apostrophes(words)
        self.assertEqual(1, len(words), "2 forms collapsed to 1: moss <- moss's")
        self.assertEqual(2, words['moss'][0], "2 forms collapsed to 1: moss <- moss's")

    def test_write_read_base(self):
        """count_words.write_to_base, count_words.word_in_base"""
        word_for_test = 'hello'
        count_words.write_to_base('l1', word_for_test)
        ret = count_words.word_in_base('l1', word_for_test)
        self.assertTrue(ret, f'"{word_for_test}" is not found in base')

    @classmethod
    def tearDownClass(cls) -> None:
        dir_path = os.path.join(count_words.SCRIPT_DIR, 'db')
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)


if __name__ == '__main__':
    unittest.main()
