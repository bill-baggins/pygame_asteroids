# spawn.py: Handles the spawning of asteroids, explosions, and the player.

import pygame as pg

from game.background import Background
from game.asteroid import Asteroid
from game.animated_sizes import AnimatedSize
from game.ship import Ship

from globals import GameMode
import globals

class SpawnHandler:
    count: float = 0
    count_limit: float = 10
    max_number_of_large_asteroids: int = 8
    
    @classmethod
    def spawn_asteroids(cls, screen: pg.Surface, asteroid_list: 'list[Asteroid]', dt: float):
        # Prevent the screen from getting recked with lots of asteroids.
        number_of_large_asteroids = 0
        for asteroid in asteroid_list:
            if asteroid.size == AnimatedSize.Large:
                number_of_large_asteroids += 1
        if number_of_large_asteroids > cls.max_number_of_large_asteroids:
            return
        
        cls.count += dt
        if cls.count >= cls.count_limit:
            cls.count = 0
            asteroid_list.append(Asteroid(screen, AnimatedSize.Large))
    
    @classmethod
    def respawn_player(cls, 
                       screen: pg.Surface, 
                       background: Background, 
                       ship: Ship, 
                       asteroid_list: 'list[Asteroid]'):

        background = Background()
        ship = Ship(screen, 0.35)
        asteroid_list = [Asteroid(screen, AnimatedSize.Large) for _ in range(4)]
        globals.game_mode = GameMode.Running
        return background, ship, asteroid_list