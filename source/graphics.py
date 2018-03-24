#Re-factor effort 3/11/18
#Contains the render class , and all supporting classes

from enum import Enum
from parameters import *

class AnimatedConditionEnum(Enum):
    FROZEN = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2

class DirectionEnum(Enum):
    DOWN = 0
    DOWN_LEFT = 1
    LEFT = 2
    LEFT_UP = 3
    UP = 4
    UP_RIGHT = 5
    RIGHT = 6
    RIGHT_DOWN = 7

class RenderQBox:
    def __init__(self, position, size):
        self.position = position
        self.size = size

class CropPosition:
    def __init__(self, position, size):
        self.position = position
        self.size = size


#container class for coordinates of 1 frame of a sprite image
class SpriteCoordinates:
    def __init__(self, start, size):
        self.start = start
        self.size = size

#container class for a sprite accessory, needs to know the raltive position of the base image to blit to
class AccessoryCoordinates(SpriteCoordinates):
    def __init__(self, start, size, relative_start):
        super(AccessoryCoordinates, self).__init__(start, size)
        self.relative_start = relative_start

class ScrollSpeed:
    def __init__(self, mult_x, div_x, mult_y, div_y):
        self.mult_x = mult_x
        self.div_x = div_x
        self.mult_y = mult_y
        self.div_y = div_y

class ImageBuffer:
    def __init__(self, imageData, screenX, screenY, cropX, cropY, width, height):
        self.imageData = imageData
        self.screenX = screenX
        self.screenY = screenY
        self.cropX = cropX
        self.cropY = cropY
        self.width = width
        self.height = height

class AnimationState:
    def __init__(self,
                 animatedConditionEnum = AnimatedConditionEnum.FROZEN,
                 speed = 100,
                 frameIndex = 0,
                 frameCount = 0):
        self.animatedConditionEnum = animatedConditionEnum
        self.speed = speed  # percent
        self.frameIndex = frameIndex
        self.frameCount = frameCount

        self.numFrames = 1
        self.fpi = 1

    #call this with the num frames and fpi
    def initialize(self,
                   numFrames = 1,
                   fpi = 1,
                   animatedConditionEnum = AnimatedConditionEnum.FROZEN,
                   speed = 100,
                   frameIndex = 0,
                   frameCount = 0):
        self.numFrames = numFrames
        self.fpi = fpi
        self.animatedConditionEnum = animatedConditionEnum
        self.speed = speed
        self.frameIndex = frameIndex
        self.frameCount = frameCount

    #returns true if image index updated
    def updateAnimatedIndex(self):
        if self.animatedConditionEnum != AnimatedConditionEnum.FROZEN:
            self.frameCount += 1
        if self.numFrames ==1:
            return False
        if self.frameCount % self.fpi == 0:
            self.frameIndex = (self.frameIndex+1)%self.numFrames
            return True
        return False

class AnimatedTile:
    def __init__(self,
                 name,
                 tilemapIndex,
                 imageCoordinates,
                 fps,
                 numFrames):
        self.name = name
        self.tilemampIndex = tilemapIndex
        self.imageCoordinates = imageCoordinates
        self.fps = fps
        self.numFrames = numFrames

        self.fpi = 1 #TODO where calculated?
        self.animationState = AnimationState()
        self.isChanged = False

    def currentImage(self):
        return [] #CropPosition()

    def updateAnimation(self):
        pass #TODO update animation index
        return [] #RenderQBox()TODO return render box

class SpriteAccessory:
    def __init__(self,
                 name,
                 filepath,
                 accessoryCoordinates):
        self.name = name
        self.filepath = filepath
        self.accessoryCoordinates = accessoryCoordinates

        self.accessoryImage = None

class AnimatedSprite:
    def __init__(self,
                 name,
                 filepath,
                 spriteCoordinates,
                 fps,
                 numFrames,
                 animationAccessories):
        self.name = name
        self.filepath = filepath
        self.spriteCoordinates = spriteCoordinates
        self.fps = fps
        self.numFrames = numFrames
        self.animationAccessories = animationAccessories

        self.spriteImage = None

        self.fpi = 1 #TODO where calculated?

    def curentImage(self, animationState, direction):
        return [] #CropPosition() TODO return coordinates of image

class Actor: #TODO note this is defined several spots, this should be most up to date, others deleted.
    def __init__(self,
                  name,
                  size,
                  isFocus,
                  characterSprites,
                  position,
                  direction):
        self.name = name
        self.size = size
        self.isFocus = isFocus
        self.characterSprites = characterSprites
        self.position = position
        self.direction = direction

        self.currentSprite = None
        self.animationState = AnimationState()
        self.isChanged = False

    def updateAnimation(self):
        isChanged = self.animationState.updateAnimatedIndex()
        if isChanged: #TODO - return a render box
            return []#RenderQBox()
        else:
            return []

    def genImageBuf(self, offsets, renderQ):
        return [] #ImageBuffer() TODO return the imageBuffer


class RenderableLayer:
    def __init__(self, name, isNeedsSorting):
        self.name = name
        self.isNeedsSorting = isNeedsSorting

    def updateAnimations(self):
        return []

    def genImageBufs(self, offsets, renderQ):
        return []

class PanoramaLayer(RenderableLayer):
    def __init__(self,
                 name,
                 filepath,
                 isAlpha,
                 visibleSections,
                 size,
                 fps,
                 numFrames,
                 scrollSpeed,
                 isMotion,
                 motion_pps,
                 isNeedsSorting = False):
        super(PanoramaLayer, self).__init__(name, isNeedsSorting = isNeedsSorting)
        self.filepath = filepath
        self.isAlpha = isAlpha
        self.visibleSections = visibleSections
        self.size = size
        self.fps = fps
        self.numFrames = numFrames
        self.scrollSpeed = scrollSpeed
        self.isMotion = isMotion
        self.motion_pps = motion_pps

        self.panoramicImages = None
        self.motionMultiplier = [motion_pps[0]/GAME_FPS, motion_pps[1]/GAME_FPS]
        self.fpi = 1 #TODO where is this calculated?
        self.motionOffset = [0,0]
        self.animationState = AnimationState() #TODO, need fpi in here and in class?
        self.animationState.initialize(self.numFrames, self.fpi)

    def updateAnimations(self):
        isUpdated = self.animationState.updateAnimatedIndex()
        if self.isMotion[0]:
            motionOffset = int(self.motionMultiplier[0] * self.animationState.frameCount)
            if motionOffset != self.motionOffset[0]:  # panorama needs to move
                self.motionOffset[0] = motionOffset
                isUpdated = True  # if panorama needs to scroll, re-render visibile sections
        if self.isMotion[1]:
            motionOffset = int(self.motionMultiplier[1] * self.animationState.frameCount)
            if motionOffset != self.motionOffset[1]:
                self.motionOffset[1] = motionOffset
                isUpdated = True

        if isUpdated:
            return [] #RenderQBox() TODO - return a render box here
        return []

    def genImageBufs(self, offsets, renderQ):
        return [] #ImageBuffer() TODO return the imageBuffers

class TilemapLayer(RenderableLayer):
    def __init__(self,
                 name,
                 filepath,
                 size_tiles,
                 tileSize,
                 isAlpha,
                 animatedTiles,
                 isNeedsSorting = False):
        super(TilemapLayer, self).__init__(name, isNeedsSorting = isNeedsSorting)
        self.filepath = filepath
        self.size_tiles = size_tiles
        self.tileSize = tileSize
        self.isAlpha = isAlpha
        self.animatedTiles = animatedTiles

        self.tilemapImage = None

    def updateAnimations(self):
        return [] #RenderQBox() TODO - return render boxes here

    def genImageBufs(self, offsets, renderQ):
        return [] #ImageBuffer() TODO return the imageBuffers

    def tilemapIndexCoordinateConvert(self):
        pass #TODO

class SpriteLayer(RenderableLayer):
    def __init__(self,
                 name,
                 filepath,
                 size_tiles,
                 tileSize,
                 isAlpha,
                 animatedTiles,
                 actors,
                 isNeedsSorting = True):
        super(SpriteLayer, self).__init__(name, isNeedsSorting = isNeedsSorting)
        self.filepath = filepath
        self.size_tiles = size_tiles
        self.tileSize = tileSize
        self.isAlpha = isAlpha
        self.animatedTiles = animatedTiles
        self.actors = actors

        self.tilemapImage = None

    def updateAnimations(self):
        return [] #RenderQBox()TODO - return render boxes here for tiles and actors

    def genImageBufs(self, offsets, renderQ):
        return [] #ImageBuffer() TODO return the imageBuffers for tiles and actors

    def tilemapIndexCoordinateConvert(self):
        pass #TODO