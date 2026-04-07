import random
import os
import time

class Board:

    def __init__(self,size):
        self.win_size = 5
        self.size = size
        self.rows = [[" "] * size  for _ in range(size)]

    def display(self,highlight_coords=None):
        if highlight_coords is None:
            highlight_coords = []


        RED = "\033[91m"
        BLUE = "\033[94m"
        WIN_COLOR = "\033[38;5;118m"
        RESET = "\033[0m"


        # f"{x:4}" — Rezervuje 4 místa, zarovná doprava
        #  f"{x:<4}" — Rezervuje 4 místa, zarovná doleva.
        # f"{x:^4}" — Rezervuje 4 místa, zarovná na střed.

        print("    ", end="")
        for x in range(1,self.size+1):
            print(f"{x:^4}",end="")
        print()

        for i, line in  enumerate(self.rows):
            print(f"{i+1:2} ",end="")

            for  c ,place in enumerate(line):
                color = RESET

                if (i,c) in highlight_coords:
                    color = WIN_COLOR
                elif place == "X":
                    color = RED
                elif place == "O":
                    color = BLUE

                print(f"| {color}{place}{RESET} ", end="")
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

    def check_line(self, line, coords):
        """Vrací (vítězný_symbol, seznam_souřadnic) nebo (None, [])"""
        if len(line)<self.win_size:
            return None, []

        for i in range(len(line)-self.win_size + 1):
            window = line[i : i + self.win_size]
            if window[0] != " " and all(cell == window[0] for cell in window):
                return window[0], coords[i : i + self.win_size]
        return None, []

    def checking_winning(self):

        # 1. Kontrola řádků (dynamicky pro jakoukoli délku)
        for r, row in enumerate(self.rows):
            line_coords = [(r,c) for c in range(self.size)]
            res, win_coords = self.check_line(row, line_coords)
            if res: return res, win_coords

        # 2. Kontrola sloupců (vytvoříme si seznam pro každý sloupec)
        for c in range(self.size):
            col = [self.rows[r][c] for r in range(self.size)]
            line_coords =  [(r,c) for r in range(self.size)]
            res, win_coords = self.check_line(col, line_coords)
            if res: return res, win_coords


        # 3. Hlavní diagonála (sestupná \)
        for r in range(self.size - self.win_size + 1):
            for c in range(self.size - self.win_size + 1):
                diag = [self.rows[r+i][c+i] for i in range(self.win_size)]
                win_coords = [(r+i,c+i) for i in range(self.win_size)]
                if diag[0] != " " and all(cell == diag[0] for cell in diag):
                    return diag[0], win_coords

        # 4. Vedlejší diagonála (sestupné /)
        for r in range(self.size - self.win_size + 1):
            for c in range(self.win_size  -1, self.size):
                diag = [self.rows[r+i][c-i] for i in range(self.win_size)]
                win_coords = [(r+i, c-i) for i in range(self.win_size)]
                if diag[0] != " " and all(cell == diag[0] for cell in diag):
                    return diag[0], win_coords


        # 5. Remíza (pokud na desce nezbyla žádná mezera)
        if all(cell != " " for row in self.rows for cell in row):
            return "Remíza", []

        return None,[]


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
            souradnice_x =input(f"Zadej číslo 1-{board.size:}:")
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
                    if board.checking_winning()[0] == self.symbol:
                        board.rows[r][c] = " "
                        return r, c
                    board.rows[r][c] = " "

        # 2. potřeba zabránit soupeři dokončit 5 symbolů:
        for r in range(board.size):
            for c in range(board.size):
                if board.rows[r][c] == " ":
                    board.rows[r][c] = opponent
                    if board.checking_winning()[0] == opponent:
                        board.rows[r][c] = " "
                        return r, c
                    board.rows[r][c] = " "

        #3.preventivní blok
        original_win_size = board.win_size
        board.win_size = 4

        # A) Zkusím nejdřív vytvořit VLASTNÍ 4 v řadě (Útok)
        for r in range(board.size):
            for c in range(board.size):
                if board.rows[r][c] == " ":
                    board.rows[r][c] = self.symbol
                    if board.checking_winning()[0] == self.symbol:
                        board.rows[r][c] = " "
                        board.win_size = original_win_size
                        return r, c
                    board.rows[r][c] = " "

        # B) Pokud nemůžu útočit, zablokuju TVOJI trojku (Obrana)
        for r in range(board.size):
            for c in range(board.size):
                if board.rows[r][c] == " ":
                    board.rows[r][c] = opponent
                    if board.checking_winning()[0] == opponent:
                        board.rows[r][c] = " "
                        board.win_size = original_win_size
                        return r, c
                    board.rows[r][c] = " "

        board.win_size = original_win_size

        # 4. Pokud nic, beru střed (pokud je volný)
        stred = board.size // 2
        if board.rows[stred][stred] == " ":
            return stred, stred

        # 5. Jinak náhodný tah z volných polí
        empty = [(r, c) for r in range(board.size) for c in range(board.size) if board.rows[r][c] == " "]
        return random.choice(empty)

class GameManager:

    def __init__(self,player1,player2):
        self.board = None
        self.player1 = player1
        self.player2 = player2
        self.state = [self.player1,self.player2]
        self.current_index = 0
        self.scores = {player1.name:0, player2.name:0, "Remízy":0}

    def setup_game(self):
            os.system("cls" if os.name == "nt" else "clear")
            print(" MENU HRY")
            # volba ḧráče:
            option = ""
            print("\nVyber si herní režim:")
            print("1) Boj proti Dracovy (AI)")
            print("2) Boj dvou AI proti sobě")
            print("3) Boj dvou hráčů")
            print("4) Ukončit aplikaci")
            #volba režimu případně ukončení aplikace
            while option not in ["1","2","3","4"]:
                option = input("Tvoje volba (1/2/3/4): ")

            if option == "1":
                name1 = input("Zadej jméno hráče: ")
                player1_symbol = input("Vyber si zda chceš hrát za X nebo O: (X/O) ").upper()
                self.player1 = HumanPlayer(name1,player1_symbol)
                player2_symbol = "O" if player1_symbol == "X" else "X"
                self.player2 = AIPlayer("Draco",player2_symbol)

            elif option == "2":
                self.player1 = AIPlayer("Harry","X")
                self.player2 = AIPlayer("Draco","O")

            elif option == "3":
                name1 = input("Zadej jméno prvního hráče: ")
                player_symbol = input("Vyber si zda chceš hrát za X nebo O: (X/O) ").upper()
                self.player1 = HumanPlayer(name1, player_symbol)
                name2 = input("Zadej jméno druhého hráče: ")
                player2_symbol = "O" if player_symbol == "X" else "X"
                self.player2 = HumanPlayer(name2,player2_symbol)

            elif option == "4":
                print("Neplecha ukončena!")
                input()
                exit()


            #nastavení desky
            size = int(input("Jak velkou herní desku chceš? (např. 10):  "))
            if size >= 5:  # Udělejme raději >= 5
                self.board = Board(size)  # Tady vytvoříš opravdovou desku
            else:
                print("Příliš malé bojiště, nastavuji 5x5.")
                self.board = Board(5)

            for p in [self.player1, self.player2]:
                if p.name not in self.scores:
                    self.scores[p.name] = 0

            self.state = [self.player1, self.player2]

    def main_loop(self,):
        while True:
            self.setup_game()
            self.current_index = 0
            game_over = False

            while not game_over:
                os.system("cls" if os.name == "nt" else "clear")

                #Zobrazení score
                print(f"SKÓRE: {self.player1.name}: {self.scores[self.player1.name]} | "
                      f"{self.player2.name}: {self.scores[self.player2.name]} | ")
                print("-"* (self.board.size *4+5))

                self.board.display()


                current_player = self.state[self.current_index]
                print(f"Hraje {current_player.name} se symbolem {current_player.symbol}")

                x,y = current_player.get_move(self.board)

                if self.board.make_move(x,y, current_player.symbol):
                    # KONTROLA VÝHRY HNED PO TAHU
                    winner_symbol, win_coords = self.board.checking_winning()
                    if winner_symbol:
                        os.system("cls" if os.name == "nt" else "clear")
                        #zvýrazníme vítězná políčka
                        self.board.display(win_coords)
                        if winner_symbol == "Remíza":
                            print("Je to remíza!")
                        else:
                            winner = self.player1 if self.player1.symbol == winner_symbol else self.player2
                            print(f"Vítěz je {winner.name} se symbolem {winner.symbol}")
                            self.scores[winner.name] += 1
                        game_over = True
                    else:
                        #přepnutí hrácě pokud nikdo nevyhrál
                        self.current_index = (self.current_index + 1) % 2

                else:
                    print("Tohle pole už je obsazené! Zkus to znova.")
                    time.sleep(1)
            # dotaz na další kolo
            again = input("\nChcete hrát další hru? (a/n): ").lower()
            if again != "a":
                print("Díky za hru! Celkové skóré:")
                print(self.scores)
                break





me = AIPlayer("Harry","X")
me2 =AIPlayer("Draco","O")

hra = GameManager(me,me2)
hra.main_loop()