#Re-factor effort 3/11/18
#Contains the render class , and all supporting classes

from enum import Enum
import pygame

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

#base class used to implement loading data method
class Dataloader:
    def __init__(self):
        pass

    def loadData(self, isAlpha):
        pass

class ImageLoader(Dataloader):
    def __init__(self):
        super(ImageLoader, self).__init__()

class PanoramaLoader(ImageLoader):
    def __init__(self):
        super(PanoramaLoader, self).__init__()

    def loadData(self, isAlpha, isAnimated, numImages, filePath, imageType):
        convertedImages = []

        if isAnimated: #path is to a directory of images
            for i in range(numImages):
                if isAlpha:
                    convertedImages.append(pygame.image.load(filePath+'\\'+str(i)+'.'+imageType).convert_alpha())
                else:
                    convertedImages.append(pygame.image.load(filePath+'\\'+str(i)+'.'+imageType).convert())

        else: #path is directly to an image file
            if isAlpha:
                convertedImages.append(pygame.image.load(filePath).convert_alpha())  # tuple of one item
            else:
                convertedImages.append(pygame.image.load(filePath).convert())

        convertedImages = tuple(convertedImages)
        return convertedImages

class TileLoader(ImageLoader):
    def __init__(self):
        super(TileLoader, self).__init__()

class SpriteLoader(ImageLoader):
    def __init__(self):
        super(SpriteLoader, self).__init__()

class AnimatedConditionEnum(Enum):
    FROZEN = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2


#base class for any image class that needs to be rendered
class Animated:
    def __init__(self,
                 name,
                 dataLoader,
                 isAlpha,
                 isAnimated,
                 fps,
                 fpi,
                 numFrames,
                 imageData):

        self.name = name
        self.dataLoader = dataLoader
        self.isAlpha = isAlpha
        self.isAnimated = isAnimated
        self.fps = fps
        self.fpi = fpi
        self.numFrames = numFrames
        self.imageData = imageData

    def loadImage(self):
        self.imageData =  self.dataLoader.loadData()

class AnimatedPanorama(Animated):
    def __init__(self,
                 name,
                 panoramaLoader,
                 isAlpha,
                 isAnimated,
                 fps,
                 fpi,
                 numFrames,
                 imageData,
                 size,
                 ): #TODO - add params for panorama here
        super(AnimatedPanorama, self).__init__(name,panoramaLoader,isAlpha,isAnimated,fps,fpi,numFrames,imageData)

    def loadPanorama(self):
        self.imageData = self.loadData(self.isAlpha,self.isAnimated,self.numImages,self.filePath,self.imageType)

class AnimatedTile(Animated):
    def __init__(self,
                 name,
                 tileLoader,
                 isAlpha,
                 isAnimated,
                 fps,
                 fpi,
                 numFrames,
                 imageData): #TODO - add params for Tile here
        super(AnimatedTile, self).__init__(name,tileLoader,isAlpha,isAnimated,fps,fpi,numFrames,imageData)

class AnimatedAccessory(Animated):
    def __init__(self,
                 name,
                 spriteLoader,
                 isAlpha,
                 isAnimated,
                 fps,
                 fpi,
                 numFrames,
                 imageData,
                 accessoryCoordinates):
        super(AnimatedAccessory, self).__init__(name,spriteLoader,isAlpha,isAnimated,fps,fpi,numFrames,imageData)
        self.accessoryCoordinates = accessoryCoordinates

class AnimatedSprite(Animated):
    def __init__(self,
                 name,
                 spriteLoader,
                 isAlpha,
                 isAnimated,
                 fps,
                 fpi,
                 numFrames,
                 imageData,
                 spriteCoordinates,
                 animationAccessories):
        super(AnimatedSprite, self).__init__(name,spriteLoader,isAlpha,isAnimated,fps,fpi,numFrames,imageData)
        self.spriteCoordinates = spriteCoordinates
        self.animationAccessories = animationAccessories


#Base class for RenderParameters
class RenderParams:
    def __init_(self, imageData):
        self.imageData = imageData

class RenderPanoramaParams(RenderParams):
    def __init__(self, imageData):
        super(RenderPanoramaParams, self).__init__(imageData)

class RenderTileParams(RenderParams):
    def __init__(self, imageData):
        super(RenderTileParams, self).__init__(imageData)

class RenderActorParams(RenderParams):
    def __init__(self, imageData):
        super(RenderActorParams, self).__init__(imageData)


#base class for renderingActions
class RenderAction:
    def __init__(self, target):
        self.target = target #surface to render to, eg screen, or anoy other 'blittable' surface

    #implement in the subclass
    def renderAll(self, renderParams):
        pass

    def renderChanged(self, renderParams):
        pass

    def render(self, renderParams):
        pass

class RenderPanoramaAction(RenderAction):
    def __init__(self, target):
        super(RenderPanoramaAction, self).__init__(target)

    #algorithm here to render the panorama to the screen
    def renderAll(self, renderPanoramaParams):
        pass

    def renderChanged(self, renderPanoramaParams):
        pass

class RenderTileAction(RenderAction):
    def __init__(self, target):
        super(RenderTileAction, self).__init__(target)

    def render(self, renderTileParams):
        pass

class RenderActorAction(RenderAction):
    def __init__(self, target):
        super(RenderActorAction, self).__init__(target)

    #Always render the full actor, but may only call this method id actor has changed
    def render(self, renderActorParams):
        pass

class RenderLayer:
    def __init__(self):
        pass

    def renderAll(self, renderParams):
        pass

    def renderChanged(self, renderParams):
        pass

class PanoramaLayer(RenderLayer):
    def __init__(self, panoramicImage):
        super(PanoramaLayer, self).__init__()
        self.panoramicImage = panoramicImage

    def renderAll(self, renderPanoramaParams):
        self.panoramicImage.renderAll(renderPanoramaParams)

    def renderChanged(self, renderPanoramaParams):
        self.panoramicImage.renderChanged(renderPanoramaParams)

class TileLayer(RenderLayer):
    def __init__(self, animatedTiles):
        super(TileLayer, self).__init__()
        self.animatedTiles = animatedTiles

    def renderAll(self, renderTileParams):
        for tile in self.animatedTiles:
            tile.render(renderTileParams)

    def renderChanged(self, renderTileParams):
        for tile in self.animatedTiles:
            if tile.isChanged:
                tile.render(renderTileParams)

#contains all of the actors to be rendered on a layer
class ActorLayer(RenderLayer):
    def __init__(self, actors):
        super(ActorLayer, self).__init__()
        self.actors = actors

    def renderAll(self, renderActorParams):
        for actor in self.actors:
            actor.render(renderActorParams)

    def renderChanged(self, renderActorParams):
        for actor in self.actors:
            if actor.isChanged:
                actor.render(renderActorParams)


#Base class to be inherited by any classes which are rendered to the target (screen)
class Renderable:
    def __init__(self, renderAction):
        self.renderAction = renderAction

    def renderAll(self, renderParams):
        self.renderAction.renderAll(renderParams)

    def renderChanged(self, renderParams):
        self.renderAction.renderChanged(renderParams)

    def render(self, renderParams):
        self.renderAction.render(renderParams)

class PanoramicImage(Renderable): #TODO add animated panorama
    def __init__(self, renderPanoramaAction):
        super(PanoramicImage, self).__init__(renderPanoramaAction)

class Tilemap(Renderable): #TODO add tileList
    def __init__(self, renderTileAction):
        super(Tilemap, self).__init__(renderTileAction)

class Actor(Renderable):
    def __init__(self,
                 renderActorAction,
                 name,
                 size,
                 position,
                 direction,
                 isFocus,
                 isChanged):
        super(Actor, self).__init__(renderActorAction)
        self.name = name
        self.size = size
        self.position = position
        self.direction = direction
        self.isFocus = isFocus
        self.isChanged = isChanged

class CharacterSprite(Actor):
    def __init__(self,
                 renderActorAction,
                 name,
                 size,
                 position,
                 direction,
                 isFocus,
                 isChanged,
                 animatedSprites,
                 currentSprite,
                 animatedConditionEnum,
                 frameIndex,
                 frameCount,
                 speed):
        super(CharacterSprite, self).__init__(renderActorAction,name,size,position,direction,isFocus,isChanged)
        self.animatedSprites = animatedSprites
        self.currentSprite = currentSprite
        self.animatedConditionEnum = animatedConditionEnum
        self.frameIndex = frameIndex
        self.frameCount = frameCount
        self.speed =speed

#Controlling class for overall rendering process
#Calls the update and render methods on each layer to be rendered
class Renderer:
    def __init__(self):
        self.camera = None
        self.layers = None #contains an ordered list of layers to render
        self.mapTileSize = None

        self.renderLayers = []

        self.isRenderAll = True
        self.renderQueue = []
        self.frameCount = 0

    #increments the animated indexes, and the renderQueue
    def updateAnimatedIndex(self):
        pass

    def render(self):
        if self.camera.moveFlag:
            self.isRenderAll = True

        self.updateAnimatedIndex()

        if self.isRenderAll:
            for layer in self.renderLayers:
                layer.renderAll()
        else:
            for layer in self.renderLayers:
                layer.renderChanged()

        self.renderQueue.clear()
        self.camera.moveFlag = False
        self.isRenderAll = False
        #clear rendered tiles, stoed in tilemap now?

        self.frameCount+=1
