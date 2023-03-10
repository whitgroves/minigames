import pygame
import sys
from settings import *
from map import *
from player import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()
    
    def new_game(self) -> None:
        self.map = Map(self)
        self.player = Player(self)
    
    def update(self) -> None:
        self.player.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'FPS: {self.clock.get_fps():.1f}')
        
    def draw(self) -> None:
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()
        
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
