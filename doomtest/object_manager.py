from object_sprite import *

class ObjectManager:
    def __init__(self, game) -> None:
        self.game = game
        self.sprites = []
        add_sprite = self.add_sprite
        # sprite map (is it done this way because we're in init??)
        add_sprite(ObjectSprite(game, 'candlebra.png', (10.5, 3.5), 0.7, 0.27))
        add_sprite(AnimatedObjectSprite(game, 'green_candle/0.png', (11.5, 3.5), 0.8, 0.15, 120))
        
    def update(self):
        [sprite.update() for sprite in self.sprites]
    
    def add_sprite(self, sprite: ObjectSprite):
        self.sprites.append(sprite)