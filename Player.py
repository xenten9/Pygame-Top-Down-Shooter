
import math

import pygame

from config import *
import Projectile

class Player:

    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.x = x
        self.y = y
        self.health = 100
        self.shoot_cooldown = 0
        self.invincibility = 0
        self.spawn_timer = SPAWN_TIMER
        self.kills = 0

        self.projectiles = []

    def draw(self, screen):
        
        # Create a flicker effect when having invincibility
        if self.invincibility % 2 == 0:
            screen.blit(self.sprites[1], ((SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

        if self.invincibility % 2 == 1:
            screen.blit(self.sprites[0], ((SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

    def display_healthbar(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), (195, 745, 410, 35))
        pygame.draw.rect(screen, (255, 0, 0), (200, 750, 400, 25))

        if self.health >= 0:
            pygame.draw.rect(screen, (0, 255, 0), (200, 750, self.health * 4, 25))

    def display_kills(self, screen, assets):

        kills_label = assets["font"].render("Kills: {}".format(self.kills), 1, (255, 255, 255))

        screen.blit(kills_label, (700, 20))

    def shoot(self, assets, angle):
        """ If player shoots. """

        self.projectiles.append(Projectile.Projectile(assets["player_projectile"],
            self.x + (PLAYER_SIZE / 2) - (PROJECTILE_SIZE / 2), self.y + (PLAYER_SIZE / 2) - (PROJECTILE_SIZE / 2), angle))
        
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

def movement(player):
    """ Movement for the player. """

    keys = pygame.key.get_pressed()
    x_change = 0
    y_change = 0

    if keys[pygame.K_1]:
        print("player x: {}, player y: {}".format(player.x, player.y))

    if keys[pygame.K_w] and keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED / math.sqrt(2), -PLAYER_SPEED / math.sqrt(2))
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED / math.sqrt(2), PLAYER_SPEED / math.sqrt(2))
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED / math.sqrt(2), -PLAYER_SPEED / math.sqrt(2))
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED / math.sqrt(2), PLAYER_SPEED / math.sqrt(2))

    elif keys[pygame.K_w]:
        x_change, y_change = check_bounds(player, 0, -PLAYER_SPEED)
    elif keys[pygame.K_s]:
        x_change, y_change = check_bounds(player, 0, PLAYER_SPEED)
    elif keys[pygame.K_a]:
        x_change, y_change = check_bounds(player, -PLAYER_SPEED, 0)
    elif keys[pygame.K_d]:
        x_change, y_change = check_bounds(player, PLAYER_SPEED, 0)

    player.x += x_change
    player.y += y_change

def check_bounds(player, x_change, y_change):

    if player.x + x_change - (PLAYER_SIZE / 2) < LEFT_BORDER:
        x_change = LEFT_BORDER - player.x + (PLAYER_SIZE / 2)

    if player.x + x_change > RIGHT_BORDER - (PLAYER_SIZE / 2):
        x_change = RIGHT_BORDER - player.x - (PLAYER_SIZE / 2)

    if player.y + y_change - (PLAYER_SIZE / 2) < UPPER_BORDER:
        y_change = UPPER_BORDER - player.y + (PLAYER_SIZE / 2)

    if player.y + y_change > LOWER_BORDER - (PLAYER_SIZE / 2):
        y_change = LOWER_BORDER - player.y - (PLAYER_SIZE / 2)

    return x_change, y_change

def mouse(player, assets):

    clicks = pygame.mouse.get_pressed()
    position = pygame.mouse.get_pos()

    if clicks[0]:
        if player.shoot_cooldown == 0:
            angle = math.atan2(position[1] - (SCREEN_SIZE / 2), position[0] - (SCREEN_SIZE / 2))
            player.shoot(assets, angle)

def closest_enemy(player, enemies):
    """ Get the enemies ordered by closest distance. This is needed to figure out what
    enemy the projectile will come in contact with. """

    # Get distance from player
    for enemy in enemies:
        enemy.distance = enemy.player_distance(player)

    return sorted(enemies, key=lambda enemy: enemy.distance)
