import pygame
import sys
import os
from abc import ABC, abstractmethod

GRAVITY_CONSTANT = 0.5

# class Rule(ABC):
#     @abstractmethod
#     def apply_rule():
#         pass

# class GravityRule(Rule):
#     def __init__(self):
#         self.__GRAVITY_CONSTANT = GRAVITY_CONSTANT

#     def apply_rule(self, speed):
#         return speed - self.__GRAVITY_CONSTANT

class Display:
    def __init__(self, size: tuple[int, int]):
        self.__width = size[0]
        self.__heigth = size[1]
        self.__surface = pygame.display.set_mode(size)
        self.__background = None

    @property
    def surface(self):
        return self.__surface
    
class Rat:
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        self.__hitbox = DynamicHitbox(size, position)
        self.__y_acceleration = GRAVITY_CONSTANT
        self.__y_speed = 0
        self.__x_speed = 0

    def jump(self):
        self.__y_speed -= 100
    
    def update_y_spped(self):
        self.__y_speed += self.__y_acceleration
    
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
    
    @property
    def y_speed(self):
        return self.__y_speed

class Hitbox:
    @abstractmethod
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        self.__y_size = size[1]
        self.__x_size = size[0]
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
    
    def get_position(self):
        return self.__position
    
    def set_position(self, new_pos: tuple[int, int]):
        self.__position = new_pos
    
    # @property
    # def hitbox_type(self):
    #     return self.__hitbox_type
    
class StaticHitbox(Hitbox):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], hitbox_type: str):
        super().__init__(size, position)
        self.__hitbox_type = hitbox_type
        CollisionDetector.add_static_object(self)

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
    def __init__(self, size: tuple[int, int], position: tuple[int, int]):
        super().__init__(size, position)
        self.__collision_type = RatAndBlock()
        # self.__parent = parent
        CollisionDetector.add_dynamic_object(self)

    @property
    def size(self):
        return super().size
    
    def get_position(self):
        return super().get_position()
    
    def set_position(self, new_pos):
        super().set_position(new_pos)
    
    @property
    def collision_type(self):
        return self.__collision_type
    
    # @property
    # def parent(self):
    #     return self.__parent
    
    # @property
    # def hitbox_type(self):
    #     return super().hitbox_type
    
    def get_corners(self):
        return super().get_corners()

    def change_x_position(self, move_to: int):
        super().set_position((self.get_position()[0] + move_to, self.get_position()[1]))

    def change_y_position(self, move_to: int):
        super().set_position((self.get_position()[0], self.get_position()[1] + move_to))

class CollisionDetector:
    static_objects_on_display: list[StaticHitbox] = []
    dynamic_objects_on_display: list[DynamicHitbox] = []

    @classmethod
    def add_static_object(cls, hitbox: StaticHitbox):
        cls.static_objects_on_display.append(hitbox)

    @classmethod
    def add_dynamic_object(cls, hitbox: DynamicHitbox):
        cls.dynamic_objects_on_display.append(hitbox)

    @classmethod
    def check_collisions(cls):
        moving_hitbox = None
        for object in cls.dynamic_objects_on_display:
            moving_hitbox = object
        if moving_hitbox is not None:
            corners = moving_hitbox.get_corners()
            for object in cls.static_objects_on_display:
                if object.hitbox_type == 'block':
                    object_corners = object.get_corners()
                    # if corners[0][0] <= object_corners[3][0]:
                    #     # print(3)
                    #     if corners[0][1] <= object_corners[3][1]:
                    #         pass
                            # RatAndBlock.action(moving_hitbox, corners[1][1], object_corners[2][1])
                    if corners[1][0] < object_corners[2][0] and corners[3][0] > object_corners[0][0]:
                        # print(corners)
                        # print(corners[1][1], object_corners[2][1])
                        if corners[1][1] + 1 >= object_corners[2][1]:
                            moving_hitbox.collision_type.action(moving_hitbox, corners[1][1], object_corners[2][1])
                        elif corners[3][1] + 1 >= object_corners[0][1]:
                            # print(2)
                            moving_hitbox.collision_type.action(moving_hitbox, corners[3][1], object_corners[0][1])
                        else:
                            moving_hitbox.collision_type.set_status_for_player(False)
                    else:
                        moving_hitbox.collision_type.set_status_for_player(False)
                        continue
                    break
                        # moving_hitbox.collision_type.set_status_for_player(False)


class Collision(ABC):
    @abstractmethod
    def action():
        pass

class RatAndBlock(Collision):
    def __init__(self):
        self.__collision_status = False

    def action(self, player_hitbox: DynamicHitbox, player_hitbox_y: int, block_hitbox_y: int):
        self.set_status_for_player(True)
        if block_hitbox_y != player_hitbox_y:
            moving = block_hitbox_y - player_hitbox_y
        # player = player_hitbox.parent
            player_hitbox.change_y_position(move_to=moving)
        # cls.set_status_for_player(True)

    
    def set_status_for_player(self, status: bool):
        self.__collision_status = status

    def get_status_for_player(self):
        return self.__collision_status

    
class Block:
    def __init__(self, size, position):
        self.__hitbox = StaticHitbox(size, position, 'block')

    @property
    def hitbox(self):
        return self.__hitbox
    
    @property
    def collision(self):
        return self.__collision

if __name__ == '__main__':
    pygame.init()
    main_screen = Display((1500, 900))
    player = Rat(size=(100, 100), position=(0, 0))
    test_block1 = Block(size=(100, 100), position=(100, 550))
    test_block2 = Block(size=(100, 100), position=(700, 550))
    # player_hitbox = pygame.rect(player.rat_hitbox.position, player.rat_hitbox.size)
    clock = pygame.time.Clock()
    frames = 1

    while True:
        CollisionDetector.check_collisions()
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_d]:
        #     player.change_position(move_to_x=30)
        # elif keys[pygame.K_a]:
        #     player.change_position(move_to_x=-30)
        # elif keys[pygame.K_SPACE] and player.hitbox.collision_type.get_status_for_player() == True:
        #     player.resume_falling()
        #     player.jump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.change_position(move_to_x=30)
                    # player.change_position(move_to_x=30)
                if event.key == pygame.K_a:
                    player.change_position(move_to_x=-30)
                if event.key == pygame.K_SPACE and player.hitbox.collision_type.get_status_for_player() == True:
                    player.resume_falling()
                    player.jump()
                    player.update_y_spped()
                    player.change_position(move_to_y=player.y_speed)
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_a:
                    print ("'A'released.")
                if event.key == pygame.K_d:
                    print ("'D' released.")
                if event.key == pygame.K_SPACE:
                    print ("Space bar released.")
        if player.hitbox.collision_type.get_status_for_player():
            player.stop_falling()
        else:
            player.resume_falling()
        if frames % 5 == 0:
            frames = 1
            player.update_y_spped()
            player.change_position(move_to_y=player.y_speed)
            # print(RatAndBlock.get_status_for_player())
            main_screen.surface.fill((0, 0, 0))
            # print(player.hitbox.position, player.hitbox.size)
            player_drawn_hitbox = pygame.draw.rect(main_screen.surface, (255, 0, 0), (*player.hitbox.get_position(), *player.hitbox.size))
            block_drawn = pygame.draw.rect(main_screen.surface, (0, 255, 0), (*test_block1.hitbox.get_position(), *test_block1.hitbox.size))
            block_drawn = pygame.draw.rect(main_screen.surface, (0, 255, 0), (*test_block2.hitbox.get_position(), *test_block2.hitbox.size))

        frames += 1
        pygame.display.update()
        clock.tick(60)
