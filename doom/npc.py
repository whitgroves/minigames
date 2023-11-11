from object_sprite import *
from random import randint, random, choice

class NPC(AnimatedObjectSprite):
    def __init__(self, game, file, loc, scale=1, offset=0, animation_time=60):
        super().__init__(game, file, loc, scale, offset, animation_time)
        # state animations
        self.attack_images = self.get_images(os.path.join(self.folder, 'attack'))
        self.death_images = self.get_images(os.path.join(self.folder, 'death'))
        self.idle_images = self.get_images(os.path.join(self.folder, 'idle'))
        self.pain_images = self.get_images(os.path.join(self.folder, 'pain'))
        self.walk_images = self.get_images(os.path.join(self.folder, 'walk'))
        # characteristics
        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.line_of_sight = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.attack_damage = 10
        
    def update(self):
        self.check_animation_time()
        self.get_image()
        self.do_stuff()
        # self.draw()       # 2D mode
        
    def no_collision(self, x:int, y:int) -> bool:
        return (x, y) not in self.game.map.world_map
    
    def safe_move(self, dx:float, dy:float) -> None:
        # increments don't depend on delta time, so no lerp needed
        if self.no_collision(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.no_collision(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
        
    def movement(self):
        next_loc = self.game.pathfinding.get_path(self.map_loc, self.game.player.map_loc)
        next_x, next_y = next_loc
        # pygame.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))  # 2D mode
        if next_loc not in self.game.object_manager.npc_locs:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)  # the angle if this NPC looked at the center of the next_loc block
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.safe_move(dx, dy)
            
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:  # just like gamefreak used to do
                self.game.player.take_damage(self.attack_damage)
        
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
     
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
        
    def check_if_hit(self):
        if self.line_of_sight and self.game.player.shooting:
            # TODO: understand why self.screen_x is used here
            if HALF_WIDTH - self.half_width < self.screen_x < HALF_WIDTH + self.half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shooting = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
                
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()
        
    def do_stuff(self):
        if self.alive:
            self.line_of_sight = self.raycast_hit()
            self.check_if_hit()
            if self.pain:
                self.animate_pain()
            elif self.line_of_sight:
                self.player_search_trigger = True   # cue skyrim music
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_loc(self):
        return int(self.x), int(self.y)
    
    # TODO: generalize and make into a component
    def raycast_hit(self) -> bool:
        if self.game.player.map_loc == self.map_loc:
            return True  # easy out if we're in the same block
        
        # this time we find distance between nearest wall / the player and this NPC
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        player_x, player_y = self.game.player.loc
        x_loc, y_loc = self.game.player.map_loc
        ray_angle = self.theta
        cos_a = math.cos(ray_angle)  # used to find movement along x-axis
        sin_a = math.sin(ray_angle)  # used to find movement along y-axis
        
        # vertical intersections
        vert_x, vert_dx = (x_loc + 1, 1) if cos_a > 0 else (x_loc - 1e-6, -1)
        vert_depth = (vert_x - player_x) / cos_a    # div/0 hazard 1
        vert_y = player_y + vert_depth * sin_a
        vert_delta = vert_dx / cos_a
        vert_dy = vert_delta * sin_a
        for i in range(MAX_DEPTH):
            vert_loc = int(vert_x), int(vert_y)
            if vert_loc == self.map_loc:
                player_dist_v = vert_depth
                break
            if vert_loc in self.game.map.world_map:
                wall_dist_v = vert_depth
                break
            vert_x += vert_dx
            vert_y += vert_dy
            vert_depth += vert_delta
            
        # horizontal intersections
        horz_y, horz_dy = (y_loc + 1, 1) if sin_a > 0 else (y_loc - 1e-6, -1)
        horz_depth = (horz_y - player_y) / sin_a    # div/0 hazard 2
        horz_x = player_x + horz_depth * cos_a
        horz_delta = horz_dy / sin_a
        horz_dx = horz_delta * cos_a
        for i in range(MAX_DEPTH):
            horz_loc = int(horz_x), int(horz_y)
            if horz_loc == self.map_loc:
                player_dist_h = horz_depth
                break
            if horz_loc in self.game.map.world_map:
                wall_dist_h = horz_depth
                break
            horz_x += horz_dx
            horz_y += horz_dy
            horz_depth += horz_delta
        
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)
        
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw(self):
        pygame.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.raycast_hit():
            pygame.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                            (100 * self.x, 100 * self.y), 2)