#! /usr/bin/env python3
""" File to run to play the game. """

import sys
import time

import pygame

from config import *
import player
import enemies
import projectile
import display

def game_loop(screen, player_obj, enemy_handler, tiles, clock):

    alive = True
    while alive:

        # Iterate every 1 / 60 seconds.
        # This means that a cooldown of 60 is translated to a cooldown of 1 second...
        clock.tick(60)

        # If the player quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Player movement and shooting
        player_obj.movement()
        player_obj.mouse()
        player_obj.update()

        # Enemy spawning and movement behaviour
        enemy_handler.spawn(player_obj)
        enemy_handler.update(player_obj)

        # Projectile movement and collision checking
        projectile.move_projectiles(player_obj)
        projectile.check_collisions(player_obj, enemy_handler)

        # Screen drawing
        display.draw_screen(screen, player_obj, enemy_handler, tiles)

        # Checking if player dies
        if player_obj.health <= 0:
            alive = reset(player_obj, enemy_handler)

def reset(player_obj, enemy_handler):
    """ Resets attributes in player and enemy classes to what they
    were on startup. """

    # Reset player health, kills, projectiles, and position
    player_obj.health = 100
    player_obj.kills = 0
    player_obj.projectiles = []
    player_obj.x = (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)
    player_obj.y = (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2)

    # Reset enemies
    enemy_handler.enemies = []
    enemy_handler.dead_enemies = []

    return False

def main():
    """ Initializes pygame and contains the main game loop. Eventually the game loop will be separated
    out into a function and main will call it. """

    # Initialize pygame, pygame.font, a screen, and a clock.
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()

    # Fonts and texts
    kills_font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    startup_font = pygame.font.SysFont(pygame.font.get_default_font(), 75)
    death_font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    startup_text = startup_font.render("Press any key to play.", 1, (255, 255, 255))
    death_text1 = startup_font.render("You Died.", 1, (255, 255, 255))
    death_text2 = death_font.render("Press any key to play again.", 1, (255, 255, 255))

    # Load assets and create map
    assets = display.load_assets()
    tiles = display.create_map(assets)

    # Create the player
    player_obj = player.Player([assets["player"], assets["player_hit"], assets["player_projectile"]], 
        kills_font,
        (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2))

    # Create the enemy handler
    enemy_handler = enemies.EnemyHandler([assets["chaser"], assets["dead_enemy"]])

    # This is here just so on startup a screen can be seen
    display.draw_screen(screen, player_obj, enemy_handler, tiles)

    # Draw the startup text
    screen.blit(startup_text, (130, 100))
    pygame.display.update()

    # Loop is here so if the player dies, they can quickly start again
    while True:

        # If the player quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # If the player presses any key, start the game loop
        clicks = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        for key in keys:
            if key or clicks[0] or clicks[1] or clicks[2]:
                game_loop(screen, player_obj, enemy_handler, tiles, clock)

                # Draw the death text
                screen.blit(death_text1, (300, 125))
                screen.blit(death_text2, (180, 550))
                pygame.display.update()

                # Weird bug where if the game is started using mouse input, the game will immediately start again.
                clicks = [0, 0, 0]

                time.sleep(1)

main()