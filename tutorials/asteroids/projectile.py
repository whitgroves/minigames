import math
import pygame as pg
from settings import *
from gameobject import *

class Projectile(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int, angle:float) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * PROJ_SPD
        self.dy = math.sin(angle) * PROJ_SPD

    def update(self) -> None:
        if not self.in_bounds:
            self.game.deregister(self.obj_id)
        else:
            self.x += self.dx
            self.y += self.dy
            for asteroid in self.game.get_asteroids():
                if asteroid.x - asteroid.radius < self.x < asteroid.x + asteroid.radius and \
                   asteroid.y - asteroid.radius < self.y < asteroid.y + asteroid.radius:
                    asteroid.destroyed = True
                    self.game.deregister(self.obj_id)

    def render(self) -> None:
        pg.draw.aaline(self.game.screen, 'white', (self.x, self.y), (self.x-self.dx, self.y-self.dy))
