'''
Created on Feb 24, 2017

@author: Robert
'''

import parameters as PRAM

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