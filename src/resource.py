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

    #keeps track of combined sprite images
    #need to think of which object should perform the combonation of the sprite image
    #usea MD5 hash as a lookup for the combined filepaths of sprite+accessorys
    def loadCombinedSprite(self, sprite, spriteFilepath, accessory, accessoryFilepaths):
        pass