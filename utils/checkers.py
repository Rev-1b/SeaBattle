from utils.classes import Cell, Coordinates, Ship


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


def is_cell_already_open(game_pole: list[list[Cell]], coordinates: Coordinates) -> bool:
    return game_pole[coordinates.y][coordinates.x].is_open


def check_death(ship: Ship) -> bool:
    return all(status == 'destroyed_ship' for status in ship.decks)


def is_game_finished(ship_list: list[Ship]) -> bool:
    return all(ship.is_destroyed for ship in ship_list)

