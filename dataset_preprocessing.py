import logging
import numpy as np
import pandas as pd
from datetime import datetime
from helper import *

urdu_data_dir = 'Urdu datasets/'
eng_data_dir = 'English datasets/'
roman_urdu_data_dir = 'Roman urdu datasets/'
logs_dir = 'logs/'
glue_dir = '../glue-urdu/'


def fun1():
    data = []
    data_series = pd.read_csv(urdu_data_dir + 'Roman Urdu DataSet.csv', header=None).iloc[:, 0]
    preprocessed_data_series = data_series.apply(
        lambda s: sub_space(
            sub_characters(
                sub_quotes(
                    sub_initial(s)))))

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


def fun7(count):
    mappings = [sub_initial_urdu, str.strip, sub_quotes, sub_space]
    with open(glue_dir + 'XQuAD/Urdu/XQuAD_ur.csv') as file:
        with open(glue_dir + 'XQuAD/Roman Urdu/XQuAD_ru.csv', 'a') as out:
            for index, sentence in enumerate(file):
                if index > count or count == 0:
                    process(out, flow(sentence, mappings), i=index, transliterate=True)


def fun8(count):
    prev_lines = 0
    mappings = [sub_initial_urdu, str.strip, sub_quotes, sub_space]
    file_cats = ['train', 'test', 'dev']
    file_name_template = glue_dir + 'NLI/Urdu/NLI.ur.{}.tsv'
    for i in range(len(file_cats)):
        prev_lines += file_len(file_name_template.format(file_cats[i - 1] if i > 0 else 0))
        with open(file_name_template.format(file_cats[i])) as file:
            with open(glue_dir + 'NLI/Roman Urdu/NLI.ru.{}.tsv'.format(file_cats[i]), 'a') as out:
                for index, sentence in enumerate(file, start=prev_lines):
                    if index > count or count == 0:
                        process(out, flow(sentence, mappings), i=index, transliterate=True,
                                before=lambda s: ' | '.join(s.split('\t')[:-1]),
                                after=lambda s: s.replace('|', '\t') + '\t' + sentence.split('\t')[-1][:-1])


def fun9(count):
    prev_lines = 0
    mappings = [sub_initial_urdu, preprocess_urdu, str.strip, sub_quotes, sub_space]
    file_cats = ['train', 'test', 'dev']
    file_name_template = glue_dir + 'POS/Urdu/pos.ur.{}.conllu'
    for i in range(len(file_cats)):
        prev_lines += file_len(file_name_template.format(file_cats[i - 1] if i > 0 else 0))
        with open(file_name_template.format(file_cats[i])) as file:
            with open(glue_dir + 'POS/Roman Urdu/pos.ru.{}.conllu'.format(file_cats[i]), 'a') as out:
                for index, sentence in enumerate(file, start=prev_lines):
                    if index > count or count == 0:
                        if 'sent_id' in sentence:
                            out.write(('' if index == prev_lines else '\n') + sentence)
                        elif '\n' != sentence:
                            if 'text' in sentence:
                                process(out, flow(sentence, mappings), i=index, transliterate=True)
                            else:
                                temp = sentence.split('\t')
                                process(out, flow(sentence, mappings), i=index, transliterate=True,
                                        before=lambda s: ' | '.join(s.split('\t')[1:3]).strip(),
                                        after=lambda s: temp[0] + '\t' + s.replace(' | ', '\t') + '\t' + '\t'.join(
                                            temp[3:]).strip())


def fun10(count):
    prev_lines = 0
    mappings = [sub_initial_urdu, sub_quotes, preprocess_urdu, sub_space, str.strip]
    file_cats = ['train', 'test']
    file_name_template = glue_dir + 'NER/Urdu/NER.ur.{}'
    for i in range(len(file_cats)):
        prev_lines += file_len(file_name_template.format(file_cats[i - 1] if i > 0 else 0))
        with open(file_name_template.format(file_cats[i])) as file:
            with open(glue_dir + 'NER/Roman Urdu/NER.ru.{}'.format(file_cats[i]), 'a') as out:
                for index, sentence in enumerate(file, start=prev_lines):
                    if index > count or count == 0:
                        if sentence != '\n':
                            process(out, flow(sentence.split('\t')[0], mappings), i=index, transliterate=True,
                                    after=lambda s: s + '\t' + sentence.strip().split('\t')[-1])
                        else:
                            out.write('\n')


def fun11(count):
    prev_lines = 0
    mappings = [sub_initial, sub_quotes, sub_space, str.strip]
    file_cats = ['train', 'test']
    file_name_template = glue_dir + 'SentiMix/{}/SentiMix.{{}}.{}.csv'
    for i in range(len(file_cats)):
        urdu_file = file_name_template.format('Roman Urdu', 'ru')
        prev_lines += file_len(urdu_file.format(file_cats[i - 1] if i > 0 else 0))
        with open(urdu_file.format(file_cats[i])) as file:
            with open(file_name_template.format('Urdu', 'ur').format(file_cats[i]), 'a') as out:
                out.write('uid,sentence,sentiment\n')
                for index, sentence in enumerate(file, start=prev_lines):
                    if (index > count or count == 0) and index > prev_lines:
                        process(out, flow(sentence.split(',')[1], mappings), i=index, transliterate=True,
                                urdu_to_roman=False,
                                after=lambda s: sentence.split(',')[0] + ',' + s + ',' + sentence.split(',')[2].strip())


def fun12(count):
    mappings = [sub_initial_urdu, sub_quotes, sub_space, str.strip]
    with open(urdu_data_dir + 'dr_omer/dataaa.txt', 'r') as file:
        with open(roman_urdu_data_dir + 'data_roman.txt', 'a') as out:
            for index, sentence in enumerate(file):
                if index > count or count == 0:
                    process(out, flow(sentence, mappings), i=index, transliterate=True,
                            after=lambda s: str.strip(sub_space(sub_initial(s))))


def fun13(count):
    mappings = [sub_initial_urdu, sub_quotes, sub_space, str.strip]
    with open(urdu_data_dir + 'dr_omer/transcription.txt', 'r') as file:
        with open(roman_urdu_data_dir + 'transcription_roman.txt', 'a') as out:
            for index, sentence in enumerate(file):
                if index > count or count == 0:
                    process(out, flow(sentence, mappings), i=index, transliterate=True,
                            before=lambda s: s.split(maxsplit=1)[1].strip(),
                            after=lambda s: sentence.split(maxsplit=1)[0] + ' ' + str.strip(sub_space(sub_initial(s))))


def fun14(count):
    mappings = [sub_initial_urdu, sub_quotes, sub_space, str.strip]
    sentences = pd.read_csv(urdu_data_dir + 'dr_omer/Combined.csv', header=None, sep=',')\
        .replace(np.nan, '', regex=True).to_numpy()
    with open(roman_urdu_data_dir + 'Combined_roman.csv', 'a') as out:
        for index, sentence in enumerate(sentences):
            if index > count or count == 0:
                process(out, flow(sentence[1], mappings), i=index, transliterate=True,
                        after=lambda s: sentence[0] + ',' + str.strip(sub_space(sub_initial(s))))


def process_sentences(out_file, count, numbered_sentences, start=False, i=0, transliterate=False):
    for index, sentence in numbered_sentences:
        if start or index > count:
            process(out_file, sentence, index if i == 0 else i, transliterate)


def process(out_file, sentence, i=0, transliterate=False, urdu_to_roman=True, before=lambda x: x, after=lambda x: x):
    start_time = time.time()
    if transliterate:
        out_file.write(after(
            trans(before(sentence), urdu_to_roman=urdu_to_roman,
                  fallbacks=[lambda x: translate(before(sentence), src='ur', dst='hi')])) + '\n')
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
            for l in log_file:
                pass
            value = int(l.split(':')[-1])
    else:
        value = 0

    logging.basicConfig(filename=logs_dir + f'fun{choice}.log', filemode='a', format='%(message)s')
    locals()['fun' + choice](value)

# Todo: uppc corpus, multisenti-master,  urmono
#  1. Use rule base roman urdu transliterator for left over urdu words in roman urdu text
