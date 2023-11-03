from object_sprite import *
from npc import *

class ObjectManager:
    def __init__(self, game) -> None:
        self.game = game
        self.sprites = []
        self.npcs = []
        self.npc_locs = set()
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        # sprite map (is it done this way because we're in init??)
        add_sprite(ObjectSprite(game, 'candlebra.png', (10.5, 3.5), 0.7, 0.27))
        add_sprite(AnimatedObjectSprite(game, 'green_candle/0.png', (11.5, 3.5), 0.8, 0.15, 120))
        # npc map (same question as above)
        add_npc(NPC(game, 'soldier/0.png', (10.5, 5.5), 0.6, 0.38, 180))
        add_npc(NPC(game, 'soldier/0.png', (11.5, 4.5), 0.6, 0.38, 180))
        
    def update(self):
        self.npc_locs = {npc.map_loc for npc in self.npcs if npc.alive}
        [sprite.update() for sprite in self.sprites]
        [npc.update() for npc in self.npcs]
    
    def add_sprite(self, sprite: ObjectSprite):
        self.sprites.append(sprite)
        
    def add_npc(self, npc: NPC):
        self.npcs.append(npc)