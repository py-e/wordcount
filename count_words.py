
def insert_text():
    t = input('please, provide the text:')
    return t


def cleanup_word(word):
    return word[:-1] if word[-1] in (',', '.', '?', '!') else word


def count_words(text):
    splitted_text = text.split()
    words_counter = {}
    for w in splitted_text:
        w = cleanup_word(w)
        if w in words_counter:
            words_counter[w] += 1
        else:
            words_counter[w] = 1
    sorted_words = {k: v for k, v in sorted(words_counter.items(), key=lambda item: item[1], reverse=True)}
    # print(sorted_words)
    print(f'Total number of detected words: {len(sorted_words)}')
    for w in sorted_words:
        print(w, sorted_words[w])


def main():
    count_words(insert_text())


if __name__ == '__main__':
    main()
