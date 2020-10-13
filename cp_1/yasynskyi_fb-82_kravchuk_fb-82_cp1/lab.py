import numpy as np
import math
f = open("text.txt","r",encoding="utf-8")
b_symb = list()
b_bigram1 = list()
b_bigram2 = list()
b_symb_ws = list()
b_bigram1_ws = list()
b_bigram2_ws = list()
text = list()
text_ws = list()
alf = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "

def entropy(symb,n):
    dict_text = dict()
    for i in symb:
        if i not in dict_text:
            dict_text[i] = 1
        else:
            dict_text[i]+=1
    for i,k in dict_text.items():
        dict_text[i] = k/len(symb)
    probs = np.array(list(dict_text.values()))
    ent = - probs.dot(np.log2(probs))
    ent = ent
    ent *= 1/n
    return ent,dict_text

for i in f:
    i = i.replace("\n", "").lower().replace("ё","е").replace("ъ","ь")
    for k in i:
        if k in alf:
            text.append(k)


for symb in text:
    b_symb.append(symb)

for i in range(0,len(text)-1,2):
    bigram1 = text[i]+text[i+1]
    b_bigram1.append(bigram1)

for i in range(0,len(text)-1):
    bigram2 = text[i]+text[i+1]
    b_bigram2.append(bigram2)

for i in text:
    if i !=" ":
        text_ws.append(i)
for symb in text_ws:
    b_symb_ws.append(symb)

for i in range(0,len(text_ws)-1,2):
    bigram1 = text_ws[i]+text_ws[i+1]
    b_bigram1_ws.append(bigram1)

for i in range(0,len(text_ws)-1):
    bigram2 = text_ws[i]+text_ws[i+1]
    b_bigram2_ws.append(bigram2)
def print_dict(dict_values):
    pro = 0
    string =  " "
    count = 0
    for i,b in dict_values.items():

        string += i + ":"+ str("{:.2f}".format(b*100))+"%"+"   "
        if count == len(dict_values)-1:
            print(string)
        if pro==10:
            print(string)
            pro = 0
            string = " "
        pro+=1

redundency = lambda x: 1 - (x / math.log2(32))

print("symb:")
H1,dict_values = entropy(b_symb,1)
print_dict(dict_values)
print("H1:"+str(H1))
print("R:"+str(redundency(H1)))
print("bigram1:")
H2,dict_values = entropy(b_bigram1,2)
print_dict(dict_values)
print("H2:"+str(H2))
print("R:"+str(redundency(H2)))
print("bigram2:")
H2,dict_values = entropy(b_bigram2,2)
print_dict(dict_values)
print("H2:"+str(H2))
print("R:"+str(redundency(H2)))
print("symb_ws:")
H1,dict_values = entropy(b_symb_ws,1)
print_dict(dict_values)
print("H1:"+str(H1))
print("R:"+str(redundency(H1)))
print("bigram1_ws:")
H2,dict_values = entropy(b_bigram1_ws,2)
print_dict(dict_values)
print("H2:"+str(H2))
print("R:"+str(redundency(H2)))
print("bigram2_ws:")
H2,dict_values = entropy(b_bigram2_ws,2)
print_dict(dict_values)
print("H2:"+str(H2))
print("R:"+str(redundency(H2)))
