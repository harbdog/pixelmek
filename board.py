import cocos
import pyglet

from cocos.batch import BatchNode
from cocos.sprite import Sprite


class Board(cocos.layer.ScrollableLayer):

    TILE_SIZE = 32

    KEY_TYPE = 'type'
    KEY_COLUMNS = 'cols'
    KEY_ROWS = 'rows'
    KEY_LEVEL = 'level'
    KEY_ELEVATION = 'elev'
    KEY_IMAGES = 'images'
    KEY_REF = 'ref'

    TYPE_BUILDING = 'building'

    def __init__(self):
        super(Board, self).__init__()

        self.numCols = 10
        self.numRows = 10

        self.boardMap = {}

        # add basic ground
        ground_img = pyglet.resource.image("images/board/ground-dark.png")

        for row in range(self.numRows):
            for col in range(self.numCols):
                ground = Sprite(ground_img)
                rect = ground.get_rect()
                rect.bottomleft = col * 32, row * 32
                ground.position = rect.center
                self.add(ground, z=0)

        # add buildings
        buildings_img = pyglet.resource.image("images/board/colony-buildings-32.png")
        buildings_grid = pyglet.image.ImageGrid(buildings_img,
                                                columns=(buildings_img.width // self.TILE_SIZE),
                                                rows=(buildings_img.height // self.TILE_SIZE))

        buildings_tex = pyglet.image.TextureGrid(buildings_grid)

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

        for col, row in self.boardMap:
            loc = (col, row)
            cell_data = self.boardMap[loc]

            cell_images = cell_data.get(self.KEY_IMAGES)

            if cell_images is not None:
                cell_level = cell_data[self.KEY_LEVEL]
                cell_z = self.numCols - row - cell_level

                cell_batch = BatchNode()
                cell_batch.position = col * self.TILE_SIZE, row * self.TILE_SIZE
                self.add(cell_batch, z=cell_z)

                cell_cols = cell_data[self.KEY_COLUMNS]
                cell_rows = cell_data[self.KEY_ROWS]
                for this_row in range(cell_rows + cell_level):
                    for this_col in range(cell_cols):
                        cell_index = this_col + (this_row * cell_cols)
                        cell_sprite = Sprite(cell_images[cell_index])

                        cell_rect = cell_sprite.get_rect()
                        cell_rect.bottomleft = this_col * self.TILE_SIZE, this_row * self.TILE_SIZE
                        cell_sprite.position = cell_rect.center

                        cell_batch.add(cell_sprite)

    def board_to_layer(self, *coords):
        return (coords[0] * self.TILE_SIZE), (coords[1] * self.TILE_SIZE)

    def layer_to_board(self, *point):
        return (point[0] // self.TILE_SIZE), (point[1] // self.TILE_SIZE)
