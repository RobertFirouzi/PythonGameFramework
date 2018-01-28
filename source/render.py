from actors import SimpleBox
import pygame
import parameters as PRAM

#renderMethods list populated by game depending on the needs of the currently loaded level/menu
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        
        #explicit declaration of class fields
        self.camera = None
        self.cameraTile= (0,0)
        self.cameraOffset = (0,0)
        self.cameraPosition = (0,0)
        
        self.levelData = None
        self.backgrounds = []
        self.foregrounds = []
        self.actors = []
        self.actorDict = None

        #for rendering changed tiles, keeps track of rendered tiles
        #indexed by their (x,y) coordinate pair
        self.renderedLowerTiles = {} 
        self.renderedUpperTiles = {} 
        
        self.actorsDict = {} #reference to image files
        self.lowerTileMap = None # Object holds tile mapping and image data
        self.upperTileMap = None # Object holds tile mapping and image data
        self.animatedPanorama = False

        self.isRenderAll = True #if true, will render the entire screen
        self.renderQueue = []
        self.framecount = 0 #a running count of frame ticks to animate images

        self.renderChangedMethods = [] #This will be the list of render functions to run
        self.renderAllMethods = []

    def loadAssets(self, levelData):
        self.framecount = 0 #reset framecount
        self.levelData = levelData #TODO may not need this reference
        self.lowerTileMap = levelData.lowerTileMap
        self.upperTileMap = levelData.upperTileMap
        self.backgrounds = levelData.backgrounds
        self.foregrounds = levelData.foregrounds
        self.actors = levelData.actors

        #TODO setup data structure for actors
        self.actorDict = {} #Load actor images
        # for actor in self.actors:
        #     if type(actor) is StaticSprite: #TODO this will be type Sprite or similar
        #         if self.actorDict.get(actor.image) == None:
        #             self.actorDict[actor.image] = pygame.image.load(actor.path+actor.image).convert_alpha()

        self.animatedPanorama = False #if this is true, must always re-render entire screen every frame

        for background in self.backgrounds:
            if background.isAnimated:
                self.animatedPanorama = True
                background.image = loadAnimatedPanoramas(background)
            else:
                background.image = loadPanorama(background)
            if background.isMotion_X:
                self.animatedPanorama = True
            if background.isMotion_Y:
                self.animatedPanorama = True

        for foreground in self.foregrounds:
            if foreground.isAnimated:
                self.animatedPanorama = True
                foreground.image = loadAnimatedPanoramas(foreground)
            else:
                foreground.image = loadPanorama(foreground)
            if foreground.isMotion_X:
                self.animatedPanorama = True
            if foreground.isMotion_Y:
                self.animatedPanorama = True

        self.loadTileMapImages()

    #this will just render game levels - create a seperate method for menus, and perhaps cutscenes
    def render(self):
        self.cameraTile= self.camera.tile
        self.cameraOffset = self.camera.offset
        self.cameraPosition = self.camera.position

        if  self.camera.moveFlag:# or self.animatedPanorama:
            self.isRenderAll = True

        if self.lowerTileMap is not None: #quick hack to make sure a level is loaded
            self.updateAnimatedIndex() #update any frame indexes for animated tiles

            if self.isRenderAll: #know rend
                self.renderAllPanorama(BG = True)
                self.renderAllLowerTile()
                self.renderAllActors()
                self.renderAllUpperTile()
                self.renderAllPanorama(BG = False)

            else:
                self.renderChangedPanorama(BG = True)
                self.renderChangedLowerTile()
                self.renderChangedActors()
                self.renderChangedUpperTile()
                self.renderChangedPanorama(BG = False)

            self.renderQueue.clear()
            self.renderedLowerTiles.clear()
            self.renderedUpperTiles.clear()
            self.camera.moveFlag = False
            self.isRenderAll = False

        self.framecount+=1

    #updates the index of any animated images
    def updateAnimatedIndex(self):
        if self.lowerTileMap.isAnimated:
            if int(self.framecount % self.lowerTileMap.framesPerImage) == 0:  # time to change the pic
                self.lowerTileMap.updateFrameIndex()
                if not self.isRenderAll: #if everything is being rendered, don't need to add to changed q
                    self.addRenderBoxes_AnimatedLowerTiles()

        if self.upperTileMap.isAnimated:
            if int(self.framecount % self.upperTileMap.framesPerImage) == 0:  # time to change the pic
                self.upperTileMap.updateFrameIndex()
                if not self.isRenderAll:
                    self.addRenderBoxes_AnimatedUpperTiles()

        for bg in self.backgrounds:
            addRenderBox = False
            if bg.isAnimated:
                if int(self.framecount%bg.framesPerImage)==0: #time to change the pic
                    bg.updateFrameIndex()
                    addRenderBox = True
            if bg.isMotion_X:
                motionOffset = int(bg.motion_x_multiplier * self.framecount)
                if motionOffset != bg.motionOffset_X: #panorama needs to move
                    bg.motionOffset_X = motionOffset
                    addRenderBox = True #if panorama needs to scroll, re-render visibile sections
            if bg.isMotion_Y:
                motionOffset = int(bg.motion_y_multiplier * self.framecount)
                if motionOffset != bg.motionOffset_Y:
                    bg.motionOffset_Y = motionOffset
                    addRenderBox = True
            if addRenderBox and not self.isRenderAll:
                self.addRenderBox_changedPanorama(bg)

        for fg in self.foregrounds:
            addRenderBox = False
            if fg.isAnimated:
                if int(self.framecount%fg.framesPerImage)==0: #time to change the pic
                    fg.updateFrameIndex()
                    addRenderBox = True
            if fg.isMotion_X:
                motionOffset = int(fg.motion_x_multiplier * self.framecount)
                if motionOffset != fg.motionOffset_X: #panorama needs to move
                    fg.motionOffset_X = motionOffset
                    addRenderBox = True #if panorama needs to scroll, re-render visibile sections
            if fg.isMotion_Y:
                motionOffset = int(fg.motion_y_multiplier * self.framecount)
                if motionOffset != fg.motionOffset_Y:
                    fg.motionOffset_Y = motionOffset
                    addRenderBox = True
            if addRenderBox and not self.isRenderAll:
                self.addRenderBox_changedPanorama(fg)


    #depending on the level, certain render methods will be loaded
    #if a level has animated panoramas, or tiles, use those methods.  Else the simpler methods.
    #add the render call for weather effects, etc if necessary
    def renderList(self): #TODO - not usre if going with this idea or not
        self.cameraTile= self.camera.tile
        self.cameraOffset = self.camera.offset
        self.cameraPosition = self.camera.position

        if self.camera.moveFlag or self.animatedPanorama:
            for method in self.renderAllMethods:
                method()
        else:
            for method in self.renderChangedMethods:
                method()

        self.renderQueue.clear()
        self.renderedLowerTiles.clear()
        self.renderedUpperTiles.clear()
        self.camera.moveFlag = False

        self.framecount += 1

    def renderAllLowerTile(self):
        tiles = self.lowerTileMap.tiles #for efficiency, quick reference to ptr
        image = self.lowerTileMap.image
        animatedDivide_px = self.lowerTileMap.animatedDivide_px
        animatedOffsets = self.lowerTileMap.animatedOffsets

        if self.lowerTileMap.isAnimated:
            frameIndex = self.lowerTileMap.frameIndex
        else:
            frameIndex = 0

        for y in range(PRAM.DISPLAY_TILE_HEIGHT):
            yOffset = y * PRAM.TILESIZE - self.cameraOffset[1]
            for x in range(PRAM.DISPLAY_TILE_WIDTH):
                tile = tiles[y + self.cameraTile[1]][x + self.cameraTile[0]]
                if tile[0] != -1: #-1 is blank
                    xOffset = x* PRAM.TILESIZE - self.cameraOffset[0]
                    if tile[1] >= animatedDivide_px:
                        tile = animatedOffsets.get((tile[0],tile[1]))[frameIndex]
                    self.screen.blit(image,
                                     (xOffset, yOffset), #screen position
                                     (tile[0], #tileMap x crop position
                                      tile[1], #tileMap y crop position
                                     PRAM.TILESIZE, #tilemap  width
                                     PRAM.TILESIZE)) #tilemap height

    def renderAllUpperTile(self):
        tiles = self.upperTileMap.tiles #for efficiency, quick reference to ptr
        image = self.upperTileMap.image
        animatedDivide_px = self.upperTileMap.animatedDivide_px
        animatedOffsets = self.upperTileMap.animatedOffsets

        if self.upperTileMap.isAnimated:
            frameIndex = self.upperTileMap.frameIndex
        else:
            frameIndex = 0

        for y in range(PRAM.DISPLAY_TILE_HEIGHT):
            yOffset = y * PRAM.TILESIZE - self.cameraOffset[1]
            for x in range(PRAM.DISPLAY_TILE_WIDTH):
                tile = tiles[y + self.cameraTile[1]][x + self.cameraTile[0]]
                if tile[0] != -1:
                    xOffset = x* PRAM.TILESIZE - self.cameraOffset[0]
                    if tile[1] >= animatedDivide_px:
                        tile = animatedOffsets.get((tile[0],tile[1]))[frameIndex]
                    self.screen.blit(image,
                                     (xOffset, yOffset), #screen position
                                     (tile[0], #tileMap x crop position
                                      tile[1], #tileMap y crop position
                                     PRAM.TILESIZE, #tileMap width
                                     PRAM.TILESIZE)) #tileMap height


    def renderChangedLowerTile(self):
        tiles = self.lowerTileMap.tiles #for efficiency, quick reference to ptr
        image = self.lowerTileMap.image
        animatedDivide_px = self.lowerTileMap.animatedDivide_px
        animatedOffsets = self.lowerTileMap.animatedOffsets

        if self.lowerTileMap.isAnimated:
            frameIndex = self.lowerTileMap.frameIndex
        else:
            frameIndex = 0

        for changedTile, isRendered in self.renderedLowerTiles.items():
            if not isRendered:
                tile = tiles[changedTile[0]][changedTile[1]] #the tilemap image location
                if tile[1] >= animatedDivide_px:
                    tile = animatedOffsets.get((tile[0], tile[1]))[frameIndex]
                self.screen.blit(image,
                                 ((changedTile[1]  - self.cameraTile[0]) * PRAM.TILESIZE  - self.cameraOffset[0], #x screen position
                                  (changedTile[0] - self.cameraTile[1]) * PRAM.TILESIZE  - self.cameraOffset[1]), #y screen position
                                 (tile[0], #tilemap image coordinates
                                  tile[1],
                                 PRAM.TILESIZE,
                                 PRAM.TILESIZE)) #blit one tile

                self.renderedLowerTiles[(changedTile[0],changedTile[1])] = True

    def renderChangedUpperTile(self):
        tiles = self.upperTileMap.tiles #for efficiency, quick reference to ptr
        image = self.upperTileMap.image

        animatedDivide_px = self.upperTileMap.animatedDivide_px
        animatedOffsets = self.upperTileMap.animatedOffsets

        if self.upperTileMap.isAnimated:
            frameIndex = self.upperTileMap.frameIndex
        else:
            frameIndex = 0

        for changedTile, isRendered in self.renderedUpperTiles.items():
            if not isRendered:
                tile = tiles[changedTile[0]][changedTile[1]] #the tilemap image location
                if tile[1] >= animatedDivide_px:
                    tile = animatedOffsets.get((tile[0], tile[1]))[frameIndex]
                self.screen.blit(image,
                                 ((changedTile[1]  - self.cameraTile[0]) * PRAM.TILESIZE  - self.cameraOffset[0], #x screen position
                                  (changedTile[0] - self.cameraTile[1]) * PRAM.TILESIZE  - self.cameraOffset[1]), #y screen position
                                 (tile[0], #tilemap image coordinates
                                  tile[1],
                                 PRAM.TILESIZE,
                                 PRAM.TILESIZE)) #blit one tile

                self.renderedUpperTiles[(changedTile[0],changedTile[1])] = True

    def renderAllPanorama(self, BG = True): #if BG render backgrounds, else foregrounds
        screenOffset = (self.cameraTile[0]*PRAM.TILESIZE + self.cameraOffset[0],
                        self.cameraTile[1]*PRAM.TILESIZE + self.cameraOffset[1])
        if BG:
            images = self.backgrounds
        else:
            images = self.foregrounds

        for fg in images:
            imageOffset = (((screenOffset[0]*fg.scrolling[0][0]//fg.scrolling[0][1])+fg.motionOffset_X)%fg.pxSize[1],
                           ((screenOffset[1]*fg.scrolling[1][0]//fg.scrolling[1][1])+fg.motionOffset_Y)%fg.pxSize[0])

            if fg.isAnimated:
                displayImage = fg.image[fg.imageIndex]
            else:
                displayImage = fg.image[0]

            for vs in fg.visibleSections: #vs = (left edge, right edge, top edge, bottom edge)
                
                #check if visible portion of background is on screen
                if (vs[0] < screenOffset[0] + PRAM.DISPLAY_WIDTH 
                    and vs[1]> screenOffset[0] 
                    and vs[2] < screenOffset[1] + PRAM.DISPLAY_HEIGHT 
                    and vs[3]> screenOffset[1]):
                    
                    #find boundaries of image
                    if vs[0] <= screenOffset[0]:
                        xOffset = 0
                    else:
                        xOffset = vs[0] - screenOffset[0]
                
                    if vs[2] <= screenOffset[1]:
                        yOffset = 0
                    else:
                        yOffset = vs[2]- screenOffset[1]

                    #calculate size of image square to blit  
                    xRange = vs[1] - screenOffset[0] - xOffset                      
                    if xRange + xOffset > PRAM.DISPLAY_WIDTH:
                        xRange = PRAM.DISPLAY_WIDTH - xOffset

                    yRange = vs[3] - screenOffset[1] - yOffset
                    if yRange + yOffset > PRAM.DISPLAY_HEIGHT:
                        yRange = PRAM.DISPLAY_HEIGHT - yOffset
                        
                    currentXrange = xRange #size of block of image to blit
                    currentYrange = yRange
                    currentScreenPos = [xOffset,yOffset] #absolute screen position to blit to
                    
                    currentCropX = (imageOffset[0] + xOffset)%fg.pxSize[1] #position of image to blit from
                    currentCropY = (imageOffset[1] + yOffset)%fg.pxSize[0]
                    keepGoing = True
                    shiftX = False
                    shiftY = False
                    
                    while keepGoing:
                        if currentCropX + currentXrange > fg.pxSize[1]:
                            currentXrange = fg.pxSize[1] - currentCropX
                            shiftX = True
                        if currentCropY + currentYrange > fg.pxSize[0]:
                            currentYrange = fg.pxSize[0] - currentCropY
                            shiftY = True

                        self.screen.blit(displayImage,
                                         currentScreenPos,
                                        (currentCropX, currentCropY, currentXrange, currentYrange)) 
                                                                 
                        #blit across the X direction first, then shift down the Y and reset the X  
                        if shiftX:
                            currentScreenPos = [currentScreenPos[0] + currentXrange, currentScreenPos[1]]
                            currentCropX = (currentCropX + currentXrange) % fg.pxSize[1]
                            currentXrange = xRange - currentXrange
                            shiftX = False
                        elif shiftY:
                            currentScreenPos = [xOffset, currentScreenPos[1] + currentYrange]
                            currentCropX = (imageOffset[0] + xOffset)%fg.pxSize[1]
                            currentXrange = xRange
                            currentCropY = (currentCropY + currentYrange) % fg.pxSize[0]
                            currentYrange = yRange - currentYrange                                                
                            shiftY = False    
                        else:
                            keepGoing = False #you have blitted the entire visible section


#Currently does not work with motion Y backgrounds (but works with X)
    def renderChangedPanorama(self, BG = True):
        if BG:
            images = self.backgrounds
        else:
            images = self.foregrounds

        screenOffset_Xpx = (self.cameraTile[0]*PRAM.TILESIZE)  + self.cameraOffset[0] #pixel 0 of screen is this map pixel
        screenOffset_Ypx = (self.cameraTile[1]*PRAM.TILESIZE)  + self.cameraOffset[1]

        for fg in images:

            if fg.isAnimated:
                displayImage = fg.image[fg.imageIndex]
            else:
                displayImage = fg.image[0]

            for box in self.renderQueue:
                for vs in fg.visibleSections:  #vs = (left edge, right edge, top edge, bottom edge)
                    
                    #Check to see if this renderBox is within a visible section of the foreground
                    if vs[0] <= box[1] and vs[1]>= box[0] and vs[2] <= box[3] and vs[3] >= box[2]:
                        visibleBox = list(box)
                        if vs[0] > box[0]:
                            visibleBox[0] = vs[0]
                        if vs[1] < box[1]:
                            visibleBox[1] = vs[1]
                        if vs[2] > box[2]:
                            visibleBox[2] = vs[2]
                        if vs[3] < box[3]:
                            visibleBox[3] = vs[3]


                        if visibleBox[0] < screenOffset_Xpx:
                            visibleBox[0] = screenOffset_Xpx
                        if visibleBox[1] > PRAM.DISPLAY_WIDTH+screenOffset_Xpx:
                            visibleBox[1] = PRAM.DISPLAY_WIDTH+screenOffset_Xpx
                        if visibleBox[2] < screenOffset_Ypx:
                            visibleBox[2] = screenOffset_Ypx
                        if visibleBox[3] > screenOffset_Ypx + PRAM.DISPLAY_HEIGHT:
                            visibleBox[3] = screenOffset_Ypx + PRAM.DISPLAY_HEIGHT

                        startScreenPos = [visibleBox[0] - screenOffset_Xpx,
                                          visibleBox[2] - screenOffset_Ypx]

                        if startScreenPos[0]<0:
                            startScreenPos[0]=0
                        if startScreenPos[1]<0:
                            startScreenPos[1] = 0

                        startCropX = ((self.cameraTile[0]*PRAM.TILESIZE + self.cameraOffset[0])
                                      * fg.scrolling[0][0]
                                      // fg.scrolling[0][1] 
                                      + startScreenPos[0]
                                      + fg.motionOffset_X)
                        startCropX = startCropX % fg.pxSize[1]



                        startCropY = ((self.cameraTile[1]*PRAM.TILESIZE + self.cameraOffset[1])
                                      * fg.scrolling[1][0]
                                      // fg.scrolling[1][1] 
                                      + startScreenPos[1]
                                      + fg.motionOffset_Y)
                        startCropY = startCropY % fg.pxSize[0]

                        # if fg.layer == 0:
                            # pygame.draw.line(self.screen, PRAM.COLOR_BLACK, (startCropX, 0), (startCropX, 1600), 5)
                            # pygame.draw.line(self.screen, PRAM.COLOR_WHITE, (0, startCropY), (1600, startCropY), 5)

                        currentScreenPos = startScreenPos
                        currentCropX =  startCropX
                        currentCropY = startCropY

                        imageSizeX = visibleBox[1] - visibleBox[0] 
                        imageSizeY = visibleBox[3] - visibleBox[2]


                        if startScreenPos[0] + imageSizeX > PRAM.DISPLAY_WIDTH: #If render box goes beyond screen border
                            imageSizeX = PRAM.DISPLAY_WIDTH - startScreenPos[0]

                        if startScreenPos[1] + imageSizeY > PRAM.DISPLAY_HEIGHT: #If render box goes beyond screen border
                            imageSizeY = PRAM.DISPLAY_HEIGHT - startScreenPos[1]

                        keepGoing = True
                        shiftX = False
                        shiftY = False

                        # blitcount = 0 #Debug code to see which sections are being blitted
                        # colors = [PRAM.COLOR_GREEN, PRAM.COLOR_BLACK, PRAM.COLOR_BLUE]

                        while keepGoing:  #check to see if you are at the boundries of the image, and need to tile it
                            if currentCropX + imageSizeX > fg.pxSize[1]:
                                imageSizeX = fg.pxSize[1] - currentCropX
                                shiftX = True
                            if currentCropY + imageSizeY > fg.pxSize[0]:
                                imageSizeY = fg.pxSize[0] - currentCropY
                                shiftY = True
                                                    
                            self.screen.blit(displayImage,
                                             currentScreenPos,
                                            (currentCropX,  #image x
                                            currentCropY, #image y                                 
                                              imageSizeX, #image x width crop
                                              imageSizeY)) #image y height crop   

                            #debug code to draw the blitting sections
                            # if fg.layer == 0 and BG:
                            #     pygame.draw.rect(self.screen,
                            #                      colors[blitcount%3],
                            #                     (currentScreenPos[0],currentScreenPos[1],imageSizeX,imageSizeY),
                            #                      10) #width
                            #     blitcount += 1


                            #blit across the X direction first, then shift down the Y and reset the X  
                            if shiftX:
                                currentScreenPos = [currentScreenPos[0] + imageSizeX, currentScreenPos[1]]
                                currentCropX = (currentCropX + imageSizeX) % fg.pxSize[1]
                                imageSizeX = visibleBox[1] - visibleBox[0] - imageSizeX
                                shiftX = False
                            elif shiftY:
                                currentScreenPos = [startScreenPos[0], currentScreenPos[1] + imageSizeY]
                                currentCropX = startCropX
                                imageSizeX = visibleBox[1] - visibleBox[0]
                                currentCropY = (currentCropY + imageSizeY) % fg.pxSize[0]
                                imageSizeY = visibleBox[3] - visibleBox[2] - imageSizeY                                                
                                shiftY = False    
                            else:
                                keepGoing = False #you have blitted the entire visible section

    #TODO - calculate if the actor is onscreen
#     def renderAllActors(self, actorsWrapper):
    def renderAllActors(self):
        for actor in self.actors:
            if type(actor) is SimpleBox:
                pygame.draw.rect(self.screen, actor.color, 
                                 pygame.Rect(actor.position[0]+PRAM.BOX_FUDGE - self.cameraPosition[0], 
                                             actor.position[1] - self.cameraPosition[1], 
                                             actor.size[0] - PRAM.BOX_FUDGE*2, 
                                             actor.size[1]))
            actor.changed = False
        return
    
    #TODO 
#     def renderChangedActors(self, actorsWrapper):
    def renderChangedActors(self):
        for actor in self.actors:
            if actor.changed:
                if type(actor) is SimpleBox:
                    pygame.draw.rect(self.screen, actor.color, 
                                     pygame.Rect(actor.position[0]+PRAM.BOX_FUDGE - self.cameraPosition[0], 
                                                 actor.position[1] - self.cameraPosition[1], 
                                                 actor.size[0] - PRAM.BOX_FUDGE*2, 
                                                 actor.size[1]))
                actor.changed = False
        return

    #Based on start and end position, and actor size, add a bounding box to the renderQueue (in pixels)
    # for a section of the gameLevel that needs to be rendered on the render changes call
    # #also, adds to the tileRenderQueues any tiles in the box
    def addRenderBox_movedSprite(self, size, origin, destination, direction):
        if direction == PRAM.UP:
            minx = origin[0]
            miny = destination[1]
            maxx = destination[0] + size[0]
            maxy = origin[1] + size[1]
        elif direction == PRAM.DOWN:
            minx = origin[0]
            miny = origin[1]
            maxx = destination[0] + size[0]
            maxy = destination[1] + size[1]
        elif direction == PRAM.LEFT:
            minx = destination[0] 
            miny = origin[1]
            maxx = origin[0] + size[0]
            maxy = destination[1] + size[1]
        else: #right
            minx = origin[0]
            miny = origin[1]
            maxx = destination[0] + size[0]
            maxy = destination[1] + size[1]
        
        mapSizeX = self.levelData.size[1] * PRAM.TILESIZE #TODO save this as a levelData parameter?
        mapSizeY = self.levelData.size[0] * PRAM.TILESIZE
        
        #get the entire tile
        minx = minx - (minx % PRAM.TILESIZE)
        miny = miny - (miny % PRAM.TILESIZE)
        maxx = (maxx//PRAM.TILESIZE + 1)*PRAM.TILESIZE
        maxy = (maxy//PRAM.TILESIZE + 1)*PRAM.TILESIZE        
             
        if minx<0:
            minx = 0
        if miny<0:
            miny = 0
        if maxx > mapSizeX:
            maxx = mapSizeX
        if maxy > mapSizeY:
            maxy = mapSizeY

        renderBox = (minx, maxx, miny, maxy)
        self.renderQueue.append(renderBox) #for panorama rendering
        self.addChangedTilesFromRenderBox(renderBox) #for tile re-rendering

    def addChangedTilesFromRenderBox(self, renderBox):
        xRange = (renderBox[0]//PRAM.TILESIZE, renderBox[1]//PRAM.TILESIZE)
        yRange = (renderBox[2]//PRAM.TILESIZE, renderBox[3]//PRAM.TILESIZE)
        for x in range(xRange[0], xRange[1]):
            for y in range(yRange[0], yRange[1]):
                lowerTile = self.lowerTileMap.tiles[y][x]
                upperTile = self.upperTileMap.tiles[y][x]
                if self.renderedLowerTiles.get((y,x)) != True and lowerTile[0] != -1: #-1 is blank
                    self.renderedLowerTiles[(y,x)] = False
                if self.renderedUpperTiles.get((y,x)) != True and upperTile[0] != -1:
                    self.renderedUpperTiles[(y,x)] = False


    def addRenderBox_changedPanorama(self, panorama):
        screenOffset = (self.cameraTile[0]*PRAM.TILESIZE + self.cameraOffset[0],
                        self.cameraTile[1]*PRAM.TILESIZE + self.cameraOffset[1])

        for vs in panorama.visibleSections:  # vs = (left edge, right edge, top edge, bottom edge)
            # check if visible portion of background is on screen
            if (vs[0] < screenOffset[0] + PRAM.DISPLAY_WIDTH
                and vs[1] > screenOffset[0]
                and vs[2] < screenOffset[1] + PRAM.DISPLAY_HEIGHT
                and vs[3] > screenOffset[1]):

                # self.renderQueue.append((minx, maxx, miny, maxy))  # for panorama rendering
                self.renderQueue.append(vs)  # for panorama rendering
                self.addChangedTilesFromRenderBox(vs)

    def addRenderBoxes_AnimatedLowerTiles(self):
        lowerTiles = self.lowerTileMap.tiles #for efficiency, quick reference to ptr
        upperTiles = self.upperTileMap.tiles
        animatedDivide_px = self.lowerTileMap.animatedDivide_px
        cameraTile = self.cameraTile

        for y in range(PRAM.DISPLAY_TILE_HEIGHT):
            miny = (y + cameraTile[1]) * PRAM.TILESIZE
            maxy = miny + PRAM.TILESIZE
            tileOffset_y = y + cameraTile[1]
            for x in range(PRAM.DISPLAY_TILE_WIDTH):
                tileOffset_x = x + cameraTile[0]
                lowerTile = lowerTiles[tileOffset_y][tileOffset_x]
                if lowerTile[0] != -1:
                    if lowerTile[1] >= animatedDivide_px:
                        minx = (x + cameraTile[0])*PRAM.TILESIZE
                        maxx = minx+PRAM.TILESIZE
                        self.renderQueue.append((minx, maxx, miny, maxy))  # for panorama rendering
                        self.renderedLowerTiles[(tileOffset_y, tileOffset_x)] = False
                        upperTile = upperTiles[tileOffset_y][tileOffset_x]
                        if upperTile[0] != -1:
                            self.renderedUpperTiles[(tileOffset_y, tileOffset_x)] = False #If we re-render lower, must also do upper


    def addRenderBoxes_AnimatedUpperTiles(self):
        lowerTiles = self.lowerTileMap.tiles #for efficiency, quick reference to ptr
        upperTiles = self.upperTileMap.tiles
        animatedDivide_px = self.upperTileMap.animatedDivide_px
        cameraTile = self.cameraTile

        for y in range(PRAM.DISPLAY_TILE_HEIGHT):
            miny = (y + cameraTile[1]) * PRAM.TILESIZE
            maxy = miny + PRAM.TILESIZE
            tileOffset_y = y + cameraTile[1]
            for x in range(PRAM.DISPLAY_TILE_WIDTH):
                tileOffset_x = x + cameraTile[0]
                upperTile = upperTiles[tileOffset_y][tileOffset_x]
                if upperTile[0] != -1:
                    if upperTile[1] >= animatedDivide_px:
                        minx = (x + cameraTile[0])*PRAM.TILESIZE
                        maxx = minx+PRAM.TILESIZE
                        self.renderQueue.append((minx, maxx, miny, maxy))  # for panorama rendering
                        self.renderedUpperTiles[(tileOffset_y, tileOffset_x)] = False
                        lowerTile = lowerTiles[tileOffset_y][tileOffset_x]
                        if lowerTile[0] != -1:
                            self.renderedLowerTiles[(tileOffset_y, tileOffset_x)] = False #If we re-render upper, must also do lower


    def loadTileMapImages(self):
        if self.lowerTileMap.alpha:
            self.lowerTileMap.image = pygame.image.load(self.lowerTileMap.filePath).convert_alpha()
        else:
            self.lowerTileMap.image = pygame.image.load(self.lowerTileMap.filePath).convert()

        if self.upperTileMap.alpha:
            self.upperTileMap.image = pygame.image.load(self.upperTileMap.filePath).convert_alpha()
        else:
            self.upperTileMap.image = pygame.image.load(self.upperTileMap.filePath).convert()

#use pygame image.load, convert alpha if necessary, return the image file
def loadPanorama(panorama):
    if panorama.alpha:
        return (pygame.image.load(panorama.filePath).convert_alpha(),) #tuple of one item
    else:
        return (pygame.image.load(panorama.filePath).convert(),)

#Images are named "0.<type>", "1.<type>", etc...
def loadAnimatedPanoramas(panorama):
    convertedImages = []
    for i in range(panorama.numbImages):
        if panorama.alpha:
            convertedImages.append(pygame.image.load(panorama.filePath+'\\' +str(i)+'.'+panorama.imageType).convert_alpha())
        else:
            convertedImages.append(pygame.image.load(panorama.filePath+'\\' +str(i)+'.'+panorama.imageType).convert())
    convertedImages = tuple(convertedImages)
    return convertedImages