import pygame as pg

from game.animated_sizes import AnimatedSize
from game.handler.surface import SurfaceHandler
from game.handler.audio import AudioHandler


class Explosion:
    def __init__(self, screen: pg.Surface, size: AnimatedSize):
        AudioHandler.get_explosion_sound(size).play()
        self.original_surface = SurfaceHandler.get_explosion_surf(size)
        