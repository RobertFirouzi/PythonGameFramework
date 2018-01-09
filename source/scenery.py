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
# animated panorama filepath is to a directory of numbered pictures [0.<extension>, 1.<extension>, etc]
# engine will go through all images in order at designated fps (frames per second)
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
                 motionY_pxs = 0,
                 isAnimated = False,
                 animated_fps = 0):
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
        self.isAnimated = isAnimated
        self.animated_fps = animated_fps

        #explicit declaration of class fields
        self.image = None # the image date

        self.motion_x_multiplier = 0 #calculated by the Renderer on level load based on Game FPS
        self.motion_y_multiplier = 0
        self.framesPerImage = 1 #if animated, the number of frames per each image flip, calculated in renderer leve load
        self.numbImages = 1 #calculated when loaded
        self.imageIndex = 0 #tracks which image to display, if animated


# Class to contain data for a tilemap
# The tiles are stored in 1 image file. To blit a tile correctly, use tiles index -
# - and calculate based on tilesize and tiles per row
# A tile index 0 is blank (nothing blitted)
# If the tilemap contains animated tiles, the animated tiles begin at the highest index.  All frames are stored
# sequentially in the tilemap image.  The tiles index will always reference the first tile in an animated group
# Go througn the animated tiles sequence based on framecount
# Although upper and lower stored in same DB row, this continer holds just one
# Does not hold the borders info
class Tilemap():
    def __init__(self,
                 filePath = '', #location of image to load
                 height_tiles = 3,
                 width_tiles = 3,
                 tileSize_px = 48,
                 tiles = ((0,0,0),(0,0,0),(0,0,0),), #this maps the location on the image to load based on tilesize
                 type = 'lower', #lower or upper tilemap
                 isAnimated = False, #if animated, some tiles contain multiple frames
                 animatedIndex = 9, #the tiles at this index and higher are part of animated groups
                 frames = 1, #how many frames there are in the animation, ie how many tiles in an animated group
                 fps = 1): #how fast the animation should play
        self.filePath = filePath
        self.height_tiles = height_tiles
        self.width_tiles = width_tiles
        self.tileSize_px = tileSize_px
        self.tiles = tiles
        self.type = type
        self.isAnimated = isAnimated
        self.animatedIndex = animatedIndex
        self.frames = frames
        self.fps = fps

        #explicit declaration of class fields
        self.image = None
        self.framesPerImage = 1 #if animated, the number of frames per each image flip, calculated in renderer leve load
        self.frameIndex = 0 #tracks which frame to display, if tile is animated



