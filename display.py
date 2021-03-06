""" Load assets, create map and draw screen for the game. """

import pygame

from config import *

class Tile:

    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y

    def draw(self, screen, player):

        # Need to get the displacement of the player from the initial position to determine where the sprite should be drawn
        # relative to the player. 
        screen.blit(self.sprite, (self.x - player.x + (SCREEN_SIZE / 2), self.y - player.y + (SCREEN_SIZE / 2)))


def load_assets():
    """ Load assets and return a dictionary with the name of the assets as the keys and the pygame image objects as the values. """

    assets = dict()

    # Load player assets
    assets["player"] = pygame.transform.scale(pygame.image.load("assets/player.png"), (PLAYER_SIZE, PLAYER_SIZE))
    assets["player_hit"] = pygame.transform.scale(pygame.image.load("assets/shooter.png"), (PLAYER_SIZE, PLAYER_SIZE))
    assets["player_projectile"] = pygame.transform.scale(pygame.image.load("assets/player.png"), (PROJECTILE_SIZE, PROJECTILE_SIZE))

    # Load the enemy assets
    assets["chaser"] = pygame.transform.scale(pygame.image.load("assets/chaser.png"), (ENEMY_SIZE, ENEMY_SIZE))
    assets["shooter_projectile"] = pygame.transform.scale(pygame.image.load("assets/shooter.png"), (PROJECTILE_SIZE, PROJECTILE_SIZE))
    assets["dead_enemy"] = pygame.transform.scale(pygame.image.load("assets/shooter.png"), (ENEMY_SIZE, ENEMY_SIZE))

    # Load the map assets
    assets["floor_tile"] = pygame.transform.scale(pygame.image.load("assets/floor_tile.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile1"] = pygame.transform.scale(pygame.image.load("assets/wall_tile1.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile2"] = pygame.transform.scale(pygame.image.load("assets/wall_tile2.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile3"] = pygame.transform.scale(pygame.image.load("assets/wall_tile3.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile4"] = pygame.transform.scale(pygame.image.load("assets/wall_tile4.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile5"] = pygame.transform.scale(pygame.image.load("assets/wall_tile5.png"), (TILE_SIZE, TILE_SIZE))
    assets["wall_tile6"] = pygame.transform.scale(pygame.image.load("assets/wall_tile6.png"), (TILE_SIZE, TILE_SIZE))

    # Load the powerup assets
    assets["heart"] = pygame.transform.scale(pygame.image.load("assets/shooter.png"), (POWERUP_SIZE, POWERUP_SIZE))

    return assets

def create_map(assets):
    """ Create a map by returning a list of tile objects. """

    tiles = []

    # Corner tiles
    tiles.append(Tile(assets["wall_tile2"], LEFT_BORDER - 200, UPPER_BORDER - 200))
    tiles.append(Tile(assets["wall_tile3"], RIGHT_BORDER, UPPER_BORDER - 200))

    # Upper tiles with grass
    for width in range(8):
        tiles.append(Tile(assets["wall_tile6"], width * TILE_SIZE + LEFT_BORDER - 200, UPPER_BORDER - 400))

    # Upper tiles with cliff face
    for width in range(6):
        tiles.append(Tile(assets["wall_tile1"], width * TILE_SIZE + LEFT_BORDER, UPPER_BORDER - 200))

    # Left side with cliff face
    for height in range(6):
        tiles.append(Tile(assets["wall_tile4"], LEFT_BORDER - TILE_SIZE, height * TILE_SIZE - 200))

    # Left side with grass
    for height in range(8):
        tiles.append(Tile(assets["wall_tile6"], LEFT_BORDER - 400, height * TILE_SIZE - 600))

    # Right side with cliff face
    for height in range(6):
        tiles.append(Tile(assets["wall_tile5"], RIGHT_BORDER, height * TILE_SIZE - 200))

    # Right side with grass
    for height in range(8):
        tiles.append(Tile(assets["wall_tile6"], RIGHT_BORDER + 200, height * TILE_SIZE - 600))

    # Bottom tiles with grass
    for width in range(10):
        for height in range(2):
            tiles.append(Tile(assets["wall_tile6"], width * TILE_SIZE - 600, height * TILE_SIZE + LOWER_BORDER))

    # Floor tiles with grass
    for width in range(6):
        for height in range(6):
            tiles.append(Tile(assets["floor_tile"], width * TILE_SIZE - 200, height * TILE_SIZE - 200))

    return tiles

def draw_screen(screen, player_obj, enemy_handler, tiles):
    """ Draw the screen using the tiles, dead enemies, player_projectiles, enemies, and player in
    that specific order. """

    # Draw the map tiles.
    for tile in tiles:
        tile.draw(screen, player_obj)

    # Draw the dead enemies.
    for dead_enemy in enemy_handler.dead_enemies:
        dead_enemy.draw(screen, player_obj)

    # Draw the player projectiles.
    for projectile in player_obj.projectiles:
        projectile.draw(screen, player_obj)

    # Draw the enemies.
    for enemy in enemy_handler.enemies:
        enemy.draw(screen, player_obj)

    # Draw the player and other player things
    player_obj.draw(screen)
    player_obj.display_healthbar(screen)
    player_obj.display_kills(screen)

    pygame.display.update()