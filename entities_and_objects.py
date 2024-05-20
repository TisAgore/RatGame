import pygame as pg
from abc import ABC, abstractmethod
from collision import StaticHitbox, DynamicHitbox
from constants import GRAVITY_CONSTANT


class Entity(ABC):
    @abstractmethod
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        self.__hitbox = DynamicHitbox(size, position, direction)

    @property
    def hitbox(self):
        return self.__hitbox

class Rat(Entity):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        # super().__init__(size, position, direction)
        self.__hitbox = DynamicHitbox(size, position, direction)
        self.__y_acceleration = GRAVITY_CONSTANT
        # self.y_speed = 0
        self.__x_speed = 0

    # def jump(self):
    #     self.__y_speed -= 10
    
    # def update_y_spped(self):
    #     self.__y_speed += self.__y_acceleration
    
    def change_position(self, move_to_x: int = 0, move_to_y: int = 0):
        self.__hitbox.change_x_position(move_to_x)
        self.__hitbox.change_y_position(move_to_y)

    def stop_falling(self):
        self.__y_speed = 0
        self.__y_acceleration = 0
    
    def resume_falling(self):
        self.__y_acceleration = GRAVITY_CONSTANT

    @property
    def hitbox(self):
        return self.__hitbox
    
    # @property
    # def y_speed(self):
    #     return self.__y_speed

class Block:
    def __init__(self, size, position):
        self.__hitbox = StaticHitbox(size, position, 'block')

    @property
    def hitbox(self):
        return self.__hitbox