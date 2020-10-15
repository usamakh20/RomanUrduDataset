import re
import time
import requests
from bs4 import BeautifulSoup

base_transliteration_url = 'https://www.ijunoon.com/transliteration/'
base_translation_url = 'https://translate.ijunoon.com/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Firefox/80.0'}


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'


def transliterate(text, urdu_to_roman=True):
    transliteration_url = base_transliteration_url + 'urdu-to-roman/' if urdu_to_roman else base_transliteration_url
    transliterated = []
    for sentence in re.findall(r'(.{1,500})(?=\s|$)', text):
        if not sentence.isspace():
            while True:
                try:
                    r = requests.post(transliteration_url, headers=headers, data={'text': sentence}, timeout=300)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    transliterated.append(soup.find('div', id='ctl00_inpageResulting').p.text)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    pass

    return ' '.join(transliterated)


# Todo: Generalize transliteration and translation function for large text and failed requests
def trans(text,urdu_to_roman=True,transliterate=True):
    try:
        r = requests.get(base_translation_url, headers=headers, params={'text': text}, timeout=300)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find('div', id='ctl00_inpageResult').find_all('p')[-1].text.strip()
    except Exception as e:
        print(e)


def is_english_letters(string):
    return all(ord(c) < 128 and (c.isalpha() or c.isspace()) for c in string)


if __name__ == '__main__':
    start_time = time.time()
    print(transliterate('تبدیل'))
    print("Time Taken: %.2f s" % (time.time() - start_time))
    start_time = time.time()
    print(transliterate('tabdeel', False))
    print("Time Taken: %.2f s" % (time.time() - start_time))
