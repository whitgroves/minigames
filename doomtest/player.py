from settings import *
import pygame
import math

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_LOC
        self.angle = PLAYER_ANGLE
        
    def movement(self) -> None:
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time 
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pygame.K_d]:
            dx -= speed_sin
            dy += speed_cos
        
        self.safe_move(dx, dy)
        
        # delta_rot = PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pygame.K_LEFT]:
        #     self.angle -= delta_rot
        # if keys[pygame.K_RIGHT]:
        #     self.angle += delta_rot
        self.angle %= math.tau  # bound angle between 0 and tau (== 2 * pi)
    
    def no_collision(self, x:int, y:int) -> bool:
        return (x, y) not in self.game.map.world_map
    
    def safe_move(self, dx:float, dy:float) -> None:
        scale = PLAYER_SCALE / self.game.delta_time  # inverted delta time scale needed for dx, dy
        if self.no_collision(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.no_collision(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def draw(self) -> None:
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
        
    def mouse_input(self):
        # TODO: understand how pygame.mouse works
        x, y = pygame.mouse.get_pos()
        if x < MOUSE_BORDER_LEFT or x > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
    
    def update(self) -> None:
        self.movement()
        self.mouse_input()
        
    @property
    def loc(self) -> tuple[float, float]:
        return self.x, self.y
    
    @property
    def map_loc(self) -> tuple [int, int]:
        return int(self.x), int(self.y)