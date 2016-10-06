import model

from cocos.euclid import Point2


class Battle(object):
    RANGE_SHORT = 6
    RANGE_MEDIUM = 24
    RANGE_LONG = 42

    BATTLE = None

    def __init__(self):
        Battle.BATTLE = self
        self.map = None

        self.player_list = []

        self.unit_list = []
        self.unit_turn = -1

        self.sel_cell_pos = None

    def setMap(self, map_model):
        self.map = map_model

    def addUnit(self, battle_unit):
        self.unit_list.append(battle_unit)

    def updateUnitsTurnOrder(self):
        # TODO: implement a better way to determine initiative for unit turn order
        self.unit_list = sorted(self.unit_list, key=lambda x: x.getTurnMove(), reverse=True)

    def addPlayer(self, player):
        self.player_list.append(player)

    def clearSelectedCell(self):
        self.sel_cell_pos = None

    def setSelectedCellPosition(self, col, row):
        if col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return

        self.sel_cell_pos = col, row

    def getSelectedCellPosition(self):
        return self.sel_cell_pos

    def getTurnPlayer(self):
        turn_unit = self.getTurnUnit()
        if turn_unit is None:
            return None

        return turn_unit.getPlayer()

    def getTurnUnit(self):
        if self.unit_turn < 0:
            return None

        return self.unit_list[self.unit_turn]

    def isTurnUnit(self, battle_unit):
        return battle_unit is not None and battle_unit is self.getTurnUnit()

    def nextTurn(self):
        self.unit_turn += 1
        if self.unit_turn >= len(self.unit_list):
            self.unit_turn = 0

        next_unit = self.getTurnUnit()

        if next_unit.isDestroyed():
            while next_unit.isDestroyed():
                self.unit_turn += 1
                if self.unit_turn >= len(self.unit_list):
                    self.unit_turn = 0

                next_unit = self.getTurnUnit()

        # initialize the unit for its next turn
        # TODO: account for critical and heat effects on move
        next_unit.move = next_unit.mech.move

    def getCellsInRange(self, col, row, max_dist):
        cells = {}
        self._recurseCellsInRange(col, row, 0, max_dist, cells)
        return cells

    def _recurseCellsInRange(self, col, row, dist, max_dist, cells):
        cell = (col, row)
        if dist > max_dist or (cell in cells and dist >= cells[cell]) \
                or col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return

        if dist >= 0:
            cells[cell] = dist

        # TODO: distinguish between LOS related range and move related range recursion

        # allow passing through friendly unit occupied cells
        turn_unit = self.getTurnUnit()
        turn_player = turn_unit.getPlayer()

        cell_unit = self.getUnitAt(col, row)
        is_friendly_occupied = False
        if cell_unit is not None:
            is_friendly_occupied = self.isFriendlyUnit(turn_player, cell_unit)

        if dist == 0 or self.isCellAvailable(col, row) or \
                (cell_unit is not None and is_friendly_occupied):
            self._recurseCellsInRange(col, row + 1, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col, row - 1, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col + 1, row, dist + 1, max_dist, cells)
            self._recurseCellsInRange(col - 1, row, dist + 1, max_dist, cells)

    def isCellAvailable(self, col, row):
        if self.map is None:
            return False

        if col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return False

        # check to see if any units occupy the space
        for battle_unit in self.unit_list:
            if battle_unit.col == col and battle_unit.row == row \
                    and not battle_unit.isDestroyed():
                return False

        loc = (col, row)
        cell_data = self.map.boardMap.get(loc)

        if cell_data is None:
            return True

        # TODO: check cell data to see if it is passable terrain object, such as trees, rocks, etc

        return False

    def getUnitAt(self, col, row):
        if self.map is None:
            return None

        if col < 0 or row < 0 or col >= self.map.numCols or row >= self.map.numRows:
            return None

        # find the unit that occupies the space
        for battle_unit in self.unit_list:
            if battle_unit.col == col and battle_unit.row == row \
                    and not battle_unit.isDestroyed():
                return battle_unit

        return None

    def getNumRows(self):
        return self.map.numRows

    def getNumCols(self):
        return self.map.numCols

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

    @staticmethod
    def isFriendlyUnit(player, battle_unit):
        if player is None or battle_unit is None \
                or player.team == -1:
            return False

        return player.team == battle_unit.getTeam()

    @staticmethod
    def isEnemyUnit(player, battle_unit):
        return not Battle.isFriendlyUnit(player, battle_unit)


class BattleMech(object):
    def __init__(self, player, mech, col, row):
        self.player = player
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
        self.shutdown = False

        self.armor = int(mech.armor)
        self.structure = int(mech.structure)

        # critical hit effects
        self.crit_engine = 0    # +1 Heat when weapons fire, 2nd hit: Unit destroyed
        self.crit_mp = 0        # 1/2 Move (MV), minimum loss of 2 MV each, can be 0 (immobile)
        self.crit_to_hit = 0    # +2 To-Hit each for weapons fire
        self.crit_weapons = 0   # -1 Damage each for weapons fire

    def __repr__(self):
        return "%s(name='%s %s', location=[%s,%s])" % (
            self.__class__.__name__, self.mech.name, self.mech.variant, self.col, self.row
        )

    def getPlayer(self):
        return self.player

    def getTeam(self):
        if self.player is None:
            return -1

        return self.player.team

    def setSprite(self, sprite):
        self.sprite = sprite

    def getName(self):
        return self.mech.name

    def getVariant(self):
        return self.mech.variant

    def getSprite(self):
        return self.sprite

    def getImagePath(self):
        return self.mech.image_path

    def getSize(self):
        return self.mech.size

    def getTurnMove(self):
        turn_move = self.mech.move

        if self.crit_mp > 0:
            # reduce move based on critical hits
            for i in range(self.crit_mp):
                if turn_move > 0:
                    move_reduce = round(turn_move / 2.0)
                    if move_reduce < 2.0:
                        # minimum of 2 MV reduction per critical
                        move_reduce = 2.0

                    turn_move -= int(move_reduce)

        if self.heat > 0:
            # reduce move based on heat
            turn_move -= (self.heat * 2)

        if turn_move < 0:
            return 0

        return turn_move

    def getTurnJump(self):
        return self.mech.get_jump()

    def isDestroyed(self):
        return self.structure <= 0

    def isShutdown(self):
        return self.shutdown

    def applyDamage(self, damage):
        # returns a number >0 only if there is excess damage after being destroyed
        if damage <= 0:
            return 0
        elif self.armor == 0 and self.structure == 0:
            return damage

        remaining_damage = damage

        if self.armor > 0:
            if remaining_damage > self.armor:
                # all armor will be destroyed
                remaining_damage -= self.armor
                self.armor = 0
            else:
                # only some armor is destroyed
                self.armor -= remaining_damage
                remaining_damage = 0

        if remaining_damage > 0 and self.structure > 0:
            if remaining_damage > self.structure:
                # all structure will be destroyed
                remaining_damage -= self.structure
                self.structure = 0
            else:
                # only some structure is destroyed
                self.structure -= remaining_damage
                remaining_damage = 0

        return remaining_damage


class Player(object):

    def __init__(self, callsign, team=-1, is_bot=False):
        self.callsign = callsign
        self.team = team
        self.is_bot = is_bot
