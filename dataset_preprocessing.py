import re
import os
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from helper import transliterate, translate, Colors

urdu_data_dir = 'Urdu datasets/'
eng_data_dir = 'English datasets/'


def sub_initial_urdu(string):
    return re.sub(r"[/\\<>]", ' ', string)


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


def output_color(words_per_second):
    if words_per_second == 0:
        print(Colors.NORMAL, end='')
    elif words_per_second < 20:
        print(Colors.RED, end='')
    elif words_per_second < 50:
        print(Colors.YELLOW, end='')
    else:
        print(Colors.GREEN, end='')


def fun1():
    data = []
    data_series = pd.read_csv(urdu_data_dir + 'Roman Urdu DataSet.csv', header=None).iloc[:, 0]
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
    with open(urdu_data_dir + 'counter.txt') as file:
        text = file.read()

    with open('counter_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(text).split('۔')))


def fun3(count):
    data_series = pd.read_csv(urdu_data_dir + 'imdb_urdu_reviews.csv').iloc[:, 0]
    with open('imdb_urdu_reviews_roman_urdu.txt', 'a') as out:
        for i, data in enumerate(data_series):
            process_sentences(out, count, enumerate(sub_space(sub_initial_urdu(data)).split('۔')), i > count, i)


def fun4(count):
    with open(urdu_data_dir + 'uner.txt', encoding="utf16") as file:
        text = file.read()

    with open('uner_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(re.sub(r"</?[A-Z]+>", ' ', text)).split('۔')))


def fun5(count):
    text = ''
    for f_name in os.listdir(urdu_data_dir + 'news/Fake'):
        with open(urdu_data_dir + 'news/Fake/' + f_name) as file:
            text += ' ' + file.read()

    for f_name in os.listdir(urdu_data_dir + 'news/Real'):
        with open(urdu_data_dir + 'news/Real/' + f_name) as file:
            text += ' ' + file.read()

    with open('news_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(text).split('۔')))


def fun6(count):
    for i in range(1, 3):
        with open(eng_data_dir + 'books_large_p' + str(i) + '.txt', 'r') as file:
            with open('book_corpus_roman_urdu.txt', 'a') as out:
                for index, sentence in enumerate(file):
                    if index > count or count == 0:
                        process(out, sentence.strip(), i=index, transl=True)


def process_sentences(out_file, count, numbered_sentences, start=False, i=0, transl=False):
    total_time = 0
    for index, sentence in numbered_sentences:
        if start or index > count:
            process(out_file, sentence, total_time, index if i == 0 else i, transl)


def process(out_file, sentence, total_time=0, i=0, transl=False):
    start_time = time.time()
    if transl:
        out_file.write(transliterate(translate(sentence)) + '\n')
    else:
        out_file.write(transliterate(sentence) + '\n')
    current_time = time.time() - start_time
    total_time += current_time
    words_per_second = (len(sentence) / current_time if current_time else 0)
    output_color(words_per_second)
    status = "Timestamp: %s  Avg. characters per second: %.2f  Time Taken: %.2f s  characters: %s  line: %s" % (
        datetime.now().strftime("%-d %b %Y , %-I:%M:%S %p"),
        words_per_second, current_time, len(sentence), i)
    logging.warning(status)
    print(status)


if __name__ == '__main__':

    choice = input("Enter function: ")
    if os.path.isfile(f'fun{choice}.log'):
        with open(f'fun{choice}.log', 'r') as log_file:
            for line in log_file:
                pass
            value = int(line.split(':')[-1])
    else:
        value = 0

    logging.basicConfig(filename=f'fun{choice}.log', filemode='a', format='%(message)s')
    locals()['fun' + choice](value)

# Todo: uppc corpus, multisenti-master,  urmono
