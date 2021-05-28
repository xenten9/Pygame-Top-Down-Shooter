#! /usr/bin/env python3
""" Basic shooting game using pygame. """

import pygame

from config import *
import Player
import Enemies
import Projectile
import Display

def manage_time(player, enemies, dead_enemies, clock):

    # Iterate every 1 / 60 seconds
    clock.tick(60)

    if player.shoot_cooldown > 0:
        player.shoot_cooldown -= 1

    if player.invincibility > 0:
        player.invincibility -= 1

    if player.spawn_timer > 0:
        player.spawn_timer -= 1

    for enemy in enemies:
        if enemy.random_direction_time > 0:
            enemy.random_direction_time -= 1

    for dead_enemy in dead_enemies:
        if dead_enemy.death_time > 0:
            dead_enemy.death_time -= 1
        else:
            dead_enemies.remove(dead_enemy)

def main():

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()

    assets = Display.load_assets()
    tiles = Display.create_map(assets)

    player = Player.Player([assets["shooter"], assets["player"]], (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2), (SCREEN_SIZE / 2) - (PLAYER_SIZE / 2))

    enemies = []
    dead_enemies = []

    alive = True
    while alive:

        # Time
        manage_time(player, enemies, dead_enemies, clock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        # Player
        Player.movement(player)
        Player.mouse(player, assets)

        # Enemy
        Enemies.spawn(player, enemies, assets)
        Enemies.behaviour(player, enemies)

        # Projectile
        Projectile.move_projectiles(player)
        Projectile.check_collisions(player, enemies, dead_enemies, assets)

        # Screen
        Display.draw_screen(screen, player, enemies, dead_enemies, tiles, assets)

main()