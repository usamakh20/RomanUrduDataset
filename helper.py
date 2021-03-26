import re
import time
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

base_transliteration_url = 'https://www.ijunoon.com/transliteration/'
base_translation_url = 'https://translate.ijunoon.com/'
transliteration_limit = 500
translation_limit = 1500
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


def trans(text, urdu_to_roman=True, transliterate=True, fallback=None):
    result = []
    length = transliteration_limit if transliterate else translation_limit
    for sentence in re.findall(r'(.{1,' + re.escape(str(length)) + r'})(?=\s|$)', text):
        while True:
            try:
                if transliterate:
                    transliteration_url = base_transliteration_url + 'urdu-to-roman/' \
                        if urdu_to_roman else base_transliteration_url
                    r = requests.post(transliteration_url, headers=headers, data={'text': preprocess_urdu(sentence)},
                                      timeout=300)
                else:
                    r = requests.get(base_translation_url, headers=headers, params={'text': sentence}, timeout=300)

                soup = BeautifulSoup(r.text, 'html.parser')
                result_list = soup.find('div', id='ctl00_inpageResult' + ('ing' if transliterate else '')).find_all('p')
                if not result_list and fallback:
                    return fallback()
                else:
                    result.append(result_list[-1].text.strip())
                break
            except Exception as e:
                print(e)
                time.sleep(5)
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


def translate(text, src='auto', dst='ur'):
    """
    default english to urdu translation using google API
    :param text: text to translate
    :param src: source language. defaults to auto
    :param dst: destination language defaults to urdu
    :return: translated text
    """
    while True:
        try:
            translated = translator.translate(text, dest=dst, src=src).text
            if translated != text:
                return translated
            else:
                raise Exception("Google API not working!!")
        except Exception as e:
            print(e)
            time.sleep(5)
            pass


if __name__ == '__main__':
    start_time = time.time()
    print(trans('تبدیل'))
    print("Time Taken: %.2f s" % (time.time() - start_time))
    start_time = time.time()
    print(trans('tabdeel', urdu_to_roman=False))
    print("Time Taken: %.2f s" % (time.time() - start_time))
    start_time = time.time()
    print(trans('change', transliterate=False))
    print("Time Taken: %.2f s" % (time.time() - start_time))
    start_time = time.time()
    print(translate('summer vacations supposed to be fun , right ?'))
    print("Time Taken: %.2f s" % (time.time() - start_time))
