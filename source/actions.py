'''
Created on Feb 25, 2017

@author: Robert
'''

import parameters as PRAM
from event import EventSound, EventMove

'''
Base class for an Action object.  Extend for specific functionality
    Contains a link to the character which contains the action
@param character
'''
class ActionBase():
    def __init__(self,character,params=()):
        self.character=character
        self.params=params

    def act(self, character, params=()):
        return ''

'''
Moves the character's actor based on its movement speed
@Param character
@return None 
'''    
class ActionMove(ActionBase):
    def __init__(self, character, params=()):
        super(ActionMove, self).__init__(character, params)
    
    def act(self, direction):
        return EventMove(self.character, direction)

        
'''
Performs colorSwap on the character's actor containing the action, if they own this method
    returns a sound effect action
@Param character
@return EventSound 
'''      
class ActionColorSwap(ActionBase):
    def __init__(self, character, params = ()):   
        super(ActionColorSwap, self).__init__(character, params)
    
    def act(self, params=()):
        self.character.actor.colorSwap()
        self.character.actor.changed = True #re-render
        return EventSound(PRAM.SOUND_COLORSWAP)      
        
        
        
        
        