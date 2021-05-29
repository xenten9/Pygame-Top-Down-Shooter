""" Manage player input, movement mechanics and shooting mechanics. """

import math

import pygame

from config import *
import Projectile

class Player:

    def __init__(self, sprites, text, x, y):
        self.sprites = sprites
        self.text = text
        self.x = x
        self.y = y

        self.health = 100
        self.shoot_cooldown = 0
        self.invincibility = 0
        self.kills = 0

        self.projectiles = []

    def draw(self, screen):
        """ Draw the player on the screen. If the player has been hit recently, draw a red player for a flicker effect. """

        # Create a flicker effect whilst having invincibility.
        if self.invincibility % 2 == 0:
            screen.blit(self.sprites[0], ((SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

        if self.invincibility % 2 == 1:
            screen.blit(self.sprites[1], ((SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

    def display_healthbar(self, screen):
        """ Create a healthbar by multiplying player health times the desired size. """

        pygame.draw.rect(screen, (0, 0, 0), (195, 745, 410, 35))
        pygame.draw.rect(screen, (255, 0, 0), (200, 750, 400, 25))

        if self.health >= 0:
            pygame.draw.rect(screen, (0, 255, 0), (200, 750, self.health * 4, 25))

    def display_kills(self, screen):
        """ Display a number of kills using player kills and the player text font object. """

        kills_label = self.text.render("Kills: {}".format(self.kills), 1, (255, 255, 255))
        screen.blit(kills_label, (700, 20))

    def update(self):

        # Player shoot cooldown.
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Player invincibility.
        if self.invincibility > 0:
            self.invincibility -= 1

    def shoot(self, angle):
        """ Create a projectile object in the direction of the mouse from the center of the screen. """

        # Create a new projectile
        self.projectiles.append(Projectile.Projectile(self.sprites[2],
            self.x + (PLAYER_SIZE / 2) - (PROJECTILE_SIZE / 2), self.y + (PLAYER_SIZE / 2) - (PROJECTILE_SIZE / 2), angle))
        
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN


def movement(player):
    """ Movement for the player. """

    keys = pygame.key.get_pressed()
    x_change = 0
    y_change = 0

    # For debugging.
    if keys[pygame.K_1]:
        print("player x: {}, player y: {}".format(player.x, player.y))

    # For diagonal movement, player speed is divided by root two so that the diagonal speed is not faster
    # then the single directional speed.
    # NORTH WEST
    if keys[pygame.K_w] and keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED / math.sqrt(2), -PLAYER_SPEED / math.sqrt(2))
    # SOUTH WEST
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED / math.sqrt(2), PLAYER_SPEED / math.sqrt(2))
    # NORTH EAST
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED / math.sqrt(2), -PLAYER_SPEED / math.sqrt(2))
    # SOUTH EAST
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED / math.sqrt(2), PLAYER_SPEED / math.sqrt(2))
    # UP
    elif keys[pygame.K_w]:
        x_change, y_change = check_bounds(player, 0, -PLAYER_SPEED)
    # DOWN
    elif keys[pygame.K_s]:
        x_change, y_change = check_bounds(player, 0, PLAYER_SPEED)
    # LEFT
    elif keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED, 0)
    # RIGHT
    elif keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED, 0)

    player.x += x_change
    player.y += y_change

def check_bounds(player, x_change, y_change):
    """ Check if the player exits the bounds of the map. If so, do some math to put the player
    right on the edge.

    Doing something like if player.x < LEFT_BORDER, then player.x = LEFT_BORDER doesn't work because 
    the position of the other objects will not be changed.
    """

    # LEFT BORDER
    if player.x + x_change - (PLAYER_SIZE / 2) < LEFT_BORDER:
        x_change = LEFT_BORDER - player.x + (PLAYER_SIZE / 2)

    # RIGHT BORDER
    if player.x + x_change > RIGHT_BORDER - (PLAYER_SIZE / 2):
        x_change = RIGHT_BORDER - player.x - (PLAYER_SIZE / 2)

    # UPPER BORDER
    if player.y + y_change - (PLAYER_SIZE / 2) < UPPER_BORDER:
        y_change = UPPER_BORDER - player.y + (PLAYER_SIZE / 2)

    # LOWER BORDER
    if player.y + y_change > LOWER_BORDER - (PLAYER_SIZE / 2):
        y_change = LOWER_BORDER - player.y - (PLAYER_SIZE / 2)

    return x_change, y_change

def mouse(player):

    clicks = pygame.mouse.get_pressed()
    position = pygame.mouse.get_pos()

    # If left click and if the shoot cooldown is over.
    if clicks[0]:
        if player.shoot_cooldown == 0:
            angle = math.atan2(position[1] - (SCREEN_SIZE / 2), position[0] - (SCREEN_SIZE / 2))
            player.shoot(angle)

def closest_enemy(player, enemies):
    """ Get the enemies ordered by closest distance. This is needed to figure out what
    enemy the projectile will come in contact with. """

    # Get distance from player.
    for enemy in enemies:
        enemy.distance = enemy.player_distance(player)

    return sorted(enemies, key=lambda enemy: enemy.distance)
