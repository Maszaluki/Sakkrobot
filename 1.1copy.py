
'''projects:

anti_hanging/anti-blunder'''
print('Köszöntjük a sakkbotban, a lépéseket hivalolos formában kellírni("Nf3", "O-O"), ha kell tisztázás akkor ("dNf3" vagy 3Rf5)')


import string
from  itertools import product
from  itertools import permutations
from tkinter.ttk import Separator
import copy
import random

class Piece:

    def __init__(self, color: bool, skip: bool, pos: tuple[int, int], destructable: bool, distance_restricted: bool, can_transform: bool, name, material : int, can_castle : bool) -> None:
        self.color = color
        self.skip = skip
        self.pos = pos
        self.destructable = destructable
        self.distance_restricted = distance_restricted
        self.can_transform = can_transform
        self.name = name
        self.material = material
        self.can_castle = can_castle

class Knight(Piece):
    def __init__(self, color, pos,  can_castle):
        super().__init__(color, True, pos, True, True, False,  "♞" if color else "♘", 3 ,  can_castle)
        Knight.id = "N"
class Rook(Piece):
    def __init__(self, color, pos, can_castle):
        super().__init__(color, False, pos, True, False, False, "♜"if color else  "♖", 5 ,can_castle )
        Rook.id = "R"     
class Bishop(Piece):
    def __init__(self, color, pos, can_castle):
        super().__init__(color, False, pos, True, False, False, "♝"if color else "♗", 3 ,  can_castle)
        Bishop.id = "B"
class King(Piece):
    def __init__(self, color,pos, can_castle ):
        super().__init__(color, False, pos, False, True, False, "♚"if color else "♔", 100,  can_castle)
        King.id = "K"
class Queen(Piece):
    def __init__(self, color, pos, can_castle):
        super().__init__(color, False, pos, True, False, False, "♛"if color else "♕", 9, can_castle )
        Queen.id = "Q"
class Pawn(Piece):
    def __init__(self, color, pos,  can_castle):
        super().__init__(color, False,pos , True, True, True, "♟"if color else "♙", 1,  can_castle )
class Empty(Piece):
    def __init__(self,pos, ):
        super().__init__(None, None, pos , True, True, True, "✖", None,  False  )


class Tabla:
    
    def __init__(self):
        self.tabla = [[Rook(True, (1,1), True), Knight(True, (1,2), False) , Bishop(True, (1,3), False), Queen(True, (1,4), False), King(True, (1,5), True), Bishop(True, (1,6), False), Knight(True, (1,7), False),Rook(True, (1,8), True)],
                      [Pawn(True, (2,i), False)  for i in range(1, 9)],
                      [Empty((3, i) ) for i in range(1, 9)],
                      [Empty((4, i) ) for i in range(1, 9)],
                      [Empty((5, i) ) for i in range(1, 9)],
                      [Empty((6, i)) for i in range(1, 9)],  
                      [Pawn(False, (7, i), False) for i in range(1, 9)],
                      [Rook(False, (8,1), True), Knight(False, (8,2), False) , Bishop(False, (8,3), False), Queen(False, (8,4), False), King(False, (8,5), True), Bishop(False, (8,6), False), Knight(False, (8,7), False),Rook(False, (8,8), True)]]
def possible_moves(table : Tabla,  pos : tuple ) :
    piece = table.tabla[pos[0]-1][pos[1]-1]
    set_temporary = set()
    különleges_set_temporary = set()
    jelenlegi_color = table.tabla[pos[0]-1][pos[1]-1].color
    if type(piece) == Pawn:
        if table.tabla[pos[0]-1][pos[1]-1].color:
            if pos[0] == 2:
                if type(table.tabla[3-1][pos[1]-1]) == Empty : set_temporary.add((3, pos[1])) 
                if type(table.tabla[4-1][pos[1]-1]) == Empty and type(table.tabla[3-1][pos[1]-1]) == Empty :set_temporary.add((4, pos[1]))
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
                if type(table.tabla[4][pos[1]-1]) == Empty and type(table.tabla[5][pos[1]-1]) == Empty :set_temporary.add((5, pos[1]))
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
                    continue
                cel_color = table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color
                if type(table.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1]) == Empty : set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
                elif jelenlegi_color == cel_color: continue
                elif jelenlegi_color != cel_color:
                    set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
            if table.tabla[pos[0]-1][pos[1]-1].can_castle == True:
                if table.tabla[pos[0]-1][pos[1]-1+3].can_castle == True and type(table.tabla[pos[0]-1][pos[1]-1+2]) == Empty and type(table.tabla[pos[0]-1][pos[1]-1+1]) == Empty :
                    különleges_set_temporary.add((pos[0], pos[1]+3))
                if table.tabla[pos[0]-1][pos[1]-1-4].can_castle == True and type(table.tabla[pos[0]-1][pos[1]-1-3]) == Empty and type(table.tabla[pos[0]-1][pos[1]-1-2]) == Empty  and type(table.tabla[pos[0]-1][pos[1]-1-1]) == Empty:
                    különleges_set_temporary.add((pos[0], pos[1]-4))
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
        for n in range(1,pos[0]):
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
        for z in range(1,pos[1]):
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
        for t in range(1,pos[0]):
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
        for p in range(1,pos[1]):
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
        elif table.tabla[pos[0]-1][pos[1]-1].color == table.tabla[k[0]-1][k[1]-1].color :
            set1.remove(k)
        elif type(piece) == King  :
            iranyok = set(product([0,1,-1], repeat=2))
            iranyok.remove((0,0))
            iranyok_copy = copy.deepcopy(iranyok)
            for teszt in iranyok_copy:
                if k[0]+teszt[0] == 0 or k[0]+teszt[0] == 9 or k[1]+teszt[1] == 0 or k[1]+teszt[1] == 9:
                    iranyok.remove(teszt)
            for irany in iranyok:
                if table.tabla[k[0]+irany[0]-1][k[1]+irany[1]+-1].color != table.tabla[pos[0]-1][pos[1]-1].color and type(table.tabla[k[0]+irany[0]-1][k[1]+irany[1]+-1]) == King :
                    set1.remove(k)
                    continue
    for i in különleges_set_temporary:
        set1.add(i)
    return set1
def active_pieces(table, oldal):
    active_pieces = set()
    for s in range(1,9):
        for z in range(1,9):
            if table.tabla[s-1][z-1].color == oldal and len(possible_moves(table,(s,z))) != 0:
                active_pieces.add((s,z))
    return active_pieces
def all_pieces(table, oldal):
    active_pieces = set()
    for s in range(1,9):
        for z in range(1,9):
            if table.tabla[s-1][z-1].color == oldal :
                active_pieces.add((s,z))
    return active_pieces

def sakk(table, oldal):
    all_possible_enemy_moves = set()
    for n in active_pieces(table, (not oldal)):
        for m in possible_moves(table,(n)):
            all_possible_enemy_moves.add((n,m))
    for lepes in all_possible_enemy_moves:
        if type(table.tabla[lepes[1][0]-1][lepes[1][1]-1]) == King and table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == oldal:
            return True
        else :
            continue
    return False
def sakkmatt(table, oldal):
    if sakk(table,oldal):
        calc_tabla = copy.deepcopy(table)
        all_possible_moves = set()
        summa = set()
        for n in active_pieces(table, oldal ):
    
            temporary_moves = set()
            for m in possible_moves(table,(n)):
                all_possible_moves.add((m))
                temporary_moves.add((m))
                
            for lepes in temporary_moves:
                calc_tabla = copy.deepcopy(table)
                move_sakknak( calc_tabla,n, lepes)
                if sakk(calc_tabla, oldal):
                    all_possible_moves.remove(lepes)
            for k in all_possible_moves:
                summa.add(k)

            temporary_moves.clear
            all_possible_moves.clear

           
        if len(summa)==0:
            return True

       
        else:
            return False         

            
    return False
def visual(tbla: Tabla, oldal : bool):
    if oldal:
        for i in range(7,-1,-1):
            print(i + 1, end=" ")
            for k in range(0,8,1):
                print(tbla.tabla[i][k].name, end="  ")
            
            print("")
        print(' ', end=" ")
        for k in range(0,8,1):
                print(["a","b","c","d","e","f","g","h"][k], end="  ")
        
            
    else:
        for i in range(0, 8 , 1):
            print(8-i, end=" ")
            for k in range(7,-1,-1):
                print(tbla.tabla[i][k].name, end="  ")
            print("")
        print(' ', end=" ")
        for k in range(7,-1,-1):
                print(["a","b","c","d","e","f","g","h"][k], end="  ")
    print("")

def move(table : Tabla, start:tuple, end: tuple):
        if type(table.tabla[start[0]-1][start[1]-1]) == Pawn and end[0] == ( 8 if table.tabla[start[0]-1][start[1]-1].color == True else 1) and table.tabla[start[0]-1][start[1]-1].color == side:
            piece_input = input("mire cserélsz, queen/rook/bishop/knight :")
            if piece_input == "queen":
                table.tabla[end[0]-1][end[1]-1] = Queen(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "rook":
                table.tabla[end[0]-1][end[1]-1] = Rook(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "knight":
                table.tabla[end[0]-1][end[1]-1] = Knight(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "bishop":
                table.tabla[end[0]-1][end[1]-1] = Bishop(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            return
        elif type(table.tabla[start[0]-1][start[1]-1]) == Pawn and end[0] == ( 8 if table.tabla[start[0]-1][start[1]-1].color == True else 1) and table.tabla[start[0]-1][start[1]-1].color == (not side):
                table.tabla[end[0]-1][end[1]-1] = Queen(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
                return

        if type(table.tabla[start[0]-1][start[1]-1]) == King and table.tabla[start[0]-1][start[1]-1].can_castle == True and type(table.tabla[end[0]-1][end[1]-1]) == Rook and table.tabla[end[0]-1][end[1]-1].can_castle == True :
                if start[1]-end[1]>0:
                        table.tabla[start[0]-1][start[1]-1-1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-1), False)
                        table.tabla[start[0]-1][start[1]-1-2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start)
                elif start[1]-end[1]<0:
                        table.tabla[start[0]-1][start[1]-1+1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+1), False)
                        table.tabla[start[0]-1][start[1]-1+2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start,)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start,)
        if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 : 
            return
        elif type(table.tabla[start[0]-1][start[1]-1]) == Empty:
            return
        elif table.tabla[start[0]-1][start[1]-1].color == table.tabla[end[0]-1][end[1]-1].color  : 
            return
        if end in possible_moves(table, start):
            table.tabla[end[0]-1][end[1]-1] = type(table.tabla[start[0]-1][start[1]-1])(table.tabla[start[0]-1][start[1]-1].color, end, False)
            table.tabla[start[0]-1][start[1]-1] = Empty(start)
        else :    
            return
stall = 0  
moves = list()
def move_stall(table : Tabla, start:tuple, end: tuple):
        global moves
        moves.append(("Wh" if table.tabla[start[0]-1][start[1]-1].color else "BL" ,start,end))
        global stall
        if type(table.tabla[start[0]-1][start[1]-1]) == Pawn and end[0] == ( 8 if table.tabla[start[0]-1][start[1]-1].color == True else 1) and table.tabla[start[0]-1][start[1]-1].color == side:
            piece_input = "queen"
            if piece_input == "queen":
                table.tabla[end[0]-1][end[1]-1] = Queen(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "rook":
                table.tabla[end[0]-1][end[1]-1] = Rook(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "knight":
                table.tabla[end[0]-1][end[1]-1] = Knight(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            elif piece_input == "bishop":
                table.tabla[end[0]-1][end[1]-1] = Bishop(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
            stall = 0
            return
        elif type(table.tabla[start[0]-1][start[1]-1]) == Pawn and end[0] == ( 8 if table.tabla[start[0]-1][start[1]-1].color == True else 1) and table.tabla[start[0]-1][start[1]-1].color == (not side):
                table.tabla[end[0]-1][end[1]-1] = Queen(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
                stall = 0
                return
        if type(table.tabla[end[0]-1][end[1]-1]) == King:
            exit
        if type(table.tabla[start[0]-1][start[1]-1]) == Pawn or type(table.tabla[end[0]-1][end[1]-1]) != Empty:
            stall = 0
        else :

            stall += 0.5
        if type(table.tabla[start[0]-1][start[1]-1]) == King and table.tabla[start[0]-1][start[1]-1].can_castle == True and type(table.tabla[end[0]-1][end[1]-1]) == Rook and table.tabla[end[0]-1][end[1]-1].can_castle == True :
                if start[1]-end[1]>0:
                        table.tabla[start[0]-1][start[1]-1-1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-1), False)
                        table.tabla[start[0]-1][start[1]-1-2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start)
                elif start[1]-end[1]<0:
                        table.tabla[start[0]-1][start[1]-1+1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+1), False)
                        table.tabla[start[0]-1][start[1]-1+2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start,)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start,)
        if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :
             
            return
        elif type(table.tabla[start[0]-1][start[1]-1]) == Empty:
             
            return
        elif table.tabla[start[0]-1][start[1]-1].color == table.tabla[end[0]-1][end[1]-1].color  :
            
            return
        if end in possible_moves(table, start):
            table.tabla[end[0]-1][end[1]-1] = type(table.tabla[start[0]-1][start[1]-1])(table.tabla[start[0]-1][start[1]-1].color, end, False)
            table.tabla[start[0]-1][start[1]-1] = Empty(start)
        else :
            
            return 
def move_sakknak(table : Tabla, start:tuple, end: tuple):
        if type(table.tabla[start[0]-1][start[1]-1]) == Pawn and end[0] == ( 8 if table.tabla[start[0]-1][start[1]-1].color == True else 1) :
                table.tabla[end[0]-1][end[1]-1] = Queen(table.tabla[start[0]-1][start[1]-1].color, end, False)
                table.tabla[start[0]-1][start[1]-1] = Empty(start)
                return

        if type(table.tabla[start[0]-1][start[1]-1]) == King and table.tabla[start[0]-1][start[1]-1].can_castle == True and type(table.tabla[end[0]-1][end[1]-1]) == Rook and table.tabla[end[0]-1][end[1]-1].can_castle == True :
                if start[1]-end[1]>0:
                        table.tabla[start[0]-1][start[1]-1-1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-1), False)
                        table.tabla[start[0]-1][start[1]-1-2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]-2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start)
                elif start[1]-end[1]<0:
                        table.tabla[start[0]-1][start[1]-1+1] = King(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+1), False)
                        table.tabla[start[0]-1][start[1]-1+2] = Rook(table.tabla[start[0]-1][start[1]-1].color, (start[0], start[1]+2), False)
                        table.tabla[start[0]-1][start[1]-1] = Empty(start)
                        table.tabla[end[0]-1][end[1]-1] = Empty(start)
        if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :
             
            return
        elif type(table.tabla[start[0]-1][start[1]-1]) == Empty:
              
            return
        elif table.tabla[start[0]-1][start[1]-1].color == table.tabla[end[0]-1][end[1]-1].color  :
            
            return
        if end in possible_moves(table, start):
            table.tabla[end[0]-1][end[1]-1] = type(table.tabla[start[0]-1][start[1]-1])(table.tabla[start[0]-1][start[1]-1].color, end, False)
            table.tabla[start[0]-1][start[1]-1] = Empty(start)
        else :
            
            return 
def all_material(table, oldal):
    material = 0
    for piece in all_pieces(table, oldal):
        
        if type(table.tabla[piece[0]-1][piece[1]-1]) != King:
            
            material += table.tabla[piece[0]-1][piece[1]-1].material
    return material 
def patt(table):
    if all_material(maintabla,True) == 0 and all_material(maintabla,False) == 0:
        return True
    all_possible_enemy_moves = set() 
    all_possibley_moves = set()
    for n in active_pieces(table, True):
        for m in possible_moves(table,(n)):
            all_possible_enemy_moves.add((n,m))
    if len(all_possible_enemy_moves) == 0:
        return True
    for n in active_pieces(table, False):
        for m in possible_moves(table,(n)):
            all_possibley_moves.add((n,m))
    if len(all_possibley_moves) == 0 or stall >= 50:
        return True
    else:
        return False

    
def can_be_taken(table, pos : tuple):
    oldal = table.tabla[pos[0]-1][pos[1]-1].color
    taking_pieces = set()
    for piece in active_pieces(table, not oldal):

        for lepes in possible_moves(table, piece):
            if lepes == pos:
                taking_pieces.add(piece)
    if len(taking_pieces) !=0:
        for l in taking_pieces:
            lowest_material = table.tabla[l[0]-1][l[1]-1].material
            break
        small_material = 0
        for l in taking_pieces:
            if  table.tabla[l[0]-1][l[1]-1].material < lowest_material:
                lowest_material = table.tabla[l[0]-1][l[1]-1].material
                small_material = table.tabla[l[0]-1][l[1]-1].material
        return((True, small_material, len(taking_pieces)))
    else:
        return((False, 0, 0))   
def is_defended(table, pos):
    oldal = table.tabla[pos[0]-1][pos[1]-1].color

    defending_pieces = set()
    calc_tabla = copy.deepcopy(table)
    calc_tabla.tabla[pos[0]-1][pos[1]-1] = Pawn((not oldal),pos, False)
    for piece in active_pieces(calc_tabla,  oldal):
        for lepes in possible_moves(calc_tabla, piece):
            
            if lepes == pos:
                defending_pieces.add(piece)
    if len(defending_pieces) !=0:
        for l in defending_pieces:
            lowest_material = calc_tabla.tabla[l[0]-1][l[1]-1].material
            
            small_material = type(calc_tabla.tabla[l[0]-1][l[1]-1])
            break
        for l in defending_pieces:
            if  calc_tabla.tabla[l[0]-1][l[1]-1].material < lowest_material:
                lowest_material = calc_tabla.tabla[l[0]-1][l[1]-1].material
                small_material = type(calc_tabla.tabla[l[0]-1][l[1]-1])
        
        return((True, small_material, len(defending_pieces)))
    else:
        return((False, Empty, 0))   
def evaluation(table):
    print("0")
    eval_bar = 0
    eval_bar += (all_material(table, True) - all_material(table, False)) / 2
    if sakkmatt(table, True):
        eval_bar += 50
    if sakkmatt(table, False):
        eval_bar += -50
    
    all_possible_moves = set()
    for n in active_pieces(table, True):
        for m in possible_moves(table,(n)):
            all_possible_moves.add((n,m))
    all_possible_moves_copy = set()
    for n in active_pieces(table, False):
        for m in possible_moves(table,(n)):
            all_possible_moves_copy.add((n,m))       
    eval_bar += (len(all_possible_moves) - len(all_possible_moves_copy))/40
    return eval_bar

    


turn = 0
def best_move_advanced(table, oldal):
    all_possible_moves = set()
    for n in active_pieces(table, oldal):
        for m in possible_moves(table,(n)):
            all_possible_moves.add((n,m))
            print(n,m)
    calc_tabla = copy.deepcopy(table)
    best_move_evalv = tuple()
    print(best_move_better(maintabla,oldal))
    alma = best_move_better(table,oldal)
    if oldal:
        best_move_evalv = (alma[0], evaluation(maintabla)+alma[1])
    else:
        best_move_evalv = (alma[0], evaluation(maintabla)-alma[1])
    list_evalv = set()
    
    
    print(len(all_possible_moves))
    for move in all_possible_moves:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,move[0],move[1])
        if sakk(calc_tabla,oldal):
            continue
        if sakkmatt(calc_tabla, not oldal):
            return move
        else:
            move_1 = best_move(calc_tabla, not oldal)
            move_sakknak(calc_tabla,move_1[0], move_1[1] )
            
            if sakk(calc_tabla, not oldal):
                continue
            if sakkmatt(calc_tabla, oldal):
                continue
            else:
                        move_2 = best_move(calc_tabla,  oldal)
                        move_sakknak(calc_tabla,move_2[0], move_2[1] )
                        if sakk(calc_tabla, oldal):
                            continue
                        if sakkmatt(calc_tabla, not oldal):
                            return move
                        else:
                            move_3 = best_move(calc_tabla,  not oldal)
                            move_sakknak(calc_tabla,move_3[0], move_3[1] )
                            if sakk(calc_tabla, not oldal):
                                    continue
                            if sakkmatt(calc_tabla, oldal):
                                continue
                            else:
                                list_evalv.add((move, evaluation(calc_tabla)))
    
    best_evalv = best_move_evalv 
    if oldal:
        for n in list_evalv:
            if n[1]>best_evalv[1]:
                best_evalv = n
    else:
        for k in list_evalv:
            if k[1]<best_evalv[1]:
                best_evalv = k
    return best_evalv[0]

def best_move_better(table, oldal : bool):
    all_possible_moves = set()
    for n in active_pieces(table, oldal):
        for m in possible_moves(table,(n)):
            all_possible_moves.add((n,m))
 
    '''mate in 1:'''
    all_possible_moves_copy1 = copy.deepcopy(all_possible_moves)
    for lepes in all_possible_moves_copy1:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if sakkmatt(calc_tabla, not oldal):
            return (lepes, 50)
    '''mate escape'''
    all_possible_moves_copy = copy.deepcopy(all_possible_moves)
    for lepes in all_possible_moves_copy:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if sakk(calc_tabla, oldal):
            all_possible_moves.remove(lepes)
    
    better_moves = set()
    calc_tabla = copy.deepcopy(table)
    if sakk(table,oldal):
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn:
                better_moves.add(((10),((lepes[0]),(lepes[1]))))
            if table.tabla[lepes[0][0]-1][lepes[0][1]-1].color == (not  table.tabla[lepes[1][0]-1][lepes[1][1]-1].color):
                better_moves.add(((20),((lepes[0]),(lepes[1]))))
                
        '''turn-based operation 1'''
    for lepes in all_possible_moves:
            if float(turn) < 2 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 if oldal else  lepes[1][0]== 5  ):
                randomint = random.randint(23, 50)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 35)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
  
   
            if float(turn) < 4 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 40)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 10 and float(turn) >= 2  and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 4 or lepes[1][0]== 5 ) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(27, 43)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
                
            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 25)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))

            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 3 or lepes[1][0]== 6 or lepes[1][0]== 2 or lepes[1][0]== 7) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  )  and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(29, 46)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 15 and float(turn) >=5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  ) and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(25, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if all_material(table, oldal) < 12 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn :
                randomint = random.randint(45, 65)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    """sánc"""        
    for m in active_pieces(table, oldal):       
        if type(table.tabla[m[0]-1][m[1]-1]) == King :       
                for n in possible_moves(table,(m)):
                    calc_tabla = copy.deepcopy(table)
                    move(calc_tabla, m,n)
                    if m[1]-4 == n[1] and not sakk(calc_tabla,oldal):                            
                            better_moves.add((0.75, ( m , n )))
                    if m[1]+3 == n[1] and not sakk(calc_tabla,oldal):
                            better_moves.add((0.75, ( m , n )))
    """anti_blunder 1 move """
    for lepes in all_possible_moves:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if type(table.tabla[lepes[1][0]-1][lepes[1][1]-1]) == Empty and not (is_defended(calc_tabla, lepes[1])[0]) and can_be_taken(calc_tabla, lepes[1])[0]:
            better_moves.add( (-table.tabla[lepes[0][0]-1][lepes[0][1]-1].material, ((lepes[0]),(lepes[1]))))
        for piece in all_pieces(calc_tabla,oldal):
            if can_be_taken(calc_tabla, piece)[0]:
                if not is_defended(calc_tabla, piece)[0]:
                    print("je",-(calc_tabla.tabla[piece[0]-1][piece[1]-1]).material)
                    better_moves.add((-(calc_tabla.tabla[piece[0]-1][piece[1]-1].material), (lepes[0], lepes[1])))
                elif calc_tabla.tabla[piece[0]-1][piece[1]-1].material > can_be_taken(calc_tabla,piece)[1]:
                    print ("desto", can_be_taken(calc_tabla,piece)[1]-calc_tabla.tabla[piece[0]-1][piece[1]-1].material)
                    better_moves.add((can_be_taken(calc_tabla,piece)[1]-calc_tabla.tabla[piece[0]-1][piece[1]-1].material,(lepes[0], lepes[1])))
    """free material"""
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and not is_defended(maintabla, lepes[1])[0]:
            better_moves.add(((table.tabla[lepes[1][0]-1][lepes[1][1]-1].material),(lepes[0],lepes[1])))
    """tactical 1 : istant capture"""
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and table.tabla[lepes[0][0]-1][lepes[0][1]-1].material < table.tabla[lepes[1][0]-1][lepes[1][1]-1].material:
            better_moves.add(((table.tabla[lepes[1][0]-1][lepes[1][1]-1].material - table.tabla[lepes[0][0]-1][lepes[0][1]-1].material),(lepes[0],lepes[1])))
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and table.tabla[lepes[0][0]-1][lepes[0][1]-1].material == table.tabla[lepes[1][0]-1][lepes[1][1]-1].material:
            randomint_1 = random.randint(30,55)/100
            better_moves.add(((randomint_1),(lepes[0],lepes[1])))
    """progress"""
    if float(turn) > 15 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn :
                randomint = random.randint(10, 20)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    all_possible_moves_list = list(all_possible_moves)
    
    if len(better_moves) != 0:
        végső = [0, ((all_possible_moves_list[0][0]),(all_possible_moves_list[0][1]))]
        for better in better_moves:
            if better[0] >= végső[0]:
                végső = [better[0], better[1] ]
        return (végső[1],végső[0])
    randomint = random.randint(0, len(all_possible_moves)-1)
    segéd = 0
    for vége in all_possible_moves:
        if    segéd == randomint:
            return vége
        else:
            segéd += 1
                        


def best_move(table, oldal : bool):
    print("1")
    all_possible_moves = set()
    for n in active_pieces(table, oldal):
        for m in possible_moves(table,(n)):
            all_possible_moves.add((n,m))
    '''mate in 1:'''
    all_possible_moves_copy1 = copy.deepcopy(all_possible_moves)
    for lepes in all_possible_moves_copy1:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if sakkmatt(calc_tabla, not oldal):
            return lepes
    '''mate escape'''
    all_possible_moves_copy = copy.deepcopy(all_possible_moves)
    for lepes in all_possible_moves_copy:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if sakk(calc_tabla, oldal):
            all_possible_moves.remove(lepes)
    
    better_moves = set()
    calc_tabla = copy.deepcopy(table)
    if sakk(table,oldal):
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn:
                better_moves.add(((10),((lepes[0]),(lepes[1]))))
            if table.tabla[lepes[0][0]-1][lepes[0][1]-1].color == (not  table.tabla[lepes[1][0]-1][lepes[1][1]-1].color):
                better_moves.add(((20),((lepes[0]),(lepes[1]))))
                
    '''turn-based operation 1'''
    
    for lepes in all_possible_moves:
            if float(turn) < 2 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 if oldal else  lepes[1][0]== 5  ):
                randomint = random.randint(23, 50)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 35)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
  
   
            if float(turn) < 4 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 40)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 10 and float(turn) >= 2  and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 4 or lepes[1][0]== 5 ) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(27, 43)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
                
            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 25)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))

            if float(turn) < 10 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 3 or lepes[1][0]== 6 or lepes[1][0]== 2 or lepes[1][0]== 7) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  )  and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(29, 46)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if float(turn) < 15 and float(turn) >=5 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  ) and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(25, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
            if all_material(table, oldal) < 12 and type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn :
                randomint = random.randint(45, 65)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    """sánc"""        
    for m in active_pieces(table, oldal):       
        if type(table.tabla[m[0]-1][m[1]-1]) == King :       
                for n in possible_moves(table,(m)):
                    calc_tabla = copy.deepcopy(table)
                    move(calc_tabla, m,n)
                    if m[1]-4 == n[1] and not sakk(calc_tabla,oldal):                            
                            better_moves.add((0.75, ( m , n )))
                    if m[1]+3 == n[1] and not sakk(calc_tabla,oldal):
                            better_moves.add((0.75, ( m , n )))
    """anti_blunder 1 move """
    for lepes in all_possible_moves:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if type(table.tabla[lepes[1][0]-1][lepes[1][1]-1]) == Empty and not (is_defended(calc_tabla, lepes[1])[0]) and can_be_taken(calc_tabla, lepes[1])[0]:
            better_moves.add( (-table.tabla[lepes[0][0]-1][lepes[0][1]-1].material, ((lepes[0]),(lepes[1]))))
        for piece in all_pieces(calc_tabla,oldal):
            if can_be_taken(calc_tabla, piece)[0]:
                if not is_defended(calc_tabla, piece)[0]:
                    better_moves.add((-(calc_tabla.tabla[piece[0]-1][piece[1]-1].material), (lepes[0], lepes[1])))
                elif calc_tabla.tabla[piece[0]-1][piece[1]-1].material > can_be_taken(calc_tabla,piece)[1]:                
                    better_moves.add((can_be_taken(calc_tabla,piece)[1]-calc_tabla.tabla[piece[0]-1][piece[1]-1].material,(lepes[0], lepes[1])))
            
    """free material"""
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and not is_defended(maintabla, lepes[1])[0]:
            better_moves.add(((table.tabla[lepes[1][0]-1][lepes[1][1]-1].material),(lepes[0],lepes[1])))
    """tactical 1 : istant capture"""
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and table.tabla[lepes[0][0]-1][lepes[0][1]-1].material < table.tabla[lepes[1][0]-1][lepes[1][1]-1].material:
            better_moves.add(((table.tabla[lepes[1][0]-1][lepes[1][1]-1].material - table.tabla[lepes[0][0]-1][lepes[0][1]-1].material),(lepes[0],lepes[1])))
    for lepes in all_possible_moves:
        if table.tabla[lepes[1][0]-1][lepes[1][1]-1].color == (not oldal) and table.tabla[lepes[0][0]-1][lepes[0][1]-1].material == table.tabla[lepes[1][0]-1][lepes[1][1]-1].material:
            randomint_1 = random.randint(30,55)/100
            better_moves.add(((randomint_1),(lepes[0],lepes[1])))
    """progress"""
    if float(turn) > 15 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn :
                randomint = random.randint(10, 20)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    all_possible_moves_list = list(all_possible_moves)
    
    if len(better_moves) != 0:
        végső = [0, ((all_possible_moves_list[0][0]),(all_possible_moves_list[0][1]))]
        for better in better_moves:
            if better[0] >= végső[0]:
                végső = [better[0], better[1] ]
        return végső[1]
    randomint = random.randint(0, len(all_possible_moves)-1)
    segéd = 0
    for vége in all_possible_moves:
        if    segéd == randomint:
            return vége
        else:
            segéd += 1
 
maintabla = Tabla()


def order(fNf3,table, oldal):
    if fNf3 == None or len(fNf3) > 5 or len(fNf3) < 2:
            print ("helytelen lépés")
            ujlepes = input("Mást kell lépned : ")
            return order(ujlepes, maintabla, oldal)
    if fNf3 == "exit":
            exit("köszönöm a játékot")
            exit
    if fNf3 == "matt":
            print("sakk matt, nyertél")
            exit("köszönöm a játékot")
            exit
    dolgok = []
    if fNf3 == "O-O" :
        if oldal == True:
            return [(1,8),(1,5)]
        else:
            return [(8,8),(8,5)]
    if fNf3 == "O-O-O" :
        if oldal == True:
            return [(1,1),(1,5)]
        else:
            return [(8,1),(8,5)]

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
        ujlepes = input("Mást kell lépned : ")
        return order(ujlepes, maintabla, oldal)
    else:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,eredmeny[1], eredmeny[0])
        if sakk(calc_tabla, oldal) == True:
            print ("helytelen lépés")
            ujlepes = input("Mást kell lépned : ")
            return order(ujlepes, maintabla, oldal)
        if fNf3 == None:
            print ("helytelen lépés")
            ujlepes = input("Mást kell lépned : ")
            return order(ujlepes, maintabla, oldal)
        calc_tabla = copy.deepcopy(table)
    return eredmeny

start = input(" white or black? : ")
side = bool()
if start == "white":    
    side = True
elif start == "black":
    side = False
else: 
      
    exit("indisd ujra a programot és helyesen ird be a színt")

if side == True:
    turn += 0.5
    visual(maintabla, side)
    temporary_order =  order(input("Lépj:"),maintabla,side)
    move(maintabla,temporary_order[1],temporary_order[0] )
    
    visual(maintabla, side)
    print("")
kezdés = True    

while True:
    '''robots turn'''

    turn += 0.5 
    print(turn)
    if sakkmatt(maintabla, not side):
        if side:
            print("Fehér nyert")
        else:
            print("Fekete nyert")
        exit("sakk matt")
    if patt(maintabla):
        print("patt")
        exit("döntetlen")
    if sakk(maintabla, not side):
        print("robot sakk")
    if kezdés :
        temporary_order =  tuple(best_move(maintabla,  not side)) 
    else:    
        temporary_order =  tuple(best_move_advanced(maintabla,  not side)) 
    move(maintabla,temporary_order[0],temporary_order[1] )
    visual(maintabla, side)

    '''players turn'''
    turn += 0.5
    kezdés = False
    if sakkmatt(maintabla, side):
        if side:
            print("Fekete nyert")
        else:
            print("Fehér nyert")
        exit("sakk matt")
    if patt(maintabla, ):
        print("patt")
        exit("döntetlen")
    if sakk(maintabla, side):
        print("sakk")
    temporary_order_1 =  order(input("Lépj:"),maintabla,side)
    print(temporary_order_1)
    move(maintabla,temporary_order_1[1],temporary_order_1[0] )
    visual(maintabla, side)
    print("")