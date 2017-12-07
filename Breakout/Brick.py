import pygame
from pygame.locals import *
from Paddle import *

class Brick:
    def __init__(self, x, y, life, sizew, sizeh):
        self.x = x
        self.y = y
        self.sizew = sizew
        self.sizeh = sizeh
        self.life = life

    def __del__(self):
        pass
