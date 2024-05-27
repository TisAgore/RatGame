import pygame as pg
from abc import ABC, abstractmethod
from entities_and_objects import Rat
from drawer import EntityView
from constants import GRAVITY_CONSTANT, Direction

class MovingComponent:
    def __init__(self, direction: int):
        self.x_speed = 10 * direction

class JumpingComponent:
    def __init__(self):
        self.y_speed = -10

class State(ABC):
    @abstractmethod
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class IdleState(State):
    def __init__(self):
        super().__init__('idle')

    def handle_input(self, event: pg.event.Event, player: Rat):
        keys = pg.key.get_pressed()
        if not player.hitbox.collision_type.above_collision_status:
            y_speed = 0
            return JumpingMovingState(y_speed=y_speed)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                print(5)
                y_speed = JumpingComponent().y_speed
                # print(y_speed)
                return JumpingMovingState(y_speed=y_speed)
            # if event.key == pg.K_d:
            #         player.hitbox.direction = 1
            if keys[pg.K_d]:
                player.hitbox.direction = Direction.RIGHT_DIRECTION
                x_speed = MovingComponent(player.hitbox.direction).x_speed
                return JumpingMovingState(x_speed=x_speed)
            # if event.key == pg.K_a:
            #         player.hitbox.direction = -1
            if keys[pg.K_a]:
                player.hitbox.direction = Direction.LEFT_DIRECTION
                x_speed = MovingComponent(player.hitbox.direction).x_speed
                return JumpingMovingState(x_speed=x_speed)
        return self
    
    def update(self, player: Rat):
        return self

    def draw(self, display: pg.Surface, player: Rat):
        EntityView.draw('RED', display, player)

class JumpingMovingState(State):
    def __init__(self, y_speed: int = 0, x_speed: int = 0):
        super().__init__('moving')
        self.y_speed = y_speed
        self.x_speed = x_speed
        # print(1)

    def update(self, player: Rat):
        self.y_speed += GRAVITY_CONSTANT
        # print(self.y_speed)
        # player.y_speed == self.jump_height
        # print(player.hitbox.get_position())
        player.change_position(move_to_x=self.x_speed, move_to_y=self.y_speed)
        # print(player.hitbox.get_position())

    def draw(self, display: pg.Surface, player: Rat):
        EntityView.draw('RED', display, player)

    def handle_input(self, event: pg.event, player: Rat):
        keys = pg.key.get_pressed()
        # if event.type == pg.KEYUP:
            # print(event.key)
        if player.hitbox.collision_type.below_collision_status:
            self.y_speed = 0
            return self
        if not keys[pg.K_d] and not keys[pg.K_a]:
            if player.hitbox.collision_type.above_collision_status:
                return IdleState()
            self.x_speed = 0
            return self
        if keys[pg.K_d]:
            player.hitbox.direction = 1
            self.x_speed = MovingComponent(player.hitbox.direction).x_speed
            return self
        if keys[pg.K_a]:
            player.hitbox.direction = -1
            self.x_speed = MovingComponent(player.hitbox.direction).x_speed
            return self
        return self