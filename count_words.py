from words_dicts import top_100_english_words

TOP100 = '(in top 100)'

def insert_text():
    t = input('Provide the text: ')
    return t


def cleanup_word(word):
    return word[:-1] if word[-1] in (',', '.', '?', '!') else word


def print_sorted_by_number(words):
    sorted_words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1][0], reverse=True)}
    print(f'Total number of detected words: {len(sorted_words)}')
    for w in sorted_words:
        print(w, sorted_words[w][0], sorted_words[w][1])


def count_words(text):
    splitted_text = text.split()
    words_counter = {}
    for w in splitted_text:
        w = w.lower()
        w = cleanup_word(w)
        if w in words_counter:
            words_counter[w][0] += 1
        else:
            word_frequency = TOP100 if w in top_100_english_words else ''
            words_counter[w] = [1, word_frequency]
    return words_counter


def main():
    words = count_words(insert_text())
    print_sorted_by_number(words)


if __name__ == '__main__':
    main()
