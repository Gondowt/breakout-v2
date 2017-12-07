import pygame
from pygame.locals import *
from Brick import *
from Board import *
from math import sqrt

class Paddle:
    def __init__(self, image):
        self.image = pygame.image.load(image).convert()
        self.x = 325
        self.y = 550
        self.speed = 2
        self.sizew = 150
        self.sizeh = 19

    def movement(self, direction):
        #manage the movement of the paddle.
        if direction == "left":
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif direction == "right":
            self.x += self.speed
            if self.x > 650:
                self.x = 650

    def reset_paddle(self):
        self.x = 325
        self.y = 550

class Ball:
    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.radius = 12.5

    def reset_ball(self):
        self.x = 400-self.radius
        self.y = 550-2*self.radius
        self.norm_speed = 1
        self.speedx = 0
        self.speedy = -self.norm_speed
        self.start_position = True
        self.last_iteration = False
        self.collision = False
        self.game_over = False
        self.rebound_number = 0
        self.level_number = 0

    def movement(self, paddle, board):
        #move the ball and check the collision between the ball and the paddle and call the function to manage the bricks.
        if not(self.ballEnMouvement()):
            self.x = paddle.x + 150/2 - self.radius
            self.y = paddle.y- 2*self.radius
        else :
            self.x += self.speedx
            self.y += self.speedy

    def ballEnMouvement(self):
        return self.start_position == False

    def go(self):
        #Start the game.
        self.start_position = False

    def rebound_paddle(self, paddle):
        #compute the speed x and speed y thanks the position of the ball on the paddle at the time of rebound.
        self.speedx = ((self.x + self.radius - paddle.x-paddle.sizew/2)/(paddle.sizew/1.5))*self.norm_speed
        if self.speedy < 0:
            self.speedy = -sqrt(abs(self.norm_speed**2 - self.speedx**2))
        else :
            self.speedy = sqrt(abs(self.norm_speed**2 - self.speedx**2))

    def max_rebound(self):
    #return the required number of rebounds in order to add a row.
        if self.level_number//2 > 7:
            return 3
        else :
            return 10-self.level_number//2

    def under_limit(self):
    #check when the ball is under the line limit.
        if self.y + self.radius*2 > 450:
            return True
        return False
