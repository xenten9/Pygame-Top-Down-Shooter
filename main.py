#! /usr/bin/env python3
""" File to run to play the game. """

import pygame

from config import *
import Player
import Enemies
import Projectile
import Display

def main():
    """ Initializes pygame and contains the main game loop. Eventually the game loop will be separated
    out into a function and main will call it. """

    # Initialize pygame, pygame.font, a screen, and a clock.
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()

    # Load assets and create map
    assets = Display.load_assets()
    tiles = Display.create_map(assets)

    # Create the player
    player = Player.Player([assets["player"], assets["player_hit"], assets["player_projectile"]], 
        pygame.font.SysFont(pygame.font.get_default_font(), 30),
        (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2))

    # Create the enemy handler
    enemy_handler = Enemies.EnemyHandler([assets["chaser"], assets["dead_enemy"]])

    alive = True
    while alive:

        # Iterate every 1 / 60 seconds.
        # This means that a cooldown of 60 is translated to a cooldown of 1 second...
        clock.tick(60)

        # If the player quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        # Player
        Player.movement(player)
        Player.mouse(player)
        player.update()

        # Enemy
        enemy_handler.spawn(player)
        enemy_handler.update(player)

        # Projectile
        Projectile.move_projectiles(player)
        Projectile.check_collisions(player, enemy_handler)

        # Screen
        Display.draw_screen(screen, player, enemy_handler, tiles)

main()