import pygame
from database import *
from graphics import PanoramaLayer, TilemapLayer, SpriteLayer, AnimatedTile
from  scene import Scene

class ResourceManager:
    def __init__(self):
        self.spriteImages = dict()
        self.spriteAccessories = dict()
        self.combinedSprites = dict()
        self.tilemapImages = dict()
        self.panoramaImages = dict()
        self.actors = dict()
        self.musicTracks = dict()
        self.soundEffects = dict()
        self.ambientTracks = dict()

    def loadPanoramaImage(self, filepath, isAlpha):
        image = self.panoramaImages.get(filepath)
        if image is None:
            if isAlpha:
                image = pygame.image.load(filepath).convert_alpha()
            else:
                image = pygame.image.load(filepath).convert()
            self.panoramaImages[filepath] = image
        return image

    def loadTilemapImage(self, filepath, isAlpha):
        image = self.tilemapImages.get(filepath)
        if image is None:
            if isAlpha:
                image = pygame.image.load(filepath).convert_alpha()
            else:
                image = pygame.image.load(filepath).convert()
            self.tilemapImages[filepath] = image
        return image

    def loadSpriteImage(self, filepath):
        pass

    def loadAccessoryImage(self, filepath):
        pass

    #returns a combined sprite image if exists
    def loadCombinedSprite(self, spriteHash):
        image = self.combinedSprites.get(spriteHash)
        if image is None:
            return False
        return image

    def addCombinedSprite(self, combinedSprite, spriteHash):
        self.combinedSprites[spriteHash] = combinedSprite

    def addActor(self, actor):
        current = self.actors.get(actor.id)
        if current is None:
            self.actors[actor.id] = actor

class LoaderBase:
    def __init_(self, resourceManager):
        self.resourceManager = resourceManager

    def loadResource(self, resourceId):
        pass

class TilemapLoader(LoaderBase):
    def __init__(self):
        super(TilemapLoader, self).__init__()

    def loadResource(self, resourceId):
        pass

class ActorLoader(LoaderBase):
    def __init__(self):
        super(ActorLoader, self).__init__()

    def loadResource(self, resourceId):
        pass

class SpriteLoader(LoaderBase):
    def __init__(self):
        super(SpriteLoader, self).__init__()

    def loadResource(self, resourceId):
        pass

class RenderLayerLoader(LoaderBase):
    def __init__(self):
        super(RenderLayerLoader, self).__init__()

    def loadResource(self, resourceData):
        pass

class TilemapLayerLoader(RenderLayerLoader):
    def __init__(self):
        super(TilemapLayerLoader, self).__init__()

    def loadResource(self, resourceData):
        tilemapImage = self._loadTilemapImage(resourceData)
        animatedTiles = self._loadAnimatedTiles(resourceData)

        return TilemapLayer(resourceData['name'],
                            resourceData['isNeedsSorting'],
                            resourceData['size_tiles'],
                            resourceData['tile_size'],
                            tilemapImage,
                            animatedTiles)

    def _loadTilemapImage(self, resourceData):
        tileImagePath = loadTileImagePath(resourceData['tilemap_id'])  # todo change name to tilmap image id?
        tilemapImage = None
        if tileImagePath:
            tilemapImage = self.resourceManager._loadTilemap(tileImagePath, resourceData['isAlpha'])

        return tilemapImage

    def _loadAnimatedTiles(self, resourceData):
        tileData = loadTilemapData(resourceData['id'])
        animatedTiles = list()
        for i in range(len(tileData)):
            tileRow = list()
            for j in range(len(tileData[i])):
                animatedTile = AnimatedTile(tileData[i][j]['index'], tileData[i][j]['fps'])
                tileRow.append(animatedTile)
            animatedTiles.append(tileRow)

class PanoramaLayerLoader(RenderLayerLoader):
    def __init__(self):
        super(PanoramaLayerLoader, self).__init__()

    def loadResource(self, resourceData):
        panoramaImagePaths = loadPanoramicImagePaths(resourceData['panorama_id'])
        panoramicImages = list()
        for imagePath in panoramaImagePaths:
            panoramicImages.append(self.resourceManager.loadPanorama(imagePath, resourceData['isAlpha']))

        return PanoramaLayer(resourceData['name'],
                             resourceData['isNeedsSorting'],
                             panoramicImages,
                             resourceData['visibleSections'],
                             resourceData['sizePx'],
                             resourceData['scrollSpeed'],
                             resourceData['fps'],
                             resourceData['isMotion'],
                             resourceData['motion_pps'])

class SpriteLayerLoader(TilemapLayerLoader):
    def __init__(self):
        super(SpriteLayerLoader, self).__init__()

    def loadResource(self, resourceData):
        tilemapImage = self._loadTilemapImage(resourceData)
        animatedTiles = self._loadAnimatedTiles(resourceData)

        actors = list() #TODO

        return SpriteLayer(resourceData['name'],
                           resourceData['isNeedsSorting'],
                           resourceData['size_tiles'],
                           resourceData['tile_size'],
                           tilemapImage,
                           animatedTiles,
                           actors)

class ResourceLoader:
    def __init__(self, resourceManager = None):
        self.resourceManager = resourceManager

        self.tilemapLoader = TilemapLoader()
        self.actorLoader = ActorLoader()
        self.spriteLoader = SpriteLoader()
        self.tilemapLayerLoader = TilemapLayerLoader()
        self.panoramaLayerLoader = PanoramaLayerLoader()
        self.spriteLayerLoader = SpriteLayerLoader()

    def loadScene(self, sceneId):
        levelData = loadSceneData(sceneId)
        renderLayerDatas = loadRenderLayers(sceneId)

        renderLayers = list()
        for layerData in renderLayerDatas:
            renderLayers.append(self._loadLayer(layerData))

        borderData = loadBorders(sceneId) #{layerIndex : [[border]]}

        return Scene(levelData['name'],
                           levelData['id'],
                           levelData['size_tiles'],
                           renderLayers,
                           borderData,
                           list(), #TODO eventBoxes
                           list(), #TODO game evenets
                           list()) #TODO actors


    def loadActor(self, actorId):
        return self.actorLoader.loadResource(actorId)

    def _loadTilemap(self, tilemapId):
        return self.tilemapLoader.loadResource(tilemapId)

    def _loadSprite(self, spriteId):
        return self.spriteLoader.loadResource(spriteId)

    def _loadLayer(self, layerData):
        if layerData['layerType'] == 'panorama':
            return self.panoramaLayerLoader.loadResource(layerData)

        elif layerData['layerType'] == 'tilemap':
            return self.tilemapLayerLoader.loadResource(layerData)

        elif layerData['layerType'] == 'sprite':
            return self.spriteLayerLoader.loadResource(layerData)