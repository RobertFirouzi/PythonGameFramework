import parameters as PRAM

# Image that can be used as layer of background or foreground.  Can be set to tile or scroll, and
# sections that are visible relative to the game level can be chosen
#
# @param path: directory of image
# @param image: filename of image
# @param imageSize: size in pixels of image [x,y]
# @param visibleSections: 2d array: each array is a box [left edge, right edge, top edge, bottom edge]
# @param scrolling: [[Xmultiplier, Xdivisor], [Xmultiplier, Xdivisor]]
# @param: alpha: does the image contain alpha information (e.g. invisiible pixels)
#
# Scroll speed can be calculated to perfectly scroll the level in the level editor, or user chosen. Formula to scroll the level is
#
# X direction:
# numerator: levelSize - displaywidth
# denomonator: imageSize - displaywidth
# numerator/denomonator = scroll speed in X direction to scroll the image over the entire level
#
# Y direction is same using Y params and displayheight
#
# NOTE if imageSize=displayWidth than set scroll speed to 0
#
# The above calculates the divisor.  Multiplier makes the image scroll faster then the level, so this must be user chosen.
# If user desires a 1.4 scroll speed, choose a multiplier of 14 and divisor of 10.


### NEED TO ADD DATABASE ENTRIES ### #TODO
##DEV
# isMotion = True means the panorama scrolls in X/Y direction as screen stays still
# motionX_pxs - Pixels per second (positive/negative determines direction) in X direction
# movementY_pxs - Pixels per second (positive/negative determines direction) in Y direction

##DEV
# isAnimated = True means the panorama is animated
# animated_ips = number of images per second
# TODO - rest of neeed animation params (eg pics, index of pic, etc)

class PanoramicImage():
    def __init__(self, 
                 filePath = '', 
                 pxSize = [10,10],  
                 visibleSections = [[0,200,0,200],[200,500,200,500]], 
                 scrolling = [[1,1],[1,1]], 
                 alpha = False,
                 layer= 0,
                 isMotion_X = False,
                 isMotion_Y = False,
                 motionX_pxs = 0,
                 motionY_pxs = 0):
        self.filePath = filePath
        self.pxSize = pxSize
        self.visibleSections = visibleSections
        self.scrolling = scrolling
        self.alpha = alpha
        self.layer = layer
        self.isMotion_X = isMotion_X
        self.isMotion_Y = isMotion_Y
        self.motionX_pxs = motionX_pxs
        self.motionY_pxs = motionY_pxs
        
        #explicit declaration of class fields
        self.image = None # the image date

        self.motion_x_multiplier = 0 #calculated by the Renderer on level load based on Game FPS
        self.motion_y_multiplier = 0