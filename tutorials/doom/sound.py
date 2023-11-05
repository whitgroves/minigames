import pygame
import os

class Sound:
    def __init__(self, game) -> None:
        self.game = game
        pygame.mixer.init()
        self.base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sounds')
        assert os.path.exists(self.base_path)
        self.shotgun = pygame.mixer.Sound(os.path.join(self.base_path, 'shotgun.wav'))
        self.npc_pain = pygame.mixer.Sound(os.path.join(self.base_path, 'npc_pain.wav'))
        self.npc_death = pygame.mixer.Sound(os.path.join(self.base_path, 'npc_death.wav'))
        self.npc_attack = pygame.mixer.Sound(os.path.join(self.base_path, 'npc_attack.wav'))
        self.player_pain = pygame.mixer.Sound(os.path.join(self.base_path, 'player_pain.wav'))

