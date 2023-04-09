import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import count_words


# Notice, run this test with --noconftest (don't load hook)
# $ pytest original_test_with_parameters.py --noconftest

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


def get_last_lines(captured, number):
    text_all = captured.out[:-1]   # remove last new line '\n'
    text_end = text_all[-number:]
    return text_end
