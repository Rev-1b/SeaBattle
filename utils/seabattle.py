from lexicon.lexicon_ru import LEXICON_RU
from random import choice, randint
from utils.classes import Cell, Ship, Coordinates, ShootOutput


def show_game_pole(game_pole: list[list[Cell]], top_line: str, is_player=False) -> str:
    string_game_pole = f"{LEXICON_RU['crutch_line']}\n\n{top_line}"
    for indx, row in enumerate(game_pole):
        if is_player:
            united_row = "".join(LEXICON_RU[cell.status] for cell in row)
        else:
            united_row = "".join(LEXICON_RU[cell.status] if cell else LEXICON_RU["water"]for cell in row)
        string_game_pole += f'\n{LEXICON_RU["side_info_line"][indx]}{united_row}'

    return string_game_pole


def generate_ships_list() -> list[Ship]:
    result_list = []
    for i in range(4, 0, -1):
        for j in range(5 - i):
            result_list.append(Ship(length=i,
                                    position=choice(['horizontal', 'vertical'])))
    return result_list


def define_ship_area(ship: Ship, is_main: bool) -> Coordinates:
    """
    You don't need to understand it, you just need to believe it.
    """

    x_shift = ship.length if ship.position == 'horizontal' else int(is_main)
    y_shift = ship.length if ship.position == 'vertical' else int(is_main)

    upper_left_x = ship.coordinates.x - int(is_main) if ship.coordinates.x > 0 else 0
    upper_left_y = ship.coordinates.y - int(is_main) if ship.coordinates.y > 0 else 0

    lower_right_x = ship.coordinates.x + x_shift
    lower_right_y = ship.coordinates.y + y_shift

    lower_right_x = lower_right_x - int(not is_main and ship.position == 'horizontal') if lower_right_x < 10 else 9
    lower_right_y = lower_right_y - int(not is_main and ship.position == 'vertical') if lower_right_y < 10 else 9

    tmp_area = []  # generation of coordinates of all cells "covered" by the ship
    for x in range(upper_left_x, lower_right_x + 1):
        for y in range(upper_left_y, lower_right_y + 1):
            tmp_area.append(Coordinates(x=x, y=y))

    return tmp_area


def are_ships_intersected(ship1, ship2) -> bool:
    ship1_area = define_ship_area(ship=ship1, is_main=True)
    ship2_area = define_ship_area(ship=ship2, is_main=False)
    return any(coords in ship1_area for coords in ship2_area)


def is_out_of_pole(ship: Ship) -> bool:
    x_last = ship.coordinates.x + ship.length if ship.position == 'horizontal' else ship.coordinates.x
    y_last = ship.coordinates.y + ship.length if ship.position == 'vertical' else ship.coordinates.y
    return x_last >= 10 or y_last >= 10


def place_ships(ship_list: list) -> list[list[Cell]]:
    temp_ship_list = generate_ships_list()
    for ship in temp_ship_list:
        ship.set_coords(Coordinates(x=randint(0, 9),
                                    y=randint(0, 9)))
        while is_out_of_pole(ship) or any(are_ships_intersected(ship, obj) for obj in ship_list if ship != obj):
            ship.set_coords(Coordinates(x=randint(0, 9),
                                        y=randint(0, 9)))
        ship_list.append(ship)


def modify_game_pole(game_pole: list[list[Cell]], ship_list: list[Ship]) -> None:
    for ship in ship_list:
        ship_area = define_ship_area(ship=ship, is_main=False)
        for index, coords in enumerate(ship_area):
            game_pole[coords.y][coords.x].status = ship.decks[index]


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


def is_cell_already_open(game_pole: list[list[Cell]], coordinates: Coordinates) -> bool:
    return game_pole[coordinates.y][coordinates.x].is_open


def shoot(game_pole: list[list[Cell]], ship_list: list[Ship], coordinates: Coordinates) -> ShootOutput:
    is_hit = False
    is_destroyed = False

    for ship in ship_list:
        ship_area = define_ship_area(ship=ship, is_main=False)
        if coordinates in ship_area:
            for index, coords in enumerate(ship_area):
                if coords == coordinates:
                    ship.decks[index] = 'destroyed_ship'
                    game_pole[coords.y][coords.x].status = ship.decks[index]
                    game_pole[coords.y][coords.x].is_open = True

            is_hit = True
            if check_death(ship):
                is_destroyed = True
                mark_death_area(game_pole, ship)
            break

    if not is_hit:
        game_pole[coordinates.y][coordinates.x].is_open = True
        game_pole[coordinates.y][coordinates.x].status = 'opened_water'

    return ShootOutput(is_hit=is_hit,
                       is_destroyed=is_destroyed)


def check_death(ship: Ship) -> bool:
    return all(status == 'destroyed_ship' for status in ship.decks)


def mark_death_area(game_pole: list[list[Cell]], ship: Ship) -> None:
    ship.is_destroyed = True
    ship_area = define_ship_area(ship=ship, is_main=True)

    for coords in ship_area:
        game_pole[coords.y][coords.x].is_open = True
        if game_pole[coords.y][coords.x].status == 'water':
            game_pole[coords.y][coords.x].status = 'opened_water'


def give_random_coords(game_pole: list[list[Cell]]) -> Coordinates:
    x, y = randint(0, 9), randint(0, 9)
    not_valid_coords = is_cell_already_open(game_pole, Coordinates(x=x,
                                                                   y=y))

    while not_valid_coords:
        x, y = randint(0, 9), randint(0, 9)
        not_valid_coords = is_cell_already_open(game_pole, Coordinates(x=x,
                                                                       y=y))

    return Coordinates(x=x, y=y)


def is_game_finished(ship_list: list[Ship]) -> bool:
    return all(ship.is_destroyed for ship in ship_list)

