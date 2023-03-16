from settings import *
import pygame
import math

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_LOC
        self.angle = PLAYER_ANGLE
        self.shooting = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.prev_time = pygame.time.get_ticks()
        
    def recover_health(self):
        if self.check_health_recovery() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1
        
    def check_health_recovery(self) -> bool:
        now = pygame.time.get_ticks()
        if now - self.prev_time > self.health_recovery_delay:
            self.prev_time = now
            return True
        
    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pygame.display.flip()
            pygame.time.delay(1500)
            self.game.new_game()
        
    def take_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()
        
    def fire_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shooting and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shooting = True
                self.game.weapon.reloading = True
                
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
        
        self.angle %= math.tau  # keep angle between 0 and tau (== 2 * pi)
    
    def no_collision(self, x:int, y:int) -> bool:
        return (x, y) not in self.game.map.world_map
    
    def safe_move(self, dx:float, dy:float) -> None:
        scale = PLAYER_SCALE / self.game.delta_time  # inverted delta time scale needed for dx, dy
        if self.no_collision(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.no_collision(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def draw(self) -> None:
        pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                        (self.x * 100 + WIDTH * math.cos(self.angle),
                         self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
        
    def mouse_input(self):
        x, y = pygame.mouse.get_pos()
        if x < MOUSE_BORDER_LEFT or x > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
    
    def update(self) -> None:
        self.movement()
        self.mouse_input()
        self.recover_health()
        
    @property
    def loc(self) -> tuple[float, float]:
        return self.x, self.y
    
    @property
    def map_loc(self) -> tuple [int, int]:
        return int(self.x), int(self.y)