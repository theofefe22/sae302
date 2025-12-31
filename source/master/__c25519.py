import random

# CONSTANTES
A = 486662
B = 1
a24 = 121666
p = (pow(2, 255)-19)
x1 = 9
#r = random.randint(1, p-1)


def change(P, Q, b):
    if b == 1:
        return Q, P
    else:
        return P, Q


def echelle(P2, P3, x1):
    x2, z2 = P2
    x3, z3 = P3
    T1 = pow((x2 + z2), 1, p)
    T2 = pow((x2 - z2), 1, p)
    T3 = pow((x3 + z3), 1, p)
    T4 = pow((x3 - z3), 1, p)
    T5 = pow(T1, 2)
    T6 = pow(T2, 2)
    T2 = pow((T2 * T3), 1, p)
    T1 = pow((T1 * T4), 1, p)
    T1 = pow((T1 + T2), 1, p)
    T2 = pow((T1 - T2), 1, p)
    x3 = pow(T1, 2, p)
    T2 = pow(T2, 2, p)
    z3 = pow((T2 + x1), 1, p)
    x2 = pow((T5 * T6), 1, p)
    T5 = pow((T5 - T6), 1, p)
    T1 = pow((a24 * T5), 1, p)
    T6 = pow((T6 + T1), 1, p)
    z2 = pow((T5 * T6), 1, p)
    
    return [x2, z2, x3, z3]


def montgomery(xp, r):
    x1 = xp
    x2 = 1
    z2 = 0
    x3 = xp
    z3 = 1
    avb = 0
    l = len(bin(r))
    print(f"Opération de multiplication par un scalaire de {l} bits")
    
    for i in range(l-1, -1, -1):
        bit = (r >> i) & 1
        b = bit ^ avb
        avb = bit
        [x2, z2], [x3, z3] = change([x2, z2], [x3, z3], b)
        x2, z2, x3, z3 = echelle([x2, z2], [x3, z3], x1)
        
    return (x2 * pow(z2, p-2, p))




