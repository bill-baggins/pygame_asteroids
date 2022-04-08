import pygame as pg

import globals


class Background:
    def __init__(self):
        self.surf = pg.image.load("resource/space.png").convert()
        self.surf = pg.transform.smoothscale(self.surf, [globals.screen_width, globals.screen_height])
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.surf, [0, 0])