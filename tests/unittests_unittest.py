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
