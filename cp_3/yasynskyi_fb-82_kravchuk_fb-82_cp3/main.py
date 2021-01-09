from collections import Counter

rus_bigrams_freq_max = ['то', 'ст', 'но', 'на', 'ен']
alf = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


def linear_expression(a, b, m):
    if gcd(a, m) == 1:
        return [(reverse(a, m) * b) % m]
    if gcd(a, m) > 1 and b % gcd(a, m) == 0:
        a, b, n = a // gcd(a, m), b // gcd(a, m), m // gcd(a, m)
        x = linear_expression(a, b, n)
        res = []
        for i in range(x, m, n):
            res.append(i)
        return res


def evklid(a, b):
    if (b == 0):
        return a, 1, 0
    d, x, y = evklid(b, a % b)
    return d, y, x - (a // b) * y


def reverse(b, n):
    g, x, y = evklid(b, n)
    if g == 1:
        return x % n


def gcd(a, b):#Наибольший общий делитель
    while a != 0:
        a, b = b % a, a
    return b

def text_clearing(text):
    text = text.replace("ё","е").replace('ъ', 'ь').replace("\n","").lower().replace(" ","")
    return text

def float_fix(n, prec=5):
    return f"{n:.{prec}f}"




def get_ab(rus_freq_max,text_freq_max):
    #rus_freq_max[i] и rus_freq_max[j] пара из шифротекста для проверки
    #text_freq_max[i] и text_freq_max[j] пара из реального текста для проверки
    bigram_values = dict()
    for i in alf:
        for j in alf:
            a = i + j
            val = (alf.index(i) * len(alf)) + alf.index(j)
            bigram_values.update({a: val})
    len_alphabet = len(alf)
    sqrt_m = 31**2
    list_res = []
    for i in range(5):
        for j in range(5):
            x = bigram_values[rus_freq_max[i]] - bigram_values[rus_freq_max[j]]
            for k in range(5):
                y = bigram_values[text_freq_max[i]] - bigram_values[text_freq_max[k]]
                A = linear_expression(x, y, sqrt_m)
                if A != None:
                    for koren_a in A:
                        B = (bigram_values[text_freq_max[i]] - koren_a * bigram_values[rus_freq_max[i]]) % sqrt_m
                        res = []
                        res.append(koren_a)
                        res.append(B)
                        list_res.append(res)
    return list_res



def bigrams(text):
    first_let = text
    second_let = first_let[1:]
    all_bigrams = Counter(map(''.join, zip(first_let, second_let)))
    freq_dict = dict(all_bigrams)
    total = 0
    for k in freq_dict.values():
        total += k
    for k in freq_dict:
        freq_dict[k] = float(freq_dict[k] / total)
    return dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))


def decrypt(text, a,b):
    bigram_values = dict()
    for i in alf:
        for j in alf:
            x = i + j
            val = (alf.index(i) * len(alf)) + alf.index(j)
            bigram_values.update({x: val})
    result = ''
    while len(text) > 1:
        bigram = text[:2]
        text = text[2:]
        y = bigram_values[bigram]
        reversed = reverse(a, 31**2)
        if reversed != None:
            x = (reversed * (y - b)) % 31**2
            for key in bigram_values.keys():
                if bigram_values[key] == x:
                    result += key
    return result

def get_index(text):
    len_of_text = len(text)
    letters_map = {i: 0 for i in alf}
    for letter in text:
        if letter in letters_map:
            letters_map[letter] += 1
        else:
            continue
    arr = sum([letters_map[item] * (letters_map[item] - 1) for item in letters_map])
    div = len_of_text * (len_of_text - 1)
    result = arr / div
    return result

f = open("lab3_var21.txt","r", errors="ignore",encoding="utf-8")
text = f.readline()
bigrams_counted = bigrams(text)
print(bigrams_counted)
ab = get_ab(rus_bigrams_freq_max,bigrams_counted)

for a,b in ab:
    decrypted = decrypt(text,a,b)
    if len(decrypted)!=0:
        print(a,b)
        index = get_index(decrypted)
        print(index)
        if index >=0.05:
            print("Правильные ключи: ",a,b)
            g = open("result.txt","w")
            g.write(decrypted)
            g.close()
