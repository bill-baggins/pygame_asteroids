import pygame as pg

import globals
from game.handler.surface import SurfaceHandler
from game.animated_sizes import AnimatedSize
from game.handler.audio import AudioHandler
from game.laser import Laser
from common.math import to_rad

from random import randrange


class Asteroid:
    
    surf: pg.Surface
    size: AnimatedSize

    origin: pg.Vector2
    origin_rec: pg.Rect
    origin_rec_color: pg.Color

    hitbox: pg.Rect
    hitbox_color: pg.Color

    vel: pg.Vector2

    accelerate: float
    deceleration_factor: float

    __frame_counter: float
    __frame_update_speed: float
    __frame_counter_limit: float


    __frame_width: int
    __frame_height: int

    __current_frame_x: int
    __current_frame_y: int

    __number_of_frames_x: int
    __number_of_frames_y: int
    
    def __init__(self, screen: pg.Surface, animated_size: AnimatedSize, x: int = None, y: int = None):
        self.original_surf = SurfaceHandler.get_asteroid_surf(animated_size)
        self.size = animated_size

        self.__frame_counter = 0.0
        self.__frame_update_speed = 20
        self.__frame_counter_limit = 1

        self.__frame_width = self.original_surf.get_width() / 16
        self.__frame_height = self.original_surf.get_height() / 2

        self.__current_frame_x = 0
        self.__current_frame_y = 0

        self.__number_of_frames_x = 16
        self.__number_of_frames_y = 2

        
        self.surf = self.original_surf.subsurface([0, 0], [self.__frame_width, self.__frame_height])

        # Determine spawning location. Spawning location is random if the x and y arguments for
        # the contructor are None.
        if x is None and y is None:
            spawn_points = [
                [-50, -50],
                [screen.get_width() + 50, -50],
                [-50, screen.get_height() + 50],
                [screen.get_width() + 50, screen.get_height() + 50]
            ]
            
            self.origin = pg.Vector2(spawn_points[randrange(0, spawn_points.__len__())])
        else:
            self.origin = pg.Vector2(x, y)
        
        self.origin_rec = pg.Rect(
            self.origin.x - self.surf.get_width(), self.origin.y - self.surf.get_height(),
            self.surf.get_width(), self.surf.get_height()
        )
        self.origin_rec_color = pg.Color("blue")

        self.hitbox = pg.Rect(
            self.origin_rec.width // 2, self.origin_rec.height // 2,
            self.surf.get_width(), self.surf.get_height()
        )
        self.hitbox_color = pg.Color("red")

        self.vel = pg.Vector2(randrange(-100, 100), randrange(-100, 100))
        if self.vel.x == 0:
            self.vel.x = 50
        if self.vel.y == 0:
            self.vel.y = 50

    def update(self, screen: pg.Surface, dt: float):
        self.__update_asteroid_animation_frame(dt)
        self.__move(screen, dt)

    def draw(self, screen: pg.Surface):
        screen.blit(
            self.surf,
            [self.origin_rec.x - (self.surf.get_width() >> 1),
             self.origin_rec.y - (self.surf.get_height() >> 1)]
        )
        if globals.debug_mode:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, width=1)

    def __update_asteroid_animation_frame(self, dt: float):
        self.__frame_counter += self.__frame_update_speed * dt

        if self.__frame_counter > self.__frame_counter_limit:
            self.__frame_counter = 0

            if self.__current_frame_y == self.__number_of_frames_y:
                self.__current_frame_y = 0

            if self.__current_frame_x == self.__number_of_frames_x:
                self.__current_frame_x = 0

            self.surf = self.original_surf.subsurface([self.__current_frame_x * self.__frame_width,
                                                       self.__current_frame_y * self.__frame_height],
                                                      [self.__frame_width, 
                                                       self.__frame_height])
            self.__current_frame_x += 1
            self.__current_frame_y += 1

    def __move(self, screen: pg.Surface, dt: float):
        left_bound = -self.surf.get_width()
        right_bound = screen.get_width() + self.surf.get_width()
        top_bound = -self.surf.get_height()
        bottom_bound = screen.get_height() + self.surf.get_height()
        
        if self.origin.x < left_bound:
            self.origin.x = right_bound
        elif self.origin.x > right_bound:
            self.origin.x = left_bound

        # Teleport the ship along the y-axis at the screen border.
        if self.origin.y < top_bound:
            self.origin.y = bottom_bound
        elif self.origin.y > bottom_bound:
            self.origin.y = top_bound

        self.origin += self.vel * dt
        self.origin_rec.x = self.origin.x
        self.origin_rec.y = self.origin.y
        self.hitbox.x = self.origin_rec.x - self.origin_rec.width // 2
        self.hitbox.y = self.origin_rec.y - self.origin_rec.height // 2
    

"""
Class attributes that I commented out:


"""