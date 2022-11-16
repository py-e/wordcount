"""
Getting words from files by first letter (a.txt, b.txt, ...) in circle by one word from file.
To create files (1000words_1.txt, 1000words_2.txt, ...) with 1000 words separated by spaces.
"""

import glob

txt_files = glob.glob('[a-z].txt')

words_from_files = {}
for file in txt_files:
    with open(file) as f:
        words_from_files[file] = f.readlines()

file_counter = 1
word_counter = 0
while words_from_files:
    current_file_1000 = '1000words_'+str(file_counter)+'.txt'
    print('1000words_'+str(file_counter)+'.txt')
    lists_to_del = set()
    with open(current_file_1000, 'w') as f:
        for i in range(1000):
            for file in words_from_files:
                try:
                    word = words_from_files[file].pop(0)
                    f.write(word.replace('\n', ' '))
                    word_counter += 1
                    if word_counter == 1000:
                        break
                except IndexError:
                    # print(f'list from {file} is empty now')
                    lists_to_del.add(file)
            if word_counter == 1000:
                break

    for file in lists_to_del:
        del words_from_files[file]

    word_counter = 0
    file_counter += 1
