import os
import sys
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
@pytest.mark.parametrize('text_base_files_expected_notwords', [(p_text, p_base, p_files, p_expected, p_not_words)],
                    ids=['text432not'],
                    indirect=['text_base_files_expected_notwords'])
def test_count_words(text_base_files_expected_notwords):
    text, expected, not_words = text_base_files_expected_notwords
    ret_words_counter, ret_not_words = count_words.count_words(text)
    assert expected == ret_words_counter
    assert set(not_words) == ret_not_words


@pytest.mark.parametrize('base_files_first_expected', [
('l1', (['hello', 'hi'], ['goodbye'], ['bye']), None, None),    # expected None will be updated (to all words from files)
('l1', (['hello', 'hi'], ['goodbye'], ['bye']), 'he', ['hello']),
('l1', (['hello', 'hi'], ['goodbye'], ['bye']), 'n',  [])],     # new case (absent in unittest_integration_tests): file is not found for first letter(s)
                ids=['l1_hgb-all', 'l1_hgb-he_found', 'l1_hgb-n_not_found'],
                indirect=['base_files_first_expected'])
def test_get_sorted_list_from_base(base_files_first_expected):
    base, first, exp = base_files_first_expected
    if first is None:
        sorted_words_from_base = count_words.get_sorted_list_from_base(base)
    else:
        sorted_words_from_base = count_words.get_sorted_list_from_base(base, first_letters=first)
    assert sorted(exp) == sorted_words_from_base


@pytest.mark.parametrize('base_word', [('l1', 'hello')], ids=['l1_h'], indirect=['base_word'])
def test_write_read_base(base_word):
    base_dir, base, word_for_test = base_word
    count_words.write_to_base(base, word_for_test)
    assert word_for_test == file_content(base_dir, word_for_test)
    ret = count_words.word_in_base(base, word_for_test)
    assert ret is True


# Test cases: get data from the base (print base)

@pytest.mark.parametrize('create_txt_l1, input_command, expected', [
((('word',),),                                    'l1',     '1 word'),
((('word', 'world'), ('sword',)),                 'l1',     '1 sword\n2 word\n3 world'),
(None,                                            'l1',     'Base l1 is empty for now'),
((('word', 'world'), ('sword',)),                 'l1:w',   '1 word\n2 world'),
((('wolf', 'wood', 'wool', 'wrong'), ('sword',)), 'l1:woo', '1 wood\n2 wool'),
((('word', 'world'), ('sword',)),                 'l1:f',   'No words in l1 starting with: f'),
((('word', 'world'), ('sword',)),                 'l1:5',   'No words in l1 starting with: 5'),
((('word', 'world'), ('sword',)),                 'l1:w*',   '"q" - to exit')],
ids=['1_word', '3_words_2_files', 'empty', '1letter_2from3', '2letters_2from5', '1letter_not_found', 'wrong_symbol', 'wrong_second_symbol'],
                         indirect=['create_txt_l1', 'input_command'])
def test_print_base(create_txt_l1, input_command, capsys, expected):
    """edit_base(); print_base('l1'); get_sorted_list_from_base('l1', ''); get_words_from_txt('l1')"""
    # GIVEN words added to base @create_txt_l1 AND app in edit mode (start func: edit_base())
    count_words.edit_base()
    # WHEN command sent: @input_command
    # THEN correct data is printed: @expected
    printed = get_last_lines(capsys.readouterr(), len(expected))
    assert expected == printed


### Fixtures

@pytest.fixture
def text_base_files_expected_notwords(tmp_SUT_path, request):
    text, base, files, expected, not_words = request.param
    create_txt(tmp_SUT_path, base, files)
    yield text, expected, not_words


@pytest.fixture
def base_files_first_expected(tmp_SUT_path, request):
    base, files, first, exp = request.param
    all_words, _ = create_txt(tmp_SUT_path, base, files)
    if exp is None:
        exp = all_words
    yield base, first, exp


@pytest.fixture
def base_word(tmp_SUT_path, request):
    base, word_for_test = request.param
    base_dir = tmp_SUT_path / base
    base_dir.mkdir()
    yield base_dir, base, word_for_test


### Utils

@pytest.fixture
def tmp_SUT_path(tmp_path):
    original = count_words.PATH_TO_BASE
    count_words.PATH_TO_BASE = tmp_path
    yield tmp_path
    count_words.PATH_TO_BASE = original


def create_txt(tmp_SUT_path, base, files):
    base_dir = tmp_SUT_path / base
    base_dir.mkdir()
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


@pytest.fixture
def create_txt_l1(tmp_SUT_path, request):
    if files := request.param:
        base = 'l1'
        create_txt(tmp_SUT_path, base, files)
    yield


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
