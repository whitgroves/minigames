import math
import pygame as pg
from gameobject import *
from settings import *

class Player(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game) -> None:
        super(Player, self).__init__(game)
        self.x = HALF_WIDTH
        self.y = HALF_HEIGHT
        self.angle = 0

    def _points(self):
        # https://stackoverflow.com/a/32576209/3178898
        # we draw the triangle by mapping its points relative to a unit circle
        # since each point is defined by its angle (in radians), we can add 
        # self.angle to effect a rotation, then move them back into global space.
        # NOTE: because the screen is drawn top-to-bottom, the triangle is 
        # inscribed upside-down and rotates clockwise with increases in theta.
        result = []
        for point in TRIANGLE:
            x = HALF_WIDTH  + HALF_PLAYER * math.cos(point + self.angle)
            y = HALF_HEIGHT + HALF_PLAYER * math.sin(point + self.angle)
            result.append((x, y))
        return result

    def update(self) -> None:
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.angle -= ROT_SPEED * self.game.delta_time
        if keys[pg.K_d]:
            self.angle += ROT_SPEED * self.game.delta_time
        self.angle %= math.tau # bind to unit circle - [0, 2*pi]

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 1)