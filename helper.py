import re
import os
import time
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

base_transliteration_url = 'https://www.ijunoon.com/transliteration/'
base_translation_url = 'https://translate.ijunoon.com/'
transliteration_limit = 500
translation_limit = 1500
timeout = 300
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Firefox/80.0'}
translator = Translator()


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'


# Deprecated!!!
# def transliterate(text, urdu_to_roman=True):
#     transliteration_url = base_transliteration_url + 'urdu-to-roman/' if urdu_to_roman else base_transliteration_url
#     transliterated = []
#     for sentence in re.findall(r'(.{1,500})(?=\s|$)', text):
#         if not sentence.isspace():
#             while True:
#                 try:
#                     r = requests.post(transliteration_url, headers=headers, data={'text': sentence}, timeout=300)
#                     soup = BeautifulSoup(r.text, 'html.parser')
#                     transliterated.append(soup.find('div', id='ctl00_inpageResulting').p.text)
#                     break
#                 except Exception as e:
#                     print(e)
#                     time.sleep(5)
#                     pass
#
#     return ' '.join(transliterated)


def trans(text, urdu_to_roman=True, transliterate=True, fallbacks=None, custom_len=None):
    result = []
    if custom_len:
        length = custom_len
    else:
        length = transliteration_limit if transliterate else translation_limit
    for sentence in re.findall(r'(.{1,' + re.escape(str(length)) + r'})(?=\s|$)', text):
        while True:
            try:
                if transliterate:
                    transliteration_url = base_transliteration_url + 'urdu-to-roman/' \
                        if urdu_to_roman else base_transliteration_url
                    r = requests.post(transliteration_url, headers=headers, data={'text': preprocess_urdu(sentence)},
                                      timeout=timeout)
                else:
                    r = requests.get(base_translation_url, headers=headers, params={'text': sentence}, timeout=timeout)

                soup = BeautifulSoup(r.text, 'html.parser')
                result_list = soup.find('div', id='ctl00_inpageResult' + ('ing' if transliterate else '')).find_all('p')
                if not result_list and fallbacks:
                    return fallbacks[0](fallbacks[1:])
                else:
                    result.append(result_list[-1].text.strip())
                break
            except Exception as e:
                print(e)
                time.sleep(5)
                if length > 1:
                    new_len = length-1
                    if int(length/2) > 0:
                        new_len = int(length/2)
                    return trans(text, urdu_to_roman, transliterate, fallbacks, new_len)
                pass

    return ' '.join(result)


def is_english_letters(string):
    return all(ord(c) < 128 and (c.isalpha() or c.isspace()) for c in string)


def preprocess_urdu(string):
    """
    Required for Ijunoon Urdu-Roman transliteration API
    :param string:
    :return: preprocessed string
    """
    return string.replace('یٰ', 'ی')


def preprocess_english(string):
    """
    Required for checking Google API not returning same text
    :param string:
    :return: preprocessed string
    """
    return re.sub('[!.]', '', string)


def translate(text, src='auto', dst='ur'):
    """
    default english to urdu translation using google API
    :param text: text to translate
    :param src: source language. defaults to auto
    :param dst: destination language defaults to urdu
    :return: translated text
    """
    result = []
    for sentence in re.findall(r'(.{1,' + re.escape(str(2000)) + r'})(?=\s|$)', text):
        while True:
            try:
                translated = translator.translate(sentence, dest=dst, src=src)
                output = translated.pronunciation if dst == 'hi' else translated.text
                if preprocess_english(output) != sentence:
                    result.append(output)
                    break
                else:
                    raise Exception("Google API not working!!")
            except Exception as e:
                print(e)
                time.sleep(5)
                pass
    return ' '.join(result)


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


if __name__ == '__main__':
    start_t = time.time()
    print(trans('تبدیل'))
    print("Time Taken: %.2f s" % (time.time() - start_t))
    start_t = time.time()
    print(trans('tabdeel', urdu_to_roman=False))
    print("Time Taken: %.2f s" % (time.time() - start_t))
    start_t = time.time()
    print(trans('change', transliterate=False))
    print("Time Taken: %.2f s" % (time.time() - start_t))
    start_t = time.time()
    print(translate('summer vacations supposed to be fun , right ?'))
    print("Time Taken: %.2f s" % (time.time() - start_t))
