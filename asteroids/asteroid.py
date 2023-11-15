import math
import pygame as pg
from settings import *
from gameobject import *

class Asteroid(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int, vel:int=ASTEROID_SPEED, angle:float|None=None) -> None:
        super().__init__(game)
        self.loc = pg.Vector2(x, y)
        # self.destroyed = False
        self.radius = HALF_ASTEROID_SIZE
        self.vel = vel
        if not angle: # default towards midscreen
            self.angle = math.atan2(self.loc.y-self.game.player.loc.y, self.loc.x-self.game.player.loc.x)
            self.angle %= math.tau
        else:
            self.angle = angle

    def _points(self): # similar to Player, each asteroid is inscribed into a circle
        result = []
        for point in ASTEROID:
            x = self.loc.x + self.radius * math.cos(point + self.angle)
            y = self.loc.y + self.radius * math.sin(point + self.angle)
            result.append((x, y))
        return result

    def update(self) -> None:
        if not self.in_bounds:
            self.on_destroy()
        else:
            self.loc.x -= self.vel * math.cos(self.angle)
            self.loc.y -= self.vel * math.sin(self.angle)

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 3)

class BigAsteroid(Asteroid):
    def __init__(self, game:GameObjectManager, x:int, y:int, **kwargs) -> None:
        super().__init__(game, x, y, **kwargs)
        self.radius *= 2
    
    DESTROYED = pg.event.custom_type() # spwaning more asteroids on destruction has to be done outside the update loop
    
    def on_destroy(self) -> None:
        pg.event.post(pg.event.Event(BigAsteroid.DESTROYED, {'x':self.loc.x, 'y':self.loc.y, 'a':self.angle}))
        super().on_destroy()
