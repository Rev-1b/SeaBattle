from typing import Literal


class Coordinates:
    def __init__(self, x=None, y=None):
        self.x: int = x
        self.y: int = y

    def __bool__(self):
        return not (self.x is None and self.y is None)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return {'x_diff': self.x - other.x, 'y_diff': self.y - other.y}


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
        self.coordinates: Coordinates = Coordinates(x=x, y=y)
        self.decks: list[str] = ['normal_ship' for _ in range(length)]
        self.is_destroyed: bool = False

    def set_coords(self, coordinates):
        self.coordinates = coordinates

    def __bool__(self):
        return self.is_destroyed


class ShootOutput:
    def __init__(self, is_hit, is_destroyed):
        self.is_hit = is_hit
        self.is_destroyed = is_destroyed


class MysteryShip:
    def __init__(self):
        self.first_hit_coords: Coordinates = Coordinates()
        self.around_hit_area: list[Coordinates] = []
        self.possible_location: list[Coordinates] = []

    def __bool__(self):
        return bool(self.first_hit_coords)


