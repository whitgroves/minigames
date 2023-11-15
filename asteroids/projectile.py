import math
import pygame as pg
from settings import *
from gameobject import *

class Projectile(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game:GameObjectManager, x:int, y:int, angle:float) -> None:
        super().__init__(game)
        self.loc = pg.Vector2(x, y)
        self.dx = math.cos(angle) * PROJ_SPD
        self.dy = math.sin(angle) * PROJ_SPD

    def update(self) -> None:
        if not self.in_bounds:
            self.game.deregister(self.obj_id)
        else:
            self.loc.x += self.dx * self.game.delta_time
            self.loc.y += self.dy * self.game.delta_time
            # for asteroid in self.game.get_asteroids():
            #     if asteroid.x - asteroid.radius < self.loc.x < asteroid.x + asteroid.radius and \
            #        asteroid.y - asteroid.radius < self.loc.y < asteroid.y + asteroid.radius:
            #         asteroid.destroyed = True
            #         self.game.deregister(self.obj_id)
            if self.game.check_asteroid_collision(self):
                self.on_destroy()

    def render(self) -> None:
        pg.draw.aaline(self.game.screen, 'white', (self.loc.x, self.loc.y), (self.loc.x-self.dx, self.loc.y-self.dy))
