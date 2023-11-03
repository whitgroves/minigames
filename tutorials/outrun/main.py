import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
import sys
import math

TITLE = 'Floor It!'
RESOLUTION = WIDTH, HEIGHT = 1024, 768
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
ROAD_W = 2000
SEG_L = 200
CAM_D = 0.84
MAX_SCALE = 5
TEXTURES_PATH = 'outruntest/textures/'
ROAD_LIGHT = pg.Color(107, 107, 107)
ROAD_DARK = pg.Color(105, 105, 105)
GRASS_LIGHT = pg.Color(16, 200, 16)
GRASS_DARK = pg.Color(0, 154, 0)
RUMBLE_LIGHT = pg.Color(255, 255, 255)
RUMBLE_DARK = pg.Color(0, 0, 0)
SPRITE_DESCALE = 250
BG_TILES = 3

class Line:
    def __init__(self) -> None:
        self.x = self.y = self.z = 0.0 # world coordinates
        self.X = self.Y = self.W = 0.0 # screen projection
        self.scale = self.curve = self.sprite_X = self.clip = 0.0
        self.sprite:pg.Surface = None
        self.color_road:pg.Color = 'black'
        self.color_grass:pg.Color = 'black'
        self.color_rumble:pg.Color = 'black'
        
    def project(self, cam_x:int, cam_y:int, cam_z:int) -> None:
        # camera depth scales the size of the xy-plane in focus (read: in view)
        # this depth itself scales with distance between the line and the camera
        self.scale = CAM_D / (self.z - cam_z + 0.0001) # div/0 hazard
        # oversimplified: go to the center of the screen, (optional) turn around
        # then go back (scale * delta x/y)% of the other half (or the original)
        self.X = (1 + self.scale * (self.x - cam_x)) * HALF_WIDTH
        self.Y = (1 - self.scale * (self.y - cam_y)) * HALF_HEIGHT
        # road with is a constant, so that can be scaled in the same way
        # i.e., (scale * width)% of half the screen
        self.W = self.scale * ROAD_W * HALF_WIDTH
        # note that big X is the CENTER of the line (big Y is the top)  
        
    def draw_sprite(self, app:pg.Surface) -> None:
        if self.sprite is None: return
        w = self.sprite.get_width()
        h = self.sprite.get_height()
        dest_X = self.X + self.scale * self.sprite_X * HALF_WIDTH # see project()
        dest_Y = self.Y + 5
        dest_W = w * self.W / SPRITE_DESCALE
        dest_H = h * self.W / SPRITE_DESCALE
        dest_X += dest_W * self.sprite_X
        dest_Y -= dest_H
        clip_H = dest_Y + dest_H - self.clip # hills
        if clip_H < 0: clip_H = 0
        if clip_H >= dest_H: return
        if dest_W >= w: return
        scaled = pg.transform.scale(self.sprite, (dest_W, dest_H))
        cropped = scaled.subsurface(0, 0, dest_W, dest_H - clip_H)
        app.blit(cropped, (dest_X, dest_Y))
# endclass

def draw_quad(w:pg.Surface, c:pg.Color, x1:int, y1:int, w1:int, x2:int, y2:int, w2:int) -> None:
    pg.draw.polygon(surface=w, color=c, points=[(x1 - w1, y1),(x2 - w2, y2),(x2 + w2, y2),(x1 + w1, y1)])

def get_texture(file:str, width:int = 0, height:int = 0) -> pg.Surface:
        assert os.path.exists(TEXTURES_PATH)
        texture = pg.image.load(os.path.join(TEXTURES_PATH, file)).convert_alpha()
        x = texture.get_width() if width == 0 else width
        y = texture.get_height() if height == 0 else height
        return pg.transform.scale(texture, (x, y))

class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.bg_texture:pg.Surface = get_texture('bg.png', width=WIDTH)
        self.bg_image:pg.Surface = pg.Surface((WIDTH * BG_TILES, self.bg_texture.get_height()))
        for i in range(BG_TILES):
            self.bg_image.blit(self.bg_texture, (WIDTH * i, 0))
        self.bg_container:pg.Rect = self.bg_image.get_rect(topleft=(-WIDTH, 0))
        self.screen.blit(self.bg_image, self.bg_container)
        # self.sprites:dict[str:pg.Surface] = {} # { filename : sprite }
        self.sprite_tree:pg.Surface = get_texture('oak.png')
        self.lines:list[Line] = []
        for i in range(1600):
            line = Line()
            line.z = i * SEG_L
            color_switch = (i // 3) % 2
            line.color_road = ROAD_LIGHT if color_switch else ROAD_DARK
            line.color_grass = GRASS_LIGHT if color_switch else GRASS_DARK
            line.color_rumble = RUMBLE_LIGHT if color_switch else RUMBLE_DARK
            if 300 < i < 700: line.curve = 0.5
            if i > 750: line.y = math.sin(i / 30.0) * 1500
            if i > 1100: line.curve = -0.7
            # TODO: multiple scenery sprites
            if i % 20 == 0:
                line.sprite_X = -2.5
                line.sprite = self.sprite_tree
            if i % 20 == 10:
                line.sprite_X = 1.5
                line.sprite = self.sprite_tree
            self.lines.append(line)
        self.N = len(self.lines)
        self.N_scaled = self.N * SEG_L
        self.pos = 0
        self.player_x = 0
        self.player_y = 1500
    
    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
            speed = 0
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]: speed += SEG_L
            if keys[pg.K_DOWN]: speed -= SEG_L
            if keys[pg.K_RIGHT]: self.player_x += 200
            if keys[pg.K_LEFT]: self.player_x -= 200
            if keys[pg.K_w]: self.player_y += 100
            if keys[pg.K_s]: self.player_y -= 100
            if self.player_y < 500: self.player_y = 500
            if keys[pg.K_TAB]: speed *= 2
            self.pos += speed
            self.screen.fill((105, 205, 4)) # prefill so high camera doesn't look weird
            self.screen.blit(self.bg_texture, (0, 0))
            self.pos %= self.N_scaled
            start_pos = self.pos // SEG_L
            end_pos = start_pos + 300
            x = dx = 0.0
            cam_h = self.player_y + self.lines[start_pos].y
            max_Y = HEIGHT
            if speed > 0: self.bg_container.x -= self.lines[start_pos].curve * 2
            elif speed < 0: self.bg_container.x += self.lines[start_pos].curve * 2
            if self.bg_container.right < WIDTH: self.bg_container.x = -WIDTH
            elif self.bg_container.left > 0: self.bg_container.x = -WIDTH
            self.screen.blit(self.bg_image, self.bg_container)
            for n in range(start_pos, end_pos):
                l = self.lines[n % self.N]
                l.project(self.player_x - x, cam_h, self.pos - (self.N_scaled if n >= self.N else 0))
                x += dx
                dx += l.curve
                l.clip = max_Y
                if l.Y >= max_Y: continue # hills
                max_Y = l.Y
                p = self.lines[(n - 1) % self.N]
                draw_quad(self.screen, l.color_grass, 0, p.Y, WIDTH, 0, l.Y, WIDTH)
                draw_quad(self.screen, l.color_rumble, p.X, p.Y, p.W * 1.2, l.X, l.Y, l.W * 1.2)
                draw_quad(self.screen, l.color_road, p.X, p.Y, p.W, l.X, l.Y, l.W)
            for n in range(end_pos, start_pos + 1, -1):
                self.lines[n % self.N].draw_sprite(self.screen)
            self.clock.tick(FPS)
            pg.display.flip()
            pg.display.set_caption(f'{TITLE} - FPS: {self.clock.get_fps():.1f}')
# endclass

if __name__ == '__main__':
    game = Game()
    game.run()
