import math

TITLE = 'Comets'

# display
RESOLUTION = WIDTH, HEIGHT = 1024, 768
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# player
PLAYER_SIZE = 32 # player is inscribed in a circle
HALF_PLAYER = PLAYER_SIZE // 2
QUTR_PLAYER = HALF_PLAYER // 2
ROT_UNIT = 0.0174533 # 1 degree in radians
ROT_SPEED = 0.5 * ROT_UNIT
TRIANGLE = [(3 * math.pi / 2), (math.pi / 4), (3 * math.pi / 4)] # see Player._points()
