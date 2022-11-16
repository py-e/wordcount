"""
Create files with words by first letter (a.txt, b.txt, ...).
From one file with words.

Where to find file with list of English words, examples:
- 58K words: http://www.mieliestronk.com/corncob_lowercase.txt
- 370K words: https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
"""

import os

filename = 'corncob_lowercase.txt'

first_letter = 'temp_to_start'
fl_file = open(first_letter, 'w')
with open(filename) as f:
    for line in f:
        if line[0] != first_letter:
            fl_file.close()
            first_letter = line[0]
            fl_file = open(first_letter + '.txt', 'a+')
        fl_file.write(line)

fl_file.close()
os.remove('temp_to_start')
