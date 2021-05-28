""" Spawn and chase behaviour for enemies. """

import math
import random

from config import *
import Player

class Chaser:

    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.distance = 0
        self.random_direction = 0
        self.random_direction_time = 0

    def draw(self, screen, player):

        # Need to get the displacement of the player from the initial position to determine where the sprite should be drawn
        # relative to the player. Problem arises from having player in the center of the screen.
        screen.blit(self.sprite, (self.x - player.x + (SCREEN_SIZE / 2), self.y - player.y + (SCREEN_SIZE / 2)))

    def player_distance(self, player):
        """ Get the distance from the player. """

        # Pythagorean Theorem
        return math.sqrt(((player.x - self.x) ** 2) + ((player.y - self.y) ** 2))

    def chase(self, player, enemies):
        """ Chase the player with some randomness. Prevent stepping outside of bounds and into other enemies. """

        # Get angle between enemy and center of player.
        angle = math.atan2(player.y - self.y - (PLAYER_SIZE / 2), player.x - self.x - (PLAYER_SIZE / 2))

        # Get randomness in direction.
        if self.random_direction_time == 0:
            self.random_direction = random.uniform(-math.pi / 3, math.pi / 3)
            self.random_direction_time = ENEMY_RANDOM_DIRECTION_TIME
        angle += self.random_direction

        # Apply change in position.
        self.x += ENEMY_SPEED * math.cos(angle)
        self.y += ENEMY_SPEED * math.sin(angle)

        check_bounds(self, angle)

        # Get new points on enemy.
        points = [(self.x, self.y),
                  (self.x + ENEMY_SIZE, self.y),
                  (self.x, self.y + ENEMY_SIZE),
                  (self.x + ENEMY_SIZE, self.y + ENEMY_SIZE)]

        # Check if causes overlap.
        prevent_overlap(self, enemies, points, angle)

        if player.invincibility == 0:
            check_hit_player(player, self, points, enemies)

    def check_shot(self, player, enemies, dead_enemies, projectile, points, assets):
        """ Check if enemy has been shot by a player. If so, create a dead enemy. """

        # Check for collision.
        for point in points:
            if (point[0] - 25 > self.x and point[0] < self.x + ENEMY_SIZE and 
                point[1] > self.y and point[1] - 25 < self.y + ENEMY_SIZE):

                # Actions for if enemy has been shot.
                dead_enemies.append(Dead_Enemies(assets["shooter"], self.x, self.y, projectile.angle))
                player.kills += 1

                # For some reason, sometimes the player projectile will be removed twice and cause an index error.
                # This is the easiest solution, but something better would be good.
                try:
                    player.projectiles.remove(projectile)
                except:
                    pass

                enemies.remove(self)
                return

class Dead_Enemies:

    def __init__(self, sprite, x, y, angle):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.angle = angle
        self.death_time = ENEMY_DEATH_TIME

        # Apply knockback to the enemy using the projectile angle.
        self.x += PLAYER_KNOCKBACK * math.cos(angle)
        self.y += PLAYER_KNOCKBACK * math.sin(angle)

    def draw(self, screen, player):

        screen.blit(self.sprite, (self.x - player.x + (SCREEN_SIZE / 2), self.y - player.y + (SCREEN_SIZE / 2)))

def spawn_overlap(enemies, x_position, y_position):
    """ Check that the spawning enemy does not overlap with another enemy. """

    # Get points on potential position.
    points = [(x_position, y_position),
              (x_position + ENEMY_SIZE, y_position),
              (x_position, y_position + ENEMY_SIZE),
              (x_position + ENEMY_SIZE, y_position + ENEMY_SIZE)]

    # Check if potential points overlap with another enemy.
    for enemy in enemies:
        for point in points:
            if (point[0] > enemy.x and point[0] < enemy.x + ENEMY_SIZE and 
                point[1] > enemy.y and point[1] < enemy.y + ENEMY_SIZE):
                return True

    return False

def behaviour(player, enemies):
    """ Behaviour for the enemies. """

    # Get closest enemy to player to mitigate enemies getting stuck on one another.
    # Move the enemy closest to the player in order to get the one on the front moving first.
    ordered_enemies = Player.closest_enemy(player, enemies)

    for enemy in ordered_enemies:
        if isinstance(enemy, Chaser):
            enemy.chase(player, enemies)

def check_bounds(enemy, angle):
    """ Check if enemy exits the boundaries of the map. If so, under the x or y change. """

    # Left and right border.
    if enemy.x < LEFT_BORDER or enemy.x > RIGHT_BORDER - ENEMY_SIZE:
        enemy.x -= ENEMY_SPEED * math.cos(angle)
    # Upper and lower border.
    if enemy.y < UPPER_BORDER or enemy.y > LOWER_BORDER - ENEMY_SIZE:
        enemy.y -= ENEMY_SPEED * math.sin(angle)

def prevent_overlap(self, enemies, points, angle):
    """ Prevent overlap with other enemies. """

    # Check if that enemy has now just entered another enemy.
    # If so, bring it back.
    for enemy in enemies:
        if enemy != self:
            for point in points:
                # If the enemy overlaps, bring in back.
                if (point[0] > enemy.x and point[0] < enemy.x + ENEMY_SIZE and 
                    point[1] > enemy.y and point[1] < enemy.y + ENEMY_SIZE):
                    self.x -= ENEMY_SPEED * math.cos(angle)
                    self.y -= ENEMY_SPEED * math.sin(angle)
                    return

def check_hit_player(player, enemy, points, enemies):
    """ Check if the enemy comes in contact with the player. """

    # Check for collisions with player.
    for point in points:
        if (point[0] + (PLAYER_SIZE / 2) > player.x and point[0] < player.x + (PLAYER_SIZE / 2) and
            point[1] + (PLAYER_SIZE / 2) > player.y and point[1] < player.y + (PLAYER_SIZE / 2)):
            # Damage player and give invincibility.
            player.health -= ENEMY_DAMAGE
            player.invincibility = PLAYER_INVINCIBILITY
            return

def spawn(player, enemies, assets):
    """ Spawn behaviour for the enemies. Used to make enemies spawn off screen, not out of bounds, and not inside another enemy. 

    This definitely needs to be cleaned up using four different function calls. Probably will need to be done a better way. """

    if len(enemies) < MAX_ENEMIES:

        if player.spawn_timer == 0:

            # This is required in case the random spawn quadrant is an invalid location.
            picking_quadrant = True
            while picking_quadrant:
                spawn_quadrant = random.randint(1, 4)
                # Spawn left of player.
                if spawn_quadrant == 1:
                    if player.x - (SCREEN_SIZE / 2) > LEFT_BORDER:
                        picking_quadrant = False
                        # Make sure that enemy does not spawn inside of another enemy.
                        while True:
                            x_position = random.randint(LEFT_BORDER, round(player.x) - round(SCREEN_SIZE / 2))
                            y_position = random.randint(UPPER_BORDER, LOWER_BORDER - ENEMY_SIZE)
                            overlap = spawn_overlap(enemies, x_position, y_position)
                            if not overlap:
                                enemies.append(Chaser(assets["chaser"], x_position, y_position))
                                break

                # Spawn right of player.
                if spawn_quadrant == 2:
                    if player.x + (SCREEN_SIZE / 2) < RIGHT_BORDER - 50:
                        picking_quadrant = False
                        # Make sure that enemy does not spawn inside of another enemy.
                        while True:
                            x_position = random.randint(round(player.x) + round(SCREEN_SIZE / 2), RIGHT_BORDER - ENEMY_SIZE)
                            y_position = random.randint(UPPER_BORDER, LOWER_BORDER - ENEMY_SIZE)
                            overlap = spawn_overlap(enemies, x_position, y_position)
                            if not overlap:
                                enemies.append(Chaser(assets["chaser"], x_position, y_position))
                                break

                # Spawn above player.
                if spawn_quadrant == 3:
                    if player.y - (SCREEN_SIZE / 2) > UPPER_BORDER:
                        picking_quadrant = False
                        # Make sure that enemy does not spawn inside of another enemy.
                        while True:
                            x_position = random.randint(LEFT_BORDER, RIGHT_BORDER - ENEMY_SIZE)
                            y_position = random.randint(UPPER_BORDER, round(player.y) - round(SCREEN_SIZE / 2))
                            overlap = spawn_overlap(enemies, x_position, y_position)
                            if not overlap:
                                enemies.append(Chaser(assets["chaser"], x_position, y_position))
                                break

                # Spawn below player.
                if spawn_quadrant == 4:
                    if player.y + (SCREEN_SIZE / 2) < LOWER_BORDER - 50:
                        picking_quadrant = False
                        # Make sure that enemy does not spawn inside of another enemy.
                        while True:
                            x_position = random.randint(LEFT_BORDER, RIGHT_BORDER - ENEMY_SIZE)
                            y_position = random.randint(round(player.y) + round(SCREEN_SIZE / 2), LOWER_BORDER - ENEMY_SIZE)
                            overlap = spawn_overlap(enemies, x_position, y_position)
                            if not overlap:
                                enemies.append(Chaser(assets["chaser"], x_position, y_position))
                                break

            # Have some variance in spawn rates.
            player.spawn_timer = SPAWN_TIMER + random.randint(-5, 5)

    return enemies


