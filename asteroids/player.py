import math
import pygame as pg
from settings import *
from gameobject import *
from projectile import *

class Player(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game) -> None:
        super().__init__(game)
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
            x = self.x  + HALF_PLAYER * math.cos(point + self.angle)
            y = self.y + HALF_PLAYER * math.sin(point + self.angle)
            result.append((x, y))
        return result
    
    def fire_event(self) -> None:
        Projectile(self.game, self.x, self.y, (self.angle - ROT_OFFSET))

    def update(self) -> None:
        x, y = pg.mouse.get_pos()
        self.angle = math.atan2(y-self.y, x-self.x) + ROT_OFFSET
        self.angle %= math.tau # bind to unit circle - [0, 2*pi]

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 1)
