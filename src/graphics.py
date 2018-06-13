class AnimationState:
    def __init__(self):
        pass

class AnimatedTile:
    def __init__(self, tilemapIndex, fps):
        self.tilemapIndex = tilemapIndex
        self.fps = fps

        self.numFrames = len(tilemapIndex)
        self.imageCorodinates = [0,0] #TODO - calculate based on index
        self.fpi = 0 #TODO calculate based on game fps and objec fps
        self.animationState = AnimationState()
        self.isChanged = False

class RenderableLayer:
    def __init__(self, name, isNeedsSorting):
        self.name = name
        self.isNeedsSorting = isNeedsSorting

class PanoramaLayer(RenderableLayer):
    def __init__(self,
                 name,
                 isNeedsSorting, #if the layer has sprites which need to be rendered in order
                 images,
                 visibleSections,
                 sizePx,
                 scrollSpeed,
                 fps,
                 isMotion,
                 motion_pps):
        super(PanoramaLayer, self).__init__(name, isNeedsSorting)
        self.images = images
        self.visibleSections = visibleSections
        self.sizePx = sizePx
        self.scrollSpeed = scrollSpeed
        self.fps = fps
        self.isMotion = isMotion
        self.motion_pps = motion_pps

        self.numFrames = len(images)
        self.fpi = 0 #TODO - calc based on fps
        self.motionMultiplier = 0 #TODO calc
        self.motionOffset = 0
        self.animationState = AnimationState()

class TilemapLayer(RenderableLayer):
    def __init__(self,
                 name,
                 isNeedsSorting,
                 size_tiles,
                 tileSize,
                 img,
                 animatedTiles):
        super(TilemapLayer, self).__init__(name, isNeedsSorting)
        self.size_tiles = size_tiles
        self.tileSize = tileSize
        self.img = img
        self.animatedTiles = animatedTiles

    def tilemapIndexCoordinateConvert(self):
        pass

class SpriteLayer(TilemapLayer):
    def __init__(self,
                 name,
                 isNeedsSorting,
                 size_tiles,
                 tileSize,
                 img,
                 animatedTiles,
                 actors):
        super(SpriteLayer, self).__init__(name, isNeedsSorting, size_tiles, tileSize, img, animatedTiles)
        self.actors = actors

class Sprite:
    def __init__(self,
                 id,
                 name,
                 spriteBoxes,
                 accessories,
                 fps):
        self.id = id
        self.name = name
        self.spriteBoxes = spriteBoxes
        self.accessories = accessories
        self.fps = fps

        self.img = None
        self.numFrames = len(next(iter(spriteBoxes.values()))) #this gets the number of items in the lest = numb frames


    def currentImg(self, animationState, direction):
        pass

class Accessory:
    def __init__(self,
                 id,
                 name,
                 spriteBoxes,
                 relativeStarts):
        self.id = id
        self.name = name
        self.spriteBoxes = spriteBoxes
        self.relativeStarts = relativeStarts

        self.img = None





