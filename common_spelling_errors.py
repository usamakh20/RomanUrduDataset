import re
import random
from helper import flow, sub_space
from words_compilation import regex_chars, regex_alphabets
from collections import Counter, defaultdict

limit = 36100
filename = 'Roman urdu datasets/Roman_Urdu_Words_big.csv'


def isDistanceOne(s1, s2):
    if abs(len(s1) - len(s2)) > 1:
        return False

    elif abs(len(s1) - len(s2)) == 1:
        max_s = max(s1, s2, key=len)
        min_s = min(s1, s2, key=len)
        i = 0
        mismatch = False
        for i, _ in enumerate(min_s):
            if max_s[i] != min_s[i]:
                mismatch = True
                break
        if i == len(min_s) - 1 and not mismatch:
            return True
        for j in range(i, len(min_s)):
            if max_s[j + 1] != min_s[j]:
                return False
        return True
    else:
        matches = [s2[i] == s for i, s in enumerate(s1)]
        if sum(matches) == len(s1) - 2:
            match_index = matches.index(False)
            if match_index + 1 < len(matches) and not matches[match_index + 1] and \
                    s1[match_index] == s2[match_index + 1] and s1[match_index + 1] == s2[match_index]:
                return True
        return False


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def common_misspellings(word_counter):
    misspellings = defaultdict(list)
    print('Original words: ', len(word_counter))
    for i, word in enumerate(list(word_counter)):
        word_edits = {word: True for word in edits1(word)}
        matches = list(filter(lambda x: x in word_edits, list(misspellings)))
        if matches:
            misspellings[matches[0]].append(word)
        else:
            misspellings[word] = []
        if i % 1000 == 0:
            print('Current: ', len(misspellings))

    with open('common_misspellings', 'w') as out:
        out.write('Correct, Wrong\n')
        for correct, wrongs in misspellings.items():
            out.write(correct + ', ')
            out.write('\t'.join(wrongs) + '\n')


def clean_data(word_counter):
    correct_words = [word[0] for word in word_counter.most_common(limit)]
    mappings = [str.strip, sub_space, str.lower]
    with open('data.txt', 'r') as infile:
        with open('cleaned_data.txt', 'a') as out:
            for i, line in enumerate(infile):
                if not line.isspace():
                    preprocessed_line = flow(re.sub(regex_chars, ' ', re.sub(regex_alphabets, ' ', line)), mappings)
                    if sum(map(lambda x: x in correct_words, preprocessed_line.split(' '))) == len(
                            preprocessed_line.split(' ')):
                        out.write(preprocessed_line + '\n')
                        if i % 1000 == 0:
                            print("Written: ", i)


def common_misspellings2(word_counter):
    misspellings = defaultdict(list)
    correct_words = [word[0] for word in word_counter.most_common(limit)]
    print('Original words: ', len(correct_words))
    correct_words_dict = {word: True for word in correct_words}
    for i, word in enumerate(list(correct_words)):
        word_edits = list(filter(lambda x: x not in correct_words_dict, edits1(word)))
        random.shuffle(word_edits)
        misspellings[word] = word_edits[:random.randint(1, 10)]

    with open('common_misspellings', 'w') as out:
        out.write('Correct, Wrong\n')
        for correct, wrongs in misspellings.items():
            out.write(correct + ', ')
            out.write('\t'.join(wrongs) + '\n')


if __name__ == '__main__':
    with open(filename, 'r') as f:
        f.readline()
        words = Counter({key: int(val) for key, val in (line.split(',') for line in f)})

    op = int(input('Option: '))

    if op == 1:
        common_misspellings(words)
    elif op == 2:
        common_misspellings2(words)
    else:
        clean_data(words)
