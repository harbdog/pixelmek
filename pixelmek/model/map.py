from pixelmek.misc.resources import Resources


class Map:

    MAP = None

    TYPE_NONE = 'none'
    TYPE_BUILDING = 'building'

    numCols = 20
    numRows = 20

    def __init__(self):
        Map.MAP = self

        self.boardMap = {}

        # generate a simple test map model

        # add buildings
        buildings_tex = Resources.buildings_tex

        # test 3x2 Building at 1,4
        self.boardMap[(1, 4)] = Tile(tile_type=Map.TYPE_BUILDING, cols=3, rows=2,
                                     elevation=0, level=1,
                                     images=buildings_tex[(0, 0):(3, 3)])
        self.boardMap[(2, 4)] = Tile(ref=(1, 4))
        self.boardMap[(3, 4)] = Tile(ref=(1, 4))
        self.boardMap[(1, 5)] = Tile(ref=(1, 4))
        self.boardMap[(2, 5)] = Tile(ref=(1, 4))
        self.boardMap[(3, 5)] = Tile(ref=(1, 4))

        # test 2x2 Building at 5,4
        self.boardMap[(5, 4)] = Tile(tile_type=Map.TYPE_BUILDING, cols=2, rows=2,
                                     elevation=0, level=1,
                                     images=buildings_tex[(3, 0):(7, 2)])
        self.boardMap[(6, 4)] = Tile(ref=(5, 4))
        self.boardMap[(5, 5)] = Tile(ref=(5, 4))
        self.boardMap[(6, 5)] = Tile(ref=(5, 4))

        # test 2x2 Building at 10,6
        self.boardMap[(10, 6)] = Tile(tile_type=Map.TYPE_BUILDING, cols=2, rows=2,
                                     elevation=0, level=1,
                                     images=buildings_tex[(3, 2):(7, 4)])
        self.boardMap[(11, 6)] = Tile(ref=(10, 6))
        self.boardMap[(10, 7)] = Tile(ref=(10, 6))
        self.boardMap[(11, 7)] = Tile(ref=(10, 6))

        # test 3x2 Building at 10,2
        self.boardMap[(10, 2)] = Tile(tile_type=Map.TYPE_BUILDING, cols=3, rows=2,
                                     elevation=0, level=1,
                                     images=buildings_tex[(3, 5):(7, 8)])
        self.boardMap[(11, 2)] = Tile(ref=(10, 2))
        self.boardMap[(12, 2)] = Tile(ref=(10, 2))
        self.boardMap[(10, 3)] = Tile(ref=(10, 2))
        self.boardMap[(11, 3)] = Tile(ref=(10, 2))
        self.boardMap[(12, 3)] = Tile(ref=(10, 2))

        # test 2x2x2 Building at 12,12
        self.boardMap[(12, 12)] = Tile(tile_type=Map.TYPE_BUILDING, cols=2, rows=2,
                                     elevation=0, level=2,
                                     images=buildings_tex[(3, 10):(8, 12)])
        self.boardMap[(13, 12)] = Tile(ref=(12, 12))
        self.boardMap[(12, 13)] = Tile(ref=(12, 12))
        self.boardMap[(13, 13)] = Tile(ref=(12, 12))

        # test 3x3 Building at 15,10
        self.boardMap[(15, 10)] = Tile(tile_type=Map.TYPE_BUILDING, cols=3, rows=3,
                                     elevation=0, level=1,
                                     images=buildings_tex[(7, 10):(13, 13)])
        self.boardMap[(16, 10)] = Tile(ref=(15, 10))
        self.boardMap[(17, 10)] = Tile(ref=(15, 10))
        self.boardMap[(15, 11)] = Tile(ref=(15, 10))
        self.boardMap[(16, 11)] = Tile(ref=(15, 10))
        self.boardMap[(17, 11)] = Tile(ref=(15, 10))
        self.boardMap[(15, 12)] = Tile(ref=(15, 10))
        self.boardMap[(16, 12)] = Tile(ref=(15, 10))
        self.boardMap[(17, 12)] = Tile(ref=(15, 10))

        # test 5x2 Building at 3,14
        self.boardMap[(3, 14)] = Tile(tile_type=Map.TYPE_BUILDING, cols=5, rows=2,
                                     elevation=0, level=0,
                                     images=buildings_tex[(9, 0):(11, 5)])
        self.boardMap[(4, 14)] = Tile(ref=(3, 14))
        self.boardMap[(5, 14)] = Tile(ref=(3, 14))
        self.boardMap[(6, 14)] = Tile(ref=(3, 14))
        self.boardMap[(7, 14)] = Tile(ref=(3, 14))
        self.boardMap[(3, 15)] = Tile(ref=(3, 14))
        self.boardMap[(4, 15)] = Tile(ref=(3, 14))
        self.boardMap[(5, 15)] = Tile(ref=(3, 14))
        self.boardMap[(6, 15)] = Tile(ref=(3, 14))
        self.boardMap[(7, 15)] = Tile(ref=(3, 14))

    def getTileAt(self, col, row):
        if col < 0 or row < 0 or col >= self.numCols or row >= self.numRows:
            return None

        pos = (col, row)
        if pos not in self.boardMap:
            self.boardMap[pos] = Tile()

        return self.boardMap[pos]

    def clearLOS(self):
        for pos, tile in self.boardMap.items():
            tile.los = False


class Tile:
    def __init__(self, tile_type=Map.TYPE_NONE, cols=1, rows=1,
                 elevation=0, level=0, images=None, ref=None):
        self.type = tile_type
        self.cols = cols
        self.rows = rows
        self.elevation = elevation
        self.level = level
        self.images = images
        self.ref = ref

        self.los = False
