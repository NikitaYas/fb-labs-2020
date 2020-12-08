import codecs as cs
import re
from collections import Counter
import math
from itertools import cycle


def clear_func(file):

    text = open(file,"r",encoding="utf-8")
    text = text.read().lower()
    #print(text)
    text = text.replace('ё', 'е')
    text = text.replace('\n', '')
    text = re.sub('[^а-я]', '', text)
    open('clearText', 'w').write(text)

clear_func('data.txt')
my_text = open('clearText','r').read()
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
our_alphabet=dict((alphabet[i], i) for i in range(len(alphabet)))

def encode_func(text, keytext):
    func = lambda x: alphabet[ (alphabet.index(x[0])+alphabet.index(x[1])) %32]
    return ''.join(map(func, zip(text, cycle(keytext))))

arr_of_keys = ['як','сыр','река','лента','логово','авиаприбор','стихотворец','подмигивание','свидетельство','соблазненность','богохульничанье','эксплуатирование','электроинструмент','электрометаллургия','доброкачественность','светонепроницаемость']
for i in arr_of_keys:
    open('encode/text_key_'+i,'w').write(encode_func(my_text, i))


with open('clearText', 'r') as file:
    data = file.read()


def freq_func(filename):
    with open(filename) as f:
        c = Counter()
        for line in f:
            c += Counter(line)
    freq = dict(c)
    return freq

def accordance_index(some_dict, number):
    result_index=0
    for i in some_dict:
        result_index+=some_dict[i]*(some_dict[i]-1)
    result_index=result_index/(len(number)*(len(number)-1))
    return result_index


print(accordance_index(freq_func('clearText'), data))

for i in arr_of_keys:
    print('ключ '+i+':', accordance_index(freq_func('encode/text_key_'+i), data))
