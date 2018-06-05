import pygame
from render import RenderManager
from parameters import *
from setup import eventHandlerFactory, playerFactory, soundPlayerFactory
from input import InputHandler, ButtonMap

class Camera:
    def __init__(self):
        pass

class ResourceManager:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        self.player = playerFactory()
        self.renderManager = RenderManager()
        self.resourceManager = ResourceManager()
        self.eventHandler = eventHandlerFactory(self)
        self.inputHandler = InputHandler(self, self.player, ButtonMap())
        self.musicHandler, self.soundEffectHandler = soundPlayerFactory()
        self.camera = Camera

        self.screen = None
        self.gameScene = None
        self.running = True

    def run(self):
        #TODO - load the startup menu event here
        pygame.init()
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