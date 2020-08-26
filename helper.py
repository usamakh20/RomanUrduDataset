import re
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.ijunoon.com/transliteration/'


def transliterate(text, urdu_to_roman=True):
    transliteration_url = url + 'urdu-to-roman/' if urdu_to_roman else url
    transliterated = []
    for sentence in re.findall(r'(.{1,500})(?=\s|$)', text):
        if not sentence.isspace():
            while True:
                try:
                    r = requests.post(transliteration_url, data={'text': sentence})
                    soup = BeautifulSoup(r.text, 'html.parser')
                    transliterated.append(soup.find('div', id='ctl00_inpageResult').p.text)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    pass

    return ' '.join(transliterated)


def is_english_letters(string):
    return all(ord(c) < 128 and (c.isalpha() or c.isspace()) for c in string)

# if __name__ == '__main__':
#     start_time = time.time()
#     print(transliterate('تبدیل'))
#     print("Time Taken: %.2f s" % (time.time() - start_time))
#     start_time = time.time()
#     print(transliterate('tabdeel', False))
#     print("Time Taken: %.2f s" % (time.time() - start_time))
