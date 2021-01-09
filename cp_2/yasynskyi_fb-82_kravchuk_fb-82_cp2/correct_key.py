from collections import Counter
text = ""
alf = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
alf_value = dict()
for i in range(0,len(alf)):
    alf_value[alf[i]] = i

f = open("var11.txt","r",encoding="utf-8")
for i in f:
    k=i.replace("\n","").replace(" ","").replace("ё","е").replace(".","е").lower()
    for p in k:
        if p in alf:
            text+=p
f.close()

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def frq(text):
    let = text
    all_bigrams = Counter(let)
    freq_dict = dict(all_bigrams)

    count_letters = 0
    for key,val in freq_dict.items():
        count_letters+=val
    for key,val in freq_dict.items():
        freq_dict[key]=val/count_letters
frq(text)


def crack_wrong(text, len_of_key):
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

def crack(text, len_of_key):
    key = ""
    right_key = "венецианскийкупец"
    count_key = 0
    for k in range(0,len_of_key):
        temp_list = list()
        for i in range(k, len(text), len_of_key):
            temp_list.append(text[i])
        clount_letters = Counter(temp_list)
        maybe_O = (Counter(clount_letters).most_common(1)[0][0])

        right = 0
        i = 0
        while right==0:
            y_with_star = int(alf_value[maybe_O])
            k_key = (y_with_star - i) % 32
            if get_key(alf_value,k_key)==right_key[count_key]:
                right=1
            i += 1
        count_key+=1
        key+=get_key(alf_value,k_key)
        print("----------------------------------")
        print(count_key, "буква ключа")
        print(maybe_O+" шифруется в: "+get_key(alf_value,k_key))
        print("Самая часто встречаемая буква: "+ get_key(alf_value,i-1))
    return print("Ключ:",key)
print("Неправильный ключ (учитывая что самая часто встречаемая буква 'O')")
crack_wrong(text,17)
crack(text,17)