from typing import Literal, NamedTuple
from dataclasses import dataclass


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

