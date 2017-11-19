'''
Created on Mar 5, 2017

@author: Robert
'''
from event import EventLoadLevel, EventLoadMenu, EventDefaultAction

'''
Class to store the type of input received (keydown, presseed, mousemove, etc) and
    the input trigger (arrow key, letter, mouse click...)
'''

import parameters as PRAM

'''
Class defines which keys are mapped to which actions (allows for changing buttons during
    game play dynamically i.e. controller config)
@param up
@param down
@param left
@param right
@param default
'''
class ButtonMap():
    def __init__(self, 
                 up = PRAM.INPUT_UP, 
                 down = PRAM.INPUT_DOWN, 
                 left =  PRAM.INPUT_LEFT, 
                 right = PRAM.INPUT_RIGHT, 
                 action = PRAM.INPUT_ACTION,
                 status = PRAM.INPUT_STATUS,
                 enterDebug = PRAM.INPUT_DEBUG,
                 ):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.action = action
        self.status = status
        self.enterDebug = enterDebug

'''
Class has the behaviors of each input dynamically assigned and processes input
each frame
@param game
@param player
@param buttonMap
'''
class InputHandler():
    def __init__(self, game = None, player = None, buttonMap = None, inputType = PRAM.INPTYPE_OBSERVER):
        self.game = game
        self.player = player
        self.buttonMap = buttonMap
        
        self.setInputBehavior(inputType)
      
    def handleInputs(self):
        while len(self.game.keydownEvents) > 0:
            event = self.game.keydownEvents.pop()
            if event.type == PRAM.KEYDOWN:
                if event.key == self.buttonMap.action:
                    self.inputActionBehavior()
                elif event.key == self.buttonMap.status:
                    self.inputStatusBehavior()
                elif event.key == self.buttonMap.enterDebug:
                    self.enterDebugBehavior()
            elif event.type == PRAM.CLICKDOWN:
                if event.button == PRAM.INPUT_LEFTCLICK:
                    self.leftClickBehavior(event.pos)
            #Add more key events here
        
        #check which keys are currently pressed down        
        if self.game.keysPressed[self.buttonMap.up]:
            self.inputUpBehavior()
        if self.game.keysPressed[self.buttonMap.down]:
            self.inputDownBehavior()
        if self.game.keysPressed[self.buttonMap.left]:
            self.inputLeftBehavior()
        if self.game.keysPressed[self.buttonMap.right]:
            self.inputRightBehavior()
        
        return

    def setInputBehavior(self, inputType):
        if inputType == PRAM.INPTYPE_OBSERVER:
            self.inputUpBehavior = self.doNothing
            self.inputDownBehavior = self.doNothing
            self.inputLeftBehavior = self.doNothing
            self.inputRightBehavior = self.doNothing
            self.inputActionBehavior = self.doNothing
            self.inputCancelBehavior = self.doNothing
            self.inputStatusBehavior = self.doNothing
            self.leftClickBehavior = self.printPixelPosition

        elif inputType == PRAM.INPTYPE_MENU:
            self.inputUpBehavior = self.menuUp
            self.inputDownBehavior = self.menuDown
            self.inputLeftBehavior = self.menuLeft
            self.inputRightBehavior = self.menuRight
            self.inputActionBehavior = self.menuAction 
            self.inputCancelBehavior = self.menuCancel
            self.inputStatusBehavior = self.doNothing
            self.leftClickBehavior = self.printPixelPosition

        elif inputType == PRAM.INPTYPE_NORMAL:        
            self.inputUpBehavior = self.movementUp
            self.inputDownBehavior = self.movementDown
            self.inputLeftBehavior = self.movementLeft
            self.inputRightBehavior = self.movementRight
            self.inputActionBehavior = self.defaultAction 
            self.inputCancelBehavior = self.doNothing
            self.inputStatusBehavior = self.statusAction
            self.enterDebugBehavior = self.startDebug
            self.leftClickBehavior = self.printPixelPosition
                        
#TODO - should dirrectional events return an event for the queue?    
    def movementUp(self, args=''):
        self.game.addEvent(self.player.actionMove(PRAM.UP))
        
    def movementDown(self, args=''):
        self.game.addEvent(self.player.actionMove(PRAM.DOWN))
    
    def movementLeft(self, args=''):
        self.game.addEvent(self.player.actionMove(PRAM.LEFT))
    
    def movementRight(self, args=''):
        self.game.addEvent(self.player.actionMove(PRAM.RIGHT))
    
    def defaultAction(self, args=''):
        self.game.addEvent(EventDefaultAction(self.player)) #'default behavior'
    
    def statusAction(self, args=''):
        self.game.addEvent(EventLoadMenu(PRAM.MENU_TEST1)) #TODO temp code to test menu/level load       
    
    def menuUp(self, args=''):
        pass

    def menuDown(self, args=''):
        pass

    def menuLeft(self, args=''):
        pass
    
    def menuRight(self, args=''):
        pass

    def menuAction(self, args=''):
        self.game.addEvent(EventLoadLevel(3, [250,350])) #TODO temp code to test menu/level load
    
    def menuCancel(self, args=''):
        pass
   
    def doNothing(self, args=''):
        pass

    def printPixelPosition(self, args=''):
        print('('+str(args[0])+','+str(args[1])+')') #prints the coordinates of the mouse click

    def startDebug(self, args=''):
        self.game.runDebug = True