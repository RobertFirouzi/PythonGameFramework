import pygame
from database import DataLoader

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
    def __init_(self):
        pass

    def loadResource(self, resourceId):
        pass

class PanoramaLoader(LoaderBase):
    def __init__(self):
        super(PanoramaLoader, self).__init__()

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

    def loadResource(self, resourceId):
        pass

class TilemapLayerLoader(RenderLayerLoader):
    def __init__(self):
        super(TilemapLayerLoader, self).__init__()

    def loadResource(self, resourceId):
        pass

class PanoramaLayerLoader(RenderLayerLoader):
    def __init__(self):
        super(PanoramaLayerLoader, self).__init__()

    def loadResource(self, resourceId):
        pass

class SpriteLayerLoader(RenderLayerLoader):
    def __init__(self):
        super(SpriteLayerLoader, self).__init__()

    def loadResource(self, resourceId):
        pass


class ResourceLoader:
    def __init__(self, resourceManager = None):
        self.resourceManager = resourceManager

        self.panoramaLoader = PanoramaLoader()
        self.tilemapLoader = TilemapLoader()
        self.actorLoader = ActorLoader()
        self.spriteLoader = SpriteLoader()
        self.tilemapLayerLoader = TilemapLayerLoader()
        self.panoramaLayerLoader = PanoramaLayerLoader()
        self.spriteLayerLoader = SpriteLayerLoader()

    def loadScene(self, sceneId):
        return None

    def loadActor(self, actorId):
        return self.actorLoader.loadResource(actorId)

    def loadPanorama(self, panoramaId):
        return self.panoramaLoader.loadResource(panoramaId)

    def loadTilemap(self, tilemapId):
        return self.tilemapLoader.loadResource(tilemapId)

    def loadSprite(self, spriteId):
        return self.spriteLoader.loadResource(spriteId)

    def loadLayer(self, layerId):
        pass