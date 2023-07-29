from lexicon.lexicon_ru import LEXICON_RU
from random import choice, randint
from typing import Literal
from states.states import Coordinates


class Cell:
    def __init__(self, value='water'):
        self.status: str = value
        self.is_open: bool = False

    def __bool__(self):
        return self.is_open


class Ship:
    def __init__(self, length, position, x=None, y=None):
        self.length: int = length
        self.position: Literal['horizontal', 'vertical'] = position
        self.x: int = x
        self.y: int = y
        self.decks: list[str] = ['normal_ship' for _ in range(length)]
        self.is_destroyed: bool = False

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def __bool__(self):
        return self.is_destroyed


def generate_empty_pole() -> list[list[Cell]]:
    return [[Cell() for _ in range(10)] for _ in range(10)]


def show_game_pole(game_pole: list[list[Cell]], is_player=False) -> str:
    string_game_pole = f"{LEXICON_RU['crutch_line']}\n\n{LEXICON_RU['top_info_line']}"
    for indx, row in enumerate(game_pole):
        if is_player:
            united_row = "".join(LEXICON_RU[cell.status] for cell in row)
        else:
            united_row = "".join(LEXICON_RU[cell.status] if cell else LEXICON_RU["hidden_cell"]for cell in row)
        string_game_pole += f'\n{indx}  {united_row}'

    return string_game_pole


def generate_ships_list() -> list[Ship]:
    result_list = []
    for i in range(4, 0, -1):
        for j in range(5 - i):
            result_list.append(Ship(length=i,
                                    position=choice(['horizontal', 'vertical'])))
    return result_list


def define_ship_area(ship: Ship, is_main: bool) -> list[tuple[int]]:
    """
    Функция принимает экземпляр класса Ship и возвращает список кортежей с координатами ячеек игрового поля,
    на которые "влияет" корабль. Дополнительный параметр is_main показывает, следует ли в область "влияния"
    корабля включать все клетки вокруг него, или же стоит ограничиться клетками, которые корабль
    занимает непосредственно. Стартовые координаты x, y у корабля всегда указывают на ЛЕВЫЙ ВЕРХНИЙ угол!,
    соответственно отсчет палуб корабля будет начинаться именно оттуда.
    В функции are_ships_intersected() эта функция будет вызываться для 2х кораблей, притом только один
    из них будет вызван с параметром is_main=True. Это нужно для проверки пересечения кораблей. Есди в списках
    проверяемых кораблей найдется хоть одно совпадение, это будет значить, что корабли пересекаются.

    Если кто-нибудь будет ревьюить мой код, НЕ СМОТРИТЕ ЭТУ ФУНКЦИЮ!!! Руководствуйтесть прицнипом: Работает - не лезь!
    Если разобраться, то тут все просто и логично, но как бы я не старался написать понятно для стороннего наблюдателя,
    получилось... ЭТО.
    """

    x_shift = ship.length if ship.position == 'horizontal' else int(is_main)
    y_shift = ship.length if ship.position == 'vertical' else int(is_main)

    upper_left_x = ship.x - int(is_main) if ship.x > 0 else 0
    upper_left_y = ship.y - int(is_main) if ship.y > 0 else 0

    lower_right_x = ship.x + x_shift
    lower_right_y = ship.y + y_shift

    lower_right_x = lower_right_x - int(not is_main and ship.position == 'horizontal') if lower_right_x < 10 else 9
    lower_right_y = lower_right_y - int(not is_main and ship.position == 'vertical') if lower_right_y < 10 else 9

    tmp_area = []  # генерация координат всех клеток покрытия кораблем
    for x in range(upper_left_x, lower_right_x + 1):
        for y in range(upper_left_y, lower_right_y + 1):
            tmp_area.append((x, y))

    return tmp_area


def are_ships_intersected(ship1, ship2) -> bool:
    ship1_area = define_ship_area(ship=ship1, is_main=True)
    ship2_area = define_ship_area(ship=ship2, is_main=False)
    return any(coords in ship1_area for coords in ship2_area)


def is_out_of_pole(ship: Ship) -> bool:
    x_last = ship.x + ship.length if ship.position == 'horizontal' else ship.x
    y_last = ship.y + ship.length if ship.position == 'vertical' else ship.y
    return x_last >= 10 or y_last >= 10


def place_ships(ship_list: list) -> list[list[Cell]]:
    temp_ship_list = generate_ships_list()
    for ship in temp_ship_list:
        ship.set_coords(x=randint(0, 9), y=randint(0, 9))
        while is_out_of_pole(ship) or any(are_ships_intersected(ship, obj) for obj in ship_list if ship != obj):
            x, y = randint(0, 9), randint(0, 9)
            ship.set_coords(x, y)
        ship_list.append(ship)


def modify_game_pole(game_pole: list[list[Cell]], ship_list: list[Ship]) -> None:
    for ship in ship_list:
        ship_area = define_ship_area(ship=ship, is_main=False)
        for index, coords in enumerate(ship_area):
            game_pole[coords[1]][coords[0]].status = ship.decks[index]


def translate_letter_to_number(letter: str) -> int:
    dictionary = {'A': 0,
                  'B': 1,
                  'C': 2,
                  'D': 3,
                  'E': 4,
                  'F': 5,
                  'G': 6,
                  'H': 7,
                  'I': 8,
                  'J': 9}

    return dictionary[letter]


def verify_shot_coordinates(game_pole: list[list[Cell]], coordinates: Coordinates) -> bool:
    return bool(game_pole[coordinates.y][coordinates.x])


def shoot(game_pole: list[list[Cell]], ship_list: list[Ship], coordinates: Coordinates) -> bool:
    is_hit = False

    for ship in ship_list:
        ship_area = define_ship_area(ship=ship, is_main=False)
        if (coordinates.x, coordinates.y) in ship_area:
            for index, coords in enumerate(ship_area):
                if coords == coordinates:
                    ship.decks[index] = 'destroyed_ship'
                    game_pole[coords[1]][coords[0]].status = ship.decks[index]
                    game_pole[coords[1]][coords[0]].is_open = True

            is_hit = True
            if check_death(ship):
                mark_death_area(game_pole, ship)
            break

    if not is_hit:
        game_pole[coordinates.y][coordinates.x].is_open = True
    return is_hit


def check_death(ship: Ship) -> bool:
    return all(status == 'destroyed_ship' for status in ship.decks)


def mark_death_area(game_pole: list[list[Cell]], ship: Ship) -> None:
    ship_area = define_ship_area(ship=ship, is_main=True)

    for coords in ship_area:
        game_pole[coords[1]][coords[0]].is_open = True


def generate_ai_shot() -> Coordinates:
    pass







