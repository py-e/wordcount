import os
import glob
import argparse
from string import ascii_letters

from words_dicts import top_100_english_words, from100_to1000_basic_words

TOP100 = '(in top 100)'
TOP1000 = '(from 100 to 1000)'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
for dirs in (('db',), ('db', 'txt'), ('db', 'txt', 'l1'), ('db', 'txt', 'l2')):
    path_now = SCRIPT_DIR
    for d in dirs:
        path_now = os.path.join(path_now, d)
    if not os.path.isdir(path_now):
        os.mkdir(path_now)
PATH_TO_BASE = os.path.join(SCRIPT_DIR, 'db', 'txt')


def get_text(user_path=None):
    if user_path:
        while 1:
            try:
                with open(user_path, encoding='utf-8') as f:
                    t = f.read().replace('\n', ' ')
                    break
            except FileNotFoundError:
                user_path = input(f'File {user_path} cannot be found, please check and provide the path: ')
    else:
        t = input('Provide the text: ')
    return t


def cleanup_beginning(word):
    """Recursion for more than one symbol, like:
    '("robots' -> 'robots'."""
    if not word[0].islower():
        return cleanup_beginning(word[1:])
    else:
        return word


def cleanup_end(word):
    """Recursion for more than one symbol, like:
    'robots").' -> 'robots'."""
    if not word[-1].islower():
        return cleanup_end(word[:-1])
    else:
        return word


def cleanup_word(word):
    """Remove first/last symbol if it's not a letter.
    ex.: '(robots' -> 'robots'; 'robots:' -> 'robots'."""
    word = cleanup_beginning(word)
    word = cleanup_end(word)
    return word


def convert_symbols(word):
    word = word.replace("`", "'").replace("’", "'")
    return word


def print_totals(words):
    print(f'Total number of the words: {sum(words[w][0] for w in words)}')
    print(f'Number of the unique words: {len(words)}')


def sort_and_exclude(words, exclude=None):
    if exclude:
        sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)
                        if v[1] not in exclude}
        words_num = len(sorted_words)
        words_num_str = f', the rest is shown below ({words_num}):' if words_num else ''
        print(f'Words from {exclude} are hidden{words_num_str}')
    else:
        sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)}

    # Data structure - key: word; value: [frequency, list, variants, index]
    for e, (k, v) in enumerate(sorted_words.items(), 1):
        v[3] = e
    return sorted_words


def print_sorted_by_number(words):
    """Print results, sorted descent by frequency.
    <number> <frequency> <word> <(in top 100/1000)> <variants counted>

    Handling options: -t100,-t1000,-l1,-l2."""
    if any([args.top1000_hide, args.top100_hide, args.list1, args.list2]):
        hide_list = []
        if args.top1000_hide:
            hide_list.extend((TOP100, TOP1000))
        elif args.top100_hide:
            hide_list.append(TOP100)
        if args.list1:
            hide_list.append('(l1)')
        if args.list2:
            hide_list.append('(l2)')
        sorted_words = sort_and_exclude(words, exclude=hide_list)

    else:
        sorted_words = sort_and_exclude(words)

    for w in sorted_words:
        print(f'{str(sorted_words[w][3])+":":<5}', end='')
        print(f'{sorted_words[w][0]:<5}', end='')
        print(f'{w:<10}', end='')
        print(f' {sorted_words[w][1]:<27}', end='')
        print(f' {sorted_words[w][2]}')

    return sorted_words


def add_to_counter(w, words_counter, l1, l2):
    if w not in words_counter:
        if w in top_100_english_words:
            word_list = TOP100
        elif w in from100_to1000_basic_words:
            word_list = TOP1000
        elif w in l1:
            word_list = '(l1)'
        elif w in l2:
            word_list = '(l2)'
        else:
            word_list = ''
        # Data structure - key: word; value: [frequency, list, variants, index]
        words_counter[w] = [0, word_list, '', '']
    words_counter[w][0] += 1


def get_words_from_txt(base):
    db_txt_files = glob.glob(os.path.join(PATH_TO_BASE, base, '[a-z].txt'))
    if not db_txt_files:
        print(f'Base {base} is empty for now')
    list_from_txt = []
    for file in db_txt_files:
        with open(file) as f:
            for line in f:
                list_from_txt.append(line.replace('\n', ''))
    return list_from_txt


def count_words(text):
    """
    Split words from text, then:
        - convert to lowercase,
        - clean up (symbols before and after),
        - convert some symbols to one format (apostrophe)
    And then add_to_counter() launched for each word.

    :returns: (words with frequency and base, not words)
    :rtype: (dict, set)
    """
    l1 = get_words_from_txt('l1')
    l2 = get_words_from_txt('l2')
    words_counter = {}
    not_words = set()
    for w in text.split():
        w = w.lower()
        if w.islower():
            w = cleanup_word(w)
            w = convert_symbols(w)
            add_to_counter(w, words_counter, l1, l2)
        else:
            not_words.add(w)

    return words_counter, not_words


def recount_variants(words, variants):
    for form_type, pair in variants.items():
        for form, word in pair:
            # exception: 'not' is not related to notes, noted, noting
            if word == 'not':
                continue

            words[word][2] += f"({words[form][0]} with {form_type}: {form})"
            words[word][0] += words[form][0]
            del words[form]


def count_apostrophes(words):
    apostrophes = {"'s": []}
    for w in words:
        if "'" in w:
            if w[-2:] == "'s":
                if w[:-2] in words:
                    apostrophes["'s"].append((w, w[:-2]))

    recount_variants(words, apostrophes)


def count_forms(words):
    """Find forms of word (end: ends, ended, ending)"""
    forms = {'s': [], 'es': [], 'ed': [], 'd': [], 'ing': []}
    for w in words:
        # s/es: plant <- plant[s], moss <- moss[es]
        if w[-1] == 's' and len(w) > 3:
            if w[:-1] in words:
                forms['s'].append((w, w[:-1]))
            elif w[-2:] == 'es':
                if w[:-2] in words:
                    forms['es'].append((w, w[:-2]))

        # ed/d: touch <- touch[ed], release <- release[d]
        if w[-2:] == 'ed' and len(w) > 4:
            if w[:-2] in words:
                forms['ed'].append((w, w[:-2]))
            elif w[:-1] in words:
                forms['d'].append((w, w[:-1]))

        # ing: touch <- touch[ing], write <- writ(e) <- writ[ing]
        if w[-3:] == 'ing' and len(w) > 5:
            if w[:-3] in words:
                forms['ing'].append((w, w[:-3]))
            elif w[:-3]+'e' in words:
                forms['ing'].append((w, w[:-3]+'e'))

    recount_variants(words, forms)


def print_sizes(sizes):
    print('\nSize of words:')
    for i in sorted(sizes):
        print(f'{i}, {sizes[i][1]}: {sizes[i][0]}')


def size_of_words(words):
    sizes = {}
    for w in words:
        if len(w) not in sizes:
            sizes[len(w)] = [[], 0]
        sizes[len(w)][0].append(w)
        sizes[len(w)][1] += 1

    return sizes


def write_to_base(base, word):
    with open(os.path.join(PATH_TO_BASE, base, word[0] + '.txt'), 'a+') as f:
        f.write(word+'\n')
    print(f'{word}, added to ({base})')


def get_words_by_indexes(indexes_to_add, list_words, words_to_add):
    for i in indexes_to_add:
        if i > 0:
            try:
                words_to_add.add(list_words[i-1])
            except IndexError:
                print(f'{i} - is out of range')
            except TypeError:
                print(f'{i} - should be int')
        else:
            print(f'{i} - is less than one')


def is_letter_first(word):
    if word[0] in ascii_letters:
        return True
    else:
        print(f'{word} - skipped, word should start with a letter')
        return False


def add_to_base(base, str_elements, words=None):
    elements = str_elements.split()
    indexes_to_add = set()
    words_to_add = set()
    for el in elements:
        if el.isdigit():
            indexes_to_add.add(int(el))
        else:
            if is_letter_first(el):
                words_to_add.add(el)

    if indexes_to_add:
        if words:
            list_words = list(words)
            get_words_by_indexes(indexes_to_add, list_words, words_to_add)
        else:
            print(f'seems a digit: {indexes_to_add}')

    for word in words_to_add:
        if word in top_100_english_words:
            print(f'{word}, already in {TOP100}')
        elif word in from100_to1000_basic_words:
            print(f'{word}, already in {TOP1000}')
        elif not word_in_base(base, word):
            write_to_base(base, word)
            try:
                words[word][1] = f'({base})'
            except (KeyError, TypeError):
                # word is not from text, just skip
                pass


def main():
    text = get_text(args.file)
    words, not_words = count_words(text)
    count_forms(words)
    count_apostrophes(words)
    print_totals(words)
    sorted_words = print_sorted_by_number(words)
    if not_words:
        print(f'Items excluded (not words): {not_words}')
    if args.size_of_words:
        print_sizes(size_of_words(sorted_words))

    print('You can add words to the lists (l1, l2)\n'
          'by indexes, like: "l1 add: 4 15 21"\n'
          'or just words, like: "l1 add: word, wood"\n'
          'l1 - list of words one - I know these words very well\n'
          'l2 - list of words two - I know the words basically, but can forget\n'
          '"p" - print the words\n'
          '"q" - to exit')
    while 1:
        command = input('Provide the command: ')
        if command[:7] in ('l1 add:', 'l2 add:'):
            add_to_base(command[:2], command[7:], sorted_words)
        elif command == 'p':
            sorted_words = print_sorted_by_number(words)
        elif command == 'q':
            break
        else:
            print('Command is not recognized')


def get_sorted_list_from_base(base, first_letters=''):
    if first_letters:
        stripped_fl = first_letters.strip()
        db_txt_file = os.path.join(PATH_TO_BASE, base, stripped_fl[0] + '.txt')
        list_from_txt = []
        try:
            with open(db_txt_file) as f:
                for line in f:
                    if line.startswith(stripped_fl):
                        list_from_txt.append(line.replace('\n', ''))
        except FileNotFoundError:
            print(f'No words in {base} starting with: {stripped_fl[0]}')
    else:
        list_from_txt = get_words_from_txt(base)

    list_from_txt.sort()
    return list_from_txt


def print_base(base, first_letters=''):
    sorted_words_from_base = get_sorted_list_from_base(base, first_letters)
    for e, word in enumerate(sorted_words_from_base, 1):
        print(e, word)


def word_in_base(base, word):
    try:
        db_txt_file = os.path.join(PATH_TO_BASE, base, word[0] + '.txt')
        with open(db_txt_file) as f:
            if word+'\n' in f:
                print(f'{word}, found in ({base})')
                return True
    except FileNotFoundError:
        # print(f'{word}, is not found in ({base})')
        return False


def rem_from_txt(base, word):
    db_txt_file = os.path.join(PATH_TO_BASE, base, word[0] + '.txt')
    lines = []
    removed = None
    word_found_in_txt = False
    with open(db_txt_file) as f:
        for line in f:
            lines.append(line)
            if word == line.replace('\n', ''):
                word_found_in_txt = True
    if word_found_in_txt:
        with open(db_txt_file, 'w') as f:
            for line in lines:
                if line.strip('\n') != word:
                    f.write(line)
        removed = word
    else:
        print(f'{word} is not found in {base}')
    return removed


def rem_words(base, str_words):
    list_words = str_words.lower().split()
    removed = []
    for w in list_words:
        removed_word = rem_from_txt(base, w)
        removed.append(removed_word)
    if removed:
        print(f'removed from ({base}): {removed}')


def edit_base():
    print('Options:\n'
          '"l1" - print l1 list\n'
          '"l2" - print l2 list\n'
          '"l1:wo" - print sublist (ex: from l1), beginning with letters (ex: wo)\n'
          '"l1 add: word wood" - add words (ex: word, wood) to the list (ex: l1)\n'
          '"l1 rem: word wood" - remove words from list\n'
          '"q" - to exit')
    while 1:
        command = input('Provide the command: ')
        if command in ('l1', 'l2'):
            print_base(command)
        elif command[:3] in ('l1:', 'l2:'):
            print_base(command[:2], command[3:])
        elif command[:2] in ('l1', 'l2'):
            if command[2:7] == ' add:':
                add_to_base(command[:2], command[7:])
            elif command[2:7] == ' rem:':
                rem_words(command[:2], command[7:])
        elif command == 'q':
            break
        else:
            print('Command is not recognized')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Count number of words in a text. '
                                                     'Detect words from top 100 and top 1000 lists.')
    arg_parser.add_argument('-f', '--file', action='store', type=str, help='path to text file')
    arg_parser.add_argument('-t100', '--top100_hide', action='store_true', help='do not print top 100 words')
    arg_parser.add_argument('-t1000', '--top1000_hide', action='store_true', help='do not print top 1000 words')
    arg_parser.add_argument('-l1', '--list1', action='store_true', help='do not print words from l1 list')
    arg_parser.add_argument('-l2', '--list2', action='store_true', help='do not print words from l2 list')
    arg_parser.add_argument('-s', '--size_of_words', action='store_true', help='print words length statistic')
    arg_parser.add_argument('-e', '--edit_base', action='store_true', help='edit list of words in l1 and l2 bases')
    args = arg_parser.parse_args()

    if args.edit_base:
        edit_base()
    else:
        main()
