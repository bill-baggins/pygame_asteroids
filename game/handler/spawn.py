import pygame as pg

from game.asteroid import Asteroid
from game.animated_sizes import AnimatedSize

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