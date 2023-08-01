from typing import Literal


class Coordinates:
    def __init__(self, x=None, y=None):
        self.x: int = x
        self.y: int = y

    def __bool__(self):
        return self.x is None and self.y is None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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

