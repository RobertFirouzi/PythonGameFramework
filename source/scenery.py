'''
Created on Feb 24, 2017

@author: Robert
'''

import parameters as PRAM

'''
Class contains the dictionary which has the reference to all loaded sprites, and
    the list of scenery items to place.  Sprites are loaded only once to the dictionary
    but can be placed as many times as they appear in the list
'''
class SceneryWrapper():
    def __init__(self, imageDict = {}, scenery = [], background = False, foreground = False):
        self.imageDict = imageDict
        self.scenery = scenery
        self.background = background
        self.foreground = foreground

'''
Render the entire screen a solid color
@param color
'''
class SolidBackground():
    def __init__(self, color = PRAM.COLOR_BLACK):
        self.color=color
        
    def colorChange(self,color):
        self.color=color
        return True 

    '''
    Image that can be used as layer of background or foreground.  Can be set to tile or scroll, and
    sections that are visible relative to the game level can be chosen
    
    @param path: directory of image
    @param image: filename of image
    @param imageSize: size in pixels of image [x,y]
    @param visibleSections: 2d array: each array is a box [left edge, right edge, top edge, bottom edge]
    @param scrolling: [[Xmultiplier, Xdivisor], [Xmultiplier, Xdivisor]]    
    @param: alpha: does the image contain alpha information (e.g. invisiible pixels)
    
    Scroll speed can be calculated to perfectly scroll the level in the level editor, or user chosen. Formula to scroll the level is
    
    X direction:
    numerator: levelSize - displaywidth
    denomonator: imageSize - displaywidth
    numerator/denomonator = scroll speed in X direction to scroll the image over the entire level
    
    Y direction is same using Y params and displayheight
    
    NOTE if imageSize=displayWidth than set scroll speed to 0
    
    The above calculates the divisor.  Multiplier makes the image scroll faster then the level, so this must be user chosen.
    If user desires a 1.4 scroll speed, choose a multiplier of 14 and divisor of 10.
    '''
class PanoramicImage():
    def __init__(self, 
                 filePath = '', 
                 pxSize = [10,10],  
                 visibleSections = [[0,200,0,200],[200,500,200,500]], 
                 scrolling = [[1,1],[1,1]], 
                 alpha = False,
                 layer= 0):
        self.filePath = filePath
        self.pxSize = pxSize
        self.visibleSections = visibleSections
        self.scrolling = scrolling
        self.alpha = alpha
        self.layer = layer
        
        #explicit declaration of class fields
        self.image = None # the image date        

            
'''
Wrapper class for an image file. Contains the path and image name, and location
to place the image
@param image
@param location
'''         
class StaticSprite():
    def __init__(self, path, image, location = (0,0)):
        self.path = path
        self.image = image
        self.location = location