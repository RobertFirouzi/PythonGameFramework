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

    def loadPanorama(self, filepath, isAlpha):
        image = self.panoramaImages.get(filepath)
        if image is None:
            if isAlpha:
                image = pygame.image.load(filepath).convert_alpha()
            else:
                image = pygame.image.load(filepath).convert()
            self.panoramaImages[filepath] = image
        return image

    def loadTilemap(self, filepath, isAlpha):
        image = self.tilemapImages.get(filepath)
        if image is None:
            if isAlpha:
                image = pygame.image.load(filepath).convert_alpha()
            else:
                image = pygame.image.load(filepath).convert()
            self.tilemapImages[filepath] = image
        return image

    def loadSprite(self, filepath):
        pass

    def loadAccessory(self, filepath):
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

class SceneLoader(LoaderBase):
    def __init__(self):
        super(SceneLoader, self).__init__()

    def loadScene(self, sceneId):
        return None


class PanoramaLoader(LoaderBase):
    def __init__(self):
        super(PanoramaLoader, self).__init__()

    def loadPanorama(self, panoramaId):
        return None


class TilemapLoader(LoaderBase):
    def __init__(self):
        super(TilemapLoader, self).__init__()

    def loadTilemap(self, tilemapId):
        return None


class ActorLoader(LoaderBase):
    def __init__(self):
        super(ActorLoader, self).__init__()

    def loadActor(self, actorId):
        return None


class SpriteLoader(LoaderBase):
    def __init__(self):
        super(SpriteLoader, self).__init__()

    def loadSprite(self, spriteId):
        return None

class ResourceLoader:
    def __init__(self, resourceManager = None):
        self.resourceManager = resourceManager

        self.sceneLoader = SceneLoader(),
        self.panoramaLoader = PanoramaLoader(),
        self.tilemapLoader = TilemapLoader(),
        self.actorLoader = ActorLoader(),
        self.spriteLoader = SpriteLoader(),

    def loadScene(self, sceneId):
        return self.sceneLoader.loadScene(sceneId)

    def loadActor(self, actorId):
        return self.actorLoader.loadActor(actorId)

    def loadPanorama(self, panoramaId):
        return self.panoramaLoader.loadPanorama(panoramaId)

    def loadTilemap(self, tilemapId):
        return self.tilemapLoader.loadTilemap(tilemapId)

    def loadSprite(self, spriteId):
        return self.spriteLoader.loadSprite(spriteId)