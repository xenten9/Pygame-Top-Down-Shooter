
import math

from config import *
import Player

class Projectile:

    def __init__(self, sprite, x, y, angle):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self, screen, player):

        screen.blit(self.sprite, (self.x - player.x + (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), self.y - player.y + (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)))

    def move(self):

        self.x += PROJECTILE_SPEED * math.cos(self.angle)
        self.y += PROJECTILE_SPEED * math.sin(self.angle)

def move_projectiles(player):

    for projectile in player.projectiles:
        projectile.move()

        # If the projectile collides with a wall
        if projectile.x - PROJECTILE_SIZE < LEFT_BORDER:
            player.projectiles.remove(projectile)
        elif projectile.x > RIGHT_BORDER + PROJECTILE_SIZE:
            player.projectiles.remove(projectile)
        elif projectile.y - PROJECTILE_SIZE < UPPER_BORDER:
            player.projectiles.remove(projectile)
        elif projectile.y > LOWER_BORDER + PROJECTILE_SIZE:
            player.projectiles.remove(projectile)

def check_collisions(player, enemies, dead_enemies, assets):

    # Needed to determine which enemy is shot first
    ordered_enemies = Player.closest_enemy(player, enemies)

    for projectile in player.projectiles:
        points = [(projectile.x, projectile.y),
                  (projectile.x + PROJECTILE_SIZE, projectile.y),
                  (projectile.x, projectile.y + PROJECTILE_SIZE),
                  (projectile.x + PROJECTILE_SIZE, projectile.y + PROJECTILE_SIZE)]

        for enemy in enemies:
            enemy.check_shot(player, enemies, dead_enemies, projectile, points, assets)
            




