import os
import random
import time
import keyboard

width = 10
height = 20

figures = {
    "I": [["O", "O", "O", "O"]],
    "O": [["O", "O"], ["O", "O"]],
    "T": [[" ", "O", " "], ["O", "O", "O"]],
    "Z": [["O", "O", " "], [" ", "O", "O"]],
    "revZ": [[" ", "O", "O"], ["O", "O", " "]],
    "J": [["O", " ", " "], ["O", "O", "O"]],
    "revJ": [[" ", " ", "O"], ["O", "O", "O"]],
}

def create_empty_board(): #создать пустое поле
    empty_board = []
    for _ in range(height):
        empty_board.append([" " for _ in range(width)])  # Используем список символов
    return empty_board

def display_board(board): #вывод поля
    os.system("cls")  #очистка экрана
    print("#" + "-" * width + "#")
    for row in board:
        print("|" + "".join(row) + "|") #вывод строк
    print("#" + "-" * width + "#") 

def create_figure(board, figure, x, y): #спавн фигур
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == "O":
                board[y + i][x + j] = "O"

def can_place(board, figure, x, y):
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == "O":
                if y + i >= height or x + j < 0 or x + j >= width or board[y + i][x + j] == "O":
                    return False
    return True

def physics(board, figure, x, y, dx, dy): #физика падения фигур
    if can_place(board, figure, x + dx, y + dy):
        return x + dx, y + dy
    return x, y

def can_place(board, figure, x, y):
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == "O":
                if y + i >= height or x + j < 0 or x + j >= width or board[y + i][x + j] == "O":
                    return False
    return True

def rotate_figure(figure):
    reversed_figure = figure[::-1] #Перевернуть строки фигуры вверх ногами
    rotated = zip(*reversed_figure) #Преобразовать строки в столбцы
    rotated_figure = [list(row) for row in rotated] #Преобразовать кортежи в списки
    return rotated_figure

def adjust_position(board, shape, x, y):
    max_width = len(shape[0])
    max_height = len(shape)
    # Корректировка горизонтальное положение
    if x < 0:
        x = 0
    elif x + max_width > width:
        x = width - max_width
    # Корректировка вертикальное положение
    if y + max_height > height:
        y = height - max_height

    return x, y

def clear_line(board):
    cleared = 0
    new_board = []
    for row in board:
        if " " in row:
            new_board.append(row)
        else:
            cleared += 1
    for _ in range(cleared):
        new_board.insert(0, [" " for _ in range(width)])
    return new_board, cleared

def game():
    board = create_empty_board()
    current_figure = random.choice(list(figures.values()))
    x = 3 #начальная позиция фигуры
    y = 0  #начальная позиция фигуры
    score = 0
    while True:
        temp_board = [row[:] for row in board]
        create_figure(temp_board, current_figure, x, y)
        display_board(temp_board)
        print(f"Score: {score}")

        if keyboard.is_pressed("left"):
            x, y = physics(board, current_figure, x, y, -1, 0)
        if keyboard.is_pressed("right"):
            x, y = physics(board, current_figure, x, y, 1, 0)
        if keyboard.is_pressed("down"):
            x, y = physics(board, current_figure, x, y, 0, 1)
        if keyboard.is_pressed("up"):
            rotated_figure = rotate_figure(current_figure)
            adjusted_x, adjusted_y = adjust_position(board, rotated_figure, x, y)
            if can_place(board, rotated_figure, adjusted_x, adjusted_y):
                current_figure = rotated_figure
                x = adjusted_x
                y = adjusted_y
        time.sleep(0.5)
        if not can_place(board, current_figure, x, y + 1):
            create_figure(board, current_figure, x, y)
            board, lines_cleared = clear_line(board)
            score += lines_cleared * 100
            current_figure = random.choice(list(figures.values()))
            x = 3
            y = 0
            if not can_place(board, current_figure, x, y):
                print(f"Score: {score}")
                break
        else:
            y += 1

        

if __name__ == "__main__":
    game()
