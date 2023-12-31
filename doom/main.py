import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_sprite import *
from object_manager import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40) # triggers self.global_event every 40ms
        self.new_game()
    
    def new_game(self) -> None:
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        self.object_manager = ObjectManager(self)
        self.weapon = Weapon(self, 'shotgun/0.png', 0.4, 90)
        self.sound = Sound(self)
        self.pathfinding = Pathfinding(self)
    
    def update(self) -> None:
        self.player.update()
        self.raycasting.update()
        self.object_manager.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'FPS: {self.clock.get_fps():.1f}')
        
    def draw(self) -> None:
        self.object_renderer.draw()     
        self.weapon.draw()
        # 2D mode         
        # self.screen.fill('black')
        # self.map.draw()          
        # self.player.draw()       
    
    def check_events(self) -> None:
        self.global_trigger = False # used by some game objects to pace non-looped animations - see NPC.animate_death()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.fire_event(event)
        
    def run(self) -> None:
        while True:
            self.check_events()
            self.update()
            self.draw()
   

if __name__ == '__main__':
    game = Game()
    game.run()
