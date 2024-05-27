import pygame as pg
from abc import ABC, abstractmethod

class Hitbox:
    @abstractmethod
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        self.__y_size = size[1]
        self.__x_size = size[0]
        self.__rect = pg.Rect(*position, size[0], size[1])
        self.__size = size
        self.__position = position

    @abstractmethod
    def get_corners(self):
        self.__left_up_corner = list(self.__position)
        self.__left_down_corner = [self.__position[0], self.__position[1] + self.__y_size]
        self.__right_up_corner = [self.__position[0] + self.__x_size, self.__position[1]]
        self.__right_down_corner = [self.__position[0] + self.__x_size, self.__position[1] + self.__y_size]
        return self.__left_up_corner, self.__left_down_corner, self.__right_up_corner, self.__right_down_corner
    
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
    
    def get_corners(self):
        return super().get_corners()

class DynamicHitbox(Hitbox):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], direction: int):
        super().__init__(size, position)
        self.__collision_type = RatAndBlockCollision()
        self.direction = direction     # 1 - right, -1 - left
        # self.__parent = parent
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
        # self.rect = pg.Rect(*new_pos, self.size[0], self.size[1])
    
    @property
    def collision_type(self):
        return self.__collision_type
    
    def get_corners(self):
        return super().get_corners()

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
            corners = moving_hitbox.get_corners()
            collision = moving_hitbox.rect.collidelist(cls.static_objects_rects)
            if collision != -1:
                object_corners = cls.static_objects_on_display[collision].get_corners()
                moving_hitbox.collision_type.action(moving_hitbox, corners[1][1], object_corners[2][1])
            else:
                moving_hitbox.collision_type.set_status_for_player(False)


class Collision(ABC):
    @abstractmethod
    def action():
        pass

class RatAndBlockCollision(Collision):
    def __init__(self):
        self.__collision_status = False

    def action(self, player_hitbox: DynamicHitbox, player_hitbox_y: int, block_hitbox_y: int):
        self.set_status_for_player(True)
        if block_hitbox_y != (player_hitbox_y - 1):
            moving = block_hitbox_y - player_hitbox_y + 1
            player_hitbox.change_y_position(move_to=moving)

    
    def set_status_for_player(self, status: bool):
        self.__collision_status = status

    def get_status_for_player(self):
        return self.__collision_status
