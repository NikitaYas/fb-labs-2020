import math
from itertools import cycle
from collections import Counter
arr_of_keys = ['як','сыр','река','лента','логово','авиаприбор','стихотворец','подмигивание','благочестивый','соблазненность','богохульничанье','эксплуатирование','электроинструмент','электрометаллургия','доброкачественность','светонепроницаемость']
alf = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
alf_value = dict()
for i in range(0,len(alf)):
    alf_value[alf[i]] = i


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def calculate_index(text):
    len_text = len(text)
    frq_dict = dict()
    for i in text:
        if i not in frq_dict:
            frq_dict[i] = 1
        else:
            frq_dict[i]+=1
    index = 0
    for val in frq_dict.values():
        index += (val *(val - 1))
    return index / (len_text * (len_text - 1))

def encode_func(text, keytext):
    encoded = ""
    while len(text)>0:
        fragment = text[:len(keytext)]
        for i in range(0,len(fragment)):
            encoded+=get_key(alf_value,(alf_value[fragment[i]]+alf_value[keytext[i]])%len(alf))
        text = text[len(keytext):]
    return encoded


some_text = ""
f = open("some_text.txt","r",encoding="utf-8")
for i in f:
    k=i.replace("\n","").replace(" ","").replace("ё","е").replace(".","е").lower()
    for p in k:
        if p in alf:
            some_text+=p
f.close()

for key in arr_of_keys:
    print(key," : ",calculate_index(encode_func(some_text,key)))
print("Не шифрованый текст",calculate_index(some_text))



def decrypter(text, key):
    fragm = cycle(key)
    decrypted = ''
    for msg, key in zip(text, fragm):
        decrypted += get_key(alf_value,(( alf_value[msg] - alf_value[key])% 32))
    return decrypted


def average(a):
    s = 0
    for i in range(len(a)):
        s += a[i]
    return s/len(a)

def get_len_of_key(text):
    teory_index = 0.05843316543575007
    len_of_key = 0
    index_of_best_key = 0
    for len_of_key_predict in range(2,30):
        list_index = list()
        for k in range(0,len_of_key_predict):
            symbs = ""
            for i in range(0,len(text),len_of_key_predict):
                symbs+=text[i]
            list_index.append(calculate_index(symbs))
        avarage_index = average(list_index)
        if math.fabs(teory_index-list_index[0])<math.fabs(teory_index-index_of_best_key):
            index_of_best_key = avarage_index
            len_of_key = len_of_key_predict
        print(len_of_key_predict,avarage_index)
    return len_of_key,index_of_best_key


def devine_bloks(text,len_key):
    list_of_bloks = list()
    for i in range(0,len_key):
        block = ""
        for k in range(0,len(text)):
            block+=text[k]
        list_of_bloks.append(block)
    return  list_of_bloks


text_var21 = ""
f = open("var11.txt","r",encoding="utf-8")
for i in f:
    k=i.replace("\n","").replace(" ","").replace("ё","е").replace(".","").lower()
    for p in k:
        if p in alf:
            text_var21+=p
f.close()

len_key = get_len_of_key(text_var21)[0]
print(len_key)



def crack(text, len_of_key):
    key = ""
    for k in range(0,len_of_key):
        temp_list = list()
        for i in range(k, len(text), len_of_key):
            temp_list.append(text[i])
        clount_letters = Counter(temp_list)
        maybe_O = (Counter(clount_letters).most_common(1)[0][0])

        y_with_star = int(alf_value[maybe_O])
        k_key = (y_with_star - 14) % 32
        key+=get_key(alf_value,k_key)
    return print("Ключ:",key)


key = []
crack(text_var21, len_key)
print(decrypter(text_var21,"венецианскийкупец"))