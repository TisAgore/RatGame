import pygame as pg
from abc import ABC, abstractmethod
from collision import StaticHitbox, DynamicHitbox
from constants import GRAVITY_CONSTANT


class Entity(ABC):
    @abstractmethod
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        self.hitbox = DynamicHitbox(size, position, direction)

class Rat(Entity):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        self.hitbox = DynamicHitbox(size, position, direction)
    
    def change_position(self, move_to_x: int = 0, move_to_y: int = 0):
        self.__hitbox.change_x_position(move_to_x)
        self.__hitbox.change_y_position(move_to_y)

class Block:
    def __init__(self, size, position):
        self.hitbox = StaticHitbox(size, position, 'block')
