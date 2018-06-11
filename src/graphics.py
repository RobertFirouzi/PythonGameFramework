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
                 panoramicImages,
                 visibleSections,
                 sizePx,
                 scrollSpeed,
                 fps,
                 isMotion,
                 motion_pps):
        super(PanoramaLayer, self).__init__(name, isNeedsSorting)
        self.panoramicImages = panoramicImages
        self.visibleSections = visibleSections
        self.sizePx = sizePx
        self.scrollSpeed = scrollSpeed
        self.fps = fps
        self.isMotion = isMotion
        self.motion_pps = motion_pps

        self.numFrames = len(panoramicImages)
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
                 tilemapImage,
                 animatedTiles):
        super(TilemapLayer, self).__init__(name, isNeedsSorting)
        self.size_tiles = size_tiles
        self.tileSize = tileSize
        self.tilemapImage = tilemapImage
        self.animatedTiles = animatedTiles

    def tilemapIndexCoordinateConvert(self): #TODO
        pass

class SpriteLayer(TilemapLayer):
    def __init__(self,
                 name,
                 isNeedsSorting,
                 size_tiles,
                 tileSize,
                 tilemapImage,
                 animatedTiles,
                 actors):
        super(SpriteLayer, self).__init__(name, isNeedsSorting, size_tiles, tileSize, tilemapImage, animatedTiles)
        self.actors = actors