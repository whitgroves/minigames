import sys
import pygame as pg

class GameConfigBase:
    TITLE = 'Pygame'
    RESOLUTION = (1024, 768)
    FPS = 60
    BG = 'black'

class GameBase:
    def __init__(self, config:GameConfigBase) -> None:
        pg.init()
        self.config = config
        self.screen = pg.display.set_mode(self.config.RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 1

    # virtual methods - override these to implement game loop logic

    def on_game_loop_start(self) -> None:
        pass

    def on_event(self, event:pg.event.Event) -> None:
        pass

    def on_update(self) -> None:
        pass

    def on_render(self) -> None:
        pass

    def on_game_loop_end(self) -> None:
        pass

    # internal methods - do not override; use the on_<step> methods instead

    def _events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.on_event(event)

    def _update(self) -> None:
        self.on_update()
        pg.display.flip()
        self.delta_time = self.clock.tick(self.config.FPS)
        pg.display.set_caption(f'{self.config.TITLE} - FPS: {self.clock.get_fps():.1f}')

    def _render(self) -> None:
        self.screen.fill(self.config.BG)
        self.on_render()

    # run - do not override; use the on_<step> methods instead
    
    def run(self) -> None:
        while True:
            self.on_game_loop_start()
            self._events()
            self._update()
            self._render()
            self.on_game_loop_end()
