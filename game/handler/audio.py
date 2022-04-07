import pygame as pg
import numpy as np

from game.animated_sizes import AnimatedSize


class AudioHandler:
    ship_fire: pg.mixer.Sound
    
    small_explosion: pg.mixer.Sound
    medium_explosion: pg.mixer.Sound
    large_explosion: pg.mixer.Sound
    
    ship_hit: pg.mixer.Sound

    explosion_dict: 'dict[AnimatedSize, pg.mixer.Sound]'
    
    @classmethod
    def init(cls):
        cls.ship_fire = pg.mixer.Sound("resource/laser.wav")
        cls.ship_hit = pg.mixer.Sound("resource/ship_hit.wav")
        
        cls.small_explosion = pg.mixer.Sound("resource/explosion.wav")
        cls.medium_explosion = pg.mixer.Sound("resource/medium_explosion.wav")
        cls.large_explosion = pg.mixer.Sound("resource/large_explosion.wav")

        cls.explosion_dict = {
            AnimatedSize.Large: cls.large_explosion,
            AnimatedSize.Medium: cls.medium_explosion,
            AnimatedSize.Small: cls.small_explosion
        }
    

    def get_explosion_sound(cls, size: AnimatedSize) -> pg.mixer.Sound:
        return cls.explosion_dict.get(size)
