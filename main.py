import pygame as pg
import config
from game.animated_sizes import AnimatedSize

from game.background import Background
from game.ship import Ship
from game.asteroid import Asteroid

from game.handler.surface import SurfaceHandler
from game.handler.audio import AudioHandler
from game.handler.collision import CollisionHandler
from game.handler.spawn import SpawnHandler


class MainLoop:
    running: bool
    screen: pg.Surface
    clock: pg.time.Clock
    ms: float
    dt: float

    _background: Background
    _ship: Ship
    _asteroid_list: 'list[Asteroid]'
    
    def __init__(self):
        self.running = True
        
        # Pygame boilerplate.
        pg.display.set_mode([config.screen_width, config.screen_height])
        self.screen = pg.display.get_surface()
        pg.display.set_caption(config.caption)

        if config.fullscreen:
            pg.display.toggle_fullscreen()

        # More pygame boilerplate.      
        self.clock = pg.time.Clock()
        self.ms = 0.0
        self.dt = 0.0

        # The game objects.
        SurfaceHandler.init()
        AudioHandler.init()
        
        self._background = Background()
        self._ship = Ship(self.screen, scale=0.5)
        self._asteroid_list = [Asteroid(self.screen, AnimatedSize.Large) for _ in range(4)]

        pg.display.set_icon(self._ship.original_surf)
    
    def run(self):
        while self.running:
            # Get the delta time first.
            self.dt = self.ms / 1000.0
            self.__game_running()
            
    def __game_running(self):
        # Get user input.
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break

                if event.type == pg.KEYDOWN:
                    self._ship.get_key_down(event.key)
                    if event.key == pg.K_0:
                        config.debug_mode = not config.debug_mode
                    
                    if event.key == pg.K_ESCAPE:
                        print("What? You thought you could leave? Nah. You're staying here.")

                if event.type == pg.KEYUP:
                    self._ship.get_key_up(event.key)

            # Update/Draw game objects
            SpawnHandler.spawn_asteroids(self.screen, self._asteroid_list, self.dt)
            CollisionHandler.ship_asteroid_collision(self._ship, self._asteroid_list)
            CollisionHandler.ship_laser_asteroid_collision(self.screen, self._ship, self._asteroid_list)
            self._ship.update(self.dt)

            self.screen.fill([245, 245, 245, 255])

            self._background.draw(self.screen)
            self._ship.draw(self.screen)

            for asteroid in self._asteroid_list:
                asteroid.update(self.screen, self.dt)
                asteroid.draw(self.screen)

            # Tick the clock.
            self.ms = self.clock.tick(config.fps)
            pg.display.update()


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    
    MainLoop().run()
    
    pg.mixer.quit()
    pg.quit()
