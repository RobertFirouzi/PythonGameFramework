'''
dir_levels/
    000000/ #level id 000000
        level_data.json
        render_layers/
            000.json #renderlayer 0
            001.json #renderlaer 1
            etc..
        panorama/
            000/ #images for id 000 (id here corresponds to the rende_layer id)
                000.jpg #first image
                001.jpg #second image
                etc
            001/ #images for id 001
                000.jpg (id here corresponds to the rende_layer id)
                001.jpg
                etc
        tilemap/ #tilemap images
            000.jpg #image for id 000 (id here corresponds to the rende_layer id)
            001.jpg #image for id 001
            etc
        tiles/
            000.json #the 2d list of animated tiles
            001.json (id here corresponds to the rende_layer id)
            etc
        border/
            000.json #map of the borders
            001.json (id here corresponds to the rende_layer id)
    000001/ #level id 000001
        level_data.json
        render_layers/
            000.json #renderlayer 0
            001.json #renderlaer 1
            etc..
        panorama/
            000/ #images for id 000
                000.jpg #first image
                001.jpg #second image
                etc
            001/ #images for id 001
                000.jpg
                001.jpg
                etc
        tilemap/ #tilemap images
            000.jpg #image for id 000
            001.jpg #image for id 001
            etc
        border/
            000.json
    etc

Example of JSON format

LevelData
{
'name' : <String>
'id' : <Integer>
'size_tiles' : <list[height,width]>
'actors': <list[id,layer,position[x,y]]>
'gameEvents' : list[id,params[]]
'eventBox' : list[id,location/size,params[]]
}

Borders
[[]] #2d list of each cell border - the id of the border will associate with the layer it corresponds with

PanoramaLayer
{
'layerType' : <string>
'id' : <Integer>
'name' : <String>
'isNeedsSorting' : <Bool>
'isAlpha' : <Bool>
'visibleSections' : <list[list[position,size]]>
'sizePx' : <list[height, width]>
'fps' : Integer
'scrollSpeed' : <list[mult_x,mult_y,div_x,div_y]>
'isMotion' : <[Boolx, Booly]>
'motion_pps' : <[x,y]>
}

Tilemaplayer / spriteLayer (sprite layer will have actors added from the level data
{
'layerType' : <string>
'id' : <Integer>
'name' : <String>
'isNeedsSorting : <Bool>
'isAlpha' : <Bool>
'size_tiles' : <list[height,width]> #number of tiles in x and y direction
'tile_size' : <Integer> #pixel size of 1 tile (always a square)
'animatedTiles' : <2d list of dictionaries, by row/col>
    {
        'tilemapIndex' <list[list[[row,col]]> #which tile(s) from the map, multiple if it is animated
        'fps' : <Integer>
    }
}

'''

'''
level 000000 - 
there are 2 background panoramas, a lower tile layer, a sprite layer, an upper tile layer, and a foreground layer
'''

'''
dir_actors/
    000000.json
    000001.json 
    etc

dir_sprites/
    000000/
        sprite_data.json
        img.jpg
        accessories/
            000000.json #describes placment of accessory images of corresponding id
            000008.json #note that an accessory can be associated with multiple base sprites
                        #but doesn't have to be with all.  Perhaps there are multiple accessory images of a sword
                        #one in a positon for the character to hold while walking,running, jumping, etc
                        #another one that is designed for an attack animation 
            etc
    000001/
        sprite_data
        img.jpg
        accessories/
            000002.json #describes placment of accessory images of corresponding id
            000010.json
            etc
dir_accessories/
    000000/
        accessory_data.json
        img.png
    000001/
        accessory_data.json
        img.png
    etc

actor json
"id" : <int>,
"name" : <string>,
"size" : <list[width, height]>
"sprites" : dict{'type' : [id]} eg 'walk' : 1, 
"accessories" : list(id's)
(much more data for an actor to be added)


sprite data json
"id" : <int>,
"name" : <string>,
"coordinates" : <dict{'up' : [[0,0,10,20], [10,0,10,20] ... 'down' : [[.......}  #lists all directions, and the coordinates of each frame
"fps" : int

accessory json (within sprites)
"id" : <int>,
"coordinates" : <dict{'up' : [[0,0], [10,0] ... 'down' : [[.......}  #lists all directions, just the starting coordinates of each frame (rest of coords in acc data)


accessory data json
"id" : <int>
"name" : <string>
"coordinates" : <dict{'up' : [[0,0,10,20], [10,0,10,20] ... 'down' : [[.......}  #lists all directions, and the coordinates of each frame

'''

import json
import os
LEVELS_DIRECTORY = 'dir_levels\\'

class DataLoader:
    def __init__(self): #sets the path to the folder for this level
        self.currentLevelId = 0
        self.levelPath = ''

    def setLevelId(self, id):
        self.currentLevelId = id
        if id<10:
            self.levelPath = LEVELS_DIRECTORY+'00000'+str(id)+'\\'
        elif id<100:
            self.levelPath = LEVELS_DIRECTORY+'0000'+str(id)+'\\'
        elif id<1000:
            self.levelPath = LEVELS_DIRECTORY+'000'+str(id)+'\\'
        elif id<10000:
            self.levelPath = LEVELS_DIRECTORY+'00'+str(id)+'\\'
        elif id<100000:
            self.levelPath = LEVELS_DIRECTORY+'0'+str(id)+'\\'
        else:
            self.levelPath = LEVELS_DIRECTORY+str(id)+'\\'

    def loadLevelData(self): #retuns the level_data json for the loaded level path
        file = open(self.levelPath+'level_data.json')
        level_data = json.load(file)
        file.close()
        return level_data

    def loadRenderLayers(self): #returns all of the render layer jsons from levelpath
        directory = self.levelPath+'render_layers\\'
        files = os.listdir(directory)
        renderLayers = list()

        for file in files:
            fp = open(directory+file, 'r')
            renderLayers.append(json.load(fp))
            fp.close()

        return renderLayers

    def loadPanoramicImagePaths(self, id): #returns the list of panorama paths for the layer id
        if id<10:
            directory = self.levelPath + 'panorama\\00'+str(id)+'\\'
        elif id<100:
            directory = self.levelPath + 'panorama\\0'+str(id)+'\\'
        else:
            directory = self.levelPath + 'panorama\\'+str(id)+'\\'

        files = os.listdir(directory)
        imagePaths = list()

        for file in files:
            imagePaths.append(directory+file)

        return imagePaths


    def loadTileImagePath(self, id): #returns an empty string or the path to tilemap image
        directory = self.levelPath + 'tilemap\\'
        files = os.listdir(directory)
        tileImagePath = ''

        for file in files:
            index = int(file.split('.')[0]) #split of extension and convert to an id int
            if index == id:
                tileImagePath = directory+file
                break

        return tileImagePath

    def loadTilemapData(self, id): #returns the array of tileData (used for animatedTile objects)
        directory = self.levelPath + 'tiles\\'
        files = os.listdir(directory)

        for file in files:
            index = int(file.replace('.json',''))
            if index == id:
                fp = open(directory+file, 'r')
                tileData= json.load(fp)
                fp.close()
                return tileData

        return list() #no tiledata return empty list

    def loadBorders(self):
        directory = self.levelPath + 'border\\'
        borderData = dict()
        files = os.listdir(directory)

        for file in files:
            index = int(file.replace('.json',''))
            fp = open(directory + file, 'r')
            border = json.load(fp)
            fp.close()
            borderData[index] = border

        return borderData

    def loadActorData(self, id):
        directory = 'dir_actors\\'

        if id<10:
            file = directory+'00000'+str(id)+'.json'
        elif id<100:
            file = directory+'0000'+str(id)+'.json'
        elif id<1000:
            file = directory+'000'+str(id)+'.json'
        elif id<10000:
            file = directory+'00'+str(id)+'.json'
        elif id<100000:
            file = directory+'0'+str(id)+'.json'
        else:
            file = directory+str(id)+'.json'

        fp = open(file, 'r')
        actorData = json.load(fp)
        fp.close()

        return actorData

    def loadSpriteData(self, id):
        spritePath = 'dir_sprites\\'
        if id<10:
            directory = spritePath+'00000'+str(id)+'\\'
        elif id<100:
            directory = spritePath+'0000'+str(id)+'\\'
        elif id<1000:
            directory = spritePath+'000'+str(id)+'\\'
        elif id<10000:
            directory = spritePath+'00'+str(id)+'\\'
        elif id<100000:
            directory = spritePath+'0'+str(id)+'\\'
        else:
            directory = spritePath+str(id)+'\\'

        file = open(directory+'sprite_data.json')
        spriteData = json.load(file)
        file.close()

        return spriteData

    def loadAccessoryData(self, id):
        accessoryPath = 'dir_accessory\\'
        if id<10:
            directory = accessoryPath+'00000'+str(id)+'\\'
        elif id<100:
            directory = accessoryPath+'0000'+str(id)+'\\'
        elif id<1000:
            directory = accessoryPath+'000'+str(id)+'\\'
        elif id<10000:
            directory = accessoryPath+'00'+str(id)+'\\'
        elif id<100000:
            directory = accessoryPath+'0'+str(id)+'\\'
        else:
            directory = accessoryPath+str(id)+'\\'

        file = open(directory+'accessory_data.json')
        accessoryData = json.load(file)
        file.close()

        return accessoryData

    #TODO - need to check if this data exists somewhere in the code (higher level call?)
    def loadAccessoryPositionData(self, spriteId, accessoryId):
        spritePath = 'dir_sprites\\'

        if spriteId < 10:
            accessoryPath = spritePath + '00000' + str(id) + '\\accessories\\'
        elif spriteId < 100:
            accessoryPath = spritePath + '0000' + str(id) + '\\accessories\\'
        elif spriteId < 1000:
            accessoryPath = spritePath + '000' + str(id) + '\\accessories\\'
        elif spriteId < 10000:
            accessoryPath = spritePath + '00' + str(id) + '\\accessories\\'
        elif spriteId < 100000:
            accessoryPath = spritePath + '0' + str(id) + '\\accessories\\'
        else:
            accessoryPath = spritePath + str(id) + '\\accessories\\'

        if accessoryId<10:
            file = accessoryPath + '00000'+str(id)+'.json'
        elif accessoryId<100:
            file = accessoryPath + '0000' + str(id) + '.json'
        elif accessoryId<1000:
            file = accessoryPath + '000' + str(id) + '.json'
        elif accessoryId<10000:
            file = accessoryPath + '00' + str(id) + '.json'
        elif accessoryId<100000:
            file = accessoryPath + '0' + str(id) + '.json'
        else:
            file = accessoryPath + str(id) + '.json'

        fp = open(file, 'r')

        accessoryPostionData = json.load(fp)
        fp.close()

        return accessoryPostionData



'''


actor json
"id" : <int>,
"name" : <string>,
"size" : <list[width, height]>
"sprites" : dict{'type' : [id]} eg 'walk' : 1, 
"accessories" : list(id's)
(much more data for an actor to be added)


sprite data json
"id" : <int>,
"name" : <string>,
"coordinates" : <list[[[0,0,10,20], [10,0,10,20] ... [[.......}  #lists all directions, and the coordinates of each frame
                    goes in order, 0 is down, 1 is left, etc....
"fps" : int

accessory json (within sprites)
"id" : <int>,
"coordinates" : <list[[[[0,0], [10,0] ..}  #lists all directions, just the starting coordinates of each frame (rest of coords in acc data)


accessory data json
"id" : <int>
"name" : <string>
"coordinates" : <dict{'up' : [[0,0,10,20], [10,0,10,20] ... 'down' : [[.......}  #lists all directions, and the coordinates of each frame
'''