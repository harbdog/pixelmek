import cocos
import floaters
import pyglet

from cocos.batch import BatchNode
from cocos.sprite import Sprite

from resources import Resources


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

    numCols = 20
    numRows = 20

    BOARD = None

    def __init__(self):
        super(Board, self).__init__()

        Board.BOARD = self

        self.boardMap = {}
        self.cellMap = {}

        # add basic ground
        ground_img = Resources.ground_img
        node = BatchNode()
        self.add(node, z=0)

        for row in range(self.numRows):
            for col in range(self.numCols):
                cell = Cell(ground_img)
                rect = cell.get_rect()
                rect.bottomleft = col * 32, row * 32
                cell.position = rect.center
                node.add(cell, z=0)

                self.cellMap[(col, row)] = cell

        # add buildings
        buildings_tex = Resources.buildings_tex

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
                cell_z = (self.numCols - row - cell_level) * 10

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

    def get_cell(self, col, row):
        cell_pos = (col, row)
        if cell_pos not in self.cellMap:
            return None

        return self.cellMap[cell_pos]

    @staticmethod
    def board_to_layer(*coords):
        return (coords[0] * Board.TILE_SIZE), (coords[1] * Board.TILE_SIZE)

    @staticmethod
    def layer_to_board(*point):
        return (point[0] // Board.TILE_SIZE), (point[1] // Board.TILE_SIZE)


class Cell(cocos.sprite.Sprite):

    INDICATOR_PLAYER = 'player'
    INDICATOR_ENEMY = 'enemy'
    INDICATOR_FRIENDLY = 'friendly'
    INDICATOR_MOVE = 'move'
    INDICATOR_ACTION = 'action'
    INDICATOR_RANGE = 'range'

    def __init__(self, image):
        super(Cell, self).__init__(image)
        self.indicators = {}
        self.range_to_display = 0

    def show_range_to_display(self, show=True):
        indicator_name = Cell.INDICATOR_RANGE
        if show and self.range_to_display > 0:
            indicator = floaters.TextFloater(str(self.range_to_display))
            indicator.position = self.position[0], self.position[1] - self.height//4

            Board.BOARD.add(indicator, z=1000)

            self.indicators[indicator_name] = indicator
        else:
            self._remove_indicator(indicator_name)

    def show_player_indicator(self, show=True):
        indicator_name = Cell.INDICATOR_PLAYER
        if show:
            self._add_indicator(indicator_name, Resources.player_indicator_img)
        else:
            self._remove_indicator(indicator_name)

    def show_enemy_indicator(self, show=True):
        indicator_name = Cell.INDICATOR_ENEMY
        if show:
            self._add_indicator(indicator_name, Resources.enemy_indicator_img)
        else:
            self._remove_indicator(indicator_name)

    def show_friendly_indicator(self, show=True):
        indicator_name = Cell.INDICATOR_FRIENDLY
        if show:
            self._add_indicator(indicator_name, Resources.friendly_indicator_img)
        else:
            self._remove_indicator(indicator_name)

    def show_move_indicator(self, show=True):
        indicator_name = Cell.INDICATOR_MOVE
        if show:
            self._add_indicator(indicator_name, Resources.move_indicator_img)
        else:
            self._remove_indicator(indicator_name)

    def show_action_indicator(self, show=True):
        indicator_name = Cell.INDICATOR_ACTION
        if show:
            self._add_indicator(indicator_name, Resources.action_indicator_img)
        else:
            self._remove_indicator(indicator_name)

    def _add_indicator(self, indicator_name, indicator_img):
        indicator = Sprite(indicator_img)
        indicator.position = self.position

        self.add(indicator, z=len(self.indicators))

        self.indicators[indicator_name] = indicator

    def _remove_indicator(self, indicator_name):
        if indicator_name in self.indicators:
            indicator = self.indicators[indicator_name]
            indicator.kill()

            del self.indicators[indicator_name]

    def remove_indicators(self):
        self.range_to_display = 0

        for indicator_name in self.indicators.keys():
            indicator = self.indicators[indicator_name]
            indicator.kill()

            del self.indicators[indicator_name]
