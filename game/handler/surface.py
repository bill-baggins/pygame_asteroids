import pygame as pg

from game.animated_sizes import AnimatedSize


# This class contains all of the surface that will be used for the game.
class SurfaceHandler:
    ship: pg.Surface
    laser: pg.Surface
    
    small_asteroid: pg.Surface
    medium_asteroid: pg.Surface
    large_asteroid: pg.Surface
    
    small_explosion: pg.Surface
    medium_explosion: pg.Surface
    large_explosion: pg.Surface

    asteroid_surfs: 'dict[AnimatedSize, pg.Surface]'
    explosion_surfs: 'dict[AnimatedSize, pg.Surface]'
    
    heart_surf: pg.Surface

    @classmethod
    def init(cls) -> None:
        # Ship Surface. The background of the image is magenta, so the colorkey function
        # removes it.
        cls.ship = pg.image.load("resource/starfighter.png").convert()
        cls.ship.set_colorkey(pg.Color("magenta"))
        
        # Laser Surface. Since it is transparent, the background turns black whenever
        # converting it to a surface. This removes the black background.
        cls.laser = pg.image.load("resource/laser.png").convert()
        cls.laser.set_colorkey(pg.Color("black"))
        
        # Asteroid Surface. These images contain all of the frames for the
        # asteroid animation.
        cls.large_asteroid = pg.image.load("resource/animated_asteroid.png").convert()
        cls.medium_asteroid = pg.image.load("resource/animated_asteroid.png").convert()
        cls.small_asteroid = pg.image.load("resource/animated_asteroid.png").convert()
        
        cls.large_asteroid.set_colorkey(pg.Color("black"))
        cls.medium_asteroid.set_colorkey(pg.Color("black"))
        cls.small_asteroid.set_colorkey(pg.Color("black"))

        # The medium asteroid surface is the whole animated image scaled down 2x.
        cls.medium_asteroid = pg.transform.scale(
            cls.medium_asteroid, 
            [cls.large_asteroid.get_width() >> 1, cls.large_asteroid.get_height() >> 1]
        )

        # The small asteroid surface is the whole animated image scaled down 4x.
        cls.small_asteroid = pg.transform.scale(
            cls.small_asteroid, 
            [320, 40]
        )

        # Explosion Surface. Same idea here as the asteroids, just that there are
        # more frames to the animation.
        cls.large_explosion = pg.image.load("resource/animated_explosion.png").convert()
        cls.medium_explosion = pg.image.load("resource/animated_explosion.png").convert()
        cls.small_explosion = pg.image.load("resource/animated_explosion.png").convert()

        cls.medium_explosion = pg.transform.scale(
            cls.medium_explosion, 
            [cls.large_explosion.get_width() >> 1, cls.large_explosion.get_height() >> 1]
        )

        cls.small_explosion = pg.transform.scale(
            cls.small_explosion, 
            [cls.large_explosion.get_width() >> 2, cls.large_explosion.get_height() >> 2]
        )

        cls.asteroid_surfs = {
            AnimatedSize.Large: cls.large_asteroid,
            AnimatedSize.Medium: cls.medium_asteroid,
            AnimatedSize.Small: cls.small_asteroid
        }

        cls.explosion_surfs = {
            AnimatedSize.Large: cls.large_explosion,
            AnimatedSize.Medium: cls.medium_explosion,
            AnimatedSize.Small: cls.small_explosion
        }
        
        cls.heart_surf = pg.image.load("resource/heart.png").convert()
        cls.heart_surf.set_colorkey(pg.Color("black"))
        cls.heart_surf = pg.transform.scale(cls.heart_surf, [20, 20])
        
        cls.info()

    @classmethod
    def get_asteroid_surf(cls, size: AnimatedSize = AnimatedSize.Large):
        return cls.asteroid_surfs.get(size)

    @classmethod
    def get_explosion_surf(cls, size: AnimatedSize = AnimatedSize.Large):
        return cls.explosion_surfs.get(size)
    
    @classmethod
    def info(cls):
        for attribute in dir(cls):
            maybe = cls.__dict__.get(attribute, None)
            if not str(attribute).endswith("__") and \
                    not str(attribute).startswith("__") and \
                    maybe is not None and \
                    type(maybe) is pg.Surface:

                print(f"Surface: {attribute} <> Dimensions: {maybe.get_width()}x{maybe.get_height()}")