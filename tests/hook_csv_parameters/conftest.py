import ast
import pandas as pd


# Hook to load parameters from csv file

def pytest_generate_tests(metafunc):
    parameters_file = metafunc.function.__name__+'.csv'
    argnames, testdata, ids, indirect = get_data_from_csv(parameters_file)
    metafunc.parametrize(argnames, testdata, ids=ids, indirect=indirect)


def get_data_from_csv(parameters_file):
    try:
        indirect_row = pd.read_csv(parameters_file, sep=';', nrows=1, header=None)
        indirect_tuple = next(indirect_row.itertuples(index=False, name=None))
        column_row = pd.read_csv(parameters_file, sep=';', skiprows=[0], nrows=1, header=None)
        column_tuple = next(column_row.itertuples(index=False, name=None))
        argnames = ', '.join(column_tuple[1:])
        indirect = []
        for i in zip(indirect_tuple, column_tuple):
            if i[0] == 'indirect':
                indirect.append(i[1])

        df = pd.read_csv(parameters_file, sep=';', skiprows=[0], converters={'base_files': ast.literal_eval})
        df.expected = df.expected.str.replace('\\n', '\n')
        df.expected = df.expected.str.replace('\\"', '"')
        ids = []
        testdata = []
        for index, row in df.iterrows():
            id = str(row[:1].item())
            td = tuple(row[1:])
            ids.append(id)
            testdata.append(td)

        return argnames, testdata, ids, indirect

    except FileNotFoundError:
        test_name = parameters_file.split('.')[0]
        raise Exception(f'\nFor test: "{test_name}"\nExpected: "{parameters_file}" file with parameters\n'
                        f'But .csv file is not found (it should be located in the same directory as .py '
                        f'file with the test)') from None
