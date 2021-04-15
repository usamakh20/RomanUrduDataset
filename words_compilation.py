import re
import time
import numpy as np
import pandas as pd
from collections import Counter
from helper import trans, is_english_letters, sub_space, flow

data_dir = 'Urdu datasets/'
regex_chars = '[\'".-`]'
regex_alphabets = '[^a-zA-z]'
base_filename = 'Roman urdu datasets/Roman_Urdu_Words.csv'
timestamp = str(time.time()).replace('.', '')


def fun1():
    extracted_words = []
    with open(data_dir + 'English-Urdu-Roman.txt') as file:
        for line_number, line in enumerate(file):
            if not line.isspace():
                preprocessed_line = re.sub(regex_chars, '', line.strip())
                words = [word.strip() for word in preprocessed_line.split(':') if word.strip()]
                sub_words = words[-1].split()
                for sub_word in sub_words:
                    extracted_words.append(sub_word.strip())
    return extracted_words


def fun2():
    extracted_words = []
    for fname in ['Negative-and Positive-Words_pos.txt', 'Negative-and Positive-Words_neg.txt']:
        with open(data_dir + fname) as file:
            for line_number, line in enumerate(file):
                if not line.isspace():
                    preprocessed_line = re.sub(regex_chars, '', line.strip())
                    words = [word.strip() for word in preprocessed_line.split(':') if word.strip()]

                    if is_english_letters(words[-2]) and words[0] != words[1]:
                        sub_words = words[-2].split()
                        for sub_word in sub_words:
                            if sub_word != words[0]:
                                extracted_words.append(sub_word.strip())

            extracted_words.append('rehm')
            extracted_words.append('ajuti')

    return extracted_words


def fun3():
    extracted_words = []
    data_series = pd.read_csv(data_dir + 'Roman Urdu DataSet.csv', header=None).iloc[:, 0]
    preprocessed_data_series = data_series.apply(lambda l: re.sub(r'[^a-zA-Z. ]|(\.{2,})', ' ', str(l).lower()))
    for line in preprocessed_data_series:
        words = [word.strip(' .') for word in line.split(' ') if word.strip(' .')]
        extracted_words.extend(words)

    return extracted_words


def fun4():
    extracted_words = []
    for fname in ['urdu_stopwords.txt', 'urdu_stopwords_2.txt', 'urdu_stopwords_3.txt']:
        with open(data_dir + fname) as file:
            for line_number, line in enumerate(file):
                if not line.isspace():
                    preprocessed_line = re.sub('\n', '', line.strip())
                    word = re.sub(regex_alphabets, '', trans(preprocessed_line))
                    if word.strip():
                        extracted_words.append(word.strip())

    return extracted_words


def fun5():
    extracted_words = []
    mappings = [str.strip, sub_space]
    with open('data.txt', 'r', encoding="utf-8") as file:
        for i, line in enumerate(file):
            if not line.isspace():
                preprocessed_line = flow(re.sub(regex_chars, ' ', re.sub(regex_alphabets, ' ', line)), mappings)
                words = [word.strip(' .') for word in preprocessed_line.split(' ') if word.strip(' .')]
                extracted_words.extend(words)

    return extracted_words


if __name__ == '__main__':
    choice = input('Merge into existing ' + base_filename + ' (y/n): ')

    if choice == 'y' or choice == 'Y':
        existing_words = np.loadtxt(base_filename, delimiter=',', dtype=str)[1:]
    else:
        existing_words = np.empty((0, 2), dtype=str)

    filename = base_filename + '_' + str(timestamp) + '.csv'
    existing_words_counter = Counter(
        {key: value for key, value in zip(np.vectorize(str.lower)(existing_words[:, 0]), existing_words[:, 1].astype(int))})

    new_words_counter = Counter(map(str.lower, fun5()))
    print("%d Unique words extracted from %d words" % (len(new_words_counter), sum(new_words_counter.values())))
    roman_urdu_words_counter = new_words_counter + existing_words_counter

    for word in list(roman_urdu_words_counter):
        if len(word) < 2:
            del roman_urdu_words_counter[word]

    with open(filename, 'w') as f:
        f.write('Words,Frequency\n')
        for k, v in roman_urdu_words_counter.most_common():
            f.write("{},{}\n".format(k, v))

# TODO:
#  For spelling correction use existing transliteration systems based on machine learning that predict closest urdu
#  word. Reconvert the urdu word back to roman urdu for correct spelling. Assigning weight to correct words using
#  their frequencies.
#  Words after which have edit distance = 1 are misspellings
