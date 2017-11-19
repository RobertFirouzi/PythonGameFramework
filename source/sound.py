'''
Created on Feb 25, 2017

@author: Robert
'''

import pygame
import os
import parameters as PRAM
from log_errors import logError

'''
Class to hold data on a sound file
@param soundType
@param path
@param sound
@param ext
'''
class SoundWrapper():
    def __init__(self, soundType, path, sound, ext):
        self.soundType=soundType
        self.path=path
        self.sound=sound
        self.ext=ext
        self.fullPath = path+sound+ext

'''
Class to play music. Needs to have path loaded into it's dictionary to play song
@param musicDict
'''
class MusicPlayer():
    def __init__(self, musicDict={}):
        self.musicDict = musicDict
    
    '''
    Add a song to the music dictionary
    @param soundWrapper
    '''    
    def loadSong(self, soundWrapper):
        retVal = True
        if soundWrapper.soundType =='song':
            if self.musicDict.get(soundWrapper.sound) == None:
                if(os.path.exists(str(soundWrapper.fullPath))):   
                    self.musicDict[soundWrapper.sound] = soundWrapper
                else:
                    logError('MusicPlayer','loadSong', 
                             'path [' +soundWrapper.fullPath+ '] not found')
                    retVal = False
            else:
                logError('MusicPlayer','loadSong', 
                         'tried to reload [' +soundWrapper.fullPath+ '], but this already exists')
                retVal = False
        else:
            retVal = False
            logError('MusicPlayer','loadSong', 'load song with type: ' + str(soundWrapper.soundType))
        return retVal
                
    '''
    Starts playing a song.  If playthroughs = -1 the song plays on repeate
    @param song
    @param playthroughs
    '''   
    def playSong(self, song, playthroughs=-1):
        retVal = True
        if self.musicDict.get(song) == None:
            logError('MusicPlayer','playSong', 'song [' + song+ '] not found in dict')
            retVal = False
            if song != PRAM.SONG_ERROR: #avoid infinite recursion
                self.playSong(PRAM.SONG_ERROR,1)
        else:
            pygame.mixer.music.load(self.musicDict.get(song).fullPath)
            pygame.mixer.music.play(-1)
        return retVal
    
    def stopSong(self):
        pygame.mixer.music.stop()
        

'''
Class to play sound effects.  Default is one playthrough of a soundeffect.  Up to
8 tracks can play simultanously (?).  Must load sound first.
@param soundDict
'''         
class SoundEffectPlayer():
    def __init__(self, soundDict={}):
        self.soundDict = soundDict
        errorSound = SoundWrapper('sound', os.path.realpath('') +'\\dir_sound\\dir_soundeffects\\', 'ERROR', '.wav' )
        self.loadSound(errorSound)
    
    '''
    Load a sound into the dictionary
    @param soundWrapper
    '''    
    def loadSound(self, soundWrapper):
        retVal = True    
        if soundWrapper.soundType =='sound':
            if self.soundDict.get(soundWrapper.sound) == None:
                if(os.path.exists(str(soundWrapper.fullPath))):   
                    soundWrapper.soundObject = pygame.mixer.Sound(soundWrapper.fullPath) #save the sound file in the object
                    self.soundDict[soundWrapper.sound] = soundWrapper
                else:
                    logError('SoundEffectPlayer','loadSound', 'path [' +soundWrapper.fullPath+ '] not found')
                    retVal = False                
            else:
                logError('SoundEffectPlayer','loadSound', 'tried to reload [' +soundWrapper.fullPath+ '], but this already exists')
                retVal = False
        else:
            retVal=False
            logError('SoundEffectPlayer','loadSound', 'load sound with type: ' + str(soundWrapper.soundType))                                 
        return retVal

    '''
    Play a sound once.  Must be in the soundDictionary
    @param sound
    '''
    def playSound(self, sound):
        retVal = True
        if self.soundDict.get(sound) == None:
            logError('SoundEffectPlayer','playSound', 'sound [' +sound+ '] not found in dict')
            retVal = False
            if sound != PRAM.SOUND_ERROR: #prevent infinite recursion
                self.playSound(PRAM.SOUND_ERROR)
        else:
            self.soundDict[sound].soundObject.play()
        return retVal

    def stopSound(self):
        pygame.mixer.stop()
   
    '''
    Sets the volume on a specific sound.  Sound must be in the soundDict.  Range
        of volume is [0.0,1.0]
    @param sound
    @param volume
    '''   
    def setSoundVolume(self,sound,volume):
        retVal = True
        if volume>1.0 or volume<0:
            logError('SoundEffectPlayer','setSoundVolume', 'val '+str(volume)+' out of range')            
            retVal = False
        elif self.soundDict.get(sound) == None:  
            logError('SoundEffectPlayer','playSound', 'sound [' +sound+ '] not found in dict')
            retVal = False
        else: 
            self.soundDict.get(sound).soundObject.set_volume(volume)
        return retVal
        
        
        
        
