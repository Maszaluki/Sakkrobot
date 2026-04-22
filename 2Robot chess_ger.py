
'''projects:

anti_hanging/anti-blunder'''
import itertools
from abc import abstractmethod, ABC

print('Köszöntjük a sakkbotban, a lépéseket hivalolos formában kellírni("Nf3", "O-O"), ha kell tisztázás akkor ("dNf3" vagy 3Rf5)')

import copy
import random
from itertools import product

class Position:

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self._data = pos

    def as_tuple(self):
        return self._data

    def in_bound(self):
        return 0 <= self.x < 8 and 0 <= self.y < 8

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        if type(other) is not Position:
            raise ValueError(f"Can't add type {type(other)} to type position")
        return Position((self.x + other.x, self.y + other.y))

    def reverse(self):
        return Position((-self.x, -self.y))

    def __sub__(self, other):
        if type(other) is not Position:
            raise ValueError(f"Can't subtract type {type(other)} from type position")
        return Position((self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        if type(other) is not int:
            raise ValueError(f"Multiplication only allowed with int and not with {type(other)}")
        return Position((self.x * other, self.y * other))

    def __eq__(self, other):
        if type(other) is not Position:
            raise ValueError(f"Can't compare type {type(other)} to type position")
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, item):
        return self._data[item]

FORWARD_WHITE = Position((1, 0))
FORWARD_BLACK = Position((-1, 0))

class Piece(ABC):

    def __init__(self, tabla: "Tabla", color: bool, skip: bool, pos: tuple[int, int], destructable: bool, distance_restricted: bool, can_transform: bool, name, material : int, can_castle : bool) -> None:
        self.tabla = tabla
        self.color: bool | None = color
        self.skip = skip
        self.pos = pos
        self.destructable = destructable
        self.distance_restricted = distance_restricted
        self.can_transform = can_transform
        self.name = name
        self.material = material
        self.can_castle = can_castle

    def type(self):
        return type(self)

    @abstractmethod
    def possible_moves(self) -> set[tuple[int, int]]:
        return set()

    @staticmethod
    def get_promotion_type(typestr: str):
        return {
            "queen": Queen,
            "rook": Rook,
            "knight": Knight,
            "bishop": Bishop
        }.get(typestr)

class LimitlessMovePiece(Piece):

    @abstractmethod
    def directions(self) -> set[Position]:
        pass

    def possible_moves(self) -> set[tuple[int, int]]:

        possible = set()
        vectors = self.directions()

        for vec in vectors:

            for step in range(1, 8):

                position = Position(self.pos) + vec * step
                if not position.in_bound() or self.tabla.get_piece(position.as_tuple()).color is self.color: # ha nincs benne vagy sajat -> stop
                    break
                possible.add(position.as_tuple()) # ha nem sajat vagy ures

        return possible


class Knight(Piece):
    def __init__(self, table, color, pos):
        super().__init__(table, color, True, pos, True, True, False,  "♞" if color else "♘", 3 ,  False)
        Knight.id = "N"

    def possible_moves(self):
        pass

class Rook(LimitlessMovePiece):
    def __init__(self, color, pos):
        super().__init__(color, False, pos, True, False, False, "♜"if color else  "♖", 5 ,True)
        Rook.id = "R"

    def directions(self) -> set[Position]:
        directions = set()
        for direction in product([0,1,-1], repeat=2):
            vector = Position(direction)
            if vector.length() == 1: ## ha vektor nagysaga 1 -> egy axison mozog
                directions.add(vector)
        return directions


class Bishop(LimitlessMovePiece):
    def __init__(self, color, pos):
        super().__init__(color, False, pos, True, False, False, "♝"if color else "♗", 3 ,  False)
        Bishop.id = "B"

    def directions(self) -> set[Position]:
        directions = set()
        for direction in product([0,1,-1], repeat=2):
            vector = Position(direction)
            if vector.length() == 2**0.5: ## ha vektor nagysaga gyok ketto -> atlos
                directions.add(vector)
        return directions


class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, False, pos, False, True, False, "♚"if color else "♔", 100,  True)
        King.id = "K"

    def possible_moves(self) -> set[tuple[int, int]]:
        iranyok = set(product([0, 1, -1], repeat=2))
        iranyok.remove((0, 0))
        for irany in iranyok:

            position = Position(self.pos) + Position(irany)
            if not position.in_bound():
                continue

            ## TODO     castle es kiraly kore nem lephet

class Queen(LimitlessMovePiece):
    def __init__(self, color, pos):
        super().__init__(color, False, pos, True, False, False, "♛"if color else "♕", 9, False )
        Queen.id = "Q"

    def directions(self) -> set[Position]:
        return {Position(vector) for vector in product([0, 1, -1], repeat=2) if vector != (0, 0)} # barmerre ami nem 0

class Pawn(Piece):

    def __init__(self, table, color, pos):
        super().__init__(table, color,False,pos , True, True, True, "♟"if color else "♙", 1,  False )

    def possible_moves(self):
        moves: set[tuple[int, int]] = set()
        if self.color: # feher

            elore = Position(self.pos) + FORWARD_WHITE
            if self.tabla.get_piece(elore.as_tuple()).type() is Empty:
                moves.add(elore.as_tuple())

                elore_dupla = elore + FORWARD_WHITE
                if self.pos[0] == 1 and self.tabla.get_piece(elore_dupla.as_tuple()).type() is Empty: # ha elso so -> dupla elore
                    moves.add(elore_dupla.as_tuple())

            if self.pos[1] != 0: # nem legbal -> tud balra
                bal_utes = Position(self.pos) + Position((-1, -1))
                if self.tabla.get_piece(bal_utes.as_tuple()).color is False: # feka
                    moves.add(bal_utes.as_tuple())

            if self.pos[1] != 7: # nem legjob -> tud job
                job_utes = Position(self.pos) + Position((1, 1))
                if self.tabla.get_piece(job_utes.as_tuple()).color is False: # feka
                    moves.add(job_utes.as_tuple())

        else: # feka

            elore = Position(self.pos) + FORWARD_BLACK
            if self.tabla.get_piece(elore.as_tuple()).type() is Empty:
                moves.add(elore.as_tuple())

                elore_dupla = elore + FORWARD_BLACK
                if self.pos[0] == 6 and self.tabla.get_piece(
                        elore_dupla.as_tuple()).type() is Empty:  # ha elso so -> dupla elore
                    moves.add(elore_dupla.as_tuple())

            if self.pos[1] != 0:  # nem legbal -> tud balra
                bal_utes = Position(self.pos) + Position((-1, -1))
                if self.tabla.get_piece(bal_utes.as_tuple()).color:  # feher
                    moves.add(bal_utes.as_tuple())

            if self.pos[1] != 7:  # nem legjob -> tud job
                job_utes = Position(self.pos) + Position((-1, 1))
                if self.tabla.get_piece(job_utes.as_tuple()).color:  # feher
                    moves.add(job_utes.as_tuple())


class Empty(Piece):
    def __init__(self,pos):
        super().__init__(None, None, pos , True, True, True, "✖", None,  False)


class Tabla:
    
    def __init__(self):
        self.turn = 0.5
        self.tabla: list[list[Piece]] = [[Rook(True, (0, 0)), Knight(True, (0, 1)), Bishop(True, (0, 2)),
                       Queen(True, (0, 3)), King(True, (0, 4)), Bishop(True, (0, 5)), Knight(True, (0, 6)),
                       Rook(True, (0, 7))],
                      [Pawn(True, (1, i)) for i in range(0, 8)],
                      [Empty((2, i) ) for i in range(0, 8)],
                      [Empty((3, i) ) for i in range(0, 8)],
                      [Empty((4, i) ) for i in range(0, 8)],
                      [Empty((5, i)) for i in range(0, 8)],
                      [Pawn(False, (6, i)) for i in range(0, 8)],
                      [Rook(False, (7, 0)), Knight(False, (7, 1)), Bishop(False, (7, 2)),
                       Queen(False, (7, 3)), King(False, (7, 4)), Bishop(False, (7, 5)), Knight(False, (7, 6)),
                       Rook(False, (7, 7))]]

    def is_empty(self, pos: tuple[int, int]) -> bool:
        return self.get_piece((pos[0], pos[1])).type() is Empty

    def get_piece(self, pos: tuple[int, int]) -> Piece:
        return self.tabla[pos[0]][pos[1]]

    def get_piece_cords(self, oszlop: int, sor: int):
        return self.get_piece((oszlop, sor))

    def set_piece(self, pos: tuple[int, int], piece: Piece) -> None:
        self.tabla[pos[0]][pos[1]] = piece

    def possible_moves(self,  pos: tuple[int, int] ) -> set[tuple[int, int]]:
        piece = self.get_piece(pos)
        set_temporary: set[tuple[int, int]] = set()
        különleges_set_temporary = set()
        jelenlegi_color = self.get_piece(pos).color
        if type(piece) == Pawn:
            set_temporary.update(piece.possible_moves())
        elif type(piece) == King:
                iranyok = set(product([0,1,-1], repeat=2))
                iranyok.remove((0,0))
                for irany in iranyok:
                    if (pos[0]+irany[0]-1)>7 or (pos[1]+irany[1]-1)>7 or (pos[0]+irany[0]-1)<0 or (pos[1]+irany[1]-1)<0:
                        continue
                    cel_color = self.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color
                    if type(self.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1]) == Empty : set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
                    elif jelenlegi_color == cel_color: continue
                    elif jelenlegi_color != cel_color:
                        set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
                if self.get_piece(pos).can_castle:
                    if self.tabla[pos[0]-1][pos[1]-1+3].can_castle == True and type(self.tabla[pos[0]-1][pos[1]-1+2]) == Empty and type(self.tabla[pos[0]-1][pos[1]-1+1]) == Empty :
                        különleges_set_temporary.add((pos[0], pos[1]+3))
                    if self.tabla[pos[0]-1][pos[1]-1-4].can_castle == True and type(self.tabla[pos[0]-1][pos[1]-1-3]) == Empty and type(self.tabla[pos[0]-1][pos[1]-1-2]) == Empty  and type(self.tabla[pos[0]-1][pos[1]-1-1]) == Empty:
                        különleges_set_temporary.add((pos[0], pos[1]-4))

                '''sakkban való levést majd ide!'''
        elif type(piece) == Rook:
            for m in range(1,8-pos[0]):
                if type(self.tabla[pos[0]+m-1][pos[1]-1]) == Empty  :
                    set_temporary.add((pos[0]+m, pos[1]))
                else:
                    if self.tabla[pos[0]+m-1][pos[1]-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]+m, pos[1]))
                        break
            for n in range(1,pos[0]):
                if type(self.tabla[pos[0]-n-1][pos[1]-1]) == Empty:
                    set_temporary.add((pos[0]-n, pos[1]))
                else:
                    if self.tabla[pos[0]-n-1][pos[1]-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]-n, pos[1]))
                        break
            for s in range(1,8-pos[1]):
                if type(self.tabla[pos[0]-1][pos[1]+s-1]) == Empty:
                    set_temporary.add((pos[0], pos[1]+s))
                else:
                    if self.tabla[pos[0]-1][pos[1]+s-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0], pos[1]+s))
                        break
            for z in range(1,pos[1]):
                if type(self.tabla[pos[0]-1][pos[1]-z-1]) == Empty:
                    set_temporary.add((pos[0], pos[1]-z))
                else:
                    if self.tabla[pos[0]-1][pos[1]-z-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0], pos[1]-z))
                        break
        elif type(piece) == Queen:
            for m in range(1,min(8-pos[0]+1, pos[1])):
                if type(self.tabla[pos[0]+m-1][pos[1]-m-1]) == Empty:
                    set_temporary.add((pos[0]+m, pos[1]-m))
                else:
                    if self.tabla[pos[0]+m-1][pos[1]-m-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]+m, pos[1]-m))
                        break
            for n in range(1,min(8-pos[0]+1, 8-pos[1]+1)):
                if type(self.tabla[pos[0]+n-1][pos[1]+n-1]) == Empty:
                    set_temporary.add((pos[0]+n, pos[1]+n))
                else:
                    if self.tabla[pos[0]+n-1][pos[1]+n-1].color != jelenlegi_color:
                        set_temporary.add((pos[0]+n, pos[1]+n))
                    break
            for s in range(1,min(pos[0], pos[1])):
                if type(self.tabla[pos[0]-s-1][pos[1]-s-1]) == Empty:
                    set_temporary.add((pos[0]-s, pos[1]-s))
                else:
                    if self.tabla[pos[0]-s-1][pos[1]-s-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]-s, pos[1]-s))
                        break
            for z in range(1,min(pos[0], 8-pos[1]+1)):
                if type(self.tabla[pos[0]-z-1][pos[1]+z-1]) == Empty:
                    set_temporary.add((pos[0]-z, pos[1]+z))
                else:
                    if self.tabla[pos[0]-z-1][pos[1]+z-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]-z, pos[1]+z))
                        break
            for l in range(1,8-pos[0]):
                if type(self.tabla[pos[0]+l-1][pos[1]-1]) == Empty  :
                    set_temporary.add((pos[0]+l, pos[1]))
                else:
                    if self.tabla[pos[0]+l-1][pos[1]-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]+l, pos[1]))
                        break
            for t in range(1,pos[0]):
                if type(self.tabla[pos[0]-t-1][pos[1]-1]) == Empty:
                    set_temporary.add((pos[0]-t, pos[1]))
                else:
                    if self.tabla[pos[0]-t-1][pos[1]-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]-t, pos[1]))
                        break
            for f in range(1,8-pos[1]):
                if type(self.tabla[pos[0]-1][pos[1]+f-1]) == Empty:
                    set_temporary.add((pos[0], pos[1]+f))
                else:
                    if self.tabla[pos[0]-1][pos[1]+f-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0], pos[1]+f))
                        break
            for p in range(1,pos[1]):
                if type(self.tabla[pos[0]-1][pos[1]-p-1]) == Empty:
                    set_temporary.add((pos[0], pos[1]-p))
                else:
                    if self.tabla[pos[0]-1][pos[1]-p-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0], pos[1]-p))
                        break
        elif type(piece) == Bishop:
            for m in range(1,min(8-pos[0]+1, pos[1])):
                if type(self.tabla[pos[0]+m-1][pos[1]-m-1]) == Empty:
                    set_temporary.add((pos[0]+m, pos[1]-m))
                else:
                    if self.tabla[pos[0]+m-1][pos[1]-m-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]+m, pos[1]-m))
                        break
            for n in range(1,min(8-pos[0]+1, 8-pos[1]+1)):
                if type(self.tabla[pos[0]+n-1][pos[1]+n-1]) == Empty:
                    set_temporary.add((pos[0]+n, pos[1]+n))
                else:
                    if self.tabla[pos[0]+n-1][pos[1]+n-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]+n, pos[1]+n))
                        break
            for s in range(1,min(pos[0], pos[1])):
                if type(self.tabla[pos[0]-s-1][pos[1]-s-1]) == Empty:
                    set_temporary.add((pos[0]-s, pos[1]-s))
                else:
                    if self.tabla[pos[0]-s-1][pos[1]-s-1].color == jelenlegi_color:
                        break
                    else:
                        set_temporary.add((pos[0]-s, pos[1]-s))
                        break
            for z in range(1,min(pos[0], 8-pos[1]+1)):
                if type(self.tabla[pos[0]-z-1][pos[1]+z-1]) == Empty:
                    set_temporary.add((pos[0]-z, pos[1]+z))
                else:
                    if self.tabla[pos[0]-z-1][pos[1]+z-1].color == jelenlegi_color:
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
                elif type(self.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1]) == Empty : set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
                elif jelenlegi_color == self.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color: continue
                elif jelenlegi_color != self.tabla[pos[0]+irany[0]-1][pos[1]+irany[1]-1].color:
                        set_temporary.add((pos[0]+irany[0], pos[1]+irany[1]))
        set1 = set()
        for i in set_temporary:

            set1.add(i)
        for i in különleges_set_temporary:
            set1.add(i)

        for k in set_temporary:

            if k[0] < 1:
                set1.remove(k)
                continue
            elif k[0] >= 9:
                set1.remove(k)
                continue
            elif k[1] >= 9 :
                set1.remove(k)
                continue
            elif k[1] < 1:
                set1.remove(k)
                continue


            elif self.get_piece(pos).color == self.get_piece(k).color:
                set1.remove(k)
                continue
            elif type(piece) == King  :
                iranyok = set(product([0,1,-1], repeat=2))
                iranyok.remove((0,0))
                iranyok_copy = copy.deepcopy(iranyok)
                for teszt in iranyok_copy:
                    if k[0]+teszt[0] == 0 or k[0]+teszt[0] == 9 or k[1]+teszt[1] == 0 or k[1]+teszt[1] == 9:
                        iranyok.remove(teszt)
                for irany in iranyok:
                    if self.tabla[k[0]+irany[0]-1][k[1]+irany[1]+-1].color != self.get_piece(pos).color and type(self.tabla[k[0]+irany[0]-1][k[1]+irany[1]+-1]) == King :
                        set1.remove(k)
                        continue

        """print (k)
        print(piece.name)
        print ("alma")"""
        return set1

    def active_pieces(self, oldal: bool) -> set[tuple[int, int]]:
        active_pieces = set()
        for s in range(1,9):
            for z in range(1,9):
                if self.tabla[s - 1][z - 1].color == oldal and len(self.possible_moves((s, z))) != 0:
                    active_pieces.add((s,z))
        return active_pieces

    def all_pieces(self, oldal):
        active_pieces = set()
        for s in range(1,9):
            for z in range(1,9):
                if self.tabla[s - 1][z - 1].color == oldal :
                    active_pieces.add((s,z))
        return active_pieces

    def sakk(self, oldal):
        all_possible_enemy_moves = set()
        for n in self.active_pieces(not oldal):
            for m in self.possible_moves(n):
                all_possible_enemy_moves.add((n,m))
        for lepes in all_possible_enemy_moves:
            if type(self.tabla[lepes[1][0] - 1][lepes[1][1] - 1]) == King and self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color == oldal:
                return True
            continue
        return False

    def sakkmatt(self, oldal):
        if self.sakk(oldal):
            all_possible_moves = set()
            summa = set()
            for n in self.active_pieces(oldal):

                temporary_moves = set()
                for m in self.possible_moves(n):
                    all_possible_moves.add(m)
                    temporary_moves.add(m)

                for lepes in temporary_moves:
                    calc_tabla = copy.deepcopy(self)
                    calc_tabla.move_sakknak(n, lepes)
                    if calc_tabla.sakk(oldal):
                        all_possible_moves.remove(lepes)
                for k in all_possible_moves:
                    summa.add(k)

            return len(summa) == 0

        return False

    def visual(self, oldal : bool):
        if oldal:
            for i in range(7,-1,-1):
                print(i + 1, end=" ")
                for k in range(0,8,1):
                    print(self.tabla[i][k].name, end="  ")

                print("")
            print(' ', end=" ")
            for k in range(0,8,1):
                    print(["abcdefgh"][k], end="  ")


        else:
            for i in range(0, 8 , 1):
                print(8-i, end=" ")
                for k in range(7,-1,-1):
                    print(self.tabla[i][k].name, end="  ")
                print("")
            print(' ', end=" ")
            for k in range(7,-1,-1):
                    print("abcdefgh"[k], end="  ")
        print("")

    def move(self, start:tuple[int, int], end: tuple[int, int]):
            if self.get_piece(start).type() == Pawn and end[0] == ( 8 if self.tabla[start[0] - 1][start[1] - 1].color == True else 1) and self.tabla[start[0] - 1][start[1] - 1].color == side:
                piece_input = input("mire cserélsz, queen/rook/bishop/knight :")

                promotion_type = Piece.get_promotion_type(piece_input)
                if promotion_type is None:
                    raise Exception(f"nem tudsz erre promotolni: {piece_input}")

                self.set_piece(end, promotion_type(self.get_piece(start).color, end))
                self.set_piece(start, Empty(start))

            elif type(self.tabla[start[0] - 1][start[1] - 1]) == Pawn and end[0] == ( 8 if self.tabla[start[0] - 1][start[1] - 1].color == True else 1) and self.tabla[start[0] - 1][start[1] - 1].color == (not side):
                    self.tabla[end[0] - 1][end[1] - 1] = Queen(self.tabla[start[0] - 1][start[1] - 1].color, end)
                    self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                    return

            if type(self.tabla[start[0] - 1][start[1] - 1]) == King and self.tabla[start[0] - 1][start[1] - 1].can_castle == True and type(self.tabla[end[0] - 1][end[1] - 1]) == Rook and self.tabla[end[0] - 1][end[1] - 1].can_castle == True :
                    if start[1]-end[1]>0:
                            self.tabla[start[0] - 1][start[1] - 1 - 1] = King(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] - 1))
                            self.tabla[start[0] - 1][start[1] - 1 - 2] = Rook(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] - 2))
                            self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                            self.tabla[end[0] - 1][end[1] - 1] = Empty(start)
                    elif start[1]-end[1]<0:
                            self.tabla[start[0] - 1][start[1] - 1 + 1] = King(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] + 1))
                            self.tabla[start[0] - 1][start[1] - 1 + 2] = Rook(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] + 2))
                            self.tabla[start[0] - 1][start[1] - 1] = Empty(start, )
                            self.tabla[end[0] - 1][end[1] - 1] = Empty(start, )
            if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :
                return
            elif type(self.tabla[start[0] - 1][start[1] - 1]) == Empty:
                return
            elif self.tabla[start[0] - 1][start[1] - 1].color == self.tabla[end[0] - 1][end[1] - 1].color  :
                return
            if end in self.possible_moves(start):
                self.tabla[end[0] - 1][end[1] - 1] = type(self.tabla[start[0] - 1][start[1] - 1])(self.tabla[start[0] - 1][start[1] - 1].color, end, False)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            else :
                return

    def move_stall(self, start:tuple[int, int], end: tuple[int, int]):
        self.moves.append(("Wh" if self.tabla[start[0] - 1][start[1] - 1].color else "BL" , start, end))
        if type(self.tabla[start[0] - 1][start[1] - 1]) == Pawn and end[0] == ( 8 if self.tabla[start[0] - 1][start[1] - 1].color == True else 1) and self.tabla[start[0] - 1][start[1] - 1].color == side:
            piece_input = "queen"
            if piece_input == "queen":
                self.tabla[end[0] - 1][end[1] - 1] = Queen(self.tabla[start[0] - 1][start[1] - 1].color, end)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            elif piece_input == "rook":
                self.tabla[end[0] - 1][end[1] - 1] = Rook(self.tabla[start[0] - 1][start[1] - 1].color, end)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            elif piece_input == "knight":
                self.tabla[end[0] - 1][end[1] - 1] = Knight(self.tabla[start[0] - 1][start[1] - 1].color, end)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            elif piece_input == "bishop":
                self.tabla[end[0] - 1][end[1] - 1] = Bishop(self.tabla[start[0] - 1][start[1] - 1].color, end)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            self.stall = 0
            return
        elif type(self.tabla[start[0] - 1][start[1] - 1]) == Pawn and end[0] == ( 8 if self.tabla[start[0] - 1][start[1] - 1].color == True else 1) and self.tabla[start[0] - 1][start[1] - 1].color == (not side):
                self.tabla[end[0] - 1][end[1] - 1] = Queen(self.tabla[start[0] - 1][start[1] - 1].color, end)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                self.stall = 0
                return
        if type(self.tabla[end[0] - 1][end[1] - 1]) == King:
            exit
        if type(self.tabla[start[0] - 1][start[1] - 1]) == Pawn or type(self.tabla[end[0] - 1][end[1] - 1]) != Empty:
            self.stall = 0
        else :

            self.stall += 0.5
        if type(self.tabla[start[0] - 1][start[1] - 1]) == King and self.tabla[start[0] - 1][start[1] - 1].can_castle == True and type(self.tabla[end[0] - 1][end[1] - 1]) == Rook and self.tabla[end[0] - 1][end[1] - 1].can_castle == True :
                if start[1]-end[1]>0:
                        self.tabla[start[0] - 1][start[1] - 1 - 1] = King(self.tabla[start[0] - 1][start[1] - 1].color,
                                                                          (start[0], start[1] - 1))
                        self.tabla[start[0] - 1][start[1] - 1 - 2] = Rook(self.tabla[start[0] - 1][start[1] - 1].color,
                                                                          (start[0], start[1] - 2))
                        self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                        self.tabla[end[0] - 1][end[1] - 1] = Empty(start)
                elif start[1]-end[1]<0:
                        self.tabla[start[0] - 1][start[1] - 1 + 1] = King(self.tabla[start[0] - 1][start[1] - 1].color,
                                                                          (start[0], start[1] + 1))
                        self.tabla[start[0] - 1][start[1] - 1 + 2] = Rook(self.tabla[start[0] - 1][start[1] - 1].color,
                                                                          (start[0], start[1] + 2))
                        self.tabla[start[0] - 1][start[1] - 1] = Empty(start, )
                        self.tabla[end[0] - 1][end[1] - 1] = Empty(start, )
        if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :

            return
        elif type(self.tabla[start[0] - 1][start[1] - 1]) == Empty:

            return
        elif self.tabla[start[0] - 1][start[1] - 1].color == self.tabla[end[0] - 1][end[1] - 1].color  :

            return
        if end in self.possible_moves(start):
            self.tabla[end[0] - 1][end[1] - 1] = type(self.tabla[start[0] - 1][start[1] - 1])(self.tabla[start[0] - 1][start[1] - 1].color, end, False)
            self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
        else :
            return

    def move_sakknak(self, start:tuple[int, int], end: tuple[int, int]):
            if type(self.tabla[start[0] - 1][start[1] - 1]) == Pawn and end[0] == ( 8 if self.tabla[start[0] - 1][start[1] - 1].color == True else 1) :
                    self.tabla[end[0] - 1][end[1] - 1] = Queen(self.tabla[start[0] - 1][start[1] - 1].color, end)
                    self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                    return

            if type(self.tabla[start[0] - 1][start[1] - 1]) == King and self.tabla[start[0] - 1][start[1] - 1].can_castle == True and type(self.tabla[end[0] - 1][end[1] - 1]) == Rook and self.tabla[end[0] - 1][end[1] - 1].can_castle == True :
                    if start[1]-end[1]>0:
                            self.tabla[start[0] - 1][start[1] - 1 - 1] = King(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] - 1))
                            self.tabla[start[0] - 1][start[1] - 1 - 2] = Rook(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] - 2))
                            self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                            self.tabla[end[0] - 1][end[1] - 1] = Empty(start)
                    elif start[1]-end[1]<0:
                            self.tabla[start[0] - 1][start[1] - 1 + 1] = King(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] + 1))
                            self.tabla[start[0] - 1][start[1] - 1 + 2] = Rook(
                                self.tabla[start[0] - 1][start[1] - 1].color, (start[0], start[1] + 2))
                            self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
                            self.tabla[end[0] - 1][end[1] - 1] = Empty(start)
            if start == end or start[0]>8 or start[1]>8 or end[0]<1 or end[1]<1 or start[0]<1 or start[1]<1 or end[0]>8 or end[1]>8 :

                return
            elif type(self.tabla[start[0] - 1][start[1] - 1]) == Empty:

                return
            elif self.tabla[start[0] - 1][start[1] - 1].color == self.tabla[end[0] - 1][end[1] - 1].color  :

                return
            if end in self.possible_moves(start):
                self.tabla[end[0] - 1][end[1] - 1] = type(self.tabla[start[0] - 1][start[1] - 1])(self.tabla[start[0] - 1][start[1] - 1].color, end, False)
                self.tabla[start[0] - 1][start[1] - 1] = Empty(start)
            else :
                return

    def all_material(self, oldal):
        material = 0
        for piece in self.all_pieces(oldal):

            if type(self.tabla[piece[0] - 1][piece[1] - 1]) != King:

                material += self.tabla[piece[0] - 1][piece[1] - 1].material
        return material

    def patt(self):
        if self.all_material(True) == 0 and self.all_material(False) == 0:
            return True
        all_possible_enemy_moves = set()
        all_possible_moves = set()
        for n in self.active_pieces(True):
            for m in self.possible_moves(n):
                all_possible_enemy_moves.add((n,m))
        if len(all_possible_enemy_moves) == 0:
            return True
        for n in self.active_pieces(False):
            for m in self.possible_moves(n):
                all_possible_moves.add((n,m))
        if len(all_possible_moves) == 0 or self.stall >= 50:
            return True
        else:
            return False

    def can_be_taken(self, pos : tuple[int, int]):
        oldal = self.get_piece(pos).color
        taking_pieces = set()
        for piece in self.active_pieces(not oldal):

            for lepes in self.possible_moves(piece):
                if lepes == pos:
                    taking_pieces.add(piece)
        if len(taking_pieces) !=0:
            for l in taking_pieces:
                lowest_material = self.tabla[l[0] - 1][l[1] - 1].material
                break
            small_material = Empty
            for l in taking_pieces:
                if  self.tabla[l[0] - 1][l[1] - 1].material < lowest_material:
                    lowest_material = self.tabla[l[0] - 1][l[1] - 1].material
                    small_material = type(self.tabla[l[0] - 1][l[1] - 1])
            return True, small_material, len(taking_pieces)
        else:
            return False, Empty, 0

    def is_defended(self, pos):
        oldal = self.get_piece(pos).color

        defending_pieces = set()
        calc_tabla = copy.deepcopy(self)
        calc_tabla.set_piece(pos, Pawn((not oldal), pos))
        for piece in calc_tabla.active_pieces(oldal):
            for lepes in calc_tabla.possible_moves(piece):

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

            return True, small_material, len(defending_pieces)
        else:
            return False, Empty, 0

    def evaluation(self):
        print("0")
        eval_bar = 0
        eval_bar += (self.all_material(True) - self.all_material(False)) / 2
        if self.sakkmatt(True):
            eval_bar += 50
        if self.sakkmatt(False):
            eval_bar += -50
        if True:
            all_possible_moves = set()
            for n in self.active_pieces(True):
                for m in self.possible_moves(n):
                    all_possible_moves.add((n,m))
            all_possible_moves_copy = set()
            for n in self.active_pieces(False):
                for m in self.possible_moves(n):
                    all_possible_moves_copy.add((n,m))
            eval_bar += (len(all_possible_moves) - len(all_possible_moves_copy))/40
        return eval_bar

    def best_move_better(self, oldal : bool):
        all_possible_moves = set()
        for n in self.active_pieces(oldal):
            for m in self.possible_moves(n):
                all_possible_moves.add((n,m))
        '''mate in 0'''
        for lepes in all_possible_moves:
            if type(self.tabla[lepes[1][0] - 1][lepes[1][1] - 1]) == King and self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color != oldal:
                return [(lepes[0]),(lepes[1])]
        '''mate in 1:'''
        all_possible_moves_copy1 = copy.deepcopy(all_possible_moves)
        for lepes in all_possible_moves_copy1:
            calc_tabla = copy.deepcopy(self)
            calc_tabla.move_sakknak(lepes[0],lepes[1])
            if calc_tabla.sakkmatt(not oldal):
                return lepes
        '''mate escape'''
        all_possible_moves_copy = copy.deepcopy(all_possible_moves)
        for lepes in all_possible_moves_copy:
            calc_tabla = copy.deepcopy(self)
            calc_tabla.move_sakknak(lepes[0],lepes[1])
            if calc_tabla.sakk(oldal):
                all_possible_moves.remove(lepes)

        better_moves = set()
        calc_tabla = copy.deepcopy(self)
        if self.sakk(oldal):
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn:
                    better_moves.add(((10),((lepes[0]),(lepes[1]))))
                if self.tabla[lepes[0][0] - 1][lepes[0][1] - 1].color == (not  self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color):
                    better_moves.add(((20),((lepes[0]),(lepes[1]))))

        '''turn-based operation 1'''
        if self.turn < 2  :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn and (lepes[0][1] == 3 or lepes[0][1] == 4 or lepes[0][1] == 5) and (lepes[1][0] == 4 if oldal else lepes[1][0] == 5):
                    randomint = random.randint(23, 50)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 5 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn and (lepes[0][1] == 3 or lepes[0][1] == 4 or lepes[0][1] == 5 or lepes[0][1] == 2 or lepes[0][1] == 7) and (lepes[1][0] == 3 or lepes[1][0] == 6):
                    randomint = random.randint(15, 35)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 10:
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn and (lepes[0][1] == 3 or lepes[0][1] == 4 or lepes[0][1] == 5 or lepes[0][1] == 2 or lepes[0][1] == 7) and (lepes[1][0] == 3 or lepes[1][0] == 6):
                    randomint = random.randint(15, 25)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 4 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn and (lepes[0][1] == 3 or lepes[0][1] == 4 or lepes[0][1] == 5) and (lepes[1][0] == 4 or lepes[1][0] == 5):
                    randomint = random.randint(20, 40)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if 10 > self.turn >= 2:
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn and (lepes[0][1] == 3 or lepes[0][1] == 4 or lepes[0][1] == 5) and (lepes[1][0] == 4 or lepes[1][0] == 5):
                    randomint = random.randint(20, 30)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 10 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Bishop and (lepes[0][1] == 3 or lepes[0][1] == 6) and (lepes[1][0] == 4 or lepes[1][0] == 5) and (lepes[0][0] == 1 or lepes[0][0] == 8):
                    randomint = random.randint(27, 43)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 10 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Bishop and (lepes[0][1] == 3 or lepes[0][1] == 6) and (lepes[1][0] == 3 or lepes[1][0] == 6 or lepes[1][0] == 2 or lepes[1][0] == 7) and (lepes[0][0] == 1 or lepes[0][0] == 8):
                    randomint = random.randint(20, 30)/100
                    better_moves.add((randomint, ((lepes[0]), (lepes[1]))))
        if self.turn < 5 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Knight and (lepes[1][1] == 3 or lepes[1][1] == 6) and (lepes[1][0] == 3 or lepes[1][0] == 6)  and (lepes[0][0] == 1 or lepes[0][0] == 8):
                    randomint = random.randint(29, 46)/100
                    better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
        if 15 > self.turn >= 5:
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Knight and (lepes[1][1] == 3 or lepes[1][1] == 6) and (lepes[1][0] == 3 or lepes[1][0] == 6) and (lepes[0][0] == 1 or lepes[0][0] == 8):
                    randomint = random.randint(25, 30)/100
                    better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
        if self.all_material(oldal) < 12:
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn :
                    randomint = random.randint(45, 65)/100
                    better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
        """sánc"""
        for m in self.active_pieces(oldal):
            if type(self.tabla[m[0] - 1][m[1] - 1]) == King :
                for n in self.possible_moves(m):
                        if m[1]-4 == n[1] :
                                better_moves.add((0.75, ( m , n )))
                        if m[1]+3 == n[1] :
                                better_moves.add((0.75, ( m , n )))
        """anti_blunder 1 move """
        for lepes in all_possible_moves:
            calc_tabla = copy.deepcopy(self)
            calc_tabla.move_sakknak(lepes[0], lepes[1])
            if type(self.tabla[lepes[1][0] - 1][lepes[1][1] - 1]) == Empty and not (is_defended(calc_tabla, lepes[1])[0]) and can_be_taken(calc_tabla, lepes[1])[0]:
                better_moves.add((-self.tabla[lepes[0][0] - 1][lepes[0][1] - 1].material, ((lepes[0]), (lepes[1]))))
            for piece in all_pieces(calc_tabla,oldal):
                if not (is_defended(calc_tabla, piece)[0]) and can_be_taken(calc_tabla, piece)[0] and type(self.tabla[piece[0] - 1][piece[1] - 1]) != Empty:
                    better_moves.add((-self.tabla[piece[0] - 1][piece[1] - 1].material, ((lepes[0]), (lepes[1]))))
        """free material"""
        for lepes in all_possible_moves:
            if self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color == (not oldal) and not is_defended(maintabla, lepes[1])[0]:
                better_moves.add(((self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].material), (lepes[0], lepes[1])))
        """tactical 1 : istant capture"""
        for lepes in all_possible_moves:
            if self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color == (not oldal) and self.tabla[lepes[0][0] - 1][lepes[0][1] - 1].material < self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].material:
                better_moves.add(((self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].material - self.tabla[lepes[0][0] - 1][lepes[0][1] - 1].material), (lepes[0], lepes[1])))
        for lepes in all_possible_moves:
            if self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].color == (not oldal) and self.tabla[lepes[0][0] - 1][lepes[0][1] - 1].material == self.tabla[lepes[1][0] - 1][lepes[1][1] - 1].material:
                randomint_1 = random.randint(30,55)/100
                better_moves.add(((randomint_1),(lepes[0],lepes[1])))
        """progress"""
        if float(turn) > 15 :
            for lepes in all_possible_moves:
                if type(self.tabla[lepes[0][0] - 1][lepes[0][1] - 1]) == Pawn :
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
    all_possible_moves = set()
    for n in active_pieces(table, oldal):
        for m in possible_moves(table,(n)):
            all_possible_moves.add((n,m))
    '''mate in 0'''
    for lepes in all_possible_moves:
        if type(table.tabla[lepes[1][0]-1][lepes[1][1]-1]) == King and table.tabla[lepes[1][0]-1][lepes[1][1]-1].color != oldal:
            return [(lepes[0]),(lepes[1])]
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
    if float(turn) < 2  :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 if oldal else  lepes[1][0]== 5  ):
                randomint = random.randint(23, 50)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 5 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 35)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 10 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 or lepes[0][1]== 2 or lepes[0][1]== 7) and (lepes[1][0]== 3 or lepes[1][0]== 6  ):
                randomint = random.randint(15, 25)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 4 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 40)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 10 and float(turn) >= 2 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn and (lepes[0][1]== 3 or lepes[0][1]== 4 or lepes[0][1]== 5 ) and (lepes[1][0]== 4 or lepes[1][0]== 5  ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 10 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 4 or lepes[1][0]== 5 ) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(27, 43)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 10 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Bishop and (lepes[0][1]== 3 or lepes[0][1]== 6) and (lepes[1][0]== 3 or lepes[1][0]== 6 or lepes[1][0]== 2 or lepes[1][0]== 7) and (lepes[0][0]== 1 or lepes[0][0]== 8 ):
                randomint = random.randint(20, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 5 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  )  and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(29, 46)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if float(turn) < 15 and float(turn) >=5 :
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Knight and (lepes[1][1]== 3 or lepes[1][1]== 6 ) and (lepes[1][0]== 3 or lepes[1][0]== 6  ) and (lepes[0][0]== 1 or lepes[0][0]== 8):
                randomint = random.randint(25, 30)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    if all_material(table, oldal) < 12:
        for lepes in all_possible_moves:
            if type(table.tabla[lepes[0][0]-1][lepes[0][1]-1]) == Pawn :
                randomint = random.randint(45, 65)/100
                better_moves.add(((randomint),((lepes[0]),(lepes[1]))))
    """sánc"""        
    for m in active_pieces(table, oldal):       
        if type(table.tabla[m[0]-1][m[1]-1]) == King :           
            for n in possible_moves(table,(m)):                   
                    if m[1]-4 == n[1] :                            
                            better_moves.add((0.75, ( m , n )))
                    if m[1]+3 == n[1] :
                            better_moves.add((0.75, ( m , n )))
    """anti_blunder 1 move """
    for lepes in all_possible_moves:
        calc_tabla = copy.deepcopy(table)
        move_sakknak(calc_tabla,lepes[0],lepes[1])
        if type(table.tabla[lepes[1][0]-1][lepes[1][1]-1]) == Empty and not (is_defended(calc_tabla, lepes[1])[0]) and can_be_taken(calc_tabla, lepes[1])[0]:
            better_moves.add( (-table.tabla[lepes[0][0]-1][lepes[0][1]-1].material, ((lepes[0]),(lepes[1]))))
        for piece in all_pieces(calc_tabla,oldal):
            if not (is_defended(calc_tabla, piece)[0]) and can_be_taken(calc_tabla, piece)[0] and type(table.tabla[piece[0]-1][piece[1]-1]) != Empty:
                better_moves.add((-table.tabla[piece[0]-1][piece[1]-1].material, ((lepes[0]),(lepes[1]))))
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


side = bool()

side = True




    

while True:
    '''robots turn'''
    turn += 0.5 
    if sakkmatt(maintabla,  side):
        
        print("Fekete nyert")
        exit("sakk matt")
    if patt(maintabla):
        print("patt")
        exit("döntetlen")
    if sakk(maintabla, side):
        print("robot sakk")
    temporary_order =  tuple(best_move(maintabla, side))
    move_stall(maintabla,temporary_order[0],temporary_order[1] )
    visual(maintabla, side)
    """stop =input("")
    if stop == ("exit"):
        exit"""



    print (moves)
    
    turn += 0.5 
    if sakkmatt(maintabla, not side):       
        print("Fehér nyert")
        exit("sakk matt")
    if patt(maintabla):
        print("patt")
        exit("döntetlen")
    if sakk(maintabla, not side):
        print("robot sakk")
    print (stall)
    temporary_order =  tuple(best_move(maintabla,  not side))
    move_stall(maintabla,temporary_order[0],temporary_order[1] )
    
    visual(maintabla, side)
    print("")
    """stop = input("")
    if stop == ("exit"):
        exit"""
    