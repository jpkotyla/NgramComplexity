import pandas as pd
import numpy as np
import itertools
import enchant

def readText(textPath = 'sample_text.txt'):
    with open(textPath, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    return data

def get_transition(gram,text = a,order = 1):
    res = pd.DataFrame({'duplicate': [text[i] for i in range(order, len(text)) if text[i - order:i] == ''.join(gram)]})
    res[gram] = res['duplicate']
    return res.groupby('duplicate').count()[gram]

def get_next(letter,order,transitons):
    r = np.random.uniform(0,1,1)[0]
    trans  = transitons[order]
    t = trans[letter].cumsum()
    return t[t>r].index[0]


def make_text(starters,transitons,n = 100,order = 1):

    r = np.random.uniform(0,1,1)[0]

    starter = starters[order]
    ss = starter.cumsum()
    last_letter = ss[ss>r].index[0]
    if order == 2:
        last_letter = (last_letter[0],last_letter[1])
    output = [''.join(last_letter)]

    while(len(output)<n):
        letter = get_next(last_letter,order,transitons)
        if order == 2:
            last_letter = (last_letter[1],letter)
        else:
            last_letter = letter
        output.append(letter)
    return ''.join(output)

def replace_chars(word):
    return word.replace('.', '').replace(',', '')

def good_word(word):
    if len(replace_chars(word)) > 0:
        if d.check(replace_chars(word)):
            return word
        else:
            return np.NaN
    else:
        return np.NaN

def check_valid_words(text,language = 'en_US'):
    d = enchant.Dict(language)
    words = text.split(' ')
    counts = sum([d.check(replace_chars(word)) for word in words if len(replace_chars(word))>0])
    all_words = map(good_word, words)
    all_words = pd.DataFrame(all_words)
    all_words['gb'] = all_words[0]
    return all_words


def get_transitions(text):
    all_chars = list(set(text))
    all_trans = {char: get_transition(char) for char in all_chars}
    all_trans = {key: val/val.sum() for key,val in all_trans.iteritems()}

    start_count = pd.Series({chr(x):a.count(chr(x)) for x in range(65,91)})
    start_freq = start_count/start_count.sum()

    start_count2 = pd.Series({''.join(gram): a.count(''.join(gram)) for gram in itertools.product([chr(x) for x in range(65,91)],all_chars)})
    start_freq2 = start_count2/start_count2.sum()


    all_bigrams = [bigram for bigram in itertools.product(all_chars,all_chars)]
    all_trans2 = {gram: get_transition(gram,order = 2) for gram in all_bigrams}
    all_trans2 = {key: val/val.sum() for key,val in all_trans2.iteritems()}

    starters = {1:start_freq,2:start_freq2}
    transitons = {1:all_trans,2:all_trans2}

    return starters,transitons

if __name__ == 'main':
    text = readText()
    starters,transitons = get_transitions(text)
    test = make_text(starters,transitons,n = 10000,order = 2)
    df = check_valid_words(test)