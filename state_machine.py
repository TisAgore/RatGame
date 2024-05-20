import pygame as pg
from abc import ABC, abstractmethod
from entities_and_objects import Rat
from drawer import EntityDrawer
from constants import GRAVITY_CONSTANT

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
        if not player.hitbox.collision_type.get_status_for_player():
            y_speed = 0
            return JumpingMovingState(y_speed=y_speed)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # print(1)
                y_speed = JumpingComponent().y_speed
                # print(y_speed)
                return JumpingMovingState(y_speed=y_speed)
            # if event.key == pg.K_d:
            #         player.hitbox.direction = 1
            if keys[pg.K_d]:
                player.hitbox.direction = RIGHT_DIRECTION
                x_speed = MovingComponent(player.hitbox.direction).x_speed
                return JumpingMovingState(x_speed=x_speed)
            # if event.key == pg.K_a:
            #         player.hitbox.direction = -1
            if keys[pg.K_a]:
                player.hitbox.direction = LEFT_DIRECTION
                x_speed = MovingComponent(player.hitbox.direction).x_speed
                return JumpingMovingState(x_speed=x_speed)
        return self
    
    def update(self, player: Rat):
        return self

    def draw(self, display: pg.Surface, player: Rat):
        EntityDrawer.draw('RED', display, player)

class JumpingMovingState(State):
    def __init__(self, y_speed: int = 0, x_speed: int = 0):
        super().__init__('moving')
        self.y_speed = y_speed
        self.x_speed = x_speed

    def update(self, player: Rat):
        self.y_speed += GRAVITY_CONSTANT
        player.change_position(move_to_x=self.x_speed, move_to_y=self.y_speed)

    def draw(self, display: pg.Surface, player: Rat):
        EntityDrawer.draw('RED', display, player)

    def handle_input(self, event: pg.event, player: Rat):
        keys = pg.key.get_pressed()
        # if event.type == pg.KEYUP:
            # print(event.key)
        if not keys[pg.K_d] and not keys[pg.K_a]:
            if player.hitbox.collision_type.get_status_for_player():
                return IdleState()
            self.x_speed = 0
            return self
        if keys[pg.K_d]:
            player.hitbox.direction = RIGHT_DIRECTION
            self.x_speed = MovingComponent(player.hitbox.direction).x_speed
            return self
        if keys[pg.K_a]:
            player.hitbox.direction = LEFT_DIRECTION
            self.x_speed = MovingComponent(player.hitbox.direction).x_speed
            return self
        return self
