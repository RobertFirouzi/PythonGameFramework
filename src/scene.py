class Scene:
    def __init__(self,
                 name,
                 id,
                 size_tiles,
                 renderLayers,
                 borders,
                 eventBoxes,
                 gameEvents,
                 actors):
        self.name = name
        self.id = id
        self.size_tiles = size_tiles
        self.renderLayers = renderLayers
        self.borders = borders
        self.eventBoxes = eventBoxes
        self.gameEvents = gameEvents
        self.actors = actors