import random

from cocos.actions import *
from pixelmek.model.battle import Battle
from pixelmek.model.battle import Player
from pixelmek.ui import actions
from pixelmek.ui.board import Board
from pixelmek.ui.interface import Interface


class Bot(Player):
    def __init__(self, callsign, team=-1):
        super(Bot, self).__init__(callsign, team=team, is_bot=True)

    def act(self):
        print('bot > ACTING')
        # make the bot do things
        battle = Battle.BATTLE
        board = Board.BOARD

        turn_unit = battle.getTurnUnit()
        curr_col, curr_row = turn_unit.getPosition()

        turn_player = turn_unit.getPlayer()

        Interface.UI.setUnitStatsIndicatorsVisible(False)

        for cell in board.cellMap.itervalues():
            cell.remove_indicators()

        # first, determine where to move
        # for now, just find a spot that is both in range to some target and has fewest LOS to other targets
        cells_in_range = battle.getCellsInRange(turn_unit.col, turn_unit.row, turn_unit.move)
        enemy_units = battle.getEnemyUnits(turn_unit)

        cell_pos_best = turn_unit.getPosition()
        cell_los_best = 1000

        for cell_pos in cells_in_range:
            # cell_range = cells_in_range[cell_pos]
            if not battle.isCellAvailable(*cell_pos):
                continue

            num_los = 0

            for enemy in enemy_units:
                if enemy.isDestroyed():
                    continue

                target_coords = enemy.getPosition()
                if battle.hasTargetLOS(cell_pos, target_coords):
                    num_los += 1

            if num_los > 0 and num_los < cell_los_best:
                cell_pos_best = cell_pos
                cell_los_best = num_los

        move_col, move_row = curr_col, curr_row
        move_amt = 0
        if cell_pos_best is not None:
            move_col = cell_pos_best[0]
            move_row = cell_pos_best[1]
            move_amt = cells_in_range[move_col, move_row]

        animate_reverse = (turn_unit.col - move_col > 0) or (turn_unit.row - move_row > 0)

        def _ready_next_move():
            turn_unit.sprite.sulk()

            turn_cell_pos = Board.board_to_layer(turn_unit.col, turn_unit.row)
            if turn_cell_pos is not None:
                turn_cell_pos = turn_cell_pos[0] + Board.TILE_SIZE // 2, turn_cell_pos[1] + Board.TILE_SIZE // 2

            board.scroller.set_focus(*turn_cell_pos)

            # actions.nextTurn()
            self._prepare_attack()

        turn_unit.sprite.strut(reverse=animate_reverse)
        turn_unit.sprite.moveToCell(move_col, move_row, animate_reverse, _ready_next_move)

        turn_unit.move -= move_amt
        turn_unit.col = move_col
        turn_unit.row = move_row

    def _prepare_attack(self):
        battle = Battle.BATTLE
        board = Board.BOARD

        turn_unit = battle.getTurnUnit()

        target_unit = None
        target_to_hit = 0

        enemy_units = battle.getEnemyUnits(turn_unit)
        for enemy in enemy_units:
            if enemy.isDestroyed():
                continue

            to_hit = battle.getToHit(turn_unit, enemy)

            if to_hit > 0 and to_hit > target_to_hit:
                target_unit = enemy
                target_to_hit = to_hit

        if target_unit is not None:
            print('bot > attacking '+str(target_unit))
            attack_time = actions.performAttackOnUnit(board, target_unit)

            def _ready_next_turn():
                print('bot > next turn...')
                Interface.UI.setUnitStatsIndicatorsVisible(True)
                actions.nextTurn()

            # start the next turn when the attack is completed
            board.do(Delay(attack_time) + CallFunc(_ready_next_turn))

        else:
            print('bot > skipping turn...')
            Interface.UI.setUnitStatsIndicatorsVisible(True)
            actions.nextTurn()
