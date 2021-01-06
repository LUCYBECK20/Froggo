"""
Constants for Froggo

Author: Lucy Beck
Date: January 2, 2021
"""

### WINDOW CONSTANTS (all coordinates are in pixels) ###

# The initial width of the game display
GAME_WIDTH  = 704
# The initial height of the game display
GAME_HEIGHT = 640
# The size in pixels of a single grid square
GRID_SIZE    = 64


### IMAGE CONSTANTS ###
# The image file for the frog facing North
FROG_NORTH = 'frog_north.png'
# The image file for the frog facing South
FROG_SOUTH = 'frog_south.png'
# The image file for the frog facing East
FROG_EAST = 'frog_east.png'
# The image file for the frog facing West
FROG_WEST = 'frog_west.png'
# The image file for a safe frog
FROG_SAFE   = 'safe.png'
# The image file for a frog life
FROG_HEAD   = 'frog1.png'


### SPEED CONSTANTS ###
# The number of seconds that a frog movement takes
FROG_SPEED  = 0.25
# The number of seconds for a death animation
DEATH_SPEED  = 0.5
# The number of seconds for a turtle animation
TURTLE_SPEED = 3


### GAME CONSTANTS ###

# The state before the game has started
STATE_INACTIVE = 0
# The state when we are loading in a new level
STATE_LOADING  = 1
# The state when the level is activated and in play
STATE_ACTIVE   = 2
# The state when we are are paused between lives
STATE_PAUSED   = 3
# The state when we restoring the frog
STATE_CONTINUE = 4
# The state when the game is complete (won or lost)
STATE_COMPLETE = 5


### FONT CONSTANTS ###

OFFICIAL_FONT = 'KeeponTruckin.ttf'
LARGE_FONT  = 100
MEDIUM_FONT = 60
SMALL_FONT  = 48


### SOUND EFFECTS ###

RIBBIT_SOUND = 'ribbit.wav'
SQUISH_SOUND = 'squish.wav'
ACTIVATION_SOUND = 'activation.wav'


### JSON FILES ###

LEVEL_1 = 'level1.json'
LEVEL_2 = 'level2.json'
LEVEL_3 = 'level3.json'
LEVEL_4 = 'level4.json'
LEVEL_5 = 'level5.json'
LEVEL_6 = 'level6.json'
LEVEL_7 = 'level7.json'
