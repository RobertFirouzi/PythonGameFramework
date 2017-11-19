'''
Created on Mar 6, 2017

@author: Robert
'''

import parameters as PRAM
from scenery import SolidBackground, StaticSprite
from event import EventSong, EventSetInput

actors = []

scenery = [
    SolidBackground(PRAM.COLOR_BLUE),
    StaticSprite(PRAM.IMAGE_PATH,PRAM.IMG_BALL, (200,200)),
    StaticSprite(PRAM.IMAGE_PATH,PRAM.IMG_BALL, (100,200)),
    StaticSprite(PRAM.IMAGE_PATH,PRAM.IMG_BALL, (200,100))
    ]

#added to the gameEvent queue on level initialization - e.g. music and ambiant tracks
gameEvents = [
    EventSong(PRAM.SONG_SAGAWIND),
    EventSetInput(PRAM.INPTYPE_MENU),
    ]

layout = [] #TODO 