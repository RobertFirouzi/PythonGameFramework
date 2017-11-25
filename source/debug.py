import os
import threading
### PARAMETERS ###
INT = 0
STRING = 1
FLOAT = 2

DEBUG_MENU =\
'''
Select a Debug Option (or -99 to exit debugger):
0) Quit
1) Change Character Speed
2) Edit Scenery
3) Edit Tilemap
>>>'''
QUIT = 0
EXIT_DEBUGGER = -99
EXIT_DEBUGGER_STR = '-99'
CHAR_SPEED = 1
SCENERY = 2
TILEMAP = 3

MOVESPEED_MENU=\
'''
Enter an integer value for character Move Speed, or -99 to exit debugger.
(0 is no movement, 10 is average, 30 is insane)
>>>'''
MIN_MOVE_SPEED = -10000
MAX_MOVE_SPEED = 10000

SCENERY_MENU=\
'''
Choose Scenery Type (or -99 to exit debugger)
0) Quit
1) Background
2) Foreground 
>>>'''
BACKGROUND = 1
FOREGROUND = 2

PANORAMA_PROMPT='''or 0 to Cancel, or -99 to exit debugger
>>>'''

TILEMAP_MENU=\
'''
Choose Tilemap Type (or -99 to exit debugger)
0) Quit
1) Lower
2) Upper
3) Barrier
>>>'''
LOWER = 1
UPPER = 2
BARRIER = 3

SCENERY_EDIT_MENU =\
'''
What will you change? (or -99 to exit debugger)
0) Quit
1) filePath (load new image)
2) visible sections
3) scrolling
4) alpha (True or False)
5) layer
>>>
'''
FILEPATH = 1
VISIBILE_SECTIONS = 2
SCROLLING = 3
ALPHA = 4
LAYER = 5

GET_FILEPATH='''Enter a filepath to a panorama image:
>>>'''

ALLOWED_IMAGETYPES = ('.jpg', '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif', '.lbm', '.pbm', '.pgm', '.ppm', '.xpm',
                     '.JPG', '.PNG', '.GIF', '.BMP', '.PCX', '.TGA', '.TIF', '.LBM', '.PBM', '.PGM', '.PPM', '.XPM')

VISIBILE_MENU=\
'''
Add or Delete a Section? (or -99 to exit Debugger)
0) Quit
1) Delete
2) Add
>>>
'''
DELETE_VISIBILITY = 1
ADD_VISIBILITY = 2
#Class to run debug mode - allows user programmer to change in game variables to test different areas of code
class DebugLooper(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self, daemon=True)
        self.game = game #need a reference to main game to be able to tweak game variables
    def run(self):
        result = 0
        keepGoing = True
        try:
            while keepGoing:
                devInput = getInput(DEBUG_MENU, INT, [QUIT,TILEMAP])
                if devInput == EXIT_DEBUGGER:
                    keepGoing = False
                elif devInput == QUIT:
                    keepGoing = False
                elif devInput == CHAR_SPEED:
                    result = self.changePlayerSpeed()
                elif devInput == SCENERY:
                    result = self.changeScenery()
                elif devInput == TILEMAP:
                    result = self.changeTilemap
                if result == EXIT_DEBUGGER:
                    keepGoing = False

        except Exception as e:
            print('debug loop failed with exception')
            print(e)

        print('Exiting Debugger...')

    def changeScenery(self):
        keepGoing = True
        result = 0
        while keepGoing:
            devInput = getInput(SCENERY_MENU, INT, [QUIT,FOREGROUND])
            if devInput == QUIT:
                keepGoing = False
            elif devInput == EXIT_DEBUGGER:
                return EXIT_DEBUGGER
            elif devInput == BACKGROUND:
                result = self.editScenery(background = True)
            elif devInput == FOREGROUND:
                result = self.editScenery(background = False)

            if result == EXIT_DEBUGGER:
                return EXIT_DEBUGGER

    @property
    def changeTilemap(self):
        keepGoing = True

        while keepGoing:
            devInput = getInput(TILEMAP_MENU, INT, [QUIT,BARRIER])
            if devInput == QUIT:
                keepGoing = False
            elif devInput == EXIT_DEBUGGER:
                return EXIT_DEBUGGER
            elif devInput == LOWER:
                print('edit lower')
            elif devInput == UPPER:
                print('edit upper')
            elif devInput == BARRIER:
                print('edit barrier')

    def changePlayerSpeed(self):
        devInput = getInput(MOVESPEED_MENU, INT, [MIN_MOVE_SPEED,MAX_MOVE_SPEED])
        if devInput == EXIT_DEBUGGER:
            return EXIT_DEBUGGER
        self.game.player.moveSpeed = devInput
        print('Players speed changed to: ' + str(devInput))
        return 0

    def editScenery(self, background = True):
        if background:
            scenery = self.game.levelData.backgrounds
        else:
            scenery = self.game.levelData.foregrounds
        if len(scenery) == 0:
            print('No panoramas of this type on this level')
            return 0

        print('Which panorama will you edit?')
        i = 0
        for panorama in scenery:
            print(str(i+1) + ': ' + str(panorama.filePath))
            i+=1
        devInput = getInput(PANORAMA_PROMPT, INT, [QUIT,i])
        if devInput == QUIT:
            return 0
        if devInput == EXIT_DEBUGGER:
            return EXIT_DEBUGGER

        index = devInput -1 #index into array of scenery objects to edit
        keepGoing = True
        while keepGoing:
            devInput = getInput(SCENERY_EDIT_MENU, INT, [QUIT, LAYER])
            if devInput == QUIT:
                keepGoing = False

            elif devInput == EXIT_DEBUGGER:
                return EXIT_DEBUGGER

            elif devInput == FILEPATH: #Change the image
                devInput = getInput(GET_FILEPATH, STRING,[2,1000])
                allowedType = False
                for imageType in ALLOWED_IMAGETYPES:
                    if imageType in devInput:
                        allowedType = True
                if allowedType:
                    if os.path.isfile(devInput):
                        scenery[index].filePath = devInput
                        self.game.renderer.loadPanorama(scenery[index])
                    else:
                        print('File not found')
                else:
                    print('That is not an allowed image type in pygame')

            elif devInput == VISIBILE_SECTIONS:
                devInput = getInput(VISIBILE_MENU, INT, [QUIT, ADD_VISIBILITY])
                print('Current Visibility:')
                count = 0
                for visibleSection in scenery[index].visibleSections:
                    count += 1
                    print(str(count) + ') ' + str(visibleSection))
                if devInput == QUIT:
                    keepGoing = False
                elif devInput == EXIT_DEBUGGER:
                    return EXIT_DEBUGGER
                elif devInput == DELETE_VISIBILITY:
                    print('Delete which visible section?')
                    devInput = getInput('>>>', INT, [1, count])
                    scenery[index].visibleSections = list(scenery[index].visibleSections)
                    del(scenery[index].visibleSections[devInput-1])
                    scenery[index].visibleSections = tuple(scenery[index].visibleSections)
                elif devInput == ADD_VISIBILITY:
                    print('Enter ints for the 4 values')
                    newVisibility = ['xmin', 'xmax', 'ymin', 'ymax']  # placeholders tags
                    for i in range(4):
                        newVisibility[i] = getInput('Value for ' + newVisibility[i] + '\n>>>', INT, [-500000, 500000])
                    scenery[index].visibleSections = list(scenery[index].visibleSections)
                    scenery[index].visibleSections.append(newVisibility)
                    scenery[index].visibleSections = tuple(scenery[index].visibleSections)
            elif devInput == SCROLLING:
                print('Current scrolling: ' + str(scenery[index].scrolling))
                print('Enter ints for the 4 values')
                scrolling = [['xmult', 'xdiv'],['ymult','ydiv']] #placeholders tags
                for i in range(2):
                    for j in range(2):
                        scrolling[i][j] = getInput('Value for ' + scrolling[i][j]+'\n>>>',
                                                        INT, [-10000, 10000])
                scenery[index].scrolling = scrolling

            elif devInput == ALPHA:
                print('edit alpha')

            elif devInput == LAYER:
                print('edit layer')

            self.game.renderer.camera.moveFlag = True

        return 0


### STATIC METHODS ###

#get a user input type within a range, loop until propper input recieved.  Always return QUIT or EXIT values
def getInput(prompt, dataType=INT, inputRange=(-10000,10000)):
    if dataType == INT:
        devInput = ''
        while type(devInput) != int or devInput < inputRange[0] or devInput > inputRange[1]:
            try:
                devInput = int(input(prompt))
            except Exception as e:
                print('Exception, caught on user input')
                print(e)
            if devInput == QUIT or devInput == EXIT_DEBUGGER:
                return devInput
    elif dataType == STRING:
        devInput = 0
        while type(devInput) != str or len(devInput) < inputRange[0] or len(devInput) > inputRange[1]:
            try:
                devInput = str(input(prompt))
            except Exception as e:
                print('Exception, caught on user input')
                print(e)

            if devInput == EXIT_DEBUGGER_STR:
                return EXIT_DEBUGGER
    elif dataType == FLOAT:
        devInput = ''
        while type(devInput) != float or devInput < inputRange[0] or devInput > inputRange[1]:
            try:
                devInput = float(input(prompt))
            except Exception as e:
                print('Exception, caught on user input')
                print(e)

            if devInput == float(QUIT) or devInput == float(EXIT_DEBUGGER):
                return int(devInput)
    else:
        devInput = 0

    return devInput















