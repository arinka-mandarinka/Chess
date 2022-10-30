import enum
import logging

# Названия фигур.
class TypesFigures(enum.Enum):
    pawn = 0
    knight = 1
    bishop = 2
    rook = 3
    queen = 4

# Класс клетки со своими номерами вертикали и горизонтали.
class Square:
    def __init__(self, vertical : int, horizontal : int):
        self.vertical = vertical
        self.horizontal = horizontal

    # Вывод в стандартном виде для шахматной доски.
    def __str__(self):
        return chr(self.vertical - 1 + ord('A')) + str(self.horizontal)

# Класс фигуры с объектом клетки и объектом наименования фигуры.
class Figure:
    def __init__(self, square : Square, name : TypesFigures = TypesFigures.pawn):
        self.square = square
        self.name = name

# Ввод имени фигуры.
def input_name():
    min = 1
    max = 4
    invalid_input_err = 'Неверный ввод, нужно ввести число'
    out_of_range_err = f'Выберите фигуру из доступных'

    print('Выберите название для первой фигуры из представленных ниже:\n' +
          '1 - Конь\n' +
          '2 - Слон\n' +
          '3 - Ладья\n' +
          '4 - Ферзь')
    while True:
        try:
            num = int(input('- '))
            logging.info(f'Было введено: {num}')
        except:
            print('Ошибка: ' + invalid_input_err + '!')
            logging.error(invalid_input_err, exc_info=True)
            continue
        if num < min or num > max:
            print('Ошибка: ' + out_of_range_err + '!')
            logging.error(out_of_range_err)
            continue
        # Ищем в TypesFigures название фигуры с тем же value, 
        # что ввел пользователь и возвращаем.
        for name in TypesFigures:
            if name.value == num:
                logging.info(f'Была выбрана фигура: {name}')
                return name

# Ввод клетки со своими координатами.
def input_square(previous_square : Square = None):
    min = 1
    max = 8
    number_figure = 'первой' if previous_square == None else 'второй'
    text_for_input = f'Введите через пробел две цифры - номер вертикали и горизонтали для {number_figure} фигуры'
    invalid_input_err = 'Неверный ввод, нужно ввести два числа'
    out_of_range_v_err = f'Номер вертикали должен входить в промежуток [{min}, {max}]'
    out_of_range_h_err = f'Номер горизонтали должен входить в промежуток [{min}, {max}]'
    same_coordinates_err = 'Координаты клеток фигур должны быть разными'

    while True:
        try:
            text = input(text_for_input + ': ')
            logging.info(f'Было введено: {text}')
            nums = text.split()
            
            if len(nums) != 2:
                raise Exception

            vertical = int(nums[0])
            horizontal = int(nums[1])
        except:
            print('Ошибка: ' + invalid_input_err + '!')
            logging.error(invalid_input_err, exc_info=True)
            continue

        repeat = False
        if vertical < min or vertical > max:
            print('Ошибка: ' + out_of_range_v_err + '! Попробуйте ещё раз...')
            logging.error(out_of_range_v_err)
            repeat = True
        if horizontal < min or horizontal > max:
            print('Ошибка: ' + out_of_range_h_err + '! Попробуйте ещё раз...')
            logging.error(out_of_range_h_err)
            repeat = True
        
        if repeat:
            continue
        
        if previous_square != None:
            if vertical == previous_square.vertical and \
                horizontal == previous_square.horizontal:
                print('Ошибка: ' + same_coordinates_err + '! Попробуйте ещё раз...')
                logging.error(same_coordinates_err)
                continue
        
        logging.info(f'Была выбрана вертикаль {vertical} и горизонталь {horizontal}')
        return Square(vertical, horizontal)

# Возвращает булево значение на равенство цветов клеток у двух фигур.
def get_equality_color_square(figure1 : Figure, figure2 : Figure):
    return (figure1.square.vertical + figure1.square.horizontal) % 2 == \
            (figure2.square.vertical + figure2.square.horizontal) % 2

# Возвращает булево значение на возможность сруба за один ход.
def get_kill_one_move(figure1 : Figure, figure2 : Figure):
    name1 = figure1.name
    vertical1 = figure1.square.vertical
    horizontal1 = figure1.square.horizontal
    vertical2 = figure2.square.vertical
    horizontal2 = figure2.square.horizontal

    # Проверка для каждой фигуры.
    if name1 == TypesFigures.knight:
        return abs(vertical1 - vertical2) == 1 and abs(horizontal1 - horizontal2) == 2 or \
                abs(vertical1 - vertical2) == 2 and abs(horizontal1 - horizontal2) == 1
    elif name1 == TypesFigures.bishop:
        return abs(vertical1 - vertical2) == abs(horizontal1 - horizontal2)
    elif name1 == TypesFigures.rook:
        return vertical1 == vertical2 or horizontal1 == horizontal2
    elif name1 == TypesFigures.queen:
        return vertical1 == vertical2 or horizontal1 == horizontal2 or \
                abs(vertical1 - vertical2) == abs(horizontal1 - horizontal2)

# Возвращает промежуточные координаты клетки для сруба 
# за два хода, если такая имеется, иначе возвращает None.
def get_kill_two_move(figure1: Figure, figure2: Figure):
    name = figure1.name
    vertical1 = figure1.square.vertical
    horizontal1 = figure1.square.horizontal
    horizontal2 = figure2.square.horizontal

    # Проверка для каждой фигуры.
    if name == TypesFigures.knight:
        moves = [(1, 2), (2, 1), (-1, 2), (2, -1),
                    (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        # Проверяем все возможные ходы для коня.
        for move in moves:
            square = Square(vertical1 + move[0], horizontal1 + move[1])

            # Если не выходит за грани шахматной доски 
            # и если угрожает => возвращаем клетку.
            if  square.vertical >= 1 and square.vertical <= 8 and \
                square.horizontal >= 1 and square.horizontal <= 8 and \
                get_kill_one_move(Figure(square, name), figure2):
                    return square
    elif name == TypesFigures.bishop:
        # Проверяем все возможные ходы для коня и если находим
        # угрозу => возвращаем клетку.
        square = Square(vertical1, horizontal1)
        while square.vertical < 8 and square.horizontal < 8:
            square.vertical += 1
            square.horizontal += 1
            if get_kill_one_move(Figure(square, name), figure2):
                return square
        square = Square(vertical1, horizontal1)
        while square.vertical < 8 and square.horizontal > 1:
            square.vertical += 1
            square.horizontal -= 1
            if get_kill_one_move(Figure(square, name), figure2):
                return square
        square = Square(vertical1, horizontal1)
        while square.vertical > 1 and square.horizontal < 8:
            square.vertical -= 1
            square.horizontal += 1
            if get_kill_one_move(Figure(square, name), figure2):
                return square
        square = Square(vertical1, horizontal1)
        while square.vertical > 1 and square.horizontal > 1:
            square.vertical -= 1
            square.horizontal -= 1
            if get_kill_one_move(Figure(square, name), figure2):
                return square
    elif name == TypesFigures.rook:
        return Square(vertical1, horizontal2)
    elif name == TypesFigures.queen:
        return Square(vertical1, horizontal2)

    # Если ничего не произошло до этого момента, то 
    # клетка не найдена => возвращаем None.
    return None

logging.basicConfig(level=logging.INFO, filename="logfile.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
# Ввод названия фигуры.
name = input_name()
# Ввод координат клетки для первой фигуры.
square = input_square()
# Построение первой фигуры.
figure1 = Figure(square, name)

# Ввод координат клетки для второй фигуры.
square = input_square(square)
# Построение второй фигуры.
figure2 = Figure(square)

# Проверяем равенство цветов двух клеток.
word = 'одинаковыми' if get_equality_color_square(figure1, figure2) else 'разными'
# Выводим полученный результат.
print(f'а) Цвета клеток двух фигур являются {word}.')
logging.info(f'а) Цвета клеток двух фигур являются {word}.')

# Проверяем возможность сруба за один ход.
if get_kill_one_move(figure1, figure2):
    print('б) Первая фигура угрожает второй.')
    print('в) Первая фигура может срубить вторую за один ход.')
    logging.info('б) Первая фигура угрожает второй.')
    logging.info('в) Первая фигура может срубить вторую за один ход.')
# Если сруб невозможен, то ищем возможность сруба за два хода.
else:
    print('б) Первая фигура не угрожает второй.')
    logging.info('б) Первая фигура не угрожает второй.')
    square = get_kill_two_move(figure1, figure2)
    # Если невозможно срубить за два хода, выводим полученный результат.
    if square == None:
        print('в) Первая фигура не может срубить вторую за два хода.')
        logging.info('в) Первая фигура не может срубить вторую за два хода.')
    # Если возможен, то выводим клетку, через которую возможно это сделать.
    else:
        print('в) Первая фигура может срубить вторую за два хода, ' + 
                f'где первый ход будет {square}.')
        logging.info('в) Первая фигура может срубить вторую за два хода, ' + 
                f'где первый ход будет {square}.')