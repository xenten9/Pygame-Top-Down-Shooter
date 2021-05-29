""" Mostly configurable values for player, enemies, projectiles, powerups, tiles and screen. """

# Screen
# The screen size can be changed without completely breaking the game but I don't see a reason to
SCREEN_SIZE = 800
# Definitely don't change
LEFT_BORDER = -200
RIGHT_BORDER = 1000
UPPER_BORDER = -200
LOWER_BORDER = 1000

# Player
# These can be changed
PLAYER_SPEED = 10
PLAYER_SHOOT_COOLDOWN = 10
PLAYER_INVINCIBILITY = 60
PLAYER_KNOCKBACK = 25
SPAWN_TIMER = 20
PLAYER_SIZE = 50

# Enemy
# These can be changed
ENEMY_SPEED = 8
ENEMY_DAMAGE = 10
ENEMY_RANDOM_DIRECTION_TIME = 30
ENEMY_DEATH_TIME = 30
MAX_ENEMIES = 30
# Don't change yet. Eventually this will be able to be changed.
ENEMY_SIZE = 50

# Tiles
# Definitely don't change
TILE_SIZE = 200

# Projectile
# Can be changed
PROJECTILE_SPEED = 25
# Don't change
PROJECTILE_SIZE = 15

# Powerup
POWERUP_SIZE = 25

