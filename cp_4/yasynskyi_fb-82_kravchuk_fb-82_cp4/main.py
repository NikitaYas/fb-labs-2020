from random import randint


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def evklid(a, b):
    if (b == 0):
        return a, 1, 0
    d, x, y = evklid(b, a % b)
    return d, y, x - (a // b) * y


def Encrypt_message(message, open_key):
    return pow(message,open_key[0],open_key[1])

def Decrypt_message(crypted, secret_key):
    return pow(crypted,secret_key[0],secret_key[3])

def Sign(message, secret_key):
    return pow(message, secret_key[0],secret_key[3])

def Verify(sign, secret_key, message):
    encr_sign = Encrypt_message(sign, secret_key)
    if encr_sign == message:
        return True
    else:
        return False

def SendKey(A_privat,B_public,message):
    crypted_text = Encrypt_message(message,B_public)
    print("Cripted Text: "+str(hex(crypted_text)))
    signature = Sign(message,A_privat)
    print("Signature: " + str(hex(signature)))
    signature_crypted = Encrypt_message(signature,B_public)
    print("Signature crypted: " + str(hex(signature_crypted)))
    return [crypted_text,signature_crypted]

def ReceiveKey(A_sended_keys,B_privat,A_public):
    message = Decrypt_message(A_sended_keys[0], B_privat)
    signature = Decrypt_message(A_sended_keys[1], B_privat)
    print(hex(message))
    print(hex(signature))
    print("Verify: ",Verify(signature,A_public,message))

def reverse(b, n):
    g, x, y = evklid(b, n)
    if g == 1:
        return x % n

def GRN(len):
    number=2**(len)
    x = ""
    for i in range(0,int(len/3)):
        x+=str(randint(0,9))
    number+=int(x)
    while MR(number)==False:
        print(str(number)+" IS NOT PRIME")
        number=GRN(len)
    return number


def MR(n,k=5):
    if n == 3 or n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    else:
        t = n - 1
        s = 0
        while t % 2 == 0:
            t = t // 2
            s += 1
        for i in range(k):
            a = randint(2, n - 2)
            x = pow(a, t, n)
            if x == 1 or x == n - 1:
                continue
            for i in range(1, s):
                x = pow(x, 2, n)
                if x == 1:
                    return False
                if x == n - 1:
                    break
            if x != n - 1:
                return False
        return True

def Eyler(p,q):
    fi = (p-1)*(q-1)
    e = GRN(5)
    while gcd(e,fi)!=1:
        e = GRN(5)
    return fi,e



def Gen_keys():
    p = 0
    q = 0
    p1 = 0
    q1 = 0
    while p*q<=p1*q1:
        p = GRN(256)
        q = GRN(256)
    mod = p*q
    fi, e = Eyler(p,q)
    d = reverse(e,fi)

    print("P = ",hex(p))
    print("Mod = ",hex(mod))
    print("Q = ",hex(q))
    print("FI = ", hex(fi))
    print("E = ", hex(e))
    print("D = ", hex(d))

    Public_Key_A = [e,mod]
    Privat_Key_A = [d,p,q,mod]
    return Public_Key_A, Privat_Key_A

X = 123456789
print("_______________________A Keys___________________________")
A_pub, A_priv = Gen_keys()
print("_______________________B Keys___________________________")
B_pub, B_priv = Gen_keys()
print("________________________________________________________")
crypted_x = Encrypt_message(X,A_pub)
decrypted = Decrypt_message(crypted_x,A_priv)

X = "1c204283de0a1b06"
A_message_with_signature = SendKey(A_priv,B_pub,X)
ReceiveKey(A_message_with_signature,B_priv,A_pub)



print("_______________________MY KEYS___________________________")
MY_pub, MY_priv = Gen_keys()
MY_MESS = SendKey(MY_priv,[10001,int("C58563C7A3E25684C7E202AB60AF34D09ABE7B1656C787F5E0EB4DEA130A3656546431DEB9E7348D43E3A79F355744840DE70E36B75B08A9B9008DDD07F95D0D",16)],X)

