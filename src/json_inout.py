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

import json
import os
LEVELS_DIRECTORY = 'dir_levels\\'

class LevelLoader:
    def __init__(self, index): #sets the path to the folder for this level
        if index<10:
            self.levelPath = LEVELS_DIRECTORY+'00000'+str(index)+'\\'
        elif index<100:
            self.levelPath = LEVELS_DIRECTORY+'0000'+str(index)+'\\'
        elif index<1000:
            self.levelPath = LEVELS_DIRECTORY+'000'+str(index)+'\\'
        elif index<10000:
            self.levelPath = LEVELS_DIRECTORY+'00'+str(index)+'\\'
        elif index<100000:
            self.levelPath = LEVELS_DIRECTORY+'0'+str(index)+'\\'
        else:
            self.levelPath = LEVELS_DIRECTORY+str(index)+'\\'

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
            fp = open(file, 'r')
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
            index = int(file.replace('.json',''))
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
