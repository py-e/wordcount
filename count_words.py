import argparse

from words_dicts import top_100_english_words, from100_to1000_basic_words

TOP100 = '(in top 100)'
TOP1000 = '(from 100 to 1000)'

arg_parser = argparse.ArgumentParser(description='Count number of words in a text. '
                                                 'Detect words from top 100 and top 1000 lists.')
arg_parser.add_argument('-f', '--file', action='store', type=str, help='path to text file')
arg_parser.add_argument('-t100', '--top100_hide', action='store_true', help='do not print top 100 words')
arg_parser.add_argument('-t1000', '--top1000_hide', action='store_true', help='do not print top 1000 words')
arg_parser.add_argument('-s', '--size_of_words', action='store_true', help='print words length statistic')
args = arg_parser.parse_args()


def get_text():
    if args.file:
        user_path = args.file
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


def sort_and_exclude(words, exclude=None, exc_comment=None):
    if exclude:
        sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)
                        if v[1] not in exclude}
        words_num = len(sorted_words)
        words_num_str = f', unique words shown below ({words_num}):' if words_num else ''
        print(f'Words from Top {exc_comment} list are hidden{words_num_str}')
    else:
        sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)}

    # Add index to the words data structure.
    # key: word; value: [frequency, list, variants, index]
    for e, (k, v) in enumerate(sorted_words.items(), 1):
        v.append(e)
    return sorted_words


def print_sorted_by_number(words):
    """Print results, sorted descent by frequency.
    <number> <frequency> <word> <(in top 100/1000)> <variants counted>

    Handling options: -t100 (--top100_hide) and -t1000 (--top1000_hide)."""
    if args.top1000_hide:
        sorted_words = sort_and_exclude(words, exclude=(TOP100, TOP1000), exc_comment='1000')
    elif args.top100_hide:
        sorted_words = sort_and_exclude(words, exclude=(TOP100,), exc_comment='100')
    else:
        sorted_words = sort_and_exclude(words)

    for w in sorted_words:
        print(f'{str(sorted_words[w][3])+":":<5}', end='')
        print(f'{sorted_words[w][0]:<5}', end='')
        print(f'{w:<10}', end='')
        print(f' {sorted_words[w][1]:<27}', end='')
        print(f' {sorted_words[w][2]}')


def add_to_counter(w, words_counter):
    if w not in words_counter:
        if w in top_100_english_words:
            word_list = TOP100
        elif w in from100_to1000_basic_words:
            word_list = TOP1000
        else:
            word_list = ''
        words_counter[w] = [0, word_list, '']
    words_counter[w][0] += 1


def count_words(text):
    words_counter = {}
    not_words = set()
    for w in text.split():
        w = w.lower()
        if w.islower():
            w = cleanup_word(w)
            w = convert_symbols(w)
            add_to_counter(w, words_counter)
        else:
            not_words.add(w)

    return words_counter, not_words


def recount_variants(words, variant_list):
    for form, word, form_type in variant_list:

        # exception: 'not' is not related to notes, noted, noting
        if word == 'not':
            continue

        words[word][2] += f"({words[form][0]} with {form_type}: {form})"
        words[word][0] += words[form][0]
        del words[form]


def count_apostrophes(words):
    apostrophes = []
    for w in words:
        if "'" in w:
            if w[-2:] == "'s":
                if w[:-2] in words:
                    apostrophes.append((w, w[:-2], "'s"))

    recount_variants(words, apostrophes)


def count_forms(words):
    """Find forms of word (end: ends, ended, ending)"""
    # TODO: refactoring
    forms = []
    for w in words:
        if w[-1] == 's' and len(w) > 3:
            if w[:-1] in words:
                forms.append((w, w[:-1], 's'))
            elif w[-2:] == 'es':
                if w[:-2] in words:
                    forms.append((w, w[:-2], 'es'))
        if w[-2:] == 'ed' and len(w) > 4:
            if w[:-2] in words:
                forms.append((w, w[:-2], 'ed'))
            elif w[:-1] in words:
                forms.append((w, w[:-1], 'd'))
        if w[-3:] == 'ing' and len(w) > 5:
            if w[:-3] in words:
                forms.append((w, w[:-3], 'ing'))
            elif w[:-3]+'e' in words:
                forms.append((w, w[:-3]+'e', 'ing'))

    if forms:
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


def main():
    words, not_words = count_words(get_text())
    count_forms(words)
    count_apostrophes(words)
    print_totals(words)
    print_sorted_by_number(words)
    if not_words:
        print(f'Items excluded (not words): {not_words}')
    if args.size_of_words:
        print_sizes(size_of_words(words))


if __name__ == '__main__':
    main()
