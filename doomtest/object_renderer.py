import pygame
import os
from settings import *

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        
    def draw(self):  
        # order matters. drawn back to front
        self.draw_background()
        self.render_game_objects()
        
    def draw_background(self):
        # TODO: really understand why negative offset is being used here
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH  # why 4.5?
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        
    def render_game_objects(self):
        render_objects = self.game.raycasting.render_objects
        for depth, image, loc in render_objects:
            self.screen.blit(image, loc)
        
    @staticmethod
    def get_texture(texture_file, res=(TEXTURE_SIZE, TEXTURE_SIZE)) -> pygame.Surface:
        assert os.path.exists(TEXTURES_PATH)
        texture = pygame.image.load(os.path.join(TEXTURES_PATH, texture_file)).convert_alpha()
        return pygame.transform.scale(texture, res)
    
    def load_wall_textures(self) -> dict:
        
        return {
            1: self.get_texture('1.png'),
            2: self.get_texture('2.png'),
            3: self.get_texture('3.png'),
        }