import pygame
from pygame.locals import *
import sqlite3
from Const import *
from Paddle import *
from Brick import *
from random import randint

class BoardFactory:
    def get_board(self, nb, type_game):
        if type_game == GameType.LEVEL:
            return BoardLevel(nb)
        elif type_game == GameType.ENDLESS:
            return BoardEndless(nb)


class Board:
#Class that handles bricks, the different levels, the victory condition, score changing, score adding and row adding.
    def __init__(self, nb):
        self.nb = nb
        self.bricks = []
        self.color = ((232,232,0),(255,127,0),(255,0,0))
        self.end = False
        self.end_game = False
        self.score = 0

    def reset(self):
        self.bricks = []
        self.end = False
        self.score = 0

    def draw_bricks(self, window):
    #function that draw bricks.
        for brick in self.bricks :
            pygame.draw.rect(window, self.color[brick.life-1],(brick.x, brick.y, brick.sizew, brick.sizeh))

    def manage_bricks(self):
    #function which checks collisions of each brick with the ball and deletes the brick of the list bricks when the brick has 0 life.
        l = []
        for i in range(len(self.bricks)) :
            if self.bricks[i].life == 0:
                l += [i]
        for i in l : del(self.bricks[i])

    def next_level(self):
    #function which increase the level number.
        self.nb += 1

    def victory(self):
    #function wich checks if there are some bricks left in the level.
        if self.bricks == []:
            return True
        return False

    def add_score(self):
    #function which add score to the database.
        conn = sqlite3.connect("Save_scores/scores_register.sq3")
        cur = conn.cursor()
        cur.execute("INSERT INTO scores(score) VALUES(%d)" %self.score)
        conn.commit()

    def change_score(self, life, ball):
    #function which updates the scores.
        self.score += life * (ball.level_number+1)

class BoardLevel(Board):
    def __init__(self, nb):
        Board.__init__(self, nb)
        list_levels = open('Level/listLevels.txt','r')
        self.list_levels = list_levels.read().split('\n')
        list_levels.close()

    def load(self):
    #function that read each line of the file which correspond to each brick and add an object brick.
        if len(self.list_levels) > self.nb:
            name_level = self.list_levels[self.nb]
            with open(str(name_level), 'r') as level:
                for line in level.read().split('\n'):
                    if len(line) > 0:
                        brick = line.split(';')
                        self.bricks.append(Brick(int(brick[0]),int(brick[1]),int(brick[2]),int(brick[3]),int(brick[4])))
        else :
            self.end_game = True

class BoardEndless(Board):
    def __init__(self, nb):
        Board.__init__(self, nb)
        list_rows = open('Endless/listRows.txt','r')
        self.list_rows = list_rows.read().split('\n')
        list_rows.close()

    def brick_under_limit(self):
    #fucntion which checks if there is one brick under the line limit during the endless mode.
        for brick in self.bricks:
            if brick.y + brick.sizeh > 450:
                return True
        return False

    def add_row(self):
    #function wich add a row randomly among the different files of endless mode.
        for brick in self.bricks:
            brick.y += 50

        name_row = self.list_rows[randint(0, len(self.list_rows)-1)]
        with open(str(name_row), 'r') as row:
            for line in row.read().split('\n'):
                brick = line.split(';')
                self.bricks.append(Brick(int(brick[0]),int(brick[1]),int(brick[2]),int(brick[3]),int(brick[4])))
