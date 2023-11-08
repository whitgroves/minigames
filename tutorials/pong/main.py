import pygame as pg
import sys
import random

TITLE = 'Ping'
RESOLUTION = WIDTH, HEIGHT = 1024, 768
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
L_MARGIN = WIDTH // 20 # 5% of screen
R_MARGIN = WIDTH - L_MARGIN
PADDLE_W = 30
PADDLE_H = 130
MOVE_SPD = HEIGHT // 100 # 1% of screen
BALL_SIZE = 20
MAX_DIFF = (PADDLE_H // 2) - (BALL_SIZE // 2)

def draw_rect(surface:pg.Surface, color:pg.Color, x:int, y:int, width:int, height:int) -> pg.Rect:
    """Draws a <width> by <height> rectangle (pygame.Rect) centered on <x>, <y>."""
    w, h = width // 2, height // 2
    return pg.draw.polygon(surface=surface, color=color,
                           points=[(x-w, y+h), (x+w, y+h), (x+w, y-h), (x-w, y-h)])

def get_random_color() -> pg.Color:
    rgb = [random.randint(0, 255) for i in range(3)]
    return pg.Color(*rgb)

class GameObject:
    def __init__(self, start_x:int, start_y:int, width:int, height:int, color:pg.Color=None) -> None:
        self.x_start = start_x
        self.y_start = start_y
        self.width = width
        self.height = height
        self.reset_position()
        self.color = color if color else get_random_color()
        self.collider = None
    
    def reset_position(self, dx:int=0, dy:int=0) -> None:
        self.x = self.x_start
        self.y = self.y_start
        self.dx = dx
        self.dy = dy

    def update_position(self) -> None:
        self.x += self.dx
        self.y += self.dy

class Player(GameObject):
    def __init__(self, pid:int, key_up:pg.key, key_dn:pg.key, **kwargs:dict) -> None:
        super(Player, self).__init__(start_y=HALF_HEIGHT, width=PADDLE_W, height=PADDLE_H, **kwargs)
        self.pid = pid
        self.key_up = key_up
        self.key_dn = key_dn

    def update_position(self) -> None:
        super().update_position()
        offset = self.height // 2
        self.y = max(self.y, offset)
        self.y = min(self.y, (HEIGHT - offset))

class Game():
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.players = [Player(pid=0, start_x=L_MARGIN, key_up=pg.K_w, key_dn=pg.K_s),
                        Player(pid=1, start_x=R_MARGIN, key_up=pg.K_UP, key_dn=pg.K_DOWN)]
        self.ball = GameObject(start_x=HALF_WIDTH, start_y=HALF_HEIGHT, width=BALL_SIZE, height=BALL_SIZE)
        self.ball.reset_position(dx=(random.choice([-1, 1]) * MOVE_SPD))
        self.game_objects = [self.ball, *self.players]
    
    def run(self) -> None: # game loop
        while True:
            # check for exit
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
            
            # check for score
            if self.ball.x < 0 or self.ball.x > WIDTH:
                print('Score!')
                self.ball.reset_position(dx=((-1 if self.ball.x > WIDTH else 1) * MOVE_SPD), dy=(self.ball.dy // MOVE_SPD))

            # player input
            keys = pg.key.get_pressed()
            for p in self.players:
                if keys[p.key_up]: p.dy = -MOVE_SPD
                elif keys[p.key_dn]: p.dy = MOVE_SPD
                else: p.dy = 0
                p.y += p.dy

            # move and render game objects
            self.screen.fill('black')
            for go in self.game_objects:
                go.update_position()
                go.collider = draw_rect(self.screen, go.color, go.x, go.y, go.width, go.height)

            # vertical boundary for ball
            if self.ball.y < 0 or self.ball.y > HEIGHT:
                self.ball.dy = -self.ball.dy

            # collision detection: https://stackoverflow.com/a/65064907/3178898
            collision = pg.Rect(self.ball.collider).collideobjects(self.players, key=lambda go: go.collider)
            if collision:
                self.ball.dx = -1.1 * self.ball.dx # give it a 10% boost
                y_diff = collision.y - self.ball.y
                y_diff_scaled = y_diff / MAX_DIFF
                self.ball.dy += y_diff_scaled * MOVE_SPD
                self.ball.color = get_random_color()

            # boilerplate
            self.clock.tick(FPS)
            pg.display.flip()
            pg.display.set_caption(f'{TITLE} - FPS: {self.clock.get_fps():.1f}')

if __name__ == '__main__':
    game = Game()
    game.run()
