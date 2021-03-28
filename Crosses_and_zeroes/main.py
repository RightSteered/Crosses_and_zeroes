R = C = 4
nums = (1, 2, 3)
turns = 1  # Счётчик ходов и переключатель игрока
game = True  #
array = [
    [" ", 1, 2, 3],
    [1, " ", " ", " "],
    [2, " ", " ", " "],
    [3, " ", " ", " "]
]


def action():
    global turns
    global nums
    symbol = ("X" if turns % 2 != 0 else "0")
    row, col = int(input("Введите ряд ")), None
    if row in nums:
        col = int(input("Введите столбец "))
        if col not in nums:
            print("Столбец вне игрового поля")
            action()
    else:
        print("Ряд вне игрового поля")
        action()

    if array[row][col] != " ":  # Проверка заполнения ячейки
        print("Эта ячейка уже заполнена")
        action()
    else:
        array[row][col] = symbol  #
    turns += 1


def condition():  # Проверка выигрышных комбинаций
    global game
    global nums
    for i in array:
        if i[1] == i[2] == i[3] != " ":  # Проверка строк
            game = not game
    for j in nums:
        if array[1][j] == array[2][j] == array[3][j] != " ":  # Проверка столбцов
            game = not game
    if (array[1][1] == array[2][2] == array[3][3] != " ")\
            or (array[3][1] == array[2][2] == array[1][3] != " "):
        # Проверка диагоналей
        game = not game


def play():
    global turns
    condition()
    if game:
        action()
        for a in range(R):
            for b in range(C):
                print(array[a][b], end=' ')
            print()
        play()
    else:
        player = ('"X"' if turns % 2 == 0 else '"0"')
        print(f"Игра окончена за {turns - 1} ходов. Побеждает игрок {player}.")


play()
