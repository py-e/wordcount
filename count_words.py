from words_dicts import top_100_english_words

TOP100 = '(in top 100)'


def insert_text():
    t = input('Provide the text: ')
    return t


def cleanup_word(word):
    """Remove first/last symbol if it's not a letter.
    ex.: '(robots' -> 'robots'; 'robots:' -> 'robots'."""
    word = word[1:] if not word[0].islower() else word
    word = word[:-1] if not word[-1].islower() else word
    return word


def print_sorted_by_number(words):
    print(f'Total number of the words: {sum(words[w][0] for w in words)}')
    print(f'Number of the unique words: {len(words)}')

    sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)}
    for w in sorted_words:
        print(f'{sorted_words[w][0]:<5}', end='')
        print(f' {w:<10}', end='')
        print(sorted_words[w][1])


def count_words(text):
    # text_words = (cleanup_word(w).lower() for w in text.split())
    words_counter = {}
    not_words = set()
    for w in text.split():
        w = w.lower()
        if w.islower():
            w = cleanup_word(w)
            if w in words_counter:
                words_counter[w][0] += 1
            else:
                word_frequency = TOP100 if w in top_100_english_words else ''
                words_counter[w] = [1, word_frequency]
        else:
            not_words.add(w)
    return words_counter, not_words


def main():
    words, not_words = count_words(insert_text())
    print_sorted_by_number(words)
    print(f'Items excluded (not words): {not_words}')


if __name__ == '__main__':
    main()
