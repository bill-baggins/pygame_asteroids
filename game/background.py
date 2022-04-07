import pygame as pg

import config


class Background:
    surf: pg.Surface

    def __init__(self):
        self.surf = pg.image.load("resource/space.png").convert()
        self.surf = pg.transform.smoothscale(self.surf, [config.screen_width, config.screen_height])
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.surf, [0, 0])