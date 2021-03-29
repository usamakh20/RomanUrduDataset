import re
import os
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from helper import trans, Colors, translate

urdu_data_dir = 'Urdu datasets/'
eng_data_dir = 'English datasets/'
roman_urdu_data_dir = 'Roman urdu datasets/'
logs_dir = 'logs/'
glue_dir = '../glue-urdu/'


def file_len(path):
    if os.path.isfile(path):
        with open(path) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    else:
        return 0


def flow(seed, funcs):
    for func in funcs:
        seed = func(seed)
    return seed


def sub_initial_urdu(string):
    return re.sub(r"[/\\<>]", ' ', string)


def sub_initial(string):
    return re.sub(r"[^a-zA-Z0-9' ]", ' ', str(string).lower())


def sub_quotes(string):
    return re.sub(r"'\B|\B'|\"", ' ', string)


def sub_characters(string):
    return re.sub(r"(?<=\s)[dp](?=\s|$)", ' ', string)


def sub_space(string):
    return re.sub(r' {2,}', ' ', string)


def sub_nextline(string):
    return re.sub(r'\n', ' ', string)


def sub_quote(string):
    return re.sub(r'\'', ' ', string)


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

    with open(roman_urdu_data_dir + 'counter_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(text).split('۔')))


def fun3(count):
    data_series = pd.read_csv(urdu_data_dir + 'imdb_urdu_reviews.csv').iloc[:, 0]
    with open(roman_urdu_data_dir + 'imdb_reviews_roman_urdu.txt', 'a') as out:
        for i, data in enumerate(data_series):
            process_sentences(out, count, enumerate(sub_space(sub_initial_urdu(data)).split('۔')), i > count, i)


def fun4(count):
    with open(urdu_data_dir + 'uner.txt', encoding="utf16") as file:
        text = file.read()

    with open(roman_urdu_data_dir + 'uner_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(re.sub(r"</?[A-Z]+>", ' ', text)).split('۔')))


def fun5(count):
    text = ''
    for f_name in os.listdir(urdu_data_dir + 'news/Fake'):
        with open(urdu_data_dir + 'news/Fake/' + f_name) as file:
            text += ' ' + file.read()

    for f_name in os.listdir(urdu_data_dir + 'news/Real'):
        with open(urdu_data_dir + 'news/Real/' + f_name) as file:
            text += ' ' + file.read()

    with open(roman_urdu_data_dir + 'news_roman_urdu.txt', 'a') as out:
        process_sentences(out, count, enumerate(sub_nextline(text).split('۔')))


def fun6(count):
    """
    changed to google API after line 3563015
    all functions after this use google API for English to Urdu
    :param count:
    :return:
    """
    file_name_template = eng_data_dir + 'books_large_p{}.txt'
    mappings = [str.strip, sub_quote, sub_initial_urdu, sub_space]

    for i in range(1, 3):
        prev_lines = file_len(file_name_template.format(str(i - 1)))
        with open(file_name_template.format(str(i)), 'r') as file:
            with open(roman_urdu_data_dir + 'book_corpus_roman_urdu.txt', 'a') as out:
                for index, sentence in enumerate(file, start=prev_lines):
                    if index > count or count == 0:
                        process(out, flow(sentence, mappings), i=index)


# def fun7(count):
#     mappings = [sub_initial_urdu, str.strip, sub_quotes, sub_space]
#     with open(glue_dir + 'XQuAD/Urdu/XQuAD_ur.csv') as file:
#         with open(glue_dir + 'XQuAD/Roman Urdu/XQuAD_ru.csv', 'a') as out:
#             for index, sentence in enumerate(file):
#                 if index > count or count == 0:
#                     process(out, flow(sentence, mappings), i=index, transliterate=True)


def fun8(count):
    mappings = [sub_initial_urdu, str.strip, sub_quotes, sub_space]
    for split in ['train', 'test', 'dev']:
        with open(glue_dir + 'NLI/Urdu/NLI.ur.{}.tsv'.format(split)) as file:
            with open(glue_dir + 'NLI/Roman Urdu/NLI.ru.{}.tsv'.format(split), 'a') as out:
                for index, sentence in enumerate(file):
                    if index > count or count == 0:
                        process(out, flow(sentence, mappings), i=index, transliterate=True,
                                before=lambda s: ' | '.join(s.split('\t')[:-1]),
                                after=lambda s: s.replace('|', '\t') + '\t' + sentence.split('\t')[-1][:-1])


def process_sentences(out_file, count, numbered_sentences, start=False, i=0, transliterate=False):
    for index, sentence in numbered_sentences:
        if start or index > count:
            process(out_file, sentence, index if i == 0 else i, transliterate)


def process(out_file, sentence, i=0, transliterate=False, before=lambda x: x, after=lambda x: x):
    start_time = time.time()
    if transliterate:
        out_file.write(after(
            trans(before(sentence), fallbacks=[lambda x: translate(before(sentence), src='ur', dst='hi')])) + '\n')
    else:
        out_file.write(after(trans(translate(before(sentence)),
                                   fallbacks=[
                                       lambda x: trans(trans(before(sentence), transliterate=transliterate),
                                                       fallbacks=x),
                                       lambda x: translate(translate(before(sentence)), src='ur', dst='hi')])) + '\n')
    current_time = time.time() - start_time
    words_per_second = len(sentence) / current_time
    output_color(words_per_second)
    status = "Timestamp: %s  Avg. characters per second: %.2f  Time Taken: %.2f s  characters: %s  line: %s" % (
        datetime.now().strftime("%-d %b %Y , %-I:%M:%S %p"),
        words_per_second, current_time, len(sentence), i)
    logging.warning(status)
    print(status)


if __name__ == '__main__':

    choice = input("Enter function: ")
    if os.path.isfile(logs_dir + f'fun{choice}.log'):
        with open(logs_dir + f'fun{choice}.log', 'r') as log_file:
            for line in log_file:
                pass
            value = int(line.split(':')[-1])
    else:
        value = 0

    logging.basicConfig(filename=logs_dir + f'fun{choice}.log', filemode='a', format='%(message)s')
    locals()['fun' + choice](value)

# Todo: uppc corpus, multisenti-master,  urmono
