import pygame
from pygame.locals import *
import sqlite3


def sort_list(list_score):
#Sorting function that takes a list as argument and returns the list which has been sorted descending.
    return(sorted(list_score, reverse =True))

def clear_scores():
#Function that erases all the scores of the database.
    fichierDonnees ="Save_scores/scores_register.sq3"
    conn =sqlite3.connect(fichierDonnees)
    cur =conn.cursor()
    cur.execute("DELETE FROM scores")
    conn.commit()

def display_scores(screen):
#Function that displays scores.
    conn = sqlite3.connect("Save_scores/scores_register.sq3")
    cur = conn.cursor()
    cur.execute("SELECT * FROM scores")
    ten_score = sort_list(list(cur))[0:10]

    see_score = True
    #Loop that manages the events which allows the user to quit or to call the function which allows to reset the database.
    while see_score:
        for event in pygame.event.get():
            if event.type == QUIT:
                see_score = False
            elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        see_score = False
                    if event.key == K_r:
                        clear_scores()
                        conn = sqlite3.connect("Save_scores/scores_register.sq3")
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM scores")
                        ten_score = sort_list(list(cur))[0:10]
        #Printing scores on the screen.
        background = pygame.Surface(screen.get_size())
        background.fill((0, 0, 0))
        font = pygame.font.Font(None,45)
        text = font.render("SCORES", True, (255,255,255))
        text_pos = text.get_rect()
        text_pos.centerx = background.get_rect().centerx
        text_pos.centery = 50
        background.blit(text, text_pos)
        font = pygame.font.Font(None,36)
        for score1 in range(len(ten_score)):
            background.blit(font.render("%d" %ten_score[score1], True, (255,255,255)), (500,  100 + 50*score1))
            background.blit(font.render(str(score1+1)+".", True, (255,255,255)), (200,  100 + 50*score1))

        screen.blit(background, (0,0))
        pygame.display.flip()
