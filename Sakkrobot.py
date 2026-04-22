print('Köszöntjük a sakkbotban, a lépéseket hivalolos formában kellírni("Nf3"), ha kell tisztázás akkor ("N")')

import string
from  itertools import product
from  itertools import permutations
from tkinter.ttk import Separator
class Piece:

    def __init__(self, color: bool, skip: bool, pos: tuple[int, int], destructable: bool, distance_restricted: bool, can_transform: bool, name,) -> None:
        self.color = color
        self.skip = skip
        self.pos = pos
        self.destructable = destructable
        self.distance_restricted = distance_restricted
        self.can_transform = can_transform
        self.name = name
        

class Knight(Piece):
    def __init__(self, color, pos,):
        super().__init__(color, True, pos, True, True, False,  "♞" if color else "♘" )
        Knight.id = "N"
class Rook(Piece):
    def __init__(self, color, pos,):
        super().__init__(color, False, pos, True, False, False, "♜"if color else  "♖" )
        Rook.id = "R"     
class Bishop(Piece):
    def __init__(self, color, pos,):
        super().__init__(color, False, pos, True, False, False, "♝"if color else "♗" )
        Bishop.id = "B"
class King(Piece):
    def __init__(self, color,pos, ):
        super().__init__(color, False, pos, False, True, False, "♚"if color else "♔" )
        King.id = "K"
class Queen(Piece):
    def __init__(self, color, pos,):
        super().__init__(color, False, pos, True, False, False, "♛"if color else "♕" )
        Queen.id = "Q"
class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, False,pos , True, True, True, "♟"if color else "♙" )
class Empty(Piece):
    def __init__(self,pos):
        super().__init__(None, None, pos , True, True, True, "✖", )


class Tabla:
    
    def __init__(self):
        self.tabla = [[Rook(True, (1,1)), Knight(True, (1,2)) , Bishop(True, (1,3)), Queen(True, (1,4)), King(True, (1,5)), Bishop(True, (1,6)), Knight(True, (1,7)),Rook(True, (1,8))],
                      [Pawn(True, (2,i))  for i in range(1, 9)],
                      [Empty((3, i)) for i in range(1, 9)],
                      [Empty((4, i)) for i in range(1, 9)],
                      [Empty((5, i)) for i in range(1, 9)],
                      [Empty((6, i)) for i in range(1, 9)],  
                      [Pawn(False, (7, i)) for i in range(1, 9)],
                      [Rook(False, (8,1)), Knight(False, (8,2)) , Bishop(False, (8,3)), Queen(False, (8,4)), King(False, (8,5)), Bishop(False, (8,6)), Knight(False, (8,7)),Rook(False, (8,8))]]
def possible_moves(table : Tabla,  pos : tuple ) :
    piece = table.tabla[pos[0]-1][pos[1]-1]
    set_temporary = set()
    jelenlegi_color = table.tabla[pos[0]-1][pos[1]-1].color
    if type(piece) == Pawn:
        if table.tabla[pos[0]-1][pos[1]-1].color:
            if pos[0] == 2:
                if type(table.tabla[3-1][pos[1]-1]) == Empty : set_temporary.add((3, pos[1])) 
                if type(table.tabla[4-1][pos[1]-1]) == Empty :set_temporary.add((4, pos[1]))
                if  pos[1]  != 1 :   
                    if table.tabla[3-1][pos[1]-2].color == False :set_temporary.add((3, pos[1]-1))
                if pos[1]  != 8 :
                    if table.tabla[3-1][pos[1]].color == False :set_temporary.add((3, pos[1]+1))
            elif pos[0] == 8:
                print("cant move furtharer")
            else:
                if type(table.tabla[pos[0]+1-1][pos[1]-1]) == Empty : set_temporary.add((pos[0]+1, pos[1]))
                if pos[1]  != 8 :
                    if table.tabla[pos[0]+1-1][pos[1]+1-1].color == False :set_temporary.add((pos[0]+1,pos[1]+1))
                if  pos[1]  != 1  :
                    if table.tabla[pos[0]+1-1][pos[1]-2].color == False :set_temporary.add((pos[0]+1,pos[1]-1))
        else:
            if pos[0] == 7:
                if type(table.tabla[5][pos[1]-1]) == Empty :set_temporary.add((6, pos[1]))
                if type(table.tabla[4][pos[1]-1]) == Empty :set_temporary.add((5, pos[1]))
                if  pos[1]  != 1:    
                    if table.tabla[5][pos[1]-2].color == True :set_temporary.add((6, pos[1]-1))
                if pos[1]  != 8 :
                    if table.tabla[5][pos[1]].color == True :set_temporary.add((6, pos[1]+1))
            elif pos[0] == 1:
                pass
                
            else:
                if type(table.tabla[pos[0]-2][pos[1]-1]) == Empty : set_temporary.add((pos[0]-1, pos[1]))
                if pos[1]  != 8  :    
                    if table.tabla[pos[0]-2][pos[1]].color == True :set_temporary.add((pos[0]-1,pos[1]+1))
                if  pos[1]  != 1 :    
                    if table.tabla[pos[0]-2][pos[1]-2].color == True :set_temporary.add((pos[0]-1,pos[1]-1))
    elif type(piece) == King:
            iranyok = set(product([0,1,-1], repeat=2))
            iranyok.remove((0,0))
            for irany in iranyok:
                if (pos[0]+irany[0]-1)>7 or (pos[1]+irany[1]-1)>7 or (pos[0]+irany[0]-1)<0 or (pos[1]+irany[1]-1)<0:
                    break
                cel_color = table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color
                if type(table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1]) == Empty : set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
                elif jelenlegi_color == cel_color: continue
                elif jelenlegi_color != cel_color:
                    set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
            '''sakkban való levést majd ide!'''
    elif type(piece) == Rook:
        for m in range(1,8-pos[0]):
            if type(table.tabla[pos[0]+m-1][pos[1]-1]) == Empty  :
                set_temporary.add((pos[0]+m, pos[1]))
            else:
                if table.tabla[pos[0]+m-1][pos[1]-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+m, pos[1]))
                    break             
        for n in range(1,pos[0]-1):
            if type(table.tabla[pos[0]-n-1][pos[1]-1]) == Empty:
                set_temporary.add((pos[0]-n, pos[1]))
            else:
                if table.tabla[pos[0]-n-1][pos[1]-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-n, pos[1]))
                    break
        for s in range(1,8-pos[1]):
            if type(table.tabla[pos[0]-1][pos[1]+s-1]) == Empty:
                set_temporary.add((pos[0], pos[1]+s))
            else:
                if table.tabla[pos[0]-1][pos[1]+s-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0], pos[1]+s))
                    break               
        for z in range(1,pos[1]-1):
            if type(table.tabla[pos[0]-1][pos[1]-z-1]) == Empty:
                set_temporary.add((pos[0], pos[1]-z))
            else:
                if table.tabla[pos[0]-1][pos[1]-z-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0], pos[1]-z))
                    break
    elif type(piece) == Queen:
        for m in range(1,min(8-pos[0]+1, pos[1])):
            if type(table.tabla[pos[0]+m-1][pos[1]-m-1]) == Empty:
                set_temporary.add((pos[0]+m, pos[1]-m))
            else:
                if table.tabla[pos[0]+m-1][pos[1]-m-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+m, pos[1]-m))
                    break
        for n in range(1,min(8-pos[0]+1, 8-pos[1]+1)):
            if type(table.tabla[pos[0]+n-1][pos[1]+n-1]) == Empty:
                set_temporary.add((pos[0]+n, pos[1]+n))
            else:
                if table.tabla[pos[0]+n-1][pos[1]+n-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+n, pos[1]+n))
                    break
        for s in range(1,min(pos[0], pos[1])):
            if type(table.tabla[pos[0]-s-1][pos[1]-s-1]) == Empty:
                set_temporary.add((pos[0]-s, pos[1]-s))
            else:
                if table.tabla[pos[0]-s-1][pos[1]-s-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-s, pos[1]-s))
                    break
        for z in range(1,min(pos[0], 8-pos[1]+1)):
            if type(table.tabla[pos[0]-z-1][pos[1]+z-1]) == Empty:
                set_temporary.add((pos[0]-z, pos[1]+z))
            else:
                if table.tabla[pos[0]-z-1][pos[1]+z-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-z, pos[1]+z))
                    break
        for l in range(1,8-pos[0]):
            if type(table.tabla[pos[0]+l-1][pos[1]-1]) == Empty  :
                set_temporary.add((pos[0]+l, pos[1]))
            else:
                if table.tabla[pos[0]+l-1][pos[1]-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+l, pos[1]))
                    break    
        for t in range(1,pos[0]-1):
            if type(table.tabla[pos[0]-t-1][pos[1]-1]) == Empty:
                set_temporary.add((pos[0]-t, pos[1]))
            else:
                if table.tabla[pos[0]-t-1][pos[1]-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-t, pos[1]))
                    break
        for f in range(1,8-pos[1]):
            if type(table.tabla[pos[0]-1][pos[1]+f-1]) == Empty:
                set_temporary.add((pos[0], pos[1]+f))
            else:
                if table.tabla[pos[0]-1][pos[1]+f-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0], pos[1]+f))
                    break  
        for p in range(1,pos[1]-1):
            if type(table.tabla[pos[0]-1][pos[1]-p-1]) == Empty:
                set_temporary.add((pos[0], pos[1]-p))
            else:
                if table.tabla[pos[0]-1][pos[1]-p-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0], pos[1]-p))
                    break
    elif type(piece) == Bishop:
        for m in range(1,min(8-pos[0]+1, pos[1])):
            if type(table.tabla[pos[0]+m-1][pos[1]-m-1]) == Empty:
                set_temporary.add((pos[0]+m, pos[1]-m))
            else:
                if table.tabla[pos[0]+m-1][pos[1]-m-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+m, pos[1]-m))
                    break
        for n in range(1,min(8-pos[0]+1, 8-pos[1]+1)):
            if type(table.tabla[pos[0]+n-1][pos[1]+n-1]) == Empty:
                set_temporary.add((pos[0]+n, pos[1]+n))
            else:
                if table.tabla[pos[0]+n-1][pos[1]+n-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]+n, pos[1]+n))
                    break
        for s in range(1,min(pos[0], pos[1])):
            if type(table.tabla[pos[0]-s-1][pos[1]-s-1]) == Empty:
                set_temporary.add((pos[0]-s, pos[1]-s))
            else:
                if table.tabla[pos[0]-s-1][pos[1]-s-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-s, pos[1]-s))
                    break
        for z in range(1,min(pos[0], 8-pos[1]+1)):
            if type(table.tabla[pos[0]-z-1][pos[1]+z-1]) == Empty:
                set_temporary.add((pos[0]-z, pos[1]+z))
            else:
                if table.tabla[pos[0]-z-1][pos[1]+z-1].color == jelenlegi_color:
                    break
                else:
                    set_temporary.add((pos[0]-z, pos[1]+z))
                    break  
    elif type(piece) == Knight:
        iranyok = set()
        kset = set(product([2,1], repeat = 2))
        for k in kset:
            if k[0] != k[1]:
                iranyok.add(k)
        nset = set(product([-2,1], repeat = 2))
        for n in nset:
            if n[0] != n[1]:
                iranyok.add(n)
        tset = set(product([-2,-1], repeat = 2))
        for t in tset:
            if t[0] != t[1]:
                iranyok.add(t)             
        wset = set(product([2,-1], repeat = 2))
        for w in wset:
            if w[0] != w[1]:
                iranyok.add(w)
        for irany in iranyok:
            if irany[0]+pos[0] < 1:
                continue 
            elif irany[0]+pos[0] >= 9:
                continue
            elif irany[1]+pos[1] >= 9 :
                continue
            elif irany[1]+pos[1] < 1:
                continue
            elif type(table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1]) == Empty : set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
            elif jelenlegi_color == table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color: continue
            elif jelenlegi_color != table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color:
                    set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))  
    set1 = set()
    for i in set_temporary:
        
        set1.add(i)
    
    for k in set_temporary:
        if k[0] < 1:
            set1.remove(k)
        elif k[0] >= 9:
            set1.remove(k)
        elif k[1] >= 9 :
            set1.remove(k)
        elif k[1] < 1:
            set1.remove(k)
        elif table.tabla[pos[0]-1][pos[1]-1].color == table.tabla[k[0]-1][k[1]-1].color:
            set1.remove(k)
    return set1
def move(table : Tabla, start:tuple, end: tuple):
        
        if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :
            print("number out of range") 
            return
        if type(table.tabla[end[0]-1][end[1]-1]) == King and table.tabla[end[0]-1][end[1]-1].color != table.tabla[start[0]-1][start[1]-1].color:
            if table.tabla[end[0]-1][end[1]-1].color == True:
                print("Fekete nyert, sakkmatt")
            else:
                print("Fehér nyert, sakkmatt")
            exit("Game over")

        elif type(table.tabla[start[0]-1][start[1]-1]) == Empty:
            print ("nothing error")  
            return
        elif table.tabla[start[0]-1][start[1]-1].color == table.tabla[end[0]-1][end[1]-1].color  :
            print("own destruction")
            return
        if end in possible_moves(table, start):
            table.tabla[end[0]-1][end[1]-1] = type(table.tabla[start[0]-1][start[1]-1])(table.tabla[start[0]-1][start[1]-1].color, end)
            table.tabla[start[0]-1][start[1]-1] = Empty(start)
        else :
            print("nem léphet oda")
            return
'''def best_move(table, oldal : bool):
    all_possible_moves = []
    active_pieces = set()
    for s in range(1,9):
        for z in range(1,9):
            if table.tabla[s-1][z-1].color == oldal and len(possible_moves(table,(s,z))) != 0:
                active_pieces.add((s,z))
    for n in active_pieces:
        for m in possible_moves(table,(s,z))
    pass'''
maintabla = Tabla()

def order(fNf3,table, oldal):
    dolgok = []
    for p in range(1, len(fNf3)+1):
        dolgok.append(fNf3[-p])
    '''print(dolgok)'''
    eredmeny =[]
    
    cel = (int(dolgok[0]),["a", "b" ,"c", "d", "e", "f", "g", "h"].index(dolgok[1])+1) 
    eredmeny.append((int(dolgok[0]),(["a", "b" ,"c", "d", "e", "f", "g", "h"].index(dolgok[1])+1)) )
    if len(dolgok) == 2:
        cel_piece = Pawn
        start_sor = None
        start_oszlop = None
    else:
        if dolgok[2] in {"a","b","c","d","e","f","g","h"}  :
            cel_piece = Pawn
            start_oszlop = None
            start_sor = ["a", "b" ,"c", "d", "e", "f", "g", "h"].index(dolgok[2])+1
        elif dolgok[2] in {"1","2","3","4","5","6","7","8"}  :
            cel_piece = Pawn
            start_oszlop = int(dolgok[2])
            start_sor = None
        else:
            for k in {King, Knight, Rook, Bishop,Queen }:
                if k.id == dolgok[2]:
                    cel_piece = k
                    start_sor = None
                    start_oszlop = None
            if len(dolgok) == 4:
                if dolgok[3] in {"a","b","c","d","e","f","g","h"}  :
                    start_sor = ["a", "b" ,"c", "d", "e", "f", "g", "h"].index(dolgok[3])+1
                    start_oszlop = None
                elif dolgok[3] in {"1","2","3","4","5","6","7","8"}  :
                    start_oszlop = int(dolgok[3])
                    start_sor = None

    for s in range(1,9):
        for z in range(1,9):          
            if cel in possible_moves(table,(s,z)):              
                if type(table.tabla[s-1][z-1]) == cel_piece and table.tabla[s-1][z-1].color == oldal:
                    if start_oszlop == s or start_oszlop == None:
                        if start_sor == z or start_sor == None:
                            eredmeny.append((s,z))
    '''eredmeny.append()'''
    '''print (eredmeny)'''
    if len(eredmeny) != 2:
        print ("helytelen lépés")
        exit("vége")
    return eredmeny
def visual(tbla: Tabla, oldal):
    if oldal == True :
        for i in range(7,-1,-1):
            for k in range(0,8,1):
                print(tbla.tabla[i][k].name, end="  ")
            print("")
    elif oldal == False:
        for i in range(0,8,1):
            for k in range(7,-1,-1):
                print(tbla.tabla[i][k].name, end="  ")
            print("")
start = input(" white or black? : ")
side = bool()
if start == "white":    
    side = True
elif start == "black":
    side = False
else: 
    print("indisd ujra a programot és helyesen ird be a színt")
    exit


if side == True:
    visual(maintabla, side)
    temporary_order =  order(input("Lépj:"),maintabla,side)
    move(maintabla,temporary_order[1],temporary_order[0] )
    turn = 0,5 
    visual(maintabla, side)
    print("")
while True:
    '''robots turn'''
    
    temporary_order =  order(input("Lépj:"),maintabla,  not side)
    move(maintabla,temporary_order[1],temporary_order[0] )
    turn =+ 0,5 

    visual(maintabla, side)
    print("")
    '''players turn'''
    temporary_order =  order(input("Lépj:"),maintabla,side)
    move(maintabla,temporary_order[1],temporary_order[0] )
    turn =+ 0,5 
    visual(maintabla, side)