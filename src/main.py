'''
Created on Feb 24, 2017

@author: Robert
'''

from parameters import *
from event import *
import pygame

from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.addEvent(EventLoadMenu(MENU_TEST1))
    game.addEvent(EventSetInput(INPTYPE_MENU))
    game.addEvent(EventSong(SONG_SAGAWIND))


    game.run()

