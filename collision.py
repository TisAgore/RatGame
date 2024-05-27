import pygame as pg
from abc import ABC, abstractmethod
from constants import Direction
from collections import OrderedDict

class Hitbox:
    @abstractmethod
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        self.__y_size = size[1]
        self.__x_size = size[0]
        self.__rect = pg.Rect(*position, size[0], size[1])
        self.__size = size
        self.__position = position
    
    @property
    def size(self):
        return self.__size
    
    @property
    def rect(self):
        return self.__rect
    
    def get_position(self):
        return self.__position
    
    def set_position(self, new_pos: tuple[int, int]):
        self.__position = new_pos
        self.__rect = pg.Rect(*new_pos, self.size[0], self.size[1])
    
class StaticHitbox(Hitbox):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], hitbox_type: str):
        super().__init__(size, position)
        self.__hitbox_type = hitbox_type
        CollisionDetector.add_static_object(self)
        CollisionDetector.add_static_rect(self.rect)

    @property
    def size(self):
        return super().size
    
    def get_position(self):
        return super().get_position()
    
    def set_position(self, new_pos):
        super().set_position(new_pos)
    
    @property
    def hitbox_type(self):
        return self.__hitbox_type

class DynamicHitbox(Hitbox):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        super().__init__(size, position)
        self.__collision_type = RatAndBlockCollision()
        self.direction = direction     # 1 - right, -1 - left
        CollisionDetector.add_dynamic_object(self)

    @property
    def size(self):
        return super().size
    
    @property
    def rect(self):
        return super().rect
    
    def get_position(self):
        return super().get_position()
    
    def set_position(self, new_pos: tuple[int, int]):
        super().set_position(new_pos)
    
    @property
    def collision_type(self):
        return self.__collision_type

    def change_x_position(self, move_to: int):
        super().set_position((self.get_position()[0] + move_to, self.get_position()[1]))

    def change_y_position(self, move_to: int):
        super().set_position((self.get_position()[0], self.get_position()[1] + move_to))

class CollisionDetector:
    static_objects_on_display: list[StaticHitbox] = []
    dynamic_objects_on_display: list[DynamicHitbox] = []
    static_objects_rects: list[pg.Rect] = []

    @classmethod
    def add_static_object(cls, hitbox: StaticHitbox):
        cls.static_objects_on_display.append(hitbox)

    @classmethod
    def add_static_rect(cls, rect: pg.Rect):
        cls.static_objects_rects.append(rect)

    @classmethod
    def add_dynamic_object(cls, hitbox: DynamicHitbox):
        cls.dynamic_objects_on_display.append(hitbox)

    @classmethod
    def check_collisions(cls):
        moving_hitbox = None
        for object in cls.dynamic_objects_on_display:
            moving_hitbox = object
            collision = moving_hitbox.rect.collidelist(cls.static_objects_rects)
            if collision != -1:
                unmoveable_hitbox = cls.static_objects_on_display[collision]
                deltas = [unmoveable_hitbox.rect.bottom - moving_hitbox.rect.top,
                          moving_hitbox.rect.bottom - unmoveable_hitbox.rect.top,
                          moving_hitbox.rect.right - unmoveable_hitbox.rect.left,
                          unmoveable_hitbox.rect.right - moving_hitbox.rect.left]
                directions_for_deltas = [Direction.TOP_DIRECTION, Direction.BOTTOM_DIRECTIOM, Direction.LEFT_DIRECTION, Direction.RIGHT_DIRECTION]
                deltas_dict = OrderedDict()
                for delta_id in range(len(deltas)):
                    delta = deltas[delta_id]
                    direction = directions_for_deltas[delta_id]
                    if delta in deltas_dict:
                        deltas_dict[delta] += [direction]
                    else:
                        deltas_dict[delta] = [direction]
                max_delta = max(deltas)
                collision_directions = deltas_dict[max_delta]
                if len(collision_directions) == 2:
                    moving_hitbox.collision_type.action(moving_hitbox, unmoveable_hitbox, max_delta, y_direction=collision_directions[0], x_direction=collision_directions[1])
                else:
                    collision_direction = collision_directions[0]
                    if abs(collision_direction) == 1:
                        moving_hitbox.collision_type.action(moving_hitbox, unmoveable_hitbox, max_delta, x_direction=collision_direction)
                    else:
                        moving_hitbox.collision_type.action(moving_hitbox, unmoveable_hitbox, max_delta, y_direction=collision_direction)
            else:
                moving_hitbox.collision_type.above_collision_status = False
                moving_hitbox.collision_type.below_collision_status = False


class Collision(ABC):
    @abstractmethod
    def action():
        pass

class RatAndBlockCollision(Collision):
    def __init__(self):
        self.above_collision_status = False
        self.below_collision_status = False

    def action(self, player_hitbox: DynamicHitbox, block_hitbox: StaticHitbox, unification: int, y_direction: int = 0, x_direction: int = 0):
        if y_direction != 0:
            y_direction = int(y_direction/abs(y_direction))
            if y_direction == -1:
                self.above_collision_status = True
            else:
                self.below_collision_status = True
        moving_y = ((player_hitbox.size[1] + block_hitbox.size[1]) - unification - 1) * y_direction
        moving_x = ((player_hitbox.size[0] + block_hitbox.size[0]) - unification) * -x_direction
        player_hitbox.change_y_position(move_to=moving_y)
        player_hitbox.change_x_position(move_to=moving_x)

    def get_status_for_player(self):
        return self.__collision_status
