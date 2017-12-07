import pygame
from pygame.locals import *
from Const import *
from Paddle import *
from Brick import *
from Board import *
from Collision import *
import time

class GameFactory:
    def get_game(self, type_game, window):
        if type_game == GameType.LEVEL:
            return GameLevel(window)
        elif type_game == GameType.ENDLESS:
            return GameEndless(window)

class Game:
    def __init__(self, window):
        self.barre = Paddle("Img/Paddle.png")
        self.ball = Ball("Img/Ball.png")
        self.window = window
        self.nbLevel = 0

    def message(self, str_message, x=0, y=0):
        #write a message which contains str_message and the message is closed when the user takes the decision.
        font = pygame.font.SysFont('freesans', 36)
        message_ok = False
        text = font.render(str_message,True, (255,0,0))
        self.window.blit(text, (300 + x, 300 + y))
        pygame.display.flip()
        while not message_ok and not self.board.end_game:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        self.board.end_game = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.board.end_game = True
                        elif event.key == K_SPACE:
                            message_ok = True
    def reset_game(self):
        self.board.reset()
        self.barre.reset_paddle()
        self.ball.reset_ball()

class GameLevel(Game):
    def __init__(self, window):
        Game.__init__(self, window)
        self.game_type = GameType.LEVEL
        self.board = BoardFactory().get_board(self.nbLevel, self.game_type)
        self.collision_ball_paddle_context = CollisionContext()
        self.collision_ball_paddle_context.setCollisionStrategy(BallPaddleCollision())
        self.collision_ball_bricks_context = CollisionContext()
        self.collision_ball_bricks_context.setCollisionStrategy(BallBricksCollision())
        self.collision_ball_window_context = CollisionContext()
        self.collision_ball_window_context.setCollisionStrategy(BallWindowCollision())

    def check_victory(self):
        if self.board.victory() == True:
            self.message("Victory", 50)
            self.board.end = True
            self.board.next_level()

    def check_game_over(self):
        if self.ball.game_over == True:
            self.message("Game Over")
            self.board.end = True

    def collision(self):
        #print(not(self.ball.ballEnMouvement()))
        if self.ball.ballEnMouvement():
            self.collision_ball_bricks_context.checkCollision(self.ball, self.board)
            self.collision_ball_paddle_context.checkCollision(self.ball, self.barre)
            self.collision_ball_window_context.checkCollision(self.ball, None)
        self.board.manage_bricks()


    def play(self):
    #Main loop to manage the game in Level mode.
        while not self.board.end_game:

            self.reset_game()

            self.board.load()

            t=time.time()
            #loop to check event about the closure of the game
            while not self.board.end and not self.board.end_game:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.board.end_game = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.board.end_game = True
                        elif event.key == K_SPACE:
                            self.ball.go()
                #check the event every milli second
                if time.time() - t > 0.001:
                    #event to check the movement of the paddle
                    tkey = pygame.key.get_pressed()
                    if tkey[K_LEFT] != 0:
                        self.barre.movement("left")
                    elif tkey[K_RIGHT] != 0:
                        self.barre.movement("right")

                    self.ball.movement(self.barre, self.board)

                    self.collision()


                    t = time.time()
                    #Game over condition
                    self.check_game_over()
                    #Victory condition
                    self.check_victory()

                #Draw the game
                self.window.fill(0)
                self.window.blit(self.barre.image,(self.barre.x ,self.barre.y))
                self.window.blit(self.ball.image,(self.ball.x,self.ball.y))
                self.board.draw_bricks(self.window)
                pygame.display.flip()

class GameEndless(Game):
    def __init__(self, window):
        Game.__init__(self, window)
        self.font = pygame.font.SysFont('freesans', 30)
        self.game_type = GameType.ENDLESS
        self.board = BoardFactory().get_board(self.nbLevel, self.game_type)
        self.collision_ball_paddle_context = CollisionContext()
        self.collision_ball_paddle_context.setCollisionStrategy(BallPaddleCollision())
        self.collision_ball_bricks_context = CollisionContext()
        self.collision_ball_bricks_context.setCollisionStrategy(BallBricksCollision())
        self.collision_ball_window_context = CollisionContext()
        self.collision_ball_window_context.setCollisionStrategy(BallWindowCollision())

    def game_over(self):
        #Game over condition
        if self.ball.game_over == True or self.board.brick_under_limit():
            pygame.draw.rect(self.window, (0,255,0),(0, 450, 800, 2))
            self.window.blit(self.font.render("Scores : "+str(self.board.score),True, (255,0,0)), (325, 600))
            self.window.blit(self.barre.image,(self.barre.x ,self.barre.y))
            self.window.blit(self.ball.image,(self.ball.x,self.ball.y))
            self.board.draw_bricks(self.window)
            self.board.add_score()
            self.message("Game Over", y=170)
            self.board.end = True

    def add_row(self):
        #add a row when the rebound number reach a certain value.
        if self.ball.rebound_number == self.ball.max_rebound():
            self.ball.rebound_number = 0
            self.ball.level_number += 1
            self.board.add_row()

    def board_empty(self):
        #check if the ball is under the limit and if the level is empty and add a row when it's True.
        if self.ball.under_limit():
            if self.board.victory():
                self.board.change_score(6, self.ball)
                self.ball.rebound_number = 0
                self.board.add_row()

    def collision(self):
        if self.ball.ballEnMouvement():
            self.collision_ball_bricks_context.checkCollision(self.ball, self.board)
            self.collision_ball_paddle_context.checkCollision(self.ball, self.barre)
            self.collision_ball_window_context.checkCollision(self.ball, None)
        self.board.manage_bricks()

    def play(self):
        #Main loop to manage the game in Endless mode.
        while not self.board.end_game:

            self.reset_game()

            for i in range(3):
                self.board.add_row()

            t=time.time()
            self.board.end = False
            #loop to check event about the closure of the game
            while not self.board.end and not self.board.end_game:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.board.end_game = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.board.end_game = True
                        elif event.key == K_SPACE:
                            self.ball.go()
                        elif event.key == K_RETURN:
                            self.board.add_row()
                #check the event every milli second
                if time.time() - t > 0.001:
                     #event to check the movement of the paddle
                    tkey = pygame.key.get_pressed()
                    if tkey[K_LEFT] != 0:
                        self.barre.movement("left")
                    elif tkey[K_RIGHT] != 0:
                        self.barre.movement("right")

                    self.ball.movement(self.barre, self.board)
                    self.collision()

                    t = time.time()
                    self.window.fill(0)

                    self.game_over()

                    self.add_row()

                    self.board_empty()

                #Draw game
                self.window.fill(0)
                self.window.blit(self.font.render("Scores : "+str(self.board.score),True, (255,0,0)), (325, 600))
                pygame.draw.rect(self.window, (0,255,0),(0, 450, 800, 2))
                self.window.blit(self.barre.image,(self.barre.x ,self.barre.y))
                self.window.blit(self.ball.image,(self.ball.x,self.ball.y))
                self.board.draw_bricks(self.window)
                pygame.display.flip()
