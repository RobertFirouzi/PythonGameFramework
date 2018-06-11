import pygame

class ResourceManager:
    def __init__(self):
        self.spriteImages = dict()
        self.spriteAccessories = dict()
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

    def loadspriteAccessories(self, filepath):
        pass