import sqlite3 as DATABASE#using sqlite database

DB_LOCATION = 'C:\\Users\\Robert\\Desktop\\repositories\\GameDev\\PythonGameDevelopment\\swordFightProto\\dir_database\\db_CharmQuark.sqlite'


### CONNECT TO DB ###

def queryDB(conn, query):
    return conn.execute(query)

def commitDB(conn):
    conn.commit()

def closeDB(conn):
    conn.close()

def openDB(DB_LOCATION):
    conn = DATABASE.connect(DB_LOCATION)
    return conn

### GET DATA ### 

#row[0] = level index, row[1] = name, row[2] = height, row[3] = width
#row[4] = lower tiles, row[5] = upper tiles, row[6] = borders
def getLevelData(index):
    query = "SELECT * FROM Levels WHERE level_index = {}".format(index)
    conn = openDB(DB_LOCATION)
    cursor = queryDB(conn, query)
    row = cursor.fetchone() #using primary key means only 1 result should return
    closeDB(conn)
    return row

#expect two entries, one for lower and one for upper
#col[0] = tilemap_index, col[1] = level_key, col[2] = file_path
#col[3] = tilesize col[4] = height col[5] = width col[6] = type
def getTileMaps(key):
    query = "SELECT * FROM TileMaps WHERE level_key = {}".format(key)
    conn = openDB(DB_LOCATION)
    cursor = queryDB(conn, query)
    tilemaps = []
    tilemaps.append(cursor.fetchone()) #using primary key means only 1 result should return
    tilemaps.append(cursor.fetchone())
    closeDB(conn)
    return tilemaps

#col[0] = background_index, col[1] = level_key, col[2] = file_path
#col[3] = pxHeight, col[4] = pxWidth, col[5] = visibleSections,
#col[6] = scrolling, col[7] = alpha, col[8] = layer   
def getBackgrounds(key):
    query = "SELECT * FROM Backgrounds WHERE level_key = {}".format(key)
    conn = openDB(DB_LOCATION)
    cursor = queryDB(conn, query)
    backgrounds = []
    for row in cursor:
        backgrounds.append(row)
    closeDB(conn)
    return backgrounds

#col[0] = foreground_index, col[1] = level_key, col[2] = file_path
#col[3] = pxHeight, col[4] = pxWidth, col[5] = visibleSections,
#col[6] = scrolling, col[7] = alpha, col[8] = layer   
def getForegrounds(key):
    query = "SELECT * FROM Foregrounds WHERE level_key = {}".format(key)
    conn = openDB(DB_LOCATION)
    cursor = queryDB(conn, query)
    foregrounds = []
    for row in cursor:
        foregrounds.append(row)
    closeDB(conn)
    return foregrounds

### INSERT DATA ###

def putLevelData(levelData):
    pass


if __name__ == '__main__':
    pass