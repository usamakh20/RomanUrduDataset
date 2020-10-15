import re
import time
import numpy as np
import pandas as pd
from collections import Counter
from helper import trans, is_english_letters

data_dir = 'Urdu datasets/'
new_words = np.empty(0, dtype=str)
regex_chars = '[\'".-]'
regex_alphabets = '[^a-zA-z]'
base_filename = 'Roman urdu datasets/Roman_Urdu_Words.csv'
timestamp = str(time.time()).replace('.', '')

choice = input('Merge into existing ' + base_filename + ' (y/n): ')

if choice == 'y' or choice == 'Y':
    existing_words = np.loadtxt(base_filename, delimiter=',', dtype=str)[1:]
    filename = base_filename
else:
    existing_words = np.empty((0, 2), dtype=str)
    filename = base_filename + '_' + str(timestamp) + '.csv'

existing_words_counter = Counter(
    {key: value for key, value in zip(existing_words[:, 0], existing_words[:, 1].astype(int))})

# ------------------------------------------- SECTION - 1 --------------------------------------------------------------
with open(data_dir + 'English-Urdu-Roman.txt') as file:
    for line_number, line in enumerate(file):
        if not line.isspace():
            preprocessed_line = re.sub(regex_chars, '', line.strip())
            words = [word.strip() for word in preprocessed_line.split(':') if word.strip()]

            sub_words = words[-1].split()
            for sub_word in sub_words:
                new_words = np.append(new_words, sub_word.strip())

# ------------------------------------------- SECTION - 2 --------------------------------------------------------------
for filename in ['Negative-and Positive-Words_pos.txt', 'Negative-and Positive-Words_neg.txt']:
    with open(data_dir + filename) as file:
        for line_number, line in enumerate(file):
            if not line.isspace():
                preprocessed_line = re.sub(regex_chars, '', line.strip())
                words = [word.strip() for word in preprocessed_line.split(':') if word.strip()]

                if is_english_letters(words[-2]) and words[0] != words[1]:
                    sub_words = words[-2].split()
                    for sub_word in sub_words:
                        if sub_word != words[0]:
                            new_words = np.append(new_words, sub_word.strip())

        new_words = np.append(new_words, 'rehm')
        new_words = np.append(new_words, 'ajuti')

# ------------------------------------------- SECTION - 3 --------------------------------------------------------------
data_series = pd.read_csv(data_dir + 'Roman Urdu DataSet.csv', header=None).iloc[:, 0]
preprocessed_data_series = data_series.apply(lambda l: re.sub(r'[^a-zA-Z. ]|(\.{2,})', ' ', str(l).lower()))
for line in preprocessed_data_series:
    words = [word.strip(' .') for word in line.split(' ') if word.strip(' .')]
    new_words = np.append(new_words, words)

# ------------------------------------------- SECTION - 4 --------------------------------------------------------------
for filename in ['urdu_stopwords.txt', 'urdu_stopwords_2.txt', 'urdu_stopwords_3.txt']:
    with open(data_dir + filename) as file:
        for line_number, line in enumerate(file):
            if not line.isspace():
                preprocessed_line = re.sub('\n', '', line.strip())
                word = re.sub(regex_alphabets, '', trans(preprocessed_line))
                if word.strip():
                    new_words = np.append(new_words, word.strip())

new_words_counter = Counter(new_words)
print("%d Unique words extracted from %d words" % (len(new_words_counter), len(new_words)))
roman_urdu_words_counter = new_words_counter + existing_words_counter
roman_urdu_words = np.array(list(roman_urdu_words_counter.items())).reshape(-1, 2)
roman_urdu_words_sorted = roman_urdu_words[np.argsort(roman_urdu_words[:, 0])]

pd.DataFrame({'Words': roman_urdu_words_sorted[:, 0], 'Frequency': roman_urdu_words_sorted[:, 1]}) \
    .to_csv(filename, index=False)

# For spelling correction use existing transliteration systems based on machine learning that predict closest urdu
# word. Reconvert the urdu word back to roman urdu for correct spelling. Assigning weight to correct words using
# their frequencies.
