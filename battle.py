import model

from board import Board
from cocos.euclid import Point2

from resources import Resources


class Battle(object):
    RANGE_SHORT = 6
    RANGE_MEDIUM = 24
    RANGE_LONG = 42

    BATTLE = None

    def __init__(self):
        Battle.BATTLE = self
        self.board = None
        self.scroller = None
        self.unit_list = []
        self.unit_turn = -1

        self.sel_cell_pos = None

    def setBoard(self, board):
        self.board = board

    def setScroller(self, scroller):
        self.scroller = scroller

    def addUnit(self, battle_unit):
        self.unit_list.append(battle_unit)

    def clearSelectedCell(self):
        prev_cell = self.getSelectedCell()
        if prev_cell is not None:
            prev_cell.remove_indicators()

        self.sel_cell_pos = None

    def setSelectedCellPosition(self, col, row):
        if col < 0 or row < 0 or col >= Board.numCols or row >= Board.numRows:
            return

        prev_cell = self.getSelectedCell()
        if prev_cell is not None:
            prev_cell.show_action_indicator(show=False)

        self.sel_cell_pos = col, row
        new_cell = self.getSelectedCell()

        if new_cell is not None:
            new_cell.show_action_indicator()

            # TODO: only refocus if getting too close to edge of display
            # self.scroller.set_focus(*Board.board_to_layer(col, row))

    def getSelectedCellPosition(self):
        return self.sel_cell_pos

    def getSelectedCell(self):
        if self.sel_cell_pos is None:
            return None

        return self.board.get_cell(*self.sel_cell_pos)

    def getTurnUnit(self):
        if self.unit_turn < 0:
            return None

        return self.unit_list[self.unit_turn]

    def isTurnUnit(self, battle_unit):
        return battle_unit is not None and battle_unit is self.getTurnUnit()

    def getTurnUnitCell(self):
        turn_unit = self.getTurnUnit()
        if turn_unit is not None:
            return self.getCellAt(turn_unit.col, turn_unit.row)

    def isTurnUnitCell(self, cell):
        turn_unit = self.getTurnUnit()
        if turn_unit is not None and cell is not None:
            turn_unit_cell = self.getTurnUnitCell()
            return cell is turn_unit_cell

        return False

    def getUnitCell(self, battle_unit):
        if battle_unit is None:
            return None

        return self.board.get_cell(battle_unit.col, battle_unit.row)

    def nextTurn(self):
        prev_unit = self.getTurnUnit()
        if prev_unit is not None:
            prev_unit.sprite.stop()

        self.unit_turn += 1
        if self.unit_turn >= len(self.unit_list):
            self.unit_turn = 0

        for cell in self.board.cellMap.itervalues():
            cell.remove_indicators()

        next_unit = self.getTurnUnit()
        next_unit.sprite.sulk()

        self.showRangeIndicators()
        self.showUnitIndicators()

        self.setSelectedCellPosition(next_unit.col, next_unit.row)

        self.scroller.set_focus(*Board.board_to_layer(next_unit.col, next_unit.row))

    def showRangeIndicators(self):
        turn_unit = self.getTurnUnit()
        for cell_pos in self.getCellsInRange(turn_unit.col, turn_unit.row, turn_unit.move):
            cell = self.getCellAt(*cell_pos)
            if self.isCellAvailable(*cell_pos):
                cell.show_move_indicator()
            elif self.isTurnUnitCell(cell):
                cell.show_player_indicator()

    def showUnitIndicators(self):
        for battle_unit in self.unit_list:
            show_indicator = not self.isTurnUnit(battle_unit)
            battle_unit.sprite.showIndicator(visible=show_indicator)

    def getCellsInRange(self, col, row, max_dist):
        cells = {}
        self._recurseCellsInRange(col, row, 0, max_dist, cells)
        return cells

    def _recurseCellsInRange(self, col, row, dist, max_dist, cells):
        cell = (col, row)
        if dist > max_dist or (cell in cells and dist >= cells[cell]) \
                or col < 0 or row < 0 or col >= Board.numCols or row >= Board.numRows:
            return

        if dist > 0:
            cells[cell] = dist

        # TODO: distinguish between LOS related range and move related range recursion

        # TODO: allow passing through friendly unit occupied cells
        if dist == 0 or self.isCellAvailable(col, row):
            self._recurseCellsInRange(col, row + 1, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col, row - 1, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col + 1, row, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col - 1, row, dist + 1, max_dist, cells)

    def isCellAvailable(self, col, row):
        if self.board is None:
            return False

        if col < 0 or row < 0 or col >= self.board.numCols or row >= self.board.numRows:
            return False

        # check to see if any units occupy the space
        for battle_unit in self.unit_list:
            if battle_unit.col == col and battle_unit.row == row:
                return False

        loc = (col, row)
        cell_data = self.board.boardMap.get(loc)

        if cell_data is None:
            return True

        # TODO: check cell data to see if it is passable terrain object, such as trees, rocks, etc

        return False

    def getCellAt(self, col, row):
        return self.board.get_cell(col, row)

    def getUnitAtCell(self, col, row):
        if self.board is None:
            return None

        if col < 0 or row < 0 or col >= Board.numCols or row >= Board.numRows:
            return None

        # find the unit that occupies the space
        for battle_unit in self.unit_list:
            if battle_unit.col == col and battle_unit.row == row:
                return battle_unit

        return None

    @staticmethod
    def getNumRows():
        return Board.numRows

    @staticmethod
    def getNumCols():
        return Board.numCols

    @staticmethod
    def getCellDistance(cell_1, cell_2):
        point_1 = Point2(cell_1[0], cell_1[1])
        point_2 = Point2(cell_2[0], cell_2[1])

        return point_1.distance(point_2)

    @staticmethod
    def getDistanceRange(cell_distance):
        if cell_distance <= Battle.RANGE_SHORT:
            return model.Weapon.RANGE_SHORT

        elif cell_distance <= Battle.RANGE_MEDIUM:
            return model.Weapon.RANGE_MEDIUM

        elif cell_distance <= Battle.RANGE_LONG:
            return model.Weapon.RANGE_LONG

        return model.Weapon.RANGE_EXTREME


class BattleMech(object):
    def __init__(self, mech, col, row):
        self.mech = mech
        self.sprite = None

        # setup values which are dynamic in battle
        self.col = col
        self.row = row

        self.skill = mech.skill
        self.move = mech.move
        self.jump = mech.get_jump()
        self.short = mech.short
        self.medium = mech.medium
        self.long = mech.long
        self.heat = 0
        self.armor = mech.armor
        self.structure = mech.structure

    def __repr__(self):
        return "%s(name='%s %s', location=[%s,%s])" % (
            self.__class__.__name__, self.mech.name, self.mech.variant, self.col, self.row
        )

    def setSprite(self, sprite):
        self.sprite = sprite

    def getSprite(self):
        return self.sprite

    def getImagePath(self):
        return self.mech.image_path

    def getSize(self):
        return self.mech.size
