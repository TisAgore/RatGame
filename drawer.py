import pygame as pg
from entities_and_objects import Block, Entity
# from level_generator import LevelGenerator
from constants import BLOCK_SIZE, Colors

class EntityView:
    @staticmethod
    def draw(color: tuple[int, int, int], display: pg.Surface, entity: Entity):
        pg.draw.rect(display, Colors.COLORS[color], (*entity.hitbox.get_position(), *entity.hitbox.size), 6, 1)

class ObjectView:
    @staticmethod
    def draw(color: tuple[int, int, int], display: pg.Surface, object: Block):
        pg.draw.rect(display, Colors.COLORS[color], (*object.hitbox.get_position(), *object.hitbox.size))

class LevelView:
    @staticmethod
    def draw_level(display: pg.Surface, level):
        column_len = len(level[0])
        for line in range(len(level)):
            for column in range(column_len):
                if level[line][column] == 1:
                    # print(1)
                    block = Block(size=(BLOCK_SIZE, BLOCK_SIZE), position=(BLOCK_SIZE*column, BLOCK_SIZE*line))
                    # print(block.hitbox.get_position(), block.hitbox.size)
                    ObjectView.draw('GREEN', display, block)