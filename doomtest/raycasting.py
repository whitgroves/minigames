import pygame
import math
from settings import *

class Raycasting:
    def __init__(self, game) -> None:
        self.game = game
        
    def get_render_objects(self) -> None:
        pass
        
    def raycast(self) -> None:
        player_x, player_y = self.game.player.loc
        x_loc, y_loc = self.game.player.map_loc
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # avoids div/0 errors
        for j in range(NUM_RAYS):
            cos_a = math.cos(ray_angle)     # used to find movement along x-axis
            sin_a = math.sin(ray_angle)     # used to find movement along y-axis
            
            # vertical intersections
            # use the ray angle and the player's location to derive the distance between
            # the player and the edge of the next vertical boundary along that ray by 
            # drawing triangles along its length between each column of blocks and using
            # basic trig to calculate the total length of the triangles' hypotenii
            vert_x, vert_dx = (x_loc + 1, 1) if cos_a > 0 else (x_loc - 1e-6, -1)
            vert_depth = (vert_x - player_x) / cos_a    # div/0 hazard 1
            vert_y = player_y + vert_depth * sin_a
            vert_delta = vert_dx / cos_a
            vert_dy = vert_delta * sin_a
            for i in range(MAX_DEPTH):
                map_loc = int(vert_x), int(vert_y)
                if map_loc in self.game.map.world_map:
                    break
                vert_x += vert_dx
                vert_y += vert_dy
                vert_depth += vert_delta
                
            # horizontal intersections
            # same as above, but looking for horizontal boundaries along each row instead
            # effectively this swaps how we treat x and y TODO: generalize this code
            horz_y, horz_dy = (y_loc + 1, 1) if sin_a > 0 else (y_loc - 1e-6, -1)
            horz_depth = (horz_y - player_y) / sin_a    # div/0 hazard 2
            horz_x = player_x + horz_depth * cos_a
            horz_delta = horz_dy / sin_a
            horz_dx = horz_delta * cos_a
            for i in range(MAX_DEPTH):
                map_loc = int(horz_x), int(horz_y)
                if map_loc in self.game.map.world_map:
                    break
                horz_x += horz_dx
                horz_y += horz_dy
                horz_depth += horz_delta
            
            # hit distance
            depth = min(vert_depth, horz_depth)
            
            # debug
            pygame.draw.line(self.game.screen, 'yellow', (100 * player_x, 100 * player_y),
                            (100 * player_x + 100 * depth * cos_a, 
                             100 * player_y + 100 * depth * sin_a), 2)
            
            # increment to end loop
            ray_angle += DELTA_ANGLE
            
    
    def update(self) -> None:
        self.raycast()
        self.get_render_objects()