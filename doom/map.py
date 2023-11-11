import pygame

# truthy == wall, falsy == space
_ = False    # human readability
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, 3, 3, 3, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, 3, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, 3, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
    def __init__(self, game) -> None:
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        
    def get_map(self) -> None:
        for y, row in enumerate(self.mini_map):
            for x, val in enumerate(row):
                if val:
                    self.world_map[(x, y)] = val
                    
    def draw(self) -> None:
        [pygame.draw.rect(self.game.screen, 'darkgray', (loc[0] * 100, loc[1] * 100, 100, 100), 2)
         for loc in self.world_map]