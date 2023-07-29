from dataclasses import dataclass
from typing import NamedTuple
from utils.seabattle import Cell, Ship
from utils.seabattle import generate_empty_pole, generate_ships_list


class Coordinates(NamedTuple):
    x: int
    y: int


@dataclass
class User:
    user_id: int
    user_game_pole: list[list[Cell]]
    user_ship_list: list[Ship]
    bot_game_pole: list[list[Cell]]
    bot_ship_list: list[Ship]
    in_game: bool
    shot_coordinates: Coordinates

    def __bool__(self):
        return not self.in_game


users: dict[int, User] = {}


def user_registration(user_id: int) -> None:
    users[user_id] = User(user_id=user_id,
                          user_game_pole=generate_empty_pole(),
                          user_ship_list=[],
                          bot_game_pole=generate_empty_pole(),
                          bot_ship_list=[],
                          in_game=False,
                          shot_coordinates=NamedTuple)




