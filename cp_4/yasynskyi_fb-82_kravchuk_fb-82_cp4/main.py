import random, sys, math
import random

def gcd_evkl(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd_evkl(b % a, a)
        return (g, y - (b // a) * x, x)
def gcd(a, b):
    gcd, x,y = gcd_evkl(a,b);
    return gcd

def inv(b, n):     #_ = 0 => bx mod n + 0 = g
                        #если g = 1, обратный к b
    g, x, _ = gcd_evkl(b, n)
    if g == 1:
        return x % n
    else:
        return print('there is no inverse element')

def MR(n):
    if (n == 2 or n == 3):
        return True
    if (n < 2 or n % 2 == 0):
        return False
    else:
        s=0 #Крок 0
        t=n-1
        while t%2==0:
            t//=2
            s+=1
        for k in range( 5 ):
            a= random.randint(2, n-1)
            x=pow(a, t, n)
            if (x==1 or x==n-1): continue
            else:
                for i in range (0,s-1,1):
                    x=pow(x,2,n)
                    if x==n-1: break
                else: return False
        return True

def TestMR(n):
    for i in [2, 3, 5, 7, 11]:
        if gcd(i, n) > 1:
            return False

    if MR(n)==False:
        print(f'{hex(n)} is not prime number ')
        return False
    return n


def GRN():
    number=2**(255)
    for i in range(1,255,1):
        b=random.randint(0,1)
        number+=((2**i)*b)
    number+=1
    while TestMR(number)==False:
        number=GRN()
    return number

pairs=[]
pairs.append([GRN(), GRN()])


print('P and Q for Alice:', hex(pairs[0][0]), hex(pairs[0][1]))

print(pairs)

pairs.append([GRN(), GRN()])

while pairs[0][0] * pairs[0][1] >= pairs[1][0] * pairs[1][1]:
    del pairs[1]
    pairs.append([GRN(), GRN()])

print('P and Q for Bob:', hex(pairs[1][0]), hex(pairs[1][1]))

def GenKeyPair(pairPQ):
    n = int(pairPQ[0]) * int(pairPQ[1])
    dobutok = (pairPQ[0] - 1) * (pairPQ[1] - 1)
    e = 0
    while gcd(e, dobutok) != 1:
        e = random.randint(2, dobutok)
    d = inv(e, dobutok)

    open_key = [e, n]
    secret_key = [d, pairPQ, n]

    return (open_key, secret_key)

Alice_keys = GenKeyPair(pairs[0])
Bob_keys = GenKeyPair(pairs[1])
while Bob_keys[0][1]<Alice_keys[0][1]:
    Alice_keys=GenKeyPair(pairs[0])



print('Открытый ключ Алисы:\n', hex(Alice_keys[0][0]), hex(Alice_keys[0][1]),'\n')
print('Секретный ключ Алисы:\n', hex(Alice_keys[1][0]), hex(Alice_keys[1][1][0]), hex(Alice_keys[1][1][1]),'\n')
print('Открытый ключ Боба:\n', hex(Bob_keys[0][0]), hex(Bob_keys[0][1]),'\n')
print('Секретный ключ Боба:\n', hex(Bob_keys[1][0]), hex(Bob_keys[1][1][0]), hex(Bob_keys[1][1][1]),'\n')




Encrypt = lambda message, open_key: pow(message,open_key[0],open_key[1])

Decrypt = lambda C, secret_key: pow(C,secret_key[0],secret_key[2])

Sign = lambda M, key, N: pow(M,key,N)


secret_message=random.randint(0,Alice_keys[0][1])
print(secret_message)
print(hex(secret_message))

def Verify(S,M,open_key):
    print(open_key)
    if M==pow(S,open_key[0],open_key[1]):
        return True
    else: return False


def SendKey(Alice_keys, Bob_open_key, M):
    k1 = Encrypt(M, Bob_open_key)
    print('K1 =', hex(k1), '\n')

    S = Sign(M, Alice_keys[1][0], Alice_keys[1][2])
    print('S =', hex(S), '\n')

    S1 = Encrypt(S, Bob_open_key)
    print('S1 =', hex(S1), '\n')


    Alice_message = [k1, S1]
    return Alice_message


Alice_message=SendKey(Alice_keys,Bob_keys[0],secret_message)

print(hex(Alice_message[0]))


def ReceiveKey(Alice_message, Bob_secret_key, Alice_open_key):
    k = Decrypt(Alice_message[0], Bob_secret_key)
    print('k =', hex(k), '\n')

    S = Decrypt(Alice_message[1], Bob_secret_key)
    print('S =', hex(S), '\n')

    print('authentication: S^(e)mod(n)=', hex(pow(S, Alice_open_key[0], Alice_open_key[1])), '\n')

    return Verify(S, k, Alice_open_key)


result = ReceiveKey(Alice_message, Bob_keys[1], Alice_keys[0])


if result==True:
    print('RSA completed successfully')
else:
    print('RSA failed')

pairs1=[]
pairs1.append([GRN(), GRN()])


my_keys1 = GenKeyPair(pairs1[0])
print(my_keys1)

print('my_keys:\n')
print('e:\n', hex(my_keys1[0][0]),'\n')
print('n:\n', hex(my_keys1[0][1]),'\n')
print('d:\n', my_keys1[1][0],'\n')


x=[10001,9271711763580129389248431983971813097422021827264717551194175304289383244018594547060143898364539270800694809380225628417200332732148881290303334800029901]

print(SendKey(my_keys1, x, 1234))

print('d:\n', hex(my_keys1[1][0]),'\n')
