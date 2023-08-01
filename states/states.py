from dataclasses import dataclass
from utils.classes import Cell, Ship, Coordinates


@dataclass
class User:
    user_game_pole: list[list[Cell]]
    user_ship_list: list[Ship]
    bot_game_pole: list[list[Cell]]
    bot_ship_list: list[Ship]
    in_game: bool
    shot_coordinates: Coordinates
    game_pole_type: int

    def __bool__(self):
        return not self.in_game


users: dict[int, User] = {}


def _generate_empty_pole() -> list[list[Cell]]:
    return [[Cell() for _ in range(10)] for _ in range(10)]


def user_registration(user_id: int) -> None:
    user = users.get(user_id)
    pole_type = user.game_pole_type if user else 0

    users[user_id] = User(user_game_pole=_generate_empty_pole(),
                          user_ship_list=[],
                          bot_game_pole=_generate_empty_pole(),
                          bot_ship_list=[],
                          in_game=False,
                          shot_coordinates=Coordinates(),
                          game_pole_type=pole_type)





