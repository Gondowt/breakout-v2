import pygame
from pygame.locals import *
from Const import *
from Game import *
from Scores import *
#Initialisation of pygame
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
font = pygame.font.SysFont('freesans', 36)
font_title = pygame.font.SysFont('freesans', 50)

#Initialisation of game factory
game_factory = GameFactory()

#Menu
option = (("Play",(100,175)),("Play Endless Mode",(100,275)),("Score",(100,375)),("Quit",(100,475)))
index_option = 0
stop = False

#Loop which checks events for the menu.
while not stop:
    for event in pygame.event.get():
            if event.type == QUIT:
                stop = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stop = True
                elif event.key == K_DOWN :
                    index_option += 1
                    if index_option == 4: index_option = 0
                elif event.key == K_UP :
                    index_option -= 1
                    if index_option == -1 : index_option = 3
                elif event.key == K_RETURN:
                    if index_option == 0:
                        game = game_factory.get_game(GameType.LEVEL,window)
                        game.play()
                    elif index_option == 1:
                        game = game_factory.get_game(GameType.ENDLESS,window)
                        game.play()
                    elif index_option == 2:
                        display_scores(window)
                    elif index_option == 3:
                        stop = True
    #Draw the menu
    window.fill(0)

    text = font_title.render("Break Out", True, (255,255,255))
    window.blit(text, (300, 50))
    for i in range(len(option)):
        if i == index_option :
            text = font.render(option[i][0],True, (255,0,0))
        else :
            text = font.render(option[i][0],True, (255,255,255))
        window.blit(text, option[i][1])
    pygame.display.flip()

pygame.quit()
