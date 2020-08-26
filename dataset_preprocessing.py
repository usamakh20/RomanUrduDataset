import re
import os
import time
import logging
import numpy as np
import pandas as pd
from helper import transliterate

data_dir = 'Urdu datasets/'


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


def fun1():
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

    np.savetxt('Roman_Urdu_Sentences.txt', data, fmt='%s')


def fun2(count):
    with open(data_dir + 'counter.txt') as file:
        text = file.read()

    with open('counter_roman_urdu.txt', 'a') as out:
        process(out, count, enumerate(sub_nextline(text).split('۔')))


def fun3(count):
    data_series = pd.read_csv(data_dir + 'imdb_urdu_reviews.csv').iloc[:, 0]
    with open('imdb_urdu_reviews_roman_urdu.txt', 'a') as out:
        for i, data in enumerate(data_series):
            process(out, count, enumerate(data.split('۔')), i)


def fun4(count):
    with open(data_dir + 'uner.txt', encoding="utf16") as file:
        text = file.read()

    with open('uner_roman_urdu.txt', 'a') as out:
        process(out, count, enumerate(sub_nextline(re.sub(r"</?[A-Z]+>", ' ', text)).split('۔')))


def fun5(count):
    text = ''
    for f_name in os.listdir(data_dir + 'news/Fake'):
        with open(data_dir + 'news/Fake/' + f_name) as file:
            text += ' ' + file.read()

    for f_name in os.listdir(data_dir + 'news/Real'):
        with open(data_dir + 'news/Real/' + f_name) as file:
            text += ' ' + file.read()

    with open('news_roman_urdu.txt', 'a') as out:
        process(out, count, enumerate(sub_nextline(text).split('۔')))


def process(out_file, count, numbered_sentences, i=0):
    total_time = 0
    start=False
    for index, sentence in numbered_sentences:
        if index==count:
            start=True
            pass

        if start:
            start_time = time.time()
            out_file.write(transliterate(sentence) + '\n')
            current_time = time.time() - start_time
            total_time += current_time
            status = "Avg. Time: %.2f s  Time Taken: %.2f s  Words: %s  line: %s" % (
                total_time / (index - count), current_time, len(sentence), int(str(i) + str(index)))
            logging.warning(status)
            print(status)


if __name__ == '__main__':
    choice = input("Enter function: ")
    if os.path.isfile(f'fun{choice}.log'):
        with open(f'fun{choice}.log', 'r') as file:
            for line in file:
                pass
            value = int(line.split(':')[-1])
    else:
        value = 0

    logging.basicConfig(filename=f'fun{choice}.log', filemode='a', format='%(message)s')
    locals()['fun' + choice](value)
