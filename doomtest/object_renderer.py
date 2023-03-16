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
        self.damage_screen = self.get_texture('blood_screen.png', RESOLUTION)
        self.health_size = 90
        self.health_images = [self.get_texture(f'digits/{i}.png', [self.health_size] * 2) for i in range(11)]
        self.health_dict = dict(zip(map(str, range(11)), self.health_images))
        self.game_over_screen = self.get_texture('game_over.png', RESOLUTION)
        
    def draw(self):  
        # order matters. drawn back to front
        self.draw_background()
        self.render_game_objects()
        self.draw_health()
        
    def game_over(self):
        self.screen.blit(self.game_over_screen, (0, 0)) 
        
    def draw_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.health_dict[char], (i * self.health_size, 0))
        self.screen.blit(self.health_dict['10'], ((i + 1) * self.health_size, 0))
        
    def player_damage(self):
        self.screen.blit(self.damage_screen, (0, 0))
        
    def draw_background(self):
        # TODO: really understand why negative offset is being used here
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH  # why 4.5?
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
        
    def render_game_objects(self):
        # sort by depth (first index), starting with objects farthest away
        render_objects = sorted(self.game.raycasting.render_objects, key=lambda obj: obj[0], reverse=True)
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