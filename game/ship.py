import pygame as pg
import math

import config

from game.handler.surface import SurfaceHandler
from game.handler.audio import AudioHandler
from game.laser import Laser
from common.math import to_rad


class Ship:
    original_surf: pg.Surface
    surf: pg.Surface

    origin: pg.Vector2
    origin_rec: pg.Rect
    origin_rec_color: pg.Color

    hitbox: pg.Rect
    hitbox_color: pg.Color

    rotation: float
    delta_rotate: float
    vel: float
    max_vel: float
    
    accelerate: float
    deceleration_factor: float

    key_set: 'dict[int, bool]'

    laser: 'list[Laser]'
    got_hit: bool

    _screen_width: int
    _screen_height: int
    
    _got_hit_time_counter: int
    _got_hit_time_limit: int

    """
    Public methods.
    """
    def __init__(self, screen: pg.Surface, scale: float):
        self.original_surf = SurfaceHandler.ship

        self.original_surf = pg.transform.scale(
            self.original_surf,
            [int(self.original_surf.get_width() * scale),
             int(self.original_surf.get_height() * scale)]
        )

        # Where the ship surface gets drawn.
        self.origin = pg.Vector2(config.screen_width // 2, config.screen_height // 2)
        self.surf = self.original_surf.copy()

        # The rectangle which the surface rotates around.
        self.origin_rec = pg.Rect(
            self.origin.x - self.surf.get_width(), self.origin.y - self.surf.get_height(),
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

        self.rotation = 0.0
        self.delta_rotate = 150
        self.vel = 0
        self.max_vel = 200

        self.accelerate = 300
        self.deceleration_factor = 0.96

        # This is where input logic gets stored.
        self.key_set = {
            pg.K_w: False,
            pg.K_a: False,
            pg.K_d: False,
            pg.K_UP: False,
            pg.K_LEFT: False,
            pg.K_RIGHT: False,
            pg.K_SPACE: False,
            pg.K_z: False
        }

        self.laser = []
        self.got_hit = False
        self.is_invincible = False
        
        self._got_hit_time_counter = 0
        self._got_hit_time_limit = 2

        self._screen_width = screen.get_width()
        self._screen_height = screen.get_height()
        self.timer = 0

    def get_key_down(self, key: int) -> None:
        maybe = self.key_set.get(key, None)
        if maybe is not None:
            self.key_set[key] = True

    def get_key_up(self, key: int):
        maybe = self.key_set.get(key, None)
        if maybe is not None:
            self.key_set[key] = False

    def update(self, dt: float) -> None:
        # Functions to run at all times regardless of user input.
        self.__check_bounds()
        self.__cap_velocity()
        self.__mod_rotation()
        
        if self.got_hit:
            self.got_hit = False
            AudioHandler.ship_hit.play()
            self.is_invincible = True
        
        if self.is_invincible:
            self.__invincible_time_period(dt)
        
        for laser in self.laser:
            laser.update(self._screen_width, self._screen_height, dt)

        # User input related function calls.

        # Move the ship forward.
        if self.key_set[pg.K_w] or self.key_set[pg.K_UP]:
            self.vel += self.accelerate * dt
            self.__move_ship(dt)

        # Rotate the ship to the left
        if self.key_set[pg.K_a] or self.key_set[pg.K_LEFT]:
            self.__rotate_left(dt)

        # Rotate the ship to the right.
        if self.key_set[pg.K_d] or self.key_set[pg.K_RIGHT]:
            self.__rotate_right(dt)

        # Shoot a laser. I have to do it like this otherwise you can spam lasers holding both z and spacebar.
        if self.key_set[pg.K_SPACE]:
            self.__shoot(dt)
            self.key_set[pg.K_SPACE] = False
        elif self.key_set[pg.K_z]:
            self.__shoot(dt)
            self.key_set[pg.K_z] = False

        # Decelerate the ship.
        if not self.key_set[pg.K_w] or not self.key_set[pg.K_UP]:
            self.vel *= self.deceleration_factor
            self.__move_ship(dt)

    def draw(self, screen: pg.Surface) -> None:
        # Draw the ship surface to the screen.
        screen.blit(
            self.surf,
            [self.origin_rec.x - (self.surf.get_width() >> 1),
             self.origin_rec.y - (self.surf.get_height() >> 1)]
        )

        # Draw the lasers that the ship shoots.
        for laser in self.laser:
            laser.draw(screen)

        # Draws outlines around the ship.
        if config.debug_mode:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, 1)

    """
    Private methods.
    """
    def __mod_rotation(self):
        if self.rotation >= 360 or self.rotation < 0:
            self.rotation %= 360

    def __cap_velocity(self):
        if self.vel > self.max_vel:
            self.vel = self.max_vel
    
    def __check_bounds(self):
        # Teleport the ship along the x-axis at the screen border.
        if self.origin.x < -self.origin_rec.width:
            self.origin.x = self._screen_width - (self.origin_rec.width >> 1)
        elif self.origin.x > self._screen_width + (self.origin_rec.width >> 1):
            self.origin.x = -self.origin_rec.width

        # Teleport the ship along the y-axis at the screen border.
        if self.origin.y < -self.origin_rec.height:
            self.origin.y = self._screen_height - (self.origin_rec.height >> 1)
        elif self.origin.y > self._screen_height + (self.origin_rec.height >> 1):
            self.origin.y = -self.origin_rec.height

        # Removes the laser from the list.
        for i, laser in sorted(enumerate(self.laser), reverse=True):
            if laser.is_out_of_bounds:
                self.laser.pop(i)

    def __move_ship(self, dt: float) -> None:       
        # Move the ship. gross cosine and sine operations.
        self.origin.x -= math.cos(to_rad(self.rotation - 90.0)) * self.vel * dt
        self.origin.y -= math.sin(to_rad(self.rotation + 90.0)) * self.vel * dt
        self.origin_rec.x = self.origin.x
        self.origin_rec.y = self.origin.y
        self.hitbox.x = self.origin_rec.x - (self.origin_rec.width >> 1)
        self.hitbox.y = self.origin_rec.y - (self.origin_rec.height >> 1)

    def __rotate_left(self, dt: float) -> None:
        self.rotation += self.delta_rotate * dt
        self.surf = pg.transform.rotate(self.original_surf, self.rotation)

    def __rotate_right(self, dt: float) -> None:
        self.rotation -= self.delta_rotate * dt
        self.surf = pg.transform.rotate(self.original_surf, self.rotation)

    def __shoot(self, dt: float):
        laser = Laser(
            self.origin_rec.x,
            self.origin_rec.y,
            self.rotation
        )
        self.laser.append(laser)
        AudioHandler.ship_fire.play(maxtime=int(AudioHandler.ship_fire.get_length() - 200))

    def __invincible_time_period(self, dt: float):
        self._got_hit_time_counter += dt
        if self._got_hit_time_counter >= self._got_hit_time_limit:
            self._got_hit_time_counter = 0
            # self.got_hit = False
            self.is_invincible = False
