import pygame
import math
from settings import *

class Raycasting:
    def __init__(self, game) -> None:
        self.game = game
        self.raycast_result = []
        self.render_objects = []
        self.textures = self.game.object_renderer.wall_textures
    
    # uses raycast data to slice up textures and provide image scaling data for the object renderer
    def get_render_objects(self) -> None:
        self.render_objects = []
        for ray, values in enumerate(self.raycast_result):
            depth, proj_height, texture, offset = values  # TODO: create data class for this
            
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_loc = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height  # edge case for close distances
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_loc = (ray * SCALE, 0)
            
            self.render_objects.append((depth, wall_column, wall_loc))
        
    def raycast(self) -> None:
        player_x, player_y = self.game.player.loc
        x_loc, y_loc = self.game.player.map_loc
        vert_texture, horz_texture = 1, 1
        self.raycast_result = []
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # avoids div/0 errors
        for ray in range(NUM_RAYS):
            cos_a = math.cos(ray_angle)  # used to find movement along x-axis
            sin_a = math.sin(ray_angle)  # used to find movement along y-axis
            
            # vertical intersections
            # use the ray angle and the player's location to derive the distance between
            # the player and the edge of the next vertical boundary along that ray by 
            # drawing triangles along its length between each column of blocks, then use
            # trigonometry to calculate the total length of the triangles' hypotenii
            vert_x, vert_dx = (x_loc + 1, 1) if cos_a > 0 else (x_loc - 1e-6, -1)
            vert_depth = (vert_x - player_x) / cos_a    # div/0 hazard 1
            vert_y = player_y + vert_depth * sin_a
            vert_delta = vert_dx / cos_a
            vert_dy = vert_delta * sin_a
            for i in range(MAX_DEPTH):
                vert_loc = int(vert_x), int(vert_y)
                if vert_loc in self.game.map.world_map:
                    vert_texture = self.game.map.world_map[vert_loc]
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
                horz_loc = int(horz_x), int(horz_y)
                if horz_loc in self.game.map.world_map:
                    horz_texture = self.game.map.world_map[horz_loc]
                    break
                horz_x += horz_dx
                horz_y += horz_dy
                horz_depth += horz_delta
            
            # 3D projetion data
            # use the (screen) WIDTH and FOV settings to derive the screen's distance from the 
            # player, then use that distance and the hit depth to determine the scale of the wall 
            # projection, which texture to render, and the texture offset for each vertical slice
            if vert_depth < horz_depth:
                hit_depth, texture = vert_depth, vert_texture
                vert_y %= 1
                offset = vert_y if cos_a > 0 else (1 - vert_y)
            else:
                hit_depth, texture = horz_depth, horz_texture
                horz_x %= 1
                offset = (1 - horz_x) if sin_a > 0 else horz_x
            hit_depth *= math.cos(self.game.player.angle - ray_angle) # adjust for fishbowl effect
            proj_height = SCREEN_DIST / (hit_depth + 0.0001)          # div/0 hazard 3

            # store hit data & move to next ray
            self.raycast_result.append((hit_depth, proj_height, texture, offset))
            ray_angle += DELTA_ANGLE
    
    def update(self) -> None:
        self.raycast()
        self.get_render_objects()