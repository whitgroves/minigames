import math
import pygame as pg
from settings import *
from gameobject import *

class Asteroid(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.angle = 0
        self.destroyed = False
        self.radius = HALF_ASTEROID_SIZE

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
        if self.destroyed:
            self._on_destroy()
        else:
            self.angle += ASTEROID_ROT

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 3)


class BigAsteroid(Asteroid):
    def __init__(self, game:GameObjectManager, x:int, y:int) -> None:
        super().__init__(game, x, y)
        self.radius *= 2
    
    DESTROYED = pg.event.custom_type() # spwaning more asteroids on destruction has to be done outside the update loop
    
    def _on_destroy(self) -> None:
        pg.event.post(pg.event.Event(BigAsteroid.DESTROYED, {'x':self.x, 'y':self.y}))
        super()._on_destroy()
