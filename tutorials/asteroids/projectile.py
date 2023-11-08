import math
import pygame as pg
from settings import *
from gameobject import *

class Projectile(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int, speed:float, angle:float) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self) -> None:
        if not self.in_bounds:
            self.game.deregister(self.obj_id)
        else:
            self.x += self.dx
            self.y += self.dy

    def render(self) -> None:
        pg.draw.aaline(self.game.screen, 'white', (self.x, self.y), (self.x-self.dx, self.y-self.dy))