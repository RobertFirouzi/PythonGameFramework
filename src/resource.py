import pygame
import hashlib
#TODO - hash the filenames to lookup in dict?

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
