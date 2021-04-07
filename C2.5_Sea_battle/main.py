from random import randint


class Error(Exception):
    pass


class BoardOutException(Error):
    def __str__(self):
        return "Shot outside board!"


class UsedCellException(Error):
    def __str__(self):
        return "This cell already shot!"


class WrongValueException(Error):
    def __str__(self):
        return "Invalid coordinates specified!"


class CannotPlaceShip(Error):
    def __str__(self):
        return "No suitable space for ship!"


class ShipNotCreated(Error):
    def __str__(self):
        return "Error while creating ship!"


class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x, self.y == other.y


class Ship:

    def __init__(self, head, direction, length):
        self.head = head
        self.direction = direction
        self.length = length
        self.hp = length

    @property
    def dots(self):
        ship_cells = []
        for i in range(self.length):
            new_x, new_y = self.head.x, self.head.y
            if self.direction == 1 and self.length != 1:
                new_x += 1
            elif self.direction == 2 and self.length != 1:
                new_y += 1
            ship_cells.append(Dot(new_x, new_y))
        return ship_cells

    def hit(self, hit):
        return hit in self.dots


class Board:

    def __init__(self, hid=False, alive=0, size=6):
        self.hid = hid
        self.alive = alive
        self.size = size
        self.board = [[' ', '1', '2', '3', '4', '5', '6'],
                      ['1', '.', '.', '.', '.', '.', '.'],
                      ['2', '.', '.', '.', '.', '.', '.'],
                      ['3', '.', '.', '.', '.', '.', '.'],
                      ['4', '.', '.', '.', '.', '.', '.'],
                      ['5', '.', '.', '.', '.', '.', '.'],
                      ['6', '.', '.', '.', '.', '.', '.']]
        self.used = []
        self.ships = []
        self.contours = []

    def outside(self, i):
        return False if ((0 < i.x <= 6) and (0 < i.y <= 6)) else True

    def contour(self, ship, cnt=False):
        contour_ = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (0, 0), (1, 0),
                    (1, 1), (0, 1), (1, 1)]
        for i in ship.dots:
            for a, b in contour_:
                c = Dot(i.x + a, i.y + b)
                self.contours.append(c)
                if not (self.outside(i)) and c not in self.used:
                    if cnt:
                        self.board[c.x][c.y] = '0'
                    self.used.append(c)

    def add_ship(self, ship):
        for i in ship.dots:
            if self.outside(i) or i in self.contours or i in self.ships:
                raise CannotPlaceShip()
        for i in ship.dots:
            self.board[i.x][i.y] = "■"
            self.ships.append(ship)
            self.contour(ship)
            self.used.append(i)
            self.alive += 1
        return self.ships, self.used, self.alive, self.board

    def show(self):
        for i in range(1):
            for j in range(7):
                if self.hid:
                    for [a], [b] in self.board:
                        if self.board[a][b] == "■" or "0":
                            self.board[a][b] = "."
                        print(f"{''}" + "|".join(self.board[j]) + "|")
                print(f"{''}" + "|".join(self.board[j]) + "|")

    def shot(self, s):
        if self.outside(s):
            raise BoardOutException()
        if s in self.used:
            raise UsedCellException()
        for ship in self.ships:
            if s in ship.dots():
                self.board[s.x][s.y] == "X"
                ship.hp -= 1
                if ship.hp == 0:
                    self.alive -= 1
                    self.contour(ship, cnt=True)
                    print("Ship destroyed!")
                else:
                    print("Ship damaged!")
                return True
            else:
                self.board[s.x][s.y] == "0"
                print("Shot missed!")
                return False
        self.used.append([s.x][s.y])


class Player:

    def __init__(self, user_board, ai_board):
        self.user_board = user_board
        self.ai_board = ai_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                s = self.ask()
                repeat = self.ai_board.shot(s)
                return repeat

            except Error as e:
                print(e)


class AI(Player):

    def ask(self):
        s = (Dot(randint(1, 6), (randint(1, 6))))
        print(f"AI shoots to{s.x}, {s.y}")
        return s


class User(Player):

    def ask(self):
        while True:
            s = input("Specify x and y: ").split()
            if len(s) != 2:
                raise WrongValueException()
            x, y = s
            if not (x.isdigit()) or not (y.isdigit()):
                raise WrongValueException()
            x, y = int(x), int(y)
            return Dot(x, y)


class Game:

    def __init__(self, size=6):
        self.size = size
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True
        self.ai = AI(ai_board, user_board)
        self.user = User(user_board, ai_board)

    def create_ships(self):
        ships = (3, 2, 2, 1, 1, 1, 1)
        board = Board(size=self.size)
        a = 0
        for i in ships:
            while True:
                a += 1
                if a > 2000:
                    return None
                ship = Ship(Dot(randint(1, 6), randint(1, 6)), randint(1, 2), i)
                try:
                    board.add_ship(ship)
                    break
                except CannotPlaceShip:
                    print(f"Trying to create ship with length {i} one more time")
                return board

    def random_board(self):
        board = None
        while board is None:
            board = self.create_ships()
        return board

    @staticmethod
    def greet():
        print("Sea battle")
        print("Specify x and y to shoot")

    def loop(self):
        turns = 0
        while True:
            print("User")
            self.user.user_board.show()
            print()
            print("#" * 30)
            print()
            print("AI")
            self.ai.ai_board.show()
            if turns % 2 == 0:
                print("Specify your shot")
                repeat = self.user.move()
            else:
                print("AI' s turn")
                repeat = self.ai.move()
            if self.user.user_board.alive == 0:
                print("AI wins!")
                break
            if self.ai.ai_board.alive == 0:
                print("You win!")
                break
            turns += 1 if not repeat else turns

    def start(self):
        self.greet()
        self.loop()


game = Game()
print(Board.user_board.add_ship())
game.start()
