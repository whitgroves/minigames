import math
import pygame as pg
from settings import *
from gameobject import *

class Asteroid(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int, vel:int=ASTEROID_SPEED, angle:float|None=None) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.destroyed = False
        self.radius = HALF_ASTEROID_SIZE
        self.vel = vel
        if not angle: # default towards midscreen
            self.angle = math.atan2(self.y-self.game.player.loc.y, self.x-self.game.player.loc.x)
            self.angle %= math.tau
        else:
            self.angle = angle

    def _points(self): # similar to Player, each asteroid is inscribed into a circle
        result = []
        for point in ASTEROID:
            x = self.x + self.radius * math.cos(point + self.angle)
            y = self.y + self.radius * math.sin(point + self.angle)
            result.append((x, y))
        return result
    
    def _on_destroy(self) -> None:
            self.game.deregister(self.obj_id)

    def update(self) -> None:
        if self.destroyed or not self.in_bounds:
            self._on_destroy()
        else:
            # self.angle += ASTEROID_ROT
            self.x -= self.vel * math.cos(self.angle)
            self.y -= self.vel * math.sin(self.angle)

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 3)


class BigAsteroid(Asteroid):
    def __init__(self, game:GameObjectManager, x:int, y:int, **kwargs) -> None:
        super().__init__(game, x, y, **kwargs)
        self.radius *= 2
    
    DESTROYED = pg.event.custom_type() # spwaning more asteroids on destruction has to be done outside the update loop
    
    def _on_destroy(self) -> None:
        pg.event.post(pg.event.Event(BigAsteroid.DESTROYED, {'x':self.x, 'y':self.y, 'a':self.angle}))
        super()._on_destroy()
