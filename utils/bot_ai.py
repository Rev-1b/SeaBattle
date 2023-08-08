from random import choice
from states.states import User
from lexicon.lexicon_ru import LEXICON_RU

from utils.seabattle import give_random_coords, show_game_pole, shoot, is_cell_already_open
from utils.checkers import is_game_finished
from utils.classes import MysteryShip, Coordinates, Cell


def bot_ai(user: User) -> list[str]:
    """
    Terribly huge function, through recursion, collecting the states of the playing field in N moves of the bot and
    returning a list of these fields.
    """
    container = []

    if user.mystery_ship:
        if user.mystery_ship.possible_location:
            container.extend(_run_phase_3_4(user=user))
        else:
            container.extend(_run_phase_2_3_4(user=user))

    else:
        if is_game_finished(user.user_ship_list):
            return container
        bot_shot_coords = give_random_coords(user.user_game_pole)
        shoot_output1 = shoot(game_pole=user.user_game_pole,
                              ship_list=user.user_ship_list,
                              coordinates=bot_shot_coords)
        str_pole = show_game_pole(game_pole=user.user_game_pole,
                                  top_line=LEXICON_RU['info_line_types'][
                                      user.game_pole_type],
                                  is_player=True)
        container.append(str_pole)

        if shoot_output1.is_hit and not shoot_output1.is_destroyed:
            user.mystery_ship.first_hit_coords = bot_shot_coords
            user.mystery_ship.around_hit_area = _give_around_hit_area(coordinates=bot_shot_coords,
                                                                      user=user)
            container.extend(_run_phase_2_3_4(user=user))
        else:
            if shoot_output1.is_destroyed:
                user.mystery_ship = MysteryShip()
                container.extend(bot_ai(user=user))

    return container


def _give_around_hit_area(coordinates: Coordinates, user: User) -> list[Coordinates]:
    x, y = coordinates.x, coordinates.y
    around_hit_area = []
    temp_hit_area = [Coordinates(x=x - 1, y=y),
                     Coordinates(x=x + 1, y=y),
                     Coordinates(x=x, y=y - 1),
                     Coordinates(x=x, y=y + 1)]

    for coords in temp_hit_area:
        if 0 <= coords.x <= 9 and 0 <= coords.y <= 9:
            if not is_cell_already_open(game_pole=user.user_game_pole,
                                        coordinates=coords):
                around_hit_area.append(coords)

    return around_hit_area


def _give_ship_possible_area(game_pole: list[list[Cell]], first_hit_coords: Coordinates,
                             second_hit_coords: Coordinates) -> list[Coordinates]:
    difference = second_hit_coords - first_hit_coords

    x_shift = difference['x_diff']
    y_shift = difference['y_diff']
    ship_possible_area = []

    for shift in range(1, 3):
        temp_coords = Coordinates(x=second_hit_coords.x + shift * x_shift,
                                  y=second_hit_coords.y + shift * y_shift)

        if not 0 <= temp_coords.x <= 9 or not 0 <= temp_coords.y <= 9:
            break

        ship_possible_area.append(temp_coords)
        if game_pole[temp_coords.y][temp_coords.x] or\
                game_pole[temp_coords.y][temp_coords.x].status == 'water':  # PROBABLY WEAK SPOT
            break

    for shift in range(1, 3):
        temp_coords = Coordinates(x=first_hit_coords.x - shift * x_shift,
                                  y=first_hit_coords.y - shift * y_shift)

        if temp_coords.x > 9 or temp_coords.y > 9:
            break

        ship_possible_area.append(temp_coords)
        if game_pole[temp_coords.y][temp_coords.x] or\
                game_pole[temp_coords.y][temp_coords.x].status == 'water':  # PROBABLY WEAK SPOT
            break

    return ship_possible_area


def _run_phase_3_4(user: User) -> list[str]:
    """
    Only triggers if the player has a ship that has already had 2 hits and is still afloat.
    """
    sub_container = []
    shot_coords = user.mystery_ship.possible_location.pop(0)
    shoot_output3 = shoot(game_pole=user.user_game_pole,
                          ship_list=user.user_ship_list,
                          coordinates=shot_coords)
    str_pole = show_game_pole(game_pole=user.user_game_pole,
                              top_line=LEXICON_RU['info_line_types'][
                                  user.game_pole_type],
                              is_player=True)
    sub_container.append(str_pole)

    if shoot_output3.is_hit and not shoot_output3.is_destroyed:
        shot_coords = user.mystery_ship.possible_location.pop(0)
        shoot_output4 = shoot(game_pole=user.user_game_pole,
                              ship_list=user.user_ship_list,
                              coordinates=shot_coords)

        str_pole = show_game_pole(game_pole=user.user_game_pole,
                                  top_line=LEXICON_RU['info_line_types'][
                                      user.game_pole_type],
                                  is_player=True)
        sub_container.append(str_pole)

        if shoot_output4.is_destroyed:
            user.mystery_ship = MysteryShip()
            sub_container.extend(bot_ai(user=user))

    else:
        if shoot_output3.is_destroyed:
            user.mystery_ship = MysteryShip()
            sub_container.extend(bot_ai(user=user))

    return sub_container


def _run_phase_2_3_4(user: User) -> list[str]:
    """
    Срабатывает только в случае, если у игрока есть корабль, в который попали только один раз.
    """
    sub_container = []
    random_coords = choice(user.mystery_ship.around_hit_area)
    user.mystery_ship.around_hit_area.remove(random_coords)

    shoot_output2 = shoot(game_pole=user.user_game_pole,
                          ship_list=user.user_ship_list,
                          coordinates=random_coords)
    str_pole = show_game_pole(game_pole=user.user_game_pole,
                              top_line=LEXICON_RU['info_line_types'][
                                  user.game_pole_type],
                              is_player=True)
    sub_container.append(str_pole)

    if shoot_output2.is_hit and not shoot_output2.is_destroyed:
        ship_possible_area = _give_ship_possible_area(game_pole=user.user_game_pole,
                                                      first_hit_coords=user.mystery_ship.first_hit_coords,
                                                      second_hit_coords=random_coords)
        user.mystery_ship.possible_location = ship_possible_area

        sub_container.extend(_run_phase_3_4(user))

    else:
        if shoot_output2.is_destroyed:
            user.mystery_ship = MysteryShip()
            sub_container.extend(bot_ai(user=user))

    return sub_container
