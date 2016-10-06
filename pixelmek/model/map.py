from pixelmek.misc.resources import Resources


class Map:

    MAP = None

    KEY_TYPE = 'type'
    KEY_COLUMNS = 'cols'
    KEY_ROWS = 'rows'
    KEY_LEVEL = 'level'
    KEY_ELEVATION = 'elev'
    KEY_IMAGES = 'images'
    KEY_REF = 'ref'

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
        self.boardMap[(1, 4)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                 self.KEY_COLUMNS: 3,
                                 self.KEY_ROWS: 2,
                                 self.KEY_LEVEL: 1,
                                 self.KEY_ELEVATION: 0,
                                 self.KEY_IMAGES: buildings_tex[(0, 0):(3, 3)]}
        self.boardMap[(2, 4)] = {self.KEY_REF: (1, 4)}
        self.boardMap[(3, 4)] = {self.KEY_REF: (1, 4)}
        self.boardMap[(1, 5)] = {self.KEY_REF: (1, 4)}
        self.boardMap[(2, 5)] = {self.KEY_REF: (1, 4)}
        self.boardMap[(3, 5)] = {self.KEY_REF: (1, 4)}

        # test 2x2 Building at 5,4
        self.boardMap[(5, 4)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                 self.KEY_COLUMNS: 2,
                                 self.KEY_ROWS: 2,
                                 self.KEY_LEVEL: 1,
                                 self.KEY_ELEVATION: 0,
                                 self.KEY_IMAGES: buildings_tex[(3, 0):(7, 2)]}
        self.boardMap[(6, 4)] = {self.KEY_REF: (5, 4)}
        self.boardMap[(5, 5)] = {self.KEY_REF: (5, 4)}
        self.boardMap[(6, 5)] = {self.KEY_REF: (5, 4)}

        # test 2x2 Building at 10,6
        self.boardMap[(10, 6)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                  self.KEY_COLUMNS: 2,
                                  self.KEY_ROWS: 2,
                                  self.KEY_LEVEL: 1,
                                  self.KEY_ELEVATION: 0,
                                  self.KEY_IMAGES: buildings_tex[(3, 2):(7, 4)]}
        self.boardMap[(11, 6)] = {self.KEY_REF: (10, 6)}
        self.boardMap[(10, 7)] = {self.KEY_REF: (10, 6)}
        self.boardMap[(11, 7)] = {self.KEY_REF: (10, 6)}

        # test 3x2 Building at 10,2
        self.boardMap[(10, 2)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                  self.KEY_COLUMNS: 3,
                                  self.KEY_ROWS: 2,
                                  self.KEY_LEVEL: 1,
                                  self.KEY_ELEVATION: 0,
                                  self.KEY_IMAGES: buildings_tex[(3, 5):(7, 8)]}
        self.boardMap[(11, 2)] = {self.KEY_REF: (10, 2)}
        self.boardMap[(12, 2)] = {self.KEY_REF: (10, 2)}
        self.boardMap[(10, 3)] = {self.KEY_REF: (10, 2)}
        self.boardMap[(11, 3)] = {self.KEY_REF: (10, 2)}
        self.boardMap[(12, 3)] = {self.KEY_REF: (10, 2)}

        # test 2x2x2 Building at 12,12
        self.boardMap[(12, 12)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                   self.KEY_COLUMNS: 2,
                                   self.KEY_ROWS: 2,
                                   self.KEY_LEVEL: 2,
                                   self.KEY_ELEVATION: 0,
                                   self.KEY_IMAGES: buildings_tex[(3, 10):(8, 12)]}
        self.boardMap[(13, 12)] = {self.KEY_REF: (12, 12)}
        self.boardMap[(12, 13)] = {self.KEY_REF: (12, 12)}
        self.boardMap[(13, 13)] = {self.KEY_REF: (12, 12)}

        # test 3x3 Building at 15,10
        self.boardMap[(15, 10)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                   self.KEY_COLUMNS: 3,
                                   self.KEY_ROWS: 3,
                                   self.KEY_LEVEL: 1,
                                   self.KEY_ELEVATION: 0,
                                   self.KEY_IMAGES: buildings_tex[(7, 10):(13, 13)]}
        self.boardMap[(16, 10)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(17, 10)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(15, 11)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(16, 11)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(17, 11)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(15, 12)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(16, 12)] = {self.KEY_REF: (15, 10)}
        self.boardMap[(17, 12)] = {self.KEY_REF: (15, 10)}

        # test 5x2 Building at 3,14
        self.boardMap[(3, 14)] = {self.KEY_TYPE: self.TYPE_BUILDING,
                                  self.KEY_COLUMNS: 5,
                                  self.KEY_ROWS: 2,
                                  self.KEY_LEVEL: 0,
                                  self.KEY_ELEVATION: 0,
                                  self.KEY_IMAGES: buildings_tex[(9, 0):(11, 5)]}
        self.boardMap[(4, 14)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(5, 14)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(6, 14)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(7, 14)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(3, 15)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(4, 15)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(5, 15)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(6, 15)] = {self.KEY_REF: (3, 14)}
        self.boardMap[(7, 15)] = {self.KEY_REF: (3, 14)}
