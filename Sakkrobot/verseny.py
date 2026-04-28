számok = []
inverz = []
print(type(számok))
import random
for i in range (10):
    számok.append(random.randint(10, 99))
'''for ind in range(0, len(számok) - 1, 1):
    minhely = ind
    for j in range(ind + 1, len(számok)):
        if számok[j] < számok[minhely]:
            minhely = j
    if minhely != ind:
        csere = számok[ind]
        számok[ind] = számok[minhely]
        számok[minhely] = csere
print('a nyerő számok: XX XX XX XX XX')
pénzed = (input('tippjeid: ').split(" "))
cheat = "cheat"
instantwin = "instantwin"
casoh = "casoh"
sakk = "sakk"
if pénzed[0] == cheat:
    print(számok)
    pénzed = (input('tippjeid: ').split(" "))
elif  pénzed[0] == instantwin:
    print ("nyertél, 5/5")
    exit("jackpot")
elif pénzed[0] == casoh:
    exit('túlsúly')
elif pénzed[0] == sakk:
    print('Köszöntjük a sakkbotban, a lépéseket hivalolos formában kellírni("Nf3")')

    x = 'X'
    R = 'R'
    N = 'N'
    B = 'B'
    Q = 'Q'
    K = '♚'
    P = "P"

    r = 'r'
    n = 'n'
    b = 'b'
    q = 'q'
    k = '♔'
    p = 'p'

    T1 = r
    T2 = n
    T3 = b
    T4 = q
    T5 = k
    T6 = x
    T7 = n
    T8 = r
    T9 = p
    T10 = p
    T11 = p
    T12 = p
    T13 = p
    T14 = p
    T15 = p
    T16 = p
    T17 = x
    T18 = x
    T19 = x
    T20 = x
    T21 = x
    T22 = x
    T23 = x
    T24 = x
    T25 = x
    T26 = x
    T27 = x
    T28 = x
    T29 = x
    T30 = x
    T31 = x
    T32 = x
    T33 = x
    T34 = x
    T35 = x
    T36 = x
    T37 = x
    T38 = x
    T39 = x
    T40 = x
    T41 = x
    T42 = x
    T43 = x
    T44 = x
    T45 = x
    T46 = x
    T47 = x
    T48 = x
    T49 = P
    T50 = P
    T51 = P
    T52 = P
    T53 = P
    T54 = P
    T55 = P
    T56 = P
    T57 = R
    T58 = N
    T59 = B
    T60 = Q
    T61 = K
    T62 = B
    T63 = N
    T64 = R

    a = [T1, T9, T17, T25, T33, T41, T49, T57, ]
    b = [T2, T10, T18, T26, T34, T42, T50, T58]
    c = [T3, T11, T19, T27, T35, T43, T51, T59, ]
    d = [T4, T12, T20, T28, T36, T44, T52, T60, ]
    e = [T5, T13, T21, T29, T37, T45, T53, T61, ]
    f = [T6, T14, T22, T30, T38, T46, T54, T62, ]
    g = [T7, T15, T23, T31, T39, T47, T55, T63, ]
    h = [T8, T16, T24, T32, T40, T48, T56, T64, ]

    start = input(" white or black? : ")
    if start == "white":
        for i in range(0, 8):
            print(a[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i], sep="      ", end="\n\n")
        L1 = str(input("Kezdhetsz: "))
        if len(L1) == 2:

            pass
        elif len(L1) == 3:
            pass
        else:
            print()



    elif start == "black":

        for i in range(0, 8):
            print(a[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i], sep="      ", end="\n\n")
    exit
if len(pénzed) != 5:
    print('csak pontosan 5 számot írhatsz be')
    exit('abnormális vagy')


for k in range (1, 6):
    inverz.append(számok[-k] )

for ndx in range (len(számok)):
        print(f'{számok[ndx]}', end=', ')
print()
for mdx in range(len(pénzed)):
        print(f'{pénzed[mdx]}', end=', ')

megfelel = 0
for ertek in pénzed:
    if int(ertek) in számok:
        megfelel += 1
        számok.remove(int(ertek))
print("eltaláltál: ", megfelel)
if megfelel < 4 :
    print('nem kapod vissza a pénzedet')
else :
    print("visszakapsz egy kicsit a énzedből")

for i in range (5):
    számok.append(random.randint(10, 99))'''
'''

#minimum érték kiválasztása
print(min(számok))
minimumertek = számok[0]
for ertek in számok:
    if ertek < minimumertek:
        minimumertek = ertek
print(f'A számok list legkisebb értéke: {minimumertek}')

minimumertek = számok[0]
for ertek in számok[1:]:
    if ertek < minimumertek:
        minimumertek = ertek
print(f'A számok list legkisebb értéke: {minimumertek}')

for ertek in számok:
    if ertek == min(számok):
        print (ertek)'''
'''maxert = max(számok)
print (maxert)
indexi = számok.i1ndex(maxert)
print (indexi)'''
#minimum
'''print (f' Rendezés előtt :{számok=}')
for ni in range(0, len(számok) - 1, 1):
    minhely = ni
    for j in range(ni + 1, len(számok)):
        if számok[j] < számok[minhely]:
            minhely = j
    if minhely != ni:
        csere = számok[ni]
        számok[ni] = számok[minhely]
        számok[minhely] = csere
print (számok)'''
for ind in range(0, len(számok) - 1, 1):
    minhely = ind
    for j in range(ind + 1, len(számok)):
        if számok[j] > számok[minhely]:
            minhely = j
    if minhely != ind:
        csere = számok[ind]
        számok[ind] = számok[minhely]
        számok[minhely] = csere
        print (számok)

rendezett_számok = sorted(számok)



