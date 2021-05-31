""" Manage projectile movement and collision detection. """

import math

from config import *
import player

class Projectile:

    def __init__(self, sprite, x, y, angle):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self, screen, player_obj):

        # Need to get the displacement of the player from the initial position to determine where the sprite should be drawn
        # relative to the player.
        screen.blit(self.sprite, (self.x - player_obj.x + (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), self.y - player_obj.y + (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

    def move(self):
        """ Move the projectile using the angle. """

        self.x += PROJECTILE_SPEED * math.cos(self.angle)
        self.y += PROJECTILE_SPEED * math.sin(self.angle)

def move_projectiles(player_obj):
    """ Move the projectiles and check if the projectile runs into a wall. """

    for projectile in player_obj.projectiles:
        projectile.move()

        # If the projectile collides with a wall.
        # LEFT BORDER
        if projectile.x - PROJECTILE_SIZE < LEFT_BORDER:
            player_obj.projectiles.remove(projectile)

        # RIGHT BORDER
        elif projectile.x > RIGHT_BORDER + PROJECTILE_SIZE:
            player_obj.projectiles.remove(projectile)

        # UPPER BORDER
        elif projectile.y - PROJECTILE_SIZE < UPPER_BORDER:
            player_obj.projectiles.remove(projectile)

        # LOWER BORDER
        elif projectile.y > LOWER_BORDER + PROJECTILE_SIZE:
            player_obj.projectiles.remove(projectile)

def check_collisions(player_obj, enemy_handler):
    """ Check if the projectiles collide with any enemies. """

    # Needed to determine which enemy is shot first.
    ordered_enemies = player.closest_enemy(player_obj, enemy_handler.enemies)

    for projectile in player_obj.projectiles:
        points = [(projectile.x, projectile.y),
                  (projectile.x + PROJECTILE_SIZE, projectile.y),
                  (projectile.x, projectile.y + PROJECTILE_SIZE),
                  (projectile.x + PROJECTILE_SIZE, projectile.y + PROJECTILE_SIZE)]

        for enemy in enemy_handler.enemies:
            enemy_shot = enemy.check_shot(player_obj, enemy_handler, projectile, points)
            if enemy_shot:
                break
            




