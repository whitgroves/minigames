import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()
    
    def new_game(self) -> None:
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
    
    def update(self) -> None:
        self.player.update()
        self.raycasting.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'FPS: {self.clock.get_fps():.1f}')
        
    def draw(self) -> None:
        # self.screen.fill('black')
        self.object_renderer.draw()
        
    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
    def run(self) -> None:
        while True:
            self.check_events()
            self.update()
            self.draw()
   

if __name__ == '__main__':
    game = Game()
    game.run()
