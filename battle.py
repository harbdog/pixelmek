import model
from board import Board


class Battle(object):
    def __init__(self):
        self.board = None
        self.scroller = None
        self.unit_list = []
        self.unit_turn = 0

    def setBoard(self, board):
        self.board = board

    def setScroller(self, scroller):
        self.scroller = scroller

    def addUnit(self, battle_unit):
        self.unit_list.append(battle_unit)

    def getTurnUnit(self):
        return self.unit_list[self.unit_turn]

    def nextTurn(self):
        self.unit_turn += 1
        if self.unit_turn >= len(self.unit_list):
            self.unit_turn = 0

    def getNumRows(self):
        return Board.numRows

    def getNumCols(self):
        return Board.numCols

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
