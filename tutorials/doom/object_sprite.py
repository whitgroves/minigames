import pygame
import os
from collections import deque
from settings import *

class ObjectSprite:
    def __init__(self, game, file, loc, scale=1, offset=0):
        self.game = game
        self.player = game.player
        self.x, self.y = loc
        images = deque()
        target = os.path.join(os.path.abspath(os.path.dirname(__file__)), SPRITES_PATH)
        assert os.path.exists(target)
        self.image = pygame.image.load(os.path.join(target, file)).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.HALF_IMAGE_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        # attributes needed to be treated as a render object TODO:inheritance/components
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.half_width = 0  # initialization
        self.VERT_SCALE = scale
        self.HEIGHT_OFFSET = offset
        
    def get_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.VERT_SCALE  # get the vertical scale like w/ raycasting
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        image = pygame.transform.scale(self.image, (proj_width, proj_height))
        self.half_width = proj_width // 2
        height_offset = proj_height * self.HEIGHT_OFFSET
        loc = self.screen_x - self.half_width, HALF_HEIGHT - proj_height // 2 + height_offset
        self.game.raycasting.render_objects.append((self.norm_dist, image, loc))  # TODO: data class
    
    def get_image(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)
        delta = self.theta - self.player.angle
        # TODO: figure out how/why everything below this line works
        # https://youtu.be/ECqUrT7IdqQ?si=FWPyA0SyzY4Rp5FK&t=382
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau  
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.HALF_IMAGE_WIDTH < self.screen_x < (WIDTH + self.HALF_IMAGE_WIDTH) and self.norm_dist > 0.5:
            self.get_projection()
    
    def update(self):
        self.get_image()
        
        
class AnimatedObjectSprite(ObjectSprite):
    def __init__(self, game, file, loc, scale=1, offset=0, animation_time=60):
        super().__init__(game, file, loc, scale, offset)
        self.animation_time = animation_time
        self.folder = file.rsplit('/', 1)[0]
        self.images = self.get_images(self.folder)
        self.animation_time_prev = pygame.time.get_ticks() # starting frame of reference
        self.animation_trigger = False
        
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
        
    def animate(self, images: deque):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0] 
        
    def check_animation_time(self): # reset the animation trigger so it can loop
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
        
    def get_images(self, folder):
        images = deque()
        target = os.path.join(os.path.abspath(os.path.dirname(__file__)), SPRITES_PATH)
        assert os.path.exists(target)
        for filename in os.listdir(os.path.join(target, folder)):
            filepath = os.path.join(target, folder, filename)
            if os.path.isfile(filepath):
                img = pygame.image.load(filepath).convert_alpha()
                images.append(img)
        return images