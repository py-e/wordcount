# import time
import timeit


# def timer(func):
#     def wrap_time(*args, **kwargs):
#         st = timeit.timeit()
#         ret = func(*args, **kwargs)
#         ft = time.time()
#         print(f'Execution time ({func.__name__}): {ft - st} sec.')
#         return ret
#     return wrap_time

def timer(func):
    def wrap_time(*args, **kwargs):
        ex_time, ret = timeit.timeit(lambda: func(*args, **kwargs), number=1)
        print(f'Execution time ({func.__name__}): {ex_time} sec.')
        return ret
    return wrap_time

# monkey-patch template in timeit.py
# https://stackoverflow.com/questions/24812253/how-can-i-capture-return-value-with-python-timeit-module
'''
Change template in timeit.py

FROM:
template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        {stmt}
        pass
    _t1 = _timer()
    return _t1 - _t0
"""

TO:
template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        ret = {stmt}
        pass
    _t1 = _timer()
    return _t1 - _t0, ret
"""

'''
