import math

# display
RESOLUTION = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0
FLOOR_COLOR = (30, 30, 30)

# player
PLAYER_LOC = 1.5, 5.0
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SCALE = 60
PLAYER_MAX_HEALTH = 100

# mouse
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40  # max relative movement
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# raycasting
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # scale down to calculate
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# projection
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS  # scale up to display

# textures
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
TEXTURES_PATH = 'textures'

# sprites
SPRITES_PATH = 'sprites'