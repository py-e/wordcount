import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import count_words


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


# Utils

class Utils:
    @staticmethod
    def file_content(base_dir, word):
        base_file = word[0]+'.txt'
        file_path = os.path.join(base_dir, base_file)
        with open(file_path) as f:
            cont = f.read()
        return cont.replace('\n', '')


@pytest.fixture
def utils():
    return Utils


@pytest.fixture
def get_last_lines():
    def inner_get_last_lines(captured, number):
        text_all = captured.out[:-1]   # remove last new line '\n'
        text_end = text_all[-number:]
        return text_end
    return inner_get_last_lines
