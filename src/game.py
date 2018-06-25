import pygame
from render import RenderManager
from parameters import *
from setup import eventHandlerFactory, playerFactory, soundPlayerFactory
from input import InputHandler, ButtonMap
from resource import ResourceManager, ResourceLoader
from scene import Scene
from database import DataLoader
from graphics import AnimatedTile, PanoramaLayer, TilemapLayer, SpriteLayer, Sprite, Accessory
from event import EventSetInput
from character import Actor

#TODO - need to load sprites, apply accessory, pass to resource manager
#TODO - need to load actors, pass to resource manager, add to level
#TODO - get rid of renderBox classes, - just use common format of [x, y, width height]
class Camera:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        self.player = playerFactory()
        self.renderManager = RenderManager()
        self.resourceManager = ResourceManager()
        self.resourceLoader = ResourceLoader(self.resourceManager)
        self.eventHandler = eventHandlerFactory(self)
        self.inputHandler = InputHandler(self, self.player, ButtonMap())
        self.musicHandler, self.soundEffectHandler = soundPlayerFactory()
        self.camera = Camera

        self.screen = None
        self.scene = None
        self.running = True

    def loadScene(self, eventLoadScene): #TODO - this function may contain too much work, pass work to other classes create a manager class
        self.unloadScene()
        self.addEvent(EventSetInput(INPTYPE_NORMAL))
        self.dataLoader.setLevelId(eventLoadScene.levelIndex)
        levelData = self.dataLoader.loadLevelData()  #TODO - move loading data logic into ResourceLoader
        renderLayerDatas = self.dataLoader.loadRenderLayers()

        renderLayers = list()
        for layer in renderLayerDatas:

            if layer['layerType'] == 'panorama':
                panoramaImagePaths = self.dataLoader.loadPanoramicImagePaths(layer['panorama_id'])
                panoramicImages = list()
                for imagePath in panoramaImagePaths:
                    panoramicImages.append(self.resourceManager.loadPanorama(imagePath, layer['isAlpha']))

                panoramicLayer = PanoramaLayer(layer['name'],
                                               layer['isNeedsSorting'],
                                               panoramicImages,
                                               layer['visibleSections'],
                                               layer['sizePx'],
                                               layer['scrollSpeed'],
                                               layer['fps'],
                                               layer['isMotion'],
                                               layer['motion_pps'])

                renderLayers.append(panoramicLayer)

            elif layer['layerType'] == 'tilemap' or layer['layerType'] == 'sprite':
                tileImagePath = self.dataLoader.loadTileImagePath(layer['tilemap_id'])
                tileData = self.dataLoader.loadTilemapData(layer['id'])

                animatedTiles = list()
                for i in range(len(tileData)):
                    tileRow = list()
                    for j in range(len(tileData[i])):
                        animatedTile = AnimatedTile(tileData[i][j]['index'],tileData[i][j]['fps'])
                        tileRow.append(animatedTile)
                    animatedTiles.append(tileRow)

                tilemapImage = None
                if tileImagePath:
                    tilemapImage = self.resourceManager.loadTilemap(tileImagePath, layer['isAlpha'])

                #TODO - loadActors
                if layer['layerType'] == 'tilemap':
                    tilemapLayer = TilemapLayer(layer['name'],
                                                layer['isNeedsSorting'],
                                                layer['size_tiles'],
                                                layer['tile_size'],
                                                tilemapImage,
                                                animatedTiles)

                    renderLayers.append(tilemapLayer)

                elif layer['layerType'] == 'sprite':
                    spriteLayer = SpriteLayer(layer['name'],
                                              layer['isNeedsSorting'],
                                              layer['size_tiles'],
                                              layer['tile_size'],
                                              tilemapImage,
                                              animatedTiles,
                                              list())

                    renderLayers.append(spriteLayer)

        borderData = self.dataLoader.loadBorders() #{layerIndex : [[border]]}

        self.scene = Scene(levelData['name'],
                           levelData['id'],
                           levelData['size_tiles'],
                           renderLayers,
                           borderData,
                           list(), #TODO eventBoxes
                           list(), #TODO game evenets
                           list()) #TODO actors

        #TODO - pass render layers to rendermanager


    def loadActor(self, actorId, position = (0,0), direction = 0, isFocus = False):
        #TODO Note: check to see if loaded in resource manager first?
        actorData = self.dataLoader.loadActorData(actorId)
        sprites =dict()

        accessoryDatas = list()
        for accessoryId in actorData['accessories']:
            accessoryDatas.append(self.dataLoader.loadAccessoryData(accessoryId))

        for key, value in actorData['sprites']:
            spriteData = self.dataLoader.loadSpriteData(value)
            accessories = list() #to contain the objects
            for accessoryData in accessoryDatas:
                positionData = self.dataLoader.loadAccessoryPositionData(spriteData['id'], accessoryData['id'])
                accessoryImagePath = self.dataLoader.loadAccessoryImagePath(accessoryData['id'])
                accessory = Accessory(accessoryData['id'],
                                      accessoryData['name'],
                                      accessoryData['coordinates'],
                                      positionData['coordinates'],
                                      self.resourceManager.loadAccessory(accessoryImagePath))
                accessories.append(accessory)

            spriteImagePath = self.dataLoader.loadSpriteImagePath(spriteData['id'])
            sprites[key] = Sprite(spriteData['id'],
                                  spriteData['name'],
                                  spriteData['coordinates'],
                                  accessories,
                                  self.resourceManager.loadSprite(spriteImagePath),
                                  spriteData['fps'])

        actor = Actor(actorData['id'],
                      actorData['name'],
                      sprites,
                      actorData['size'],
                      position,
                      direction,
                      isFocus)

        for key, sprite in actor.sprites:
            spriteHash = sprite.getSpriteHash()
            if not self.resourceManager.loadCombinedSprite(spriteHash):
                imageBuffers = actor.generateSpriteLayers(sprite)
                combinedSpriteImage = self.renderManager.createSprite(sprite, imageBuffers)
                self.resourceManager.addCombinedSprite(combinedSpriteImage, spriteHash)

            actor.updateSpriteImage(sprite, self.resourceManager.loadCombinedSprite(spriteHash))

        self.resourceManager.addActor(actor)

    def loadMenu(self, menuFile):
        self.unloadScene()

    def addEvent(self, event):
        self.eventHandler.addEvent(event)

    def unloadScene(self):
        pass

    def render(self):
        pass

    def run(self):
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags)
        CLOCK = pygame.time.Clock()

        while self.running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.inputHandler.appendKeydownEvent(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.inputHandler.appendKeydownEvent(event)
                    # TODO can tell pygame to only check for specific events

            self.inputHandler.setKeysPressed(pygame.key.get_pressed())

            self.inputHandler.handleInputs()  # iterates through the keydown and keypressed events
            self.eventHandler.handleEvents()

            self.renderManager.render()

            # debug helper, draw the tile gridlines
            # for i in range(35):
            #     pygame.draw.line(screen, PRAM.COLOR_BLACK,(0, 48*i), (1600, 48*i))
            #     pygame.draw.line(screen, PRAM.COLOR_BLACK,(48*i, 0), (48*i, 900))
            # if game.runDebug:
            #     game.runDebugLoop()  # if debug is activated ented debug mode

            pygame.display.update()  # TODO if passing updated recs, this is more efficient
            CLOCK.tick(GAME_FPS)  # 60 FPS