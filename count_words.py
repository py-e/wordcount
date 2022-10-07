from words_dicts import top_100_english_words, from100_to1000_basic_words

TOP100 = '(in top 100)'
TOP1000 = '(in top from 100 to 1000)'


def insert_text():
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


def print_sorted_by_number(words):
    sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)}
    for w in sorted_words:
        print(f'{sorted_words[w][0]:<5}', end='')
        print(f'{w:<10}', end='')
        print(f' {sorted_words[w][1]:<27}', end='')
        print(f' {sorted_words[w][2]}')


def add_to_counter(w, words_counter):
    if w not in words_counter:
        if w in top_100_english_words:
            word_frequency = TOP100
        elif w in from100_to1000_basic_words:
            word_frequency = TOP1000
        else:
            word_frequency = ''
        words_counter[w] = [0, word_frequency, '']
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


def recount_variants(words, variant_list, variant_type):
    size = len(variant_type)
    for v in variant_list:
        if words[v[:-size]][2]:
            words[v[:-size]][2] = words[v[:-size]][2][:-1] + f"; {words[v][0]} with {variant_type}: {v})"
        else:
            words[v[:-size]][2] = f"({words[v][0]} with {variant_type}: {v})"
        words[v[:-size]][0] += words[v][0]
        del words[v]


def count_apostrophes(words):
    apostrophes = []
    for w in words:
        if "'" in w:
            if w[-2:] == "'s":
                if w[:-2] in words:
                    apostrophes.append(w)

    recount_variants(words, apostrophes, "'s")


def count_plurals(words):
    """Actually not only plurals, any words with s at the end
    (e.g. its, makes)"""
    plurals = []
    for w in words:
        if w[-1] == 's' and len(w) > 2:
            if w[:-1] in words:
                plurals.append(w)

    recount_variants(words, plurals, 's')


def main():
    words, not_words = count_words(insert_text())
    count_plurals(words)
    count_apostrophes(words)
    print_totals(words)
    print_sorted_by_number(words)
    if not_words:
        print(f'Items excluded (not words): {not_words}')


if __name__ == '__main__':
    main()
