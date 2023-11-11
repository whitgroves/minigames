import math
import pygame as pg
from game import GameBase, GameConfigBase
from gameobject import GameObject, GameObjectManager, RenderMixin

class Line(GameObject, RenderMixin):
    def __init__(self, manager: GameObjectManager, c:pg.Color, w:int, h:int, **kwargs) -> None:
        super().__init__(manager, **kwargs)
        self.color = c
        self.width = w
        self.height = h

    def _points(self) -> None:
        return [(self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height)]

    def render(self) -> None:
        pg.draw.polygon(surface=self.manager.screen, color=self.color, points=self._points())

STAR_UNIT = (2 * math.pi / 5)
STAR = [0, STAR_UNIT, 2 * STAR_UNIT, 3 * STAR_UNIT, 4 * STAR_UNIT]
STAR_OFFSET = (math.pi / 2)

class Star(GameObject, RenderMixin):
    def __init__(self, manager: GameObjectManager, c:pg.Color, r:int, **kwargs) -> None:
        super().__init__(manager, **kwargs)
        self.color = c
        self.radius = r  

    def _points(self) -> list[tuple[int, int]]:
        result = []
        for point in STAR:
            x = self.x + self.radius * math.cos(point - STAR_OFFSET)
            y = self.y + self.radius * math.sin(point - STAR_OFFSET)
            result.append((x, y))
            result.append((self.x, self.y))
        return result

    def render(self) -> None:
        pg.draw.lines(surface=self.manager.screen, color=self.color, points=self._points(), closed=True, width=3)

class GameConfig(GameConfigBase):
    RESOLUTION = 1600, 900
    BG = 'deepskyblue3'

class Game(GameBase, GameObjectManager):
    def __init__(self, config: GameConfigBase) -> None:
        GameBase.__init__(self, config)
        GameObjectManager.__init__(self)
        self.flag()

    def flag(self) -> None:
        h = 30
        x = 400
        y_offset = 200
        for i in range(13):
            w = 800
            w1 = 0
            if i < 7:
                w1 = 300
                w -= w1
                Line(self, 'blue4', w=w1, h=h, x=x, y=y_offset+(i*h))
            color = 'red3' if i % 2 == 0 else 'whitesmoke'
            Line(self, color, w=w, h=h, x=x+w1, y=y_offset+(i*h))
        for i in range(9):
            r = h / 4
            y1 = y_offset + (i * (h * 7 / 9)) + r * STAR_OFFSET
            for j in range(11):
                if j % 2 == i % 2:
                    x1 = x + (j * (300 / 11)) + r * STAR_OFFSET
                    Star(self, 'white', r=r, x=x1, y=y1)

    def on_render(self) -> None:
        [obj.render() for obj in self.game_objects.values() if isinstance(obj, RenderMixin)]

if __name__ == '__main__':
    game = Game(GameConfig)
    game.run()