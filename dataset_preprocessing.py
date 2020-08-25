import re
import time
import os
import numpy as np
import pandas as pd
from helper import transliterate

data_dir = 'Urdu datasets/'
regex_chars = '[\'".-]'
regex_alphabets = '[^a-zA-z]'
base_filename = 'Roman_Urdu_Sentences.txt'
timestamp = str(time.time()).replace('.', '')

choice = input('Merge into existing ' + base_filename + ' (y/n): ')

if choice == 'y' or choice == 'Y':
    filename = base_filename
else:
    filename = base_filename + '_' + str(timestamp) + '.txt'


def sub_initial_urdu(string):
    return re.sub(r"[^a-zA-z0-9,() ]", ' ', string.lower())


def sub_initial(string):
    return re.sub(r"[^a-zA-Z0-9' ]", ' ', str(string).lower())


def sub_quotes(string):
    return re.sub(r"\b'\B|\B'\b", ' ', string)


def sub_characters(string):
    return re.sub(r"(?<=\s)[dp](?=\s|$)", ' ', string)


def sub_space(string):
    return re.sub(r' {2,}', ' ', string)


def sub_nextline(string):
    return re.sub(r'\n', ' ', string)


# ------------------------------------------- SECTION - 1 --------------------------------------------------------------
data = []
data_series = pd.read_csv(data_dir + 'Roman Urdu DataSet.csv', header=None).iloc[:, 0]
preprocessed_data_series = data_series.apply(
    lambda l: sub_space(
        sub_characters(
            sub_quotes(
                sub_initial(l)))))

for line in preprocessed_data_series:
    if not line.isspace():
        data.append(line.strip())

np.savetxt(filename, data, fmt='%s')

# ------------------------------------------- SECTION - 2 --------------------------------------------------------------
with open(data_dir + 'counter.txt') as file:
    text = file.read()

with open('counter_roman_urdu.txt', 'w') as out:
    for sentence in sub_nextline(text).split('۔'):
        out.write(transliterate(sentence) + '\n')

# ------------------------------------------- SECTION - 3 --------------------------------------------------------------
data_series = pd.read_csv(data_dir + 'imdb_urdu_reviews.csv').iloc[:, 0]
with open('imdb_urdu_reviews_roman_urdu.txt', 'w') as out:
    for data in data_series:
        for sentence in data.split('۔'):
            out.write(transliterate(sentence) + '\n')

# ------------------------------------------- SECTION - 4 --------------------------------------------------------------
with open(data_dir + 'uner.txt', encoding="utf16") as file:
    text = file.read()

with open('uner_roman_urdu.txt', 'w') as out:
    for sentence in sub_nextline(re.sub(r"</?[A-Z]+>", ' ', text)).split('۔'):
        out.write(transliterate(sentence) + '\n')

# ------------------------------------------- SECTION - 5 --------------------------------------------------------------
text = ''
for f_name in os.listdir(data_dir + 'news/Fake'):
    with open(data_dir + 'news/Fake/' + f_name) as file:
        text += ' ' + file.read()

for f_name in os.listdir(data_dir + 'news/Real'):
    with open(data_dir + 'news/Real/' + f_name) as file:
        text += ' ' + file.read()

with open('news_roman_urdu.txt', 'w') as out:
    for sentence in sub_nextline(text).split('۔'):
        print(transliterate(sentence) + '\n')
