#Re-factor effort 3/11/18
#Contains the render class , and all supporting classes

from enum import Enum
from parameters import *

class AnimatedConditionEnum(Enum):
    FROZEN = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2

class LayerTypeEnum(Enum):
    PANORAMA = 0
    TILEMAP = 1
    SPRITE = 2

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
        self.mult_x = mult_x
        self.div_y = div_y
        self.div_y = div_y

class Image:
    def __init__(self, filepath, isAlpha):
        self.filepath = filepath
        self.isAlpha = isAlpha

        self.imageData = None

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

#base class for any image class that needs to be rendered
class Animated:
    def __init__(self,
                 name,
                 fps,
                 numFrames):
        self.name = name
        self.fps = fps
        self.numFrames = numFrames

        self.fpi = round(GAME_FPS/fps,2)

#For classes which have seperate images to create an animation
class AnimatedSet(Animated):
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 images):
        super(AnimatedSet, self).__init__(name,fps,numFrames)
        self.images = images

#for classes which animate by using sections of one image
class AnimatedImage(Animated):
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 image):
        super(AnimatedImage, self).__init__(name,fps,numFrames)
        self.image = image

class AnimatedPanorama(AnimatedSet): #TODO - documentation in scenery.py is good, ionclude it
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 images,
                 size,
                 visibleSections,
                 scrollSpeed,
                 isMotion_X,
                 isMotion_Y,
                 motionX_pxs,
                 motionY_pxs):
        super(AnimatedPanorama, self).__init__(name,fps,numFrames,images)
        self.size = size
        self.visibleSections = visibleSections
        self.scrollSpeed = scrollSpeed
        self.isMotion_X = isMotion_X
        self.isMotion_Y = isMotion_Y
        self.motionX_pxs = motionX_pxs
        self.motionY_pxs = motionY_pxs


        self.motion_x_multiplier = motionX_pxs/GAME_FPS
        self.motion_y_multiplier = motionY_pxs/GAME_FPS

        self.animationState = AnimationState()
        self.animationState.initialize(self.numFrames, self.fpi)
        self.motionOffset_X = 0 #used to determine if re-render needed on render changed call
        self.motionOffset_Y = 0

    #increments the framecount and updates the animation and motion
    def update(self):
        isUpdated = self.animationState.updateAnimatedIndex()
        if self.isMotion_X:
            motionOffset = int(self.motion_x_multiplier * self.animationState.frameCount)
            if motionOffset != self.motionOffset_X:  # panorama needs to move
                self.motionOffset_X = motionOffset
                isUpdated = True  # if panorama needs to scroll, re-render visibile sections
        if self.isMotion_Y:
            motionOffset = int(self.motion_y_multiplier * self.animationState.frameCount)
            if motionOffset != self.motionOffset_Y:
                self.motionOffset_Y = motionOffset
                isUpdated = True
        return isUpdated

class AnimatedTile(Animated):
    def __init__(self,
                 name,
                 fps,
                 numFrames,
                 coordinates):  #list of locations on the tilemap image
        super(AnimatedTile, self).__init__(name, fps, numFrames)
        self.coordinates = coordinates #index into correct positon with frameIndex

        self.isChanged = False
        self.animationState = AnimationState()
        self.animationState.initialize(self.numFrames, self.fpi)


    def update(self):
        self.isChanged = self.animationState.updateAnimatedIndex()
        return self.isChanged

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


class RenderLayer:
    def __init__(self, layerType):
        self.layerType = layerType

class PanoramaLayer(RenderLayer):
    def __init__(self, panoramicImage):
        super(PanoramaLayer, self).__init__(LayerTypeEnum.PANORAMA)
        self.panoramicImage = panoramicImage

class TileLayer(RenderLayer):
    def __init__(self, tilemap):
        super(TileLayer, self).__init__(LayerTypeEnum.TILEMAP)
        self.tilemaps = tilemap

class SpriteLayer(RenderLayer):
    def __init__(self, characterSprites):
        super(SpriteLayer, self).__init__(LayerTypeEnum.SPRITE)
        self.characterSprites = characterSprites