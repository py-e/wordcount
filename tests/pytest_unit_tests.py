import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import count_words


p_cleanup_beginning = (
    pytest.param('-15:recursion', 'recursion',      id='symbol_at_the_beginning'),
    pytest.param('recursion', 'recursion',          id='clean_word'),
    pytest.param('recur-sion', 'recur-sion',        id='symbol_inside'),
    pytest.param('recursion-#7;', 'recursion-#7;',  id='symbol_at_the_end'))
@pytest.mark.parametrize('send, exp', p_cleanup_beginning)
def test_cleanup_beginning(send, exp):
    """count_words.cleanup_beginning(word)"""
    ret = count_words.cleanup_beginning(send)
    assert exp == ret


p_cleanup_end = (
    pytest.param('recursion-#7;', 'recursion',      id='symbol_at_the_end'),
    pytest.param('recursion', 'recursion',          id='clean_word'),
    pytest.param('recur-sion', 'recur-sion',        id='symbol_inside'),
    pytest.param('-15:recursion;', '-15:recursion', id='symbol_at_the_beginning'))
@pytest.mark.parametrize('send, exp', p_cleanup_end)
def test_cleanup_end(send, exp):
    """count_words.cleanup_beginning(word)"""
    ret = count_words.cleanup_end(send)
    assert exp == ret


@pytest.mark.parametrize('send, exp', (('-15:recursion-#7;', 'recursion'),), ids=('symbols_at_both_sides',))
def test_cleanup_word(send, exp):
    """count_words.cleanup_beginning(word)
    Sort of integration test: launch other modules (cleanup_beginning, cleanup_end)"""
    ret = count_words.cleanup_word(send)
    assert exp == ret


id1 = 'sort_only'
inp1 = {'one':     [1, '(in top 100)', '', ''],
        'ten':     [10, '(from 100 to 1000)', '', ''],
        'fifteen': [15, '', '(1 with s: fifteens)', ''],
        'two':     [2, '(in top 100)', '', ''],
        'eighty':  [80, '(l1)', '', ''],
        'twice':   [2, '(from 100 to 1000)', '', '']}
exc1 = None
out1 = {'one':     [1, '(in top 100)', '', 6],
        'ten':     [10, '(from 100 to 1000)', '', 3],
        'fifteen': [15, '', '(1 with s: fifteens)', 2],
        'two':     [2, '(in top 100)', '', 4],
        'eighty':  [80, '(l1)', '', 1],
        'twice':   [2, '(from 100 to 1000)', '', 5]}

id2 = 'sort_and_exclude'
inp2 = inp1
exc2 = ['(in top 100)', '(l1)']
out2 = {'ten':     [10, '(from 100 to 1000)', '', 2],
        'fifteen': [15, '', '(1 with s: fifteens)', 1],
        'twice':   [2, '(from 100 to 1000)', '', 3]}

id3 = 'sort_only_empty'
inp3 = {}
exc3 = None
out3 = {}

id4 = 'sort_and_exclude_empty'
inp4 = {}
exc4 = ['(in top 100)', '(l1)']
out4 = {}

id5 = 'sort_only_wrong_type_int_instead_str'
inp5 = {1: [1, '', '', '']}
exc5 = None
out5 = inp5

id6 = 'wrong_exclude_value'
inp6 = {'word': [1, '', '', ''], 'and': [5, '', '', '']}
exc6 = ['(no such value)']
out6 = {'word': [1, '', '', 2], 'and': [5, '', '', 1]}

@pytest.mark.parametrize('inp, exc, out',
                         ((inp1, exc1, out1), (inp2, exc2, out2), (inp3, exc3, out3),
                          (inp4, exc4, out4), (inp5, exc5, out5), (inp6, exc6, out6)),
                         ids=(id1, id2, id3, id4, id5, id6))
def test_dataSortAndExclude(inp, exc, out):
    """count_words.sort_and_exclude(words, exclude=None)"""
    if exc:
        ret_sorted_words = count_words.sort_and_exclude(inp, exc)
    else:
        ret_sorted_words = count_words.sort_and_exclude(inp)
    assert out == ret_sorted_words

id7 = 'sort_only_wrong_type_int_instead_list'
inp7 = {'word': 1}
exc7 = None
out7 = "'int' object is not subscriptable"

id8 = 'wrong_signature'
inp8 = {'word': [1, '', '', '']}
exc8 = (['(in top 100)', '(l1)'], 'unexpected value')
out8 = 'takes from 1 to 2 positional arguments but 3 were given'

@pytest.mark.parametrize('inp, exc, out', ((inp7, exc7, out7), (inp8, exc8, out8)), ids=(id7, id8))
def test_dataSortAndExclude_exception(inp, exc, out):
    """count_words.sort_and_exclude(words, exclude=None)"""
    with pytest.raises(TypeError) as excinfo:
        if exc:
            ret_sorted_words = count_words.sort_and_exclude(inp, exc[0], exc[1])
        else:
            ret_sorted_words = count_words.sort_and_exclude(inp)
    assert out in str(excinfo)


@pytest.mark.parametrize(
'word, l1, l2, words_counter, num,                                                          exp',

(('word', ['word', 'test', 'debug'], ['prerequisite', 'snippet'], {}, 1,                    {'word': [1, '(from 100 to 1000)', '', '']}),
('word', ['word', 'test', 'debug'], ['prerequisite', 'snippet'], {}, 2,                     {'word': [2, '(from 100 to 1000)', '', '']}),
('wordnotinlist', ['wordnotinlist', 'test', 'debug'], ['prerequisite', 'snippet'], {}, 1,   {'wordnotinlist': [1, '(l1)', '', '']}),
('wordnotinlist', ['test', 'debug'], ['prerequisite', 'snippet'], {}, 1,                    {'wordnotinlist': [1, '', '', '']})),

ids=('from_top1000_once', 'from_top1000_twice', 'once_l1', 'once'))
def test_countWord(word, l1, l2, words_counter, num, exp):
    """count_words.add_to_counter(w, words_counter, l1, l2)"""
    for i in range(num):
        count_words.add_to_counter(word, words_counter, l1, l2)
    assert exp == words_counter


@pytest.mark.parametrize('words, exp',
(({'moss': [1, '', '', ''], "moss's": [1, '', '', '']},     {'moss': [2, '', "(1 with 's: moss's)", '']}),),
                         ids=('checking_s',))
def test_count_apostrophes(words, exp):
    """count_words.count_apostrophes(words)
    Kind of integration test: count_apostrophes launches recount_variants"""
    count_words.count_apostrophes(words)
    assert exp == words


@pytest.mark.parametrize('words, exp',

(({'word': [1, '(from 100 to 1000)', '', ''], 'words': [1, '', '', ''], 'worded': [1, '', '', ''], 'wording': [1, '', '', '']},
 {'word': [4, '(from 100 to 1000)', '(1 with s: words)(1 with ed: worded)(1 with ing: wording)', '']}),

({'moss': [1, '', '', ''], 'mosses': [1, '', '', '']},
 {'moss': [2, '', '(1 with es: mosses)', '']}),

({'observe': [1, '', '', ''], 'observed': [1, '', '', '']},
 {'observe': [2, '', '(1 with d: observed)', '']})),

                         ids=('_s_ed_ing', '_es', '_d'))
def test_count_forms(words, exp):
    """count_words.count_forms(words)
    Kind of integration test: count_forms launches recount_variants
    Checking endings: 's', 'es', 'ed', 'd', 'ing'
    """
    count_words.count_forms(words)
    assert exp == words


@pytest.mark.parametrize('words, exp',

(({'a': [1, '(in top 100)', '', 1]},
 {1: [['a'], 1]}),

({'dot': [2, '', '', 1], 'ten': [1, '(from 100 to 1000)', '', 2]},
 {3: [['dot', 'ten'], 2]}),

({'a': [1, '(in top 100)', '', 1], 'objectification': [1, '', '', 2]},
 {1: [['a'], 1], 15: [['objectification'], 1]})),

                         ids=('1_word_1_symbol', '2_words_3_symbols_each', '2_words_1_and_15_symbols'))
def test_sizeOfWords(words, exp):
    """
    count_words.size_of_words(words)
    Simple test: one word counted
    """
    ret_sizes = count_words.size_of_words(words)
    assert exp == ret_sizes


@pytest.mark.parametrize('index, list_words, to_add, exp',
(({2},  ['one', 'two', 'three'], set(),             {'two'}),
({2, 3},['one', 'two', 'three'], set(),             {'two', 'three'}),
({0},   ['one', 'two', 'three'], set(),             set()),
({0.5}, ['one', 'two', 'three'], set(),             set())),
                         ids=('one_word', 'two_words', 'index_out_of_range', 'index_not_int'))
def test_findWordInDataStructureByIndex(index, list_words, to_add, exp):
    """count_words.get_words_by_indexes(indexes_to_add, list_words, words_to_add)"""
    count_words.get_words_by_indexes(index, list_words, to_add)
    assert exp == to_add


@pytest.mark.parametrize('mock_file, expected', [[
    _mock_file := """hello unit test

            and more
            """,
    _mock_file.replace('\n', ' ')]],
                         indirect=['mock_file'],
                         ids=['file_with_5_words'])
def test_mock_read_text_from_file(mock_file, expected):
    """count_words.get_text()"""
    ret = count_words.get_text(mock_file)
    assert expected == ret


@pytest.mark.parametrize('mock_file, expected', [[
    _mock_file := 'cell\ncadmium\n',
    _mock_file.split('\n')[:-1]]],
                         indirect=['mock_file'],
                         ids=['file_2_words'])
def test_mock_get_words_from_txt(mock_glob, mock_file, expected):
    """count_words.get_words_from_txt()"""
    base = 'l2'     # actually does not participate in file path creation (fake path is used)
    ret = count_words.get_words_from_txt(base)
    assert expected == ret


@pytest.mark.parametrize('mock_files, expected', [[
    _mock_files := (['cell', 'cadmium'], ['velocity']),
    [word for file in _mock_files for word in file]]],
                         indirect=['mock_files'],
                         ids=['3_words_in_2_files'])
def test_mock_get_words_from_2_txt_files(mock_files, expected):
    """count_words.get_words_from_txt(base)"""
    base = 'l2'     # actually does not participate in file path creation (fake path is used)
    ret = count_words.get_words_from_txt(base)


### Fixtures

from unittest.mock import patch, mock_open

FAKE_FILE_PATH = 'some/mock/path'


@pytest.fixture
def mock_file(request):
    with patch('count_words.open', new=mock_open(read_data=request.param)) as _file:
        yield FAKE_FILE_PATH

        # Additional check (that the object was called only one time)
        try:
            _file.assert_called_once_with(FAKE_FILE_PATH, encoding='utf-8')
        except AssertionError as e:
            if 'expected call not found' in str(e) and 'utf-8' in str(e):
                _file.assert_called_once_with(FAKE_FILE_PATH)
            else:
                raise e


@pytest.fixture
def mock_glob():
    with patch('count_words.glob.glob', return_value=[FAKE_FILE_PATH]) as _file:
        yield


@pytest.fixture
def mock_files(request):
    base_dir = os.path.join(count_words.PATH_TO_BASE, 'l_base')
    input_words = []
    file_paths = []
    for file in request.param:
        file_name = file[0][0] + '.txt'
        file_path = os.path.join(base_dir, file_name)
        file_paths.append(file_path)
        words_in_file = ''
        for word in file:
            words_in_file += word+'\n'
        input_words.append(words_in_file)

    mock_files = [mock_open(read_data=content).return_value for content in input_words]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch('count_words.glob.glob', return_value=file_paths):
        with patch('count_words.open', new=mock_opener) as _file:
            yield
