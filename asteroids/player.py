import math
import pygame as pg
from settings import *
from gameobject import *
from projectile import *

class Player(GameObject, UpdateMixin, RenderMixin):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.loc = pg.Vector2(HALF_WIDTH, HALF_HEIGHT)
        self.vel = pg.Vector2()
        self.accel = 0.02
        self.frict = 0.02
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
            x = self.loc.x  + HALF_PLAYER * math.cos(point + self.angle)
            y = self.loc.y + HALF_PLAYER * math.sin(point + self.angle)
            result.append((x, y))
        return result
    
    def fire_event(self) -> None:
        Projectile(self.game, self.loc.x, self.loc.y, (self.angle - ROT_OFFSET))

    def update(self) -> None:
        x, y = pg.mouse.get_pos()
        self.angle = math.atan2(y-self.loc.y, x-self.loc.x) + ROT_OFFSET
        self.angle %= math.tau # bind to unit circle - [0, 2*pi]

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.vel += pg.Vector2(math.cos(self.angle - ROT_OFFSET), math.sin(self.angle - ROT_OFFSET)) * self.accel * self.game.delta_time

        self.vel *= 1 - self.frict
        # max_speed = MAX_SPEED * self.game.delta_time
        for dv in [self.vel.x, self.vel.y]:
            dv = pg.math.clamp(dv, -MAX_SPEED, MAX_SPEED)
            if dv < 0.0001: dv = 0

        self.loc += self.vel
        self.loc.x = pg.math.clamp(self.loc.x, 0, WIDTH)
        self.loc.y = pg.math.clamp(self.loc.y, 0, HEIGHT)

    def render(self) -> None:
        pg.draw.aalines(self.game.screen, 'white', True, self._points(), 1)
