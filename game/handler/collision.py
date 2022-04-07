import pygame as pg
from game.ship import Ship
from game.asteroid import Asteroid
from game.laser import Laser

from game.handler.audio import AudioHandler
from game.animated_sizes import AnimatedSize


class CollisionHandler:
    @classmethod
    def ship_asteroid_collision(cls, ship: Ship, asteroid_list: 'list[Asteroid]'):
        for asteroid in asteroid_list:
            if ship.hitbox.colliderect(asteroid.hitbox):
                # ref_ship_surf = ship.surf.copy()
                # ref_ship_surf.set_colorkey(pg.Color("white"))
                # ship_mask = pg.mask.from_surface(pg.transform.rotate(ref_ship_surf, ship.rotation).convert())
                # asteroid_mask = pg.mask.from_surface(asteroid.surf)
                # offset_x, offset_y = (ship_mask.get_rect().left - asteroid_mask.get_rect().left), (ship_mask.get_rect().top - asteroid_mask.get_rect().top)
                # if ship_mask.overlap(asteroid_mask, (offset_x, offset_y)) is not None:
                #     if not ship.is_invincible:
                #         print("got hit")
                #         ship.got_hit = True
                #     break
                if not ship.is_invincible:
                    print("got hit")
                    ship.got_hit = True
                    break
    
    @classmethod
    def ship_laser_asteroid_collision(cls, screen: pg.Surface, ship: Ship, asteroid_list: 'list[Asteroid]'):
        for i, laser in sorted(enumerate(ship.laser), reverse=True):
            laser_hit_something = False
            for j, asteroid in sorted(enumerate(asteroid_list), reverse=True):
                if laser.hitbox.colliderect(asteroid.hitbox):
                    laser_hit_something = True
                    if asteroid.size > AnimatedSize.Small:
                        new_size = asteroid.size - 1
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.topleft[0], asteroid.hitbox.topleft[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.topright[0], asteroid.hitbox.topright[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.bottomleft[0], asteroid.hitbox.bottomleft[1]))
                        asteroid_list.append(Asteroid(screen, new_size, asteroid.hitbox.bottomright[0], asteroid.hitbox.bottomright[1]))
                    asteroid_list.pop(j)
            if laser_hit_something:
                ship.laser.pop(i)
                    
                    