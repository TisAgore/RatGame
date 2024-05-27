import pygame as pg
import sys
import os
from level_generator import *
from drawer import *
from state_machine import *
from entities_and_objects import *
from collision import *


class Display:
    def __init__(self, size: tuple[int, int]):
        self.width = size[0]
        self.heigth = size[1]
        self.surface = pg.display.set_mode(size)
        self.__background = None


class Game:
    def __init__(self):
        # Settings
        self.is_paused = False
        self.game_speed = 1.0
        self.delta_time = 0.016  # 60 FPS (16 ms)

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def set_game_speed(self, speed):
        self.game_speed = speed

    def update(self):
        if not self.is_paused:
            scaled_delta_time = self.delta_time * self.game_speed
            self.update_game_world(scaled_delta_time)
        else:
            self.update_paused_state()

    def update_game_world(self, scaled_delta_time):
        # player.update_y_spped()
        # player.change_position(move_to_y=player.y_speed)
        # CollisionDetector.check_collisions()
        # All game logic here, such as moving objects, checking collisions, etc.
        # Example:
        # self.player.update(scaled_delta_time)
        # self.enemy.update(scaled_delta_time)
        # Physics.update(scaled_delta_time)
        pass

    def update_paused_state(self):
        # Update game menu or other paused state interactions
        # Example:
        # menu.update()
        pass

if __name__ == '__main__':
    pg.init()
    main_screen = Display((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    player = Rat(size=(BLOCK_SIZE, BLOCK_SIZE), position=(70, 70), direction=RIGHT_DIRECTION)
    clock = pg.time.Clock()
    level = LevelGenerator((main_screen.width//BLOCK_SIZE, main_screen.heigth//BLOCK_SIZE))
    level.generate()
    print(level.get_level())
    current_state: State = IdleState()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            previous_state = current_state
            current_state = current_state.handle_input(event, player)
            if previous_state != current_state:
                current_state.update(player)
                CollisionDetector.check_collisions()
        print(current_state)
        current_state.update(player)
        CollisionDetector.check_collisions()
        main_screen.surface.fill((0, 0, 0))
        current_state.draw(main_screen.surface, player)
        LevelDrawer.draw_level(main_screen.surface, level.get_level())
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()
    sys.exit()

        frames += 1
        pygame.display.update()
        clock.tick(60)
