import os
import sys
import glob
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import count_words


# Test cases: write/read functions


# text for SUT function: 4, 3, 2 word variants; one word in l2; two not words,
p_word4 = {'word': 'word', 'variants': ('word', '-&7word', 'word")', 'word")')}
p_word3 = {'word': 'test', 'variants': ('-=test=-', 'test....', r'\test/')}
p_word2 = {'word': "prerequisite's", 'variants': ('prerequisite`s', 'prerequisite’s')}
p_not_words = ('75', '#*!')
p_text = ' '.join([p_word3['variants'][0], p_word4['variants'][0], p_not_words[0], p_word4['variants'][1],
                   p_word2['variants'][0], p_word3['variants'][1], p_word2['variants'][1],
                   p_word4['variants'][2], p_word3['variants'][2], p_word4['variants'][3], p_not_words[1]])
p_base = 'l2'
p_files = ([p_word2['word']],)
p_expected = {p_word3['word']: [3, '(from 100 to 1000)', '', ''],
              p_word4['word']: [4, '(from 100 to 1000)', '', ''],
              p_word2['word']: [2, '(l2)', '', '']}
@pytest.mark.parametrize('text, base_files, expected, not_words', [(p_text, (p_base, p_files), p_expected, p_not_words)],
                    ids=['text432not'],
                    indirect=['base_files'])
def test_count_words(text, base_files, expected, not_words):
    """count_words.count_words(text)"""
    ret_words_counter, ret_not_words = count_words.count_words(text)
    assert expected == ret_words_counter
    assert set(not_words) == ret_not_words


@pytest.mark.parametrize('base_files, first, expected', [
(('l1', (['hello', 'hi'], ['goodbye'], ['bye'])), None, ['bye', 'goodbye', 'hello', 'hi']),    # for expected: here we can use all_words from base_files, but explicit is better
(('l1', (['hello', 'hi'], ['goodbye'], ['bye'])), 'he', ['hello']),
(('l1', (['hello', 'hi'], ['goodbye'], ['bye'])), 'n',  [])],     # new case (absent in unittest_integration_tests): file is not found for first letter(s)
                ids=['l1_hgb-all', 'l1_hgb-he_found', 'l1_hgb-n_not_found'],
                indirect=['base_files'])
def test_get_sorted_list_from_base(base_files, first, expected):
    """count_words.get_sorted_list_from_base(base, first_letters)"""
    base, _, _, _ = base_files
    if first is None:
        sorted_words_from_base = count_words.get_sorted_list_from_base(base)
    else:
        sorted_words_from_base = count_words.get_sorted_list_from_base(base, first_letters=first)
    assert expected == sorted_words_from_base


@pytest.mark.parametrize('base, word', [('l1', 'hello')], ids=['l1_h'])
def test_write_read_base(tmp_SUT_path, base, word):
    """count_words.write_to_base(base, word_for_test); count_words.word_in_base(base, word_for_test)"""
    count_words.write_to_base(base, word)
    assert word == file_content(os.path.join(tmp_SUT_path, base), word)
    ret = count_words.word_in_base(base, word)
    assert ret is True


@pytest.mark.parametrize('base_files, to_rem, expected_base', [
(('l1', (['hello', 'hi', 'hyphen'],)),          'hi',    ['hello', 'hyphen'])
], ids=['1_from_3'], indirect=['base_files'])
def test_rem_from_txt(tmp_SUT_path, base_files, to_rem, expected_base):
    """count_words.rem_from_txt(base, word)"""
    ret_word = count_words.rem_from_txt('l1', to_rem)
    assert to_rem == ret_word
    assert expected_base == get_base(tmp_SUT_path, 'l1')


# Test cases: get data from the base (print base)

@pytest.mark.parametrize('base_files, input_command, expected', [
(('l1', (('word',),)),                                    'l1',     '1 word'),
(('l1', (('word', 'world'), ('sword',))),                 'l1',     '1 sword\n2 word\n3 world'),
(('l1', None),                                            'l1',     'Base l1 is empty for now'),
(('l1', (('word', 'world'), ('sword',))),                 'l1:w',   '1 word\n2 world'),
(('l1', (('wolf', 'wood', 'wool', 'wrong'), ('sword',))), 'l1:woo', '1 wood\n2 wool'),
(('l1', (('word', 'world'), ('sword',))),                 'l1:f',   'No words in l1 starting with: f'),
(('l1', (('word', 'world'), ('sword',))),                 'l1:5',   'No words in l1 starting with: 5'),
(('l1', (('word', 'world'), ('sword',))),                 'l1:w*',   '"q" - to exit')],
ids=['1_word', '3_words_2_files', 'empty', '1letter_2from3', '2letters_2from5', '1letter_not_found', 'wrong_symbol', 'wrong_second_symbol'],
                         indirect=['base_files', 'input_command'])
def test_print_base(base_files, input_command, capsys, expected):
    """edit_base(); print_base('l1'); get_sorted_list_from_base('l1', ''); get_words_from_txt('l1')"""
    # GIVEN words added to base @base_files AND app in edit mode (start func: edit_base())
    count_words.edit_base()
    # WHEN command sent: @input_command
    # THEN correct data is printed: @expected
    printed = get_last_lines(capsys.readouterr(), len(expected))
    assert expected == printed


# Test cases: add data to the base

@pytest.mark.parametrize('base_files, input_command, expected_msg, expected_base',
[
(('l1', None),                  'l1 add:framework', ['framework, added to (l1)'],             ['framework']),
(('l1', None),                  'l1 add:word',      ['word, already in (from 100 to 1000)'],  []),
(('l1', (('frame', 'frost'),)), 'l1 add:framework', ['framework, added to (l1)'],             ['frame', 'framework', 'frost']),

(('l1', (('workload', 'workshop'), ('software',))),
'l1 add:cake workshop sweetie caramel candy',
['cake, already in (from 100 to 1000)', 'candy, added to (l1)', 'caramel, added to (l1)', 'sweetie, added to (l1)', 'workshop, found in (l1)'],
['candy', 'caramel', 'software', 'sweetie', 'workload', 'workshop']),

(('l1', (('frame', 'frost'),)), 'l1 add:frame',     ['frame, found in (l1)'],                 ['frame', 'frost']),
(('l1', (('frame', 'frost'),)), 'l1 add:',          ['"q" - to exit'],                        ['frame', 'frost']),
(('l1', (('frame', 'frost'),)), 'l1 add:5',         ['seems a digit: {5}'],                   ['frame', 'frost']),
(('l1', (('frame', 'frost'),)), 'l1 add:%w',        ['%w - skipped, word should start with a letter'],['frame', 'frost'])
],
ids=['word_to_empty', 'try_word_from_1000', 'word_file_exist', '5words_3added',
     'existing_word', 'without_data', 'try_number', 'try_non_letter_first'],
                         indirect=['base_files', 'input_command'])
def test_add_to_base(tmp_SUT_path, base_files, input_command, capsys, expected_msg, expected_base):
    """edit_base(); add_to_base('l1', 'framework', words=None); write_to_base('l1', 'framework')"""
    # GIVEN initial state of base in @base_files AND app in edit mode (start func: edit_base())
    count_words.edit_base()
    # WHEN command sent: @input_command
    # THEN correct message is printed: @expected_msg
    printed = get_printed_as_list(capsys.readouterr(), len(expected_msg))
    assert expected_msg == printed
    # AND state of the base @expected_base is correct
    assert expected_base == get_base(tmp_SUT_path, 'l1')


# Test cases: remove data from the base

@pytest.mark.parametrize('base_files, input_command, expected_msg, expected_base',
[
(('l1', (('framework',),)),                         'l1 rem:framework', 'removed from (l1): framework', []),
(('l1', (('workload', 'workshop'), ('software',))), 'l1 rem:workshop software processor', 'processor is not found in l1\nremoved from (l1): workshop, software', ['workload']),
(('l1', (('workload', 'workshop'), ('software',))), 'l1 rem:?', '? is not found in l1', ['software', 'workload', 'workshop']),
(('l1', (('workload', 'workshop'), ('software',))), 'l1 rem:', '"q" - to exit', ['software', 'workload', 'workshop']),
(('l1', None),                                      'l1 rem:framework', 'framework is not found in l1', [])
],
ids=['1word', '3words_2del', 'try_wrong_symbol', 'try_without_data', 'try_empty_base'],
                         indirect=['base_files', 'input_command'])
def test_remove_from_base(tmp_SUT_path, base_files, input_command, capsys, expected_msg, expected_base):
    """edit_base(); rem_words('l1', 'framework'); rem_from_txt('l1', 'framework')"""
    # GIVEN initial state of base in @base_files AND app in edit mode (start func: edit_base())
    count_words.edit_base()
    # WHEN command sent: @input_command
    # THEN correct message is printed: @expected_msg
    printed = get_last_lines(capsys.readouterr(), len(expected_msg))
    assert expected_msg == printed
    # AND state of the base @expected_base is correct
    assert expected_base == get_base(tmp_SUT_path, 'l1')


### Fixtures & Utils


@pytest.fixture
def tmp_SUT_path(tmp_path):
    original = count_words.PATH_TO_BASE
    count_words.PATH_TO_BASE = tmp_path

    for l_base in ('l1', 'l2'):
        base_dir = tmp_path / l_base
        base_dir.mkdir()

    yield tmp_path
    count_words.PATH_TO_BASE = original


@pytest.fixture
def base_files(tmp_SUT_path, request):
    base, files = request.param
    all_words, file_paths = [], []
    if files:
        all_words, file_paths = create_txt(tmp_SUT_path, base, files)
    yield base, files, all_words, file_paths


def create_txt(tmp_SUT_path, base, files):
    all_words = []
    file_paths = []
    for file in files:
        file_name = file[0][0] + '.txt'
        file_path = os.path.join(tmp_SUT_path, base, file_name)
        file_paths.append(file_path)
        with open(file_path, 'w') as f:
            for word in file:
                all_words.append(word)
                f.write(word + '\n')
    return all_words, file_paths


@pytest.fixture
def input_command(monkeypatch, request):
    responses = iter([request.param, 'q'])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    yield


def file_content(base_dir, word):
    base_file = word[0]+'.txt'
    file_path = os.path.join(base_dir, base_file)
    with open(file_path) as f:
        cont = f.read()
    return cont.replace('\n', '')


def get_last_lines(captured, number):
    text_all = captured.out[:-1]   # remove last new line '\n'
    text_end = text_all[-number:]
    return text_end


def get_printed_as_list(captured, number):
    text_all = captured.out[:-1]  # remove last new line '\n'
    text_list = text_all.split('\n')
    text_last_items = text_list[-number:]
    return sorted(text_last_items)


def get_base(tmp_SUT_path, base):
    db_txt_files = glob.glob(os.path.join(tmp_SUT_path, base, '[a-z].txt'))
    list_from_txt = []
    for file in db_txt_files:
        with open(file) as f:
            for line in f:
                list_from_txt.append(line.replace('\n', ''))
    return sorted(list_from_txt)
