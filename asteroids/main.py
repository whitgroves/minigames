import sys
import random
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
        self.asteroid_timer = 2500
        pg.time.set_timer(Game.SPAWN_ASTEROID, self.asteroid_timer)
        # self.spawn_asteroid(x=0, y=QUTR_HEIGHT)
        # self.spawn_asteroid(x=(HALF_WIDTH + QUTR_WIDTH), y=HEIGHT, size=1)

    SPAWN_ASTEROID = pg.event.custom_type()

    def spawn_asteroid(self, x:int, y:int, size:int=0, angle:float=None) -> Asteroid:
        match size:
            case 0:
                return Asteroid(self, x, y, angle=angle)
            case 1:
                return BigAsteroid(self, x, y, angle=angle)
        
    def get_asteroids(self) -> list[Asteroid]:
        return [obj for obj in self.game_objects.values() if isinstance(obj, Asteroid)]

    def events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                self.player.fire_event()
            if event.type == BigAsteroid.DESTROYED: # can't spawn GameObjects during update()
                x, y, a = event.dict['x'], event.dict['y'],event.dict['a']
                self.spawn_asteroid(x-HALF_ASTEROID_SIZE, y, angle=a)
                self.spawn_asteroid(x+HALF_ASTEROID_SIZE, y+HALF_ASTEROID_SIZE, angle=a)
                self.spawn_asteroid(x+HALF_ASTEROID_SIZE, y-HALF_ASTEROID_SIZE, angle=a)
            if event.type == Game.SPAWN_ASTEROID:
                if random.randint(0, 1):
                    x = random.choice([0, WIDTH])
                    y = random.randint(0, HEIGHT)
                else:
                    x = random.randint(0, WIDTH) 
                    y = random.choice([0, HEIGHT])
                self.spawn_asteroid(x, y, size=(random.randint(0, 1)))
                # every time an asteroid is spawned, the next one will be spawned on a decreasing trigger
                self.asteroid_timer -= 10
                pg.time.set_timer(Game.SPAWN_ASTEROID, self.asteroid_timer)
 
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
