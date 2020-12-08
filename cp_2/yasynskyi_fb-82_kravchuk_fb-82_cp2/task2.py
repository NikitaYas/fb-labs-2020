import re

import numpy as np
import matplotlib.pylab as plt
f = open("var11","r",encoding="utf-8")
ciphertext = f.readline()
ciphertext = re.sub('\n','',ciphertext)
LETTERS = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
russian_map = {letter:i for i,letter in enumerate(LETTERS)}
russian_inv_map = {russian_map[i]: i  for i in LETTERS}
for_plot = {}
letters = list('абвгдежзийклмнопрстуфхцчшщъыьэюя' + 'абвгдежзийклмнопрстуфхцчшщъыьэюя'.upper())
alph_len = len(letters)
letters_map = {letters[key] : key for key in range(alph_len)}
numbers_map = {key : letters[key] for key in range(alph_len)}

def letters_to_numbers(letters):
    return list(map(lambda x: letters_map[x] if x in letters_map else x,list(letters)))

def numbers_to_letters(numbers):
    return list(map(lambda x: numbers_map[x] if type(x) is int else x,numbers))


def vignere_crypt(plain,key,mode):
    encrypted = []
    plain = letters_to_numbers(plain)
    key = letters_to_numbers(key)
    for i in range(len(plain)):
        try:
            if plain[i] > 32:
                if mode == "decrypt":
                    encrypted.append(((plain[i] - key[i % (len(key))]) % (alph_len // 2)) + (alph_len//2) )
                else:
                    encrypted.append(((plain[i] + key[i % (len(key))]) % (alph_len // 2)) + (alph_len // 2))
            else:
                if mode == "decrypt":
                    encrypted.append((plain[i] - key[i % (len(key))]) % (alph_len // 2))
                else:
                    encrypted.append((plain[i] + key[i % (len(key))]) % (alph_len // 2))


        except TypeError:
            encrypted.append(plain[i])
    return ''.join(numbers_to_letters(encrypted))


def split_by_keylen(ciphertext,keylen):
    arr_of_parts = []
    for i in range(0,keylen):
        part_str = ''
        for j in range(i,len(ciphertext),keylen):
            part_str += ciphertext[j]
        arr_of_parts.append(part_str)
    return arr_of_parts


def icx(splited_strings):
    arr_of_icx = []
    for splited_string in splited_strings:
        len_of_splited_string = len(splited_string)
        letters_map = {i:0 for i in LETTERS}
        for letter in splited_string:
            letters_map[letter] += 1
        arr = sum([letters_map[item] * (letters_map[item] - 1) for item in letters_map])
        div = len_of_splited_string * (len_of_splited_string - 1)
        arr_of_icx.append(arr / div)
    return arr_of_icx

def not_white_noise(arr_of_icx):
    for icx in arr_of_icx:
        if not 0.049 <= icx <= 0.072:
            return False
    return True

def find_key_len(ciphertex):
    probable_keys = []
    for key_len in range(2,32):
        for_plot[key_len] = icx(split_by_keylen(ciphertext,key_len))
        if not_white_noise(icx(split_by_keylen(ciphertext,key_len))):
            #print("{}: {}".format(key_len,icx(split_by_keylen(ciphertext,key_len))))
            probable_keys.append(key_len)
    return probable_keys





def shift_substring(substring,key):
    return "".join([russian_inv_map[(russian_map[letter] + key) % len(LETTERS)] for letter in substring])

def mutal_icx(substr1,substr2):
    lenght_of_substr1 = len(substr1)
    lenght_of_substr2 = len(substr2)
    letter_map1 = {i:0 for i in LETTERS}
    letter_map2 = {i:0 for i in LETTERS}
    for letter in substr1:
        letter_map1[letter] += 1
    for letter in substr2:
        letter_map2[letter] += 1
    for letter in letter_map1:
        letter_map1[letter] += letter_map1[letter] / lenght_of_substr1
    for letter in letter_map2:
        letter_map2[letter] += letter_map2[letter] / lenght_of_substr2

    sum_of_freq = sum([letter_map1[letter] * letter_map2[letter] for letter in letter_map1])

    #letter_freq_str1 = sum([letter_map1[letter] for letter in letter_map1])
    #letter_freq_str2 = sum([letter_map2[letter] for letter in letter_map2])
    #letter_freq_product = letter_freq_str1 * letter_freq_str2
    sub1sub2_len = lenght_of_substr1 * lenght_of_substr2
    result = sum_of_freq / sub1sub2_len
    return result


def show_possible_keys(arr):
    possible_keys = []
    for i in range(0,len(LETTERS)):
        possible_key = LETTERS[i]
        for number in arr:
            possible_key += russian_inv_map[(i - number) % len(LETTERS)]
        possible_keys.append(possible_key)
    return possible_keys


def pretty_keys_display(keylen,arr_of_keys):
    print("keys of len {}".format(keylen))
    for i,key in enumerate(arr_of_keys):
        print(i,key,end='\n' if i % 10 == 0 else '\t')
    print('\n')



def hack_vigenere(ciphertext):
    for keylen in find_key_len(ciphertext):
        splited_by_keylen = split_by_keylen(ciphertext,keylen)
        first_substr = splited_by_keylen[0]
        strnum_shift = []
        for substr_num in range(1,keylen):
            for shift_num in range(1,34):
                mutal_coinc = mutal_icx(first_substr,shift_substring(splited_by_keylen[substr_num],shift_num))
                if 0.050 <= mutal_coinc <= 0.070:
                    #print("str number {} shift {} icx {} : ".format(substr_num + 1,shift_num,mutal_icx(first_substr,shift_substring(splited_by_keylen[substr_num],shift_num))))
                    strnum_shift.append(shift_num)
        arr_of_keys = show_possible_keys(strnum_shift)
        pretty_keys_display(keylen,arr_of_keys)

        icx_values = list(for_plot.values())
        icx_values = list(map(lambda x: sum(x) / len(x),icx_values))
        print(icx_values)
        keys_len = list(for_plot.keys())
        plt.plot(keys_len,icx_values)
        plt.xlabel('key length')
        plt.ylabel('index of coincidence')
        plt.show()
        plt.savefig('plot.png',dpi=100)

        print("если сдесь есть подходящий ключ,введите y,если же нет - введите n")
        answer = str(input('введите ответ: '))
        if answer == 'y' or answer == 'Y':
            key = int(input('введите номер ключа: '))
            print("расшифровываем шифротекст с помощью ключа '{}'".format(arr_of_keys[key]))
            plaintext = vignere_crypt(ciphertext,arr_of_keys[key],'decrypt')
            print(plaintext)
            decrypt_answer = str(input("расшифровано правильно? [ynYN]: "))
            if decrypt_answer == 'y' or decrypt_answer == 'Y':
                return plaintext
            else:
                continue
    return None


if __name__ == "__main__":
    print(hack_vigenere(ciphertext))