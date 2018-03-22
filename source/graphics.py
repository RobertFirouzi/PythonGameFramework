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
            return [] #TODO - return a render box here
        return []

class TilemapLayer(RenderableLayer):
    def __init__(self,
                 name,
                 filepath,
                 size_tiles,
                 tileSize,
                 isAlpha,
                 animatedTiles,
                 isNeedsSorting = False):
        super(TilemapLayer, self).__init__(name, isNeedsSorting)
        self.name = name
        self.filepath = filepath
        self.size_tiles = size_tiles
        self.tileSize = tileSize
        self.isAlpha = isAlpha
        self.animatedTiles = animatedTiles

        self.tilemapImage = None

    def updateAnimations(self):
        return []

    def genImageBufs(self, offsets, renderQ):
        return []

    def tilemapIndexCoordinateConvert(self):
        pass



class AnimatedAccessory(AnimatedImage):
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 image,
                 accessoryCoordinates):
        super(AnimatedAccessory, self).__init__(name,fps,numFrames,image)
        self.accessoryCoordinates = accessoryCoordinates

class AnimatedSprite(AnimatedImage):
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 image,
                 spriteCoordinates,
                 animationAccessories):
        super(AnimatedSprite, self).__init__(name,fps,numFrames,image)
        self.spriteCoordinates = spriteCoordinates
        self.animationAccessories = animationAccessories


#Base class to be inherited by any classes which are rendered to the target (screen)
class Renderable:
    def __init__(self):
        pass

class PanoramicImage(Renderable):
    def __init__(self,
                 animatedPanorama):
        super(PanoramicImage, self).__init__()
        self.animatedPanorama = animatedPanorama

    def update(self):
        return self.animatedPanorama.update()


class Tilemap(Renderable):
    def __init__(self,
                 name,
                 image,
                 tileSize,
                 size_tiles,
                 animatedTiles):
        super(Tilemap, self).__init__()
        self.name = name
        self.image = image
        self.tileSize = tileSize
        self.size_tiles = size_tiles
        self.animatedTiles = animatedTiles

class Actor(Renderable):
    def __init__(self,
                 name,
                 size):
        super(Actor, self).__init__()
        self.name = name
        self.size = size

        self.position = [0,0]
        self.direction = DirectionEnum.DOWN
        self.isFocus = False
        self.isChanged = False

class CharacterSprite(Actor):
    def __init__(self,
                 name,
                 size,
                 animatedSprites):
        super(CharacterSprite, self).__init__(name,size)
        self.animatedSprites = animatedSprites

        self.currentSprite = animatedSprites[0]
        self.animationState = AnimationState()
        self.animationState.initialize(self.currentSprite.numFrames, self.currentSprite.fpi)

    def update(self):
        self.isChanged = self.animationState.updateAnimatedIndex()
        return self.isChanged