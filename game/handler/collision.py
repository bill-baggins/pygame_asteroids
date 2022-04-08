# collision.py: Contains all the logic for handling collisions between game objects.

import pygame as pg
from game.ship import Ship
from game.asteroid import Asteroid
from game.laser import Laser

from game.handler.audio import AudioHandler
from game.animated_sizes import AnimatedSize

from globals import GameMode
import globals


class CollisionHandler:
    @classmethod
    def ship_asteroid_collision(cls, ship: Ship, asteroid_list: 'list[Asteroid]'):
        if ship.is_invincible:
            return
    
        for asteroid in asteroid_list:
            if ship.hitbox.colliderect(asteroid.hitbox):
                ship_surf = pg.transform.rotate(ship.surf, ship.rotation).convert()
                ship_surf.set_colorkey(pg.Color("magenta"))
                ship_mask = pg.mask.from_surface(ship_surf)
                asteroid_mask = pg.mask.from_surface(asteroid.surf)
                ship_rect = ship.surf.get_rect()
                asteroid_rect = asteroid.surf.get_rect()
                sx, sy = ship_rect.center[0], ship_rect.center[1]
                ax, ay = asteroid_rect.center[0], asteroid_rect.center[1]
                
                if asteroid_mask.overlap(ship_mask, (ax - sx, ay - sy)):
                    if not ship.is_invincible:
                        print("debug: got hit")
                        ship.got_hit = True
                        if ship.health == 0:
                            globals.game_mode = GameMode.GameOver
                        break
    
    @classmethod
    def ship_laser_asteroid_collision(cls, screen: pg.Surface, ship: Ship, asteroid_list: 'list[Asteroid]'):
        for i, laser in enumerate(ship.laser):
            laser_hit_something = False
            for j, asteroid in enumerate(asteroid_list):
                if laser.hitbox.colliderect(asteroid.hitbox):
                    laser_hit_something = True
                    if asteroid.size > AnimatedSize.Small:
                        new_size = asteroid.size - 1
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.topleft[0], asteroid.hitbox.topleft[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.topright[0], asteroid.hitbox.topright[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.bottomleft[0], asteroid.hitbox.bottomleft[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.bottomright[0], asteroid.hitbox.bottomright[1]))
                    AudioHandler.get_explosion_sound(asteroid.size).play()
                    asteroid_list.pop(j)
            if laser_hit_something:
                ship.laser.pop(i)
                    
                    