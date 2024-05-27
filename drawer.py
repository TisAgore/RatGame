import pygame as pg
from entities_and_objects import Block, Entity
from constants import BLOCK_SIZE, COLORS

class EntityDrawer:
    @staticmethod
    def draw(color: tuple[int, int, int], display: pg.Surface, entity: Entity):
        pg.draw.rect(display, COLORS[color], (*entity.hitbox.get_position(), *entity.hitbox.size), 6, 1)

class ObjectDrawer:
    @staticmethod
    def draw(color: tuple[int, int, int], display: pg.Surface, object: Block):
        pg.draw.rect(display, COLORS[color], (*object.hitbox.get_position(), *object.hitbox.size))

class LevelDrawer:
    @staticmethod
    def draw_level(display: pg.Surface, level):
        column_len = len(level[0])
        for line in range(len(level)):
            for column in range(column_len):
                if level[line][column] == 1:
                    block = Block(size=(BLOCK_SIZE, BLOCK_SIZE), position=(BLOCK_SIZE*column, BLOCK_SIZE*line))
                    ObjectDrawer.draw('GREEN', display, block)
