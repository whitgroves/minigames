import sys
import pygame as pg
from settings import *
from gameobject import *
from player import Player
from asteroid import Asteroid, BigAsteroid

class Game(GameObjectManager):
    def __init__(self) -> None:
        super().__init__()
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self) -> None:
        self.player = Player(self)
        self.spawn_asteroid(x=QUTR_WIDTH, y=QUTR_HEIGHT)
        self.spawn_asteroid(x=(HALF_WIDTH + QUTR_WIDTH), y=(HALF_HEIGHT + QUTR_HEIGHT), big=True)
        
    def get_asteroids(self) -> list[Asteroid]:
        return [obj for obj in self.game_objects.values() if isinstance(obj, Asteroid)]
    
    def spawn_asteroid(self, x, y, big=False) -> Asteroid:
        return BigAsteroid(self, x, y) if big else Asteroid(self, x, y)

    def events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
                self.player.fire_event()
            if event.type == BigAsteroid.DESTROYED: # can't spawn GameObjects during update()
                x, y = event.dict['x'], event.dict['y']
                self.spawn_asteroid(x-HALF_ASTEROID_SIZE, y)
                self.spawn_asteroid(x+HALF_ASTEROID_SIZE, y+HALF_ASTEROID_SIZE)
                self.spawn_asteroid(x+HALF_ASTEROID_SIZE, y-HALF_ASTEROID_SIZE)
 
    def update(self) -> None:
        [obj.update() for obj in self.game_objects.values() if isinstance(obj, UpdateMixin)]
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{TITLE} - FPS: {self.clock.get_fps():.1f}')

    def render(self) -> None:
        self.screen.fill('black')
        [obj.render() for obj in self.game_objects.values() if isinstance(obj, RenderMixin)]

    def run(self) -> None:
        while True:
            self.events()
            self.update()
            self.render()
            self.cleanup() # see GameObjectManager.deregister()

if __name__ == '__main__':
    game = Game()
    game.run()
