import pygame as pg
import math

import config

from game.handler.surface import SurfaceHandler
from common.math import to_rad


class Laser:
    surf: pg.Surface

    origin: pg.Vector2
    origin_rec: pg.Rect
    origin_rec_color: pg.Color

    hitbox: pg.Rect
    hitbox_color: pg.Color

    vel: float
    rotation: float

    is_out_of_bounds: bool

    def __init__(self, 
                 x: float, 
                 y: float, 
                 rotation: float):
        
        self.surf = SurfaceHandler.laser
        self.surf = pg.transform.scale(
            self.surf,
            [SurfaceHandler.laser.get_width() // 15,
             SurfaceHandler.laser.get_height() // 15]
        )

        self.origin = pg.Vector2(x, y)
        self.vel = 350

        self.origin_rec = pg.Rect(
            self.origin.x, self.origin.y,
            self.surf.get_width(), self.surf.get_height()
        )
        self.origin_rec_color = pg.Color("gold")

        # The actual hitbox.
        self.hitbox = pg.Rect(
            self.origin_rec.x - self.surf.get_width() / 2,
            self.origin_rec.y - self.surf.get_height() / 2,
            self.surf.get_width(),
            self.surf.get_height()
        )

        self.hitbox_color = pg.Color("red")
        self.rotation = rotation
        self.surf = pg.transform.rotate(self.surf, self.rotation)

        self.is_out_of_bounds = False


    def update(self, sw: int, sh: int, dt: float):
        self.__check_bounds(sw, sh)

        self.origin.x -= math.cos(to_rad(self.rotation - 90.0)) * self.vel * dt
        self.origin.y -= math.sin(to_rad(self.rotation + 90.0)) * self.vel * dt
        self.origin_rec.x = self.origin.x
        self.origin_rec.y = self.origin.y
        self.hitbox.x = self.origin_rec.x - self.origin_rec.width / 2
        self.hitbox.y = self.origin_rec.y - self.origin_rec.height / 2

    def draw(self, screen: pg.Surface):
        screen.blit(
            self.surf,
            (self.origin_rec.x - int(self.surf.get_width() / 2),
             self.origin_rec.y - int(self.surf.get_height() / 2))
        )

        if config.debug_mode:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, 1)
    
    def __check_bounds(self, sw: int, sh: int):
        if self.origin.x < -self.origin_rec.width or \
                self.origin.x > sw + self.origin_rec.width // 2 or \
                self.origin.y < -self.origin_rec.height or \
                self.origin.y > sh + self.origin_rec.height // 2:

               self.is_out_of_bounds = True
