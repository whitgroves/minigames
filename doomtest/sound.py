import pygame
import os

class Sound:
    def __init__(self, game) -> None:
        self.game = game
        pygame.mixer.init()
        self.base_path = 'doomtest/sounds/'
        assert os.path.exists(self.base_path)
        self.shotgun = pygame.mixer.Sound(os.path.join(self.base_path, 'shotgun.wav'))
        
