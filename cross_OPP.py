import random
import os
import time
from operator import index
from turtledemo.clock import setup


class Board:

    def __init__(self,size,win_size):
        self.win_size = win_size
        self.size = size
        self.rows = [[" "] * size  for _ in range(size)]

    def display(self):
        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"
        print("    ", end="")

        # f"{x:4}" — Rezervuje 4 místa, zarovná doprava
        #  f"{x:<4}" — Rezervuje 4 místa, zarovná doleva.
        # f"{x:^4}" — Rezervuje 4 místa, zarovná na střed.
        for x in range(1,self.size+1):
            print(f"{x:^4}",end="")
        print()
        for i, line in  enumerate(self.rows):
            print(f"{i+1:2} ",end="")

            for place in line:
                if place == "X":
                    print(f"| {RED}{place}{RESET} ", end="")
                elif place == "O":
                    print(f"| {BLUE}{place}{RESET} ", end="")
                else:

                    print(f"| {place} ", end="")

            print("|")
            print("    " + "-" * (self.size * 4 + 1))

    def make_move(self,souradnice_x,souradnice_y, symbol):
        try:
            if self.rows[souradnice_x][souradnice_y] == " ":
                self.rows[souradnice_x][souradnice_y] = symbol
                return True
            return False
        except IndexError:
            return False

    def check_line(self, line):
        """Pomocná metoda: zkontroluje, zda je v seznamu win_size stejných symbolů za sebou."""
        if len(line)<self.win_size:
            return None

        for i in range(len(line)-self.win_size+1):
            window = line [i : i + self.win_size]
            if window [0] != " " and all(cell == window[0] for cell in window):
                return window[0]
        return None

    def checking_winning(self):

        # 1. Kontrola řádků (dynamicky pro jakoukoli délku)
        for row in self.rows:
            res = self.check_line(row)
            if res: return res

        # 2. Kontrola sloupců (vytvoříme si seznam pro každý sloupec)
        for c in range(self.size):
            col = [self.rows[r][c] for r in range(self.size)]
            res = self.check_line(col)
            if res: return res


        # 3. Hlavní diagonála (sestupná \)
        for r in range(self.size - self.win_size + 1):
            for c in range(self.size - self.win_size + 1):
                diag = [self.rows[r+i][c+i] for i in range(self.win_size)]
                if diag[0] != " " and all(cell == diag[0] for cell in diag):
                    return diag[0]

        # 4. Vedlejší diagonála (sestupné /)
        for r in range(self.size - self.win_size + 1):
            for c in range(self.win_size  -1, self.size):
                diag = [self.rows[r+i][c-i] for i in range(self.win_size)]
                if diag[0] != " " and all(cell == diag[0] for cell in diag):
                    return diag[0]


        # 5. Remíza (pokud na desce nezbyla žádná mezera)
        if all(cell != " " for row in self.rows for cell in row):
            return "Remíza"

        return None


class Player:

    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self,board):
        pass

class HumanPlayer(Player):

    def __init__(self,name,symbol):
        super().__init__(name,symbol)


    def get_move(self, board):

        while True:
            souradnice_x =input(f"Zadej číslo 1-{board.size:}")
            souradnice_y = input(f"Zadej číslo 1-{board.size}:")
            try:
                souradnice_x = int(souradnice_x)
                souradnice_y = int(souradnice_y)
                if 0<souradnice_x <= board.size and 0<souradnice_y <= board.size:
                    return souradnice_x-1,souradnice_y-1
                else:
                    print(f"Zadej jsi špatně číslo. Zkus to znova.")
            except ValueError:
                print(f"Zadej číslo 1-{board.size}:")

class AIPlayer(Player):
    def get_move(self, board):
        print(f"{self.name} usilovně přemýšlí...")
        time.sleep(1.5)
        opponent = "O" if self.symbol == "X" else "X"

        # 1. Šance na okamžitou výhru
        for r in range(board.size):
            for c in range(board.size):
                if board.rows[r][c] == " ":
                    board.rows[r][c] = self.symbol
                    if board.checking_winning() == self.symbol:
                        board.rows[r][c] = " "
                        return r, c
                    board.rows[r][c] = " "

        # 2. Musím blokovat soupeře?
        for r in range(board.size):
            for c in range(board.size):
                if board.rows[r][c] == " ":
                    board.rows[r][c] = opponent
                    if board.checking_winning() == opponent:
                        board.rows[r][c] = " "
                        return r, c
                    board.rows[r][c] = " "

        # 3. Pokud nic, beru střed (pokud je volný)
        stred = board.size // 2
        if board.rows[stred][stred] == " ":
            return stred, stred

        # 4. Jinak náhodný tah z volných polí
        volna = [(r, c) for r in range(board.size) for c in range(board.size) if board.rows[r][c] == " "]
        return random.choice(volna)

class GameManager:

    def __init__(self,player1,player2):
        self.board = Board
        self.player1 = player1
        self.player2 = player2
        self.state = [self.player1,self.player2]
        self.current_index = 0

    def setup_game(self):

            print(" NASTAVENÍ HRY")
            size = int(input("Jak velkou herní desku chceš? (např. 10):  "))
            win_size = int(input(f"Kolik symbolů v řadě vyhrává? (max {size}):  "))
            self.board = Board(size,win_size)


    def main_loop(self,):
        self.setup_game()
        print("Vítej ve hře, pro začátek zmáčkni Enter")
        input()

        while True:
            os.system("cls" if os.name =="nt" else "clear")
            current_player = self.state[self.current_index]
            print()
            print()
            self.board.display()
            print(f"Hraje {current_player.name} se symbolem {current_player.symbol}")
            x,y =current_player.get_move(self.board)
            uspech = self.board.make_move(x, y, current_player.symbol)
            if not uspech:
                print("Pole je obsazeno.")
                continue

            self.board.display()
            end_game = self.board.checking_winning()
            if end_game:
                if end_game == "Remíza":
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Je to remíza")
                    self.board.display()
                    input()
                else:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(f"Vítěz je {current_player.name}")
                    self.board.display()
                    input()


                break
            self.current_index = (self.current_index + 1)  %2





me = AIPlayer("Harry","X")
me2 =AIPlayer("Draco","O")

hra = GameManager(me,me2)
hra.main_loop()