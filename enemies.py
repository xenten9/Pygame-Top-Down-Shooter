""" Spawn and chase behaviour for enemies. """

import math
import random

from config import *
import player

class EnemyHandler:
    """ Holds lists of enemies and important values for enemies. """

    def __init__(self, sprites):
        self.sprites = sprites

        self.spawn_timer = SPAWN_TIMER

        self.enemies = []
        self.dead_enemies = []

    def spawn(self, player_obj):
        """ If the parameters are satisfied, spawn an enemy. The location for the enemy spawn
        is handled inside of spawn enemy. """

        if self.spawn_timer == 0:
            if len(self.enemies) < MAX_ENEMIES:

                # This is required in case the random spawn quadrant is an invalid location.
                picking_quadrant = True
                while picking_quadrant:
                    spawn_quadrant = random.randint(1, 4)

                    # Spawn left of player.
                    if spawn_quadrant == 1:
                        picking_quadrant = self.horizontal_spawn_area(
                        round(player_obj.x - (SCREEN_SIZE / 2)),
                        LEFT_BORDER,
                        UPPER_BORDER,
                        LOWER_BORDER - ENEMY_SIZE)

                    # Spawn right of player.
                    if spawn_quadrant == 2:
                        picking_quadrant = self.horizontal_spawn_area(
                        RIGHT_BORDER - ENEMY_SIZE, 
                        round(player_obj.x + (SCREEN_SIZE / 2)), 
                        UPPER_BORDER, 
                        LOWER_BORDER - ENEMY_SIZE)

                    # Spawn above player.
                    if spawn_quadrant == 3:
                        picking_quadrant = self.vertical_spawn_area(
                        RIGHT_BORDER - ENEMY_SIZE,
                        LEFT_BORDER,
                        UPPER_BORDER,
                        round(player_obj.y - (SCREEN_SIZE / 2)))

                    # Spawn below player.
                    if spawn_quadrant == 4:
                        picking_quadrant = self.vertical_spawn_area(
                        RIGHT_BORDER - ENEMY_SIZE,
                        LEFT_BORDER,
                        round(player_obj.y + (SCREEN_SIZE / 2)), 
                        LOWER_BORDER - ENEMY_SIZE)

            # Have some variance in spawn rates.
            self.spawn_timer = SPAWN_TIMER + random.randint(-5, 5)

    def horizontal_spawn_area(self, a, b, c, d):
        """ Definitely not nice to read but for now this works. Right now to understand how this works,
        your gonna have to look in the spawn enemy function and look at the function call arguments. """

        if a > b:
            
            while True:
                x_position = random.randint(b, a)
                y_position = random.randint(c, d)
                # Check if the potential spawn location overlaps another enemy. If not, create the enemy.
                overlap = self.spawn_overlap(x_position, y_position)
                if not overlap:
                    self.enemies.append(Chaser(self.sprites[0], x_position, y_position))
                    return False

        return True

    def vertical_spawn_area(self, a, b, c, d):
        """ Definitely not nice to read but for now this works. Right now to understand how this works,
        your gonna have to look in the spawn enemy function and look at the function call arguments. """

        if d > c:
            
            while True:
                x_position = random.randint(b, a)
                y_position = random.randint(c, d)
                # Check if the potential spawn location overlaps another enemy. If not, create the enemy.
                overlap = self.spawn_overlap(x_position, y_position)
                if not overlap:
                    self.enemies.append(Chaser(self.sprites[0], x_position, y_position))
                    return False

        return True

    def spawn_overlap(self, x_position, y_position):
        """ Check that the spawning enemy does not overlap with another enemy. If it does overlap,
        return true. """

        # Get points on potential position.
        points = [(x_position, y_position),
                  (x_position + ENEMY_SIZE, y_position),
                  (x_position, y_position + ENEMY_SIZE),
                  (x_position + ENEMY_SIZE, y_position + ENEMY_SIZE)]

        # Check if potential points overlap with another enemy.
        for enemy in self.enemies:
            for point in points:
                if (point[0] > enemy.x and point[0] < enemy.x + ENEMY_SIZE and 
                    point[1] > enemy.y and point[1] < enemy.y + ENEMY_SIZE):
                    return True

        return False

    def update(self, player_obj):
        """ Calls the chase method for each enemy along with some values that
        need to be decreased by one for every iteration. """

        ordered_enemies = player.closest_enemy(player_obj, self.enemies)

        # Chase the player
        for enemy in ordered_enemies:
            enemy.chase(player_obj, self.enemies)

            # Decrease the time going in a slightly random direction
            if enemy.random_direction_time > 0:
                enemy.random_direction_time -= 1

        # Decrease the time till next spawn
        if self.spawn_timer > 0:
            self.spawn_timer -= 1

        for dead_enemy in self.dead_enemies:
            # Decrease the time a dead enemy is visible for
            if dead_enemy.death_time > 0:
                dead_enemy.death_time -= 1
            # Delete the enemy if that time hits zero
            else:
                self.dead_enemies.remove(dead_enemy)

class Chaser:
    """ One of the enemy types inside of the enemy handler. Chases the player
    and makes attempt to hit them. """

    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.distance = 0
        self.random_direction = 0
        self.random_direction_time = 0

    def draw(self, screen, player_obj):
        """ Draw the chaser enemy relative to the player. """

        # Need to get the displacement of the player from the initial position to determine where the sprite should be drawn
        # relative to the player. 
        screen.blit(self.sprite, (self.x - player_obj.x + (SCREEN_SIZE / 2), self.y - player_obj.y + (SCREEN_SIZE / 2)))

    def player_distance(self, player_obj):
        """ Return the absolute distance to from the player. """

        # Pythagorean Theorem
        return math.sqrt(((player_obj.x - self.x) ** 2) + ((player_obj.y - self.y) ** 2))

    def chase(self, player_obj, enemies):
        """ Chase the player by obtaining the angle between the enemy and the player. Also, apply a bit of randomness
        in that direction whilst not allowing the enemy to exit the bounds or enter another enemy. Also checks if the
        enemy has collided with the player. """

        # Get the angle between the player and the enemy for direction to chase in.
        # Also, apply some randomness to the direction.
        angle = math.atan2(player_obj.y - self.y - (PLAYER_SIZE / 2), player_obj.x - self.x - (PLAYER_SIZE / 2))
        if self.random_direction_time == 0:
            self.random_direction = random.uniform(-math.pi / 3, math.pi / 3)
            self.random_direction_time = ENEMY_RANDOM_DIRECTION_TIME
        angle += self.random_direction

        # Apply the position change
        self.x += ENEMY_SPEED * math.cos(angle)
        self.y += ENEMY_SPEED * math.sin(angle)

        # Check if the position change the enemy it out of bounds
        self.check_bounds(angle)

        # Get points on the enemy after the position change
        points = [(self.x, self.y),
                  (self.x + ENEMY_SIZE, self.y),
                  (self.x, self.y + ENEMY_SIZE),
                  (self.x + ENEMY_SIZE, self.y + ENEMY_SIZE)]

        # Check if the position change causes overlap with other enemies
        self.prevent_overlap(enemies, points, angle)

        # Check if the position change causes overlap with the player
        if player_obj.invincibility == 0:
            self.check_hit_player(player_obj, points)

    def check_shot(self, player_obj, enemy_handler, projectile, points):
        """ Check if the enemy has been shot by the player by checking the points in the projectile
        passed into the function. If so, add the enemy to the dead enemies and increment the kills. """

        # Check for collision.
        for point in points:
            if (point[0] - (ENEMY_SIZE / 2) > self.x and point[0] < self.x + ENEMY_SIZE and 
                point[1] > self.y and point[1] - (ENEMY_SIZE / 2) < self.y + ENEMY_SIZE):

                # Actions for if enemy has been shot.
                player_obj.kills += 1
                enemy_handler.dead_enemies.append(Dead_Enemies(enemy_handler.sprites[1], self.x, self.y, projectile.angle))
                enemy_handler.enemies.remove(self)
                player_obj.projectiles.remove(projectile)
                # Return true that the enemy has been shot
                return True

        return False

    def check_bounds(self, angle):
        """ Check if enemy exits the boundaries of the map. If so, undo the x or y change. """

        if self.x < LEFT_BORDER or self.x > RIGHT_BORDER - ENEMY_SIZE:
            self.x -= ENEMY_SPEED * math.cos(angle)
        if self.y < UPPER_BORDER or self.y > LOWER_BORDER - ENEMY_SIZE:
            self.y -= ENEMY_SPEED * math.sin(angle)

    def prevent_overlap(self, enemies, points, angle):
        """ Prevent overlap with other enemies by comparing the points on the enemy's new position
        and every other enemy spawned. """

        for enemy in enemies:
            if enemy != self:
                for point in points:
                    # If there is overlap, move the enemy back from the position.
                    if (point[0] > enemy.x and point[0] < enemy.x + ENEMY_SIZE and 
                        point[1] > enemy.y and point[1] < enemy.y + ENEMY_SIZE):
                        self.x -= ENEMY_SPEED * math.cos(angle)
                        self.y -= ENEMY_SPEED * math.sin(angle)
                        return

    def check_hit_player(self, player_obj, points):
        """ Check if the enemy comes in contact with the player. """

        # Check for collisions with player.
        for point in points:
            if (point[0] + (PLAYER_SIZE / 2) > player_obj.x and point[0] < player_obj.x + (PLAYER_SIZE / 2) and
                point[1] + (PLAYER_SIZE / 2) > player_obj.y and point[1] < player_obj.y + (PLAYER_SIZE / 2)):
                # Damage the player and give invincibility.
                player_obj.health -= ENEMY_DAMAGE
                player_obj.invincibility = PLAYER_INVINCIBILITY
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
        """ Draw the dead enemy relative to the player. """

        # Need to get the displacement of the player from the initial position to determine where the sprite should be drawn
        # relative to the player. 
        screen.blit(self.sprite, (self.x - player.x + (SCREEN_SIZE / 2), self.y - player.y + (SCREEN_SIZE / 2)))