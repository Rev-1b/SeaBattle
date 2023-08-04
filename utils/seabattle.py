from lexicon.lexicon_ru import LEXICON_RU
from random import choice, randint
from utils.classes import Cell, Ship, Coordinates, ShootOutput
from utils.checkers import (define_ship_area, are_ships_intersected, check_death,
                            is_out_of_pole, is_cell_already_open)


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


