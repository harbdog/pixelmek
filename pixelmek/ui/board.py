import cocos
from cocos.batch import BatchNode
from cocos.director import director
from cocos.rect import Rect
from cocos.sprite import Sprite

from pixelmek.ui import floaters
from pixelmek.ui.interface import Interface
from pixelmek.misc.resources import Resources
from pixelmek.model.battle import Battle


class Board(cocos.layer.ScrollableLayer):

    BOARD = None

    TILE_SIZE = 32

    def __init__(self, battle):
        super(Board, self).__init__()

        Board.BOARD = self
        self.scroller = None

        self.battle = battle
        self.map = battle.map
        self.cellMap = {}

        # add basic ground cell tiles
        ground_img = Resources.ground_img
        node = BatchNode()
        self.add(node, z=0)

        for row in range(self.map.numRows):
            for col in range(self.map.numCols):
                tile = self.map.getTileAt(col, row)
                cell = Cell(tile, ground_img)
                rect = cell.get_rect()
                rect.bottomleft = col * 32, row * 32
                cell.position = rect.center
                node.add(cell, z=0)

                self.cellMap[(col, row)] = cell

        # add terrain feature/building cell tiles
        for col, row in self.map.boardMap:
            loc = (col, row)
            cell_data = self.map.boardMap[loc]

            cell_images = cell_data.images

            if cell_images is not None:
                cell_level = cell_data.level
                cell_z = (self.map.numCols - row - cell_level) * 10

                cell_batch = BatchNode()
                cell_batch.position = col * self.TILE_SIZE, row * self.TILE_SIZE
                self.add(cell_batch, z=cell_z)

                cell_cols = cell_data.cols
                cell_rows = cell_data.rows
                for this_row in range(cell_rows + cell_level):
                    for this_col in range(cell_cols):
                        cell_index = this_col + (this_row * cell_cols)
                        cell_sprite = Sprite(cell_images[cell_index])

                        cell_rect = cell_sprite.get_rect()
                        cell_rect.bottomleft = this_col * self.TILE_SIZE, this_row * self.TILE_SIZE
                        cell_sprite.position = cell_rect.center

                        cell_batch.add(cell_sprite)

    def setScroller(self, scroller):
        self.scroller = scroller

    def getCellAt(self, col, row):
        cell_pos = (col, row)
        if cell_pos not in self.cellMap:
            return None

        return self.cellMap[cell_pos]

    def getTurnUnitCell(self):
        turn_unit = self.battle.getTurnUnit()
        if turn_unit is not None:
            return self.getCellAt(turn_unit.col, turn_unit.row)

    def isTurnUnitCell(self, cell):
        turn_unit = self.battle.getTurnUnit()
        if turn_unit is not None and cell is not None:
            turn_unit_cell = self.getTurnUnitCell()
            return cell is turn_unit_cell

        return False

    def getUnitCell(self, battle_unit):
        if battle_unit is None:
            return None

        return self.getCellAt(battle_unit.col, battle_unit.row)

    def clearSelectedCell(self):
        prev_cell = self.getSelectedCell()
        if prev_cell is not None:
            prev_cell.remove_indicators()

            self.battle.clearSelectedCell()

    def getSelectedCell(self):
        sel_cell_pos = self.battle.getSelectedCellPosition()
        if sel_cell_pos is None:
            return None

        return self.getCellAt(*sel_cell_pos)

    def clearSelectedCellPosition(self):
        prev_cell = self.getSelectedCell()
        if prev_cell is not None:
            prev_cell.show_action_indicator(show=False)
            prev_cell.show_range_to_display(show=False)

        self.battle.clearSelectedCell()

    def setSelectedCellPosition(self, col, row):
        if col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return

        prev_cell = self.getSelectedCell()
        if prev_cell is not None:
            prev_cell.show_action_indicator(show=False)
            prev_cell.show_range_to_display(show=False)

        self.battle.setSelectedCellPosition(col, row)
        new_cell = self.getSelectedCell()

        if new_cell is not None:
            new_cell.show_action_indicator()
            new_cell.show_range_to_display()

            cell_unit = self.battle.getUnitAt(col, row)
            if cell_unit == self.battle.getTurnUnit():
                Interface.UI.updateTargetUnitStats(None)
            else:
                Interface.UI.updateTargetUnitStats(cell_unit,
                    is_friendly=Battle.isFriendlyUnit(self.battle.getTurnPlayer(), cell_unit))

            # only refocus if getting too close to edge of display (within 3 Tiles of each side)
            self.cellInView(col, row, autofocus=True)

    def cellInView(self, col, row, autofocus=False, force_focus=False):
        if col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return False

        window_size = director.get_window_size()
        view_width = window_size[0] - Board.BOARD.TILE_SIZE * 6
        view_height = window_size[1] - Board.BOARD.TILE_SIZE * 6

        view_bottom_left = self.scroller.screen_to_world(Board.BOARD.TILE_SIZE * 3, Board.BOARD.TILE_SIZE * 3)
        view_rect = Rect(view_bottom_left[0], view_bottom_left[1], view_width, view_height)

        cell_screen_pos = Board.board_to_layer(col, row)
        cell_rect = Rect(cell_screen_pos[0], cell_screen_pos[1], Board.BOARD.TILE_SIZE, Board.BOARD.TILE_SIZE)

        intersects = cell_rect.intersects(view_rect)
        if force_focus or (autofocus and not intersects):
            self.scroller.set_focus(cell_screen_pos[0] + Board.BOARD.TILE_SIZE // 2,
                                    cell_screen_pos[1] + Board.BOARD.TILE_SIZE // 2)

        return intersects

    def cellInViewMoveBy(self, col_offset, row_offset, autofocus=False, force_focus=False):
        # determine the cell currently at the center of the view and move by offset amount
        window_size = director.get_window_size()
        view_width = window_size[0] - Board.BOARD.TILE_SIZE * 6
        view_height = window_size[1] - Board.BOARD.TILE_SIZE * 6

        view_bottom_left = self.scroller.screen_to_world(Board.BOARD.TILE_SIZE * 3, Board.BOARD.TILE_SIZE * 3)
        view_rect = Rect(view_bottom_left[0], view_bottom_left[1], view_width, view_height)

        view_center = view_rect.center
        col, row = Board.layer_to_board(*view_center)

        self.cellInView(col + col_offset, row + row_offset, autofocus, force_focus)

    def showRangeIndicators(self):
        if self.battle.isBotTurn():
            return

        turn_unit = self.battle.getTurnUnit()
        cells_in_range = self.battle.getCellsInRange(turn_unit.col, turn_unit.row, turn_unit.move)
        for cell_pos in cells_in_range:
            cell = self.getCellAt(*cell_pos)
            cell_range = cells_in_range[cell_pos]
            if self.battle.isCellAvailable(*cell_pos):
                cell.show_move_indicator()
                cell.range_to_display = cell_range
            elif self.isTurnUnitCell(cell):
                cell.show_player_indicator()

    def showUnitIndicators(self, visible=True):
        for battle_unit in self.battle.unit_list:
            show_indicator = visible and not self.battle.isTurnUnit(battle_unit)
            battle_unit.sprite.showIndicator(visible=show_indicator)

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

    def __init__(self, tile, image):
        super(Cell, self).__init__(image)
        self.tile = tile
        self.indicators = {}
        self.range_to_display = 0

        self.visible = False

    def update_los_visibility(self):
        # TODO: just see if any friendly unit has visibility to this tile
        turn_unit = Battle.BATTLE.getTurnUnit()

        self.visible = turn_unit in self.tile.los

    def show_range_to_display(self, show=True):
        indicator_name = Cell.INDICATOR_RANGE
        if show and self.range_to_display > 0:
            indicator = floaters.TextFloater(str(self.range_to_display))
            indicator.position = self.position[0], self.position[1]

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

        for indicator_name in list(self.indicators.keys()):
            indicator = self.indicators[indicator_name]
            indicator.kill()

            del self.indicators[indicator_name]
