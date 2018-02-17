'''
Created on Feb 24, 2017

@author: Robert
'''

import parameters as PRAM

#BASIC PLACEHOLDER CLASSES UNTIL ANIMATION CLASSES ARE IMPLEMENTED

class ActorBase:
    def __init__(self, size, position, direction = 'right', isFocus = False):
        self.size = size
        self.position = position
        self.direction = direction
        self.isFocus = isFocus
        self.changed = True #render if true, change to false after rendered
    
    def setPosition(self, position = (0,0)):
        self.position = position
    
    def getPosition(self):
        return self.position

class SimpleBox(ActorBase):
    def __init__(self, 
                 color = PRAM.COLOR_BLUE, 
                 size = (PRAM.SIMPLE_BOX_WIDTH, PRAM.SIMPLE_BOX_HEIGHT),
                 position =(100,100)):
        super(SimpleBox, self).__init__(size, position)
        self.color=color

    #Swaps its color between 2 predefined values
    def colorSwap(self):
        if self.color == PRAM.COLOR_BLUE: # @UndefinedVariable
            self.setColor(PRAM.COLOR_ORANGE) # @UndefinedVariable
        else:
            self.setColor(PRAM.COLOR_BLUE) # @UndefinedVariable
        
    def setColor(self,color):
        self.color=color


# ANIMATION CLASSES

#Contains all of the animations for a character sprite
class CharacterSprite:
    def __init__(self, name, animations):
        self.name = name
        self.animations = animations #all data needed to display the image

        self.animationState = None #tracks which image and frame to display, as well as when to flip

#class to main the current state of a character sprites animation
class AnimationState:
    def __init__(self):
        self.name = '' #reference to animation, eg: 'hero_walk', 'hero_attack1', etc
        self.direction = 0 #reference to which direction of animation is being played
        self.condition = 0  # 0 - Frozen, 1 - Forward, 2 - Backward, etc
        self.frameIndex = 0 #tracks which frame in the sequence is being displayed
        self.frameCount = 0 #number of frames since last image frame index transistion
        self.speed = 100  #percent of default framerate the image is moving

#Contains the base image and positional data for a sprite animation (all directions)
class SpriteAnimation:
    def __init__(self, filePath, name, numbFrames, fps, positions):
        self.filePath = filePath
        self.name = name
        self.numbFrames = numbFrames
        self.fps = fps
        self.positions = positions #Dictionary of AnimationPositions {Direction: position()}

        self.image = None #Image of the base animation, may have accessories layered on top

#contains animation for an accessory to a Sprite_Animation, which is layered on top
class AnimationAccessory:
    def __init__(self, filePath, baseName, name, positions):
        self.filePath = filePath
        self.baseName = baseName #which Sprite_Animation this corresponds to
        self.name = name
        self.positions = positions #Dictionary of AccessoryPositions {Direction: position()}

        self.image = None #loaded from DB, used to blit ontop of a Base Animation

#container class of positional information and size of a single frame of an animation
class AnimationPosition:
    def __init__(self, start_x, start_y, width, height):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height

#container class of positional information and size of a single frame of an animation accessory
#needs the relative position on the corresponding base frame as well as position of self on frame
class AccessoryPosition:
    def __init__(self, start_x, start_y, width, height, relative_x, relative_y):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.relative_x = relative_x
        self.relative_y = relative_y