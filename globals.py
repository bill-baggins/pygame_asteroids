import pygame as pg

class GameMode:
    (Running,
     GameOver,
     Paused) = range(0xfdfd21, 0xfdfd24)

screen_width: int = 800
screen_height: int = 600
caption: str = "Asteroids"
fullscreen: bool = False
fps: int = 60
debug_mode: bool = False
background_color: pg.Color = pg.Color("white")
game_mode: GameMode = GameMode.Running

