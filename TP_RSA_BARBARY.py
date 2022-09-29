"""
Auto generate from Barbary's computer
"""

import math
from base64 import b64decode
from Crypto.PublicKey import RSA


def extended_gcd(a, b):
    r_prime, r = a, b
    u, s = 1, 0
    v, t = 0, 1

    while r != 0:
        q = r_prime // r
        r_prime, r = r, r_prime - q * r
        u, s = s, u - q * s
        v, t = t, v - q * t

    return u, v


def getYi(list):
    res = []

    res.append(math.prod(list) // list[0])
    res.append(math.prod(list) // list[1])
    res.append(math.prod(list) // list[2])

    return res


def dichotomie(inf, sup, to_find):
    found = False

    while not found:

        m = (inf + sup) // 2

        if abs(to_find - m ** 3) < 1:
            return m
        elif to_find < m ** 3:
            sup = m
        elif to_find > m ** 3:
            inf = m


def prog():
    c1 = None
    c2 = None
    c3 = None

    # question 2

    """
     α ≡ c1 mod N1
     α ≡ c2 mod N2
     α ≡ c3 mod N3
     """

    with open("clef1_pub.pem", "r") as key:
        c1 = RSA.import_key(key.read())
    with open("clef2_pub.pem", "r") as key:
        c2 = RSA.import_key(key.read())
    with open("clef3_pub.pem", "r") as key:
        c3 = RSA.import_key(key.read())

    list = [c1.n, c2.n, c3.n]

    # question 3

    listYi = getYi(list)

    u1 = extended_gcd(listYi[0], list[0])[0]
    u2 = extended_gcd(listYi[1], list[1])[0]
    u3 = extended_gcd(listYi[2], list[2])[0]

    # question 4

    with open("c1", "r") as c1file:
        c1mes = c1file.read()
    with open("c2", "r") as c2file:
        c2mes = c2file.read()
    with open("c3", "r") as c3file:
        c3mes = c3file.read()

    result = int.from_bytes(b64decode(c1mes), "big") * u1 * listYi[0] + \
             int.from_bytes(b64decode(c2mes), "big") * u2 * listYi[1] + \
             int.from_bytes(b64decode(c3mes), "big") * u3 * listYi[2]
    resultAndModulo = result % math.prod(list)

    m = dichotomie(0, min(list), resultAndModulo)
    print(bytes.fromhex(hex(m)[2:]).decode('utf-8'))


if __name__ == "__main__":
    prog()
