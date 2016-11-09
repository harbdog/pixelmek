import random

from pixelmek.model.battle import Battle
from pixelmek.model.battle import Player
from pixelmek.ui import actions
from pixelmek.ui.board import Board
from pixelmek.ui.interface import Interface


class Bot(Player):
    def __init__(self, callsign, team=-1):
        super(Bot, self).__init__(callsign, team=team, is_bot=True)

    def act(self):
        print('ACTING')
        # make the bot do things
        battle = Battle.BATTLE
        board = Board.BOARD

        turn_unit = battle.getTurnUnit()
        turn_player = turn_unit.getPlayer()

        curr_col, curr_row = turn_unit.getPosition()

        move_col = curr_col + random.randint(-1, 1)
        move_row = curr_row + random.randint(-1, 1)

        while not battle.isCellAvailable(move_col, move_row):
            move_col = curr_col + random.randint(-1, 1)
            move_row = curr_row + random.randint(-1, 1)

        turn_unit.move -= 1

        Interface.UI.setUnitStatsIndicatorsVisible(False)

        for cell in board.cellMap.itervalues():
            cell.remove_indicators()

        animate_reverse = (turn_unit.col - move_col > 0) or (turn_unit.row - move_row > 0)

        def _ready_next_move():
            turn_unit.sprite.sulk()

            turn_cell_pos = Board.board_to_layer(turn_unit.col, turn_unit.row)
            if turn_cell_pos is not None:
                turn_cell_pos = turn_cell_pos[0] + Board.TILE_SIZE // 2, turn_cell_pos[1] + Board.TILE_SIZE // 2

            board.scroller.set_focus(*turn_cell_pos)

            print('next turn')
            actions.nextTurn()

        turn_unit.sprite.strut(reverse=animate_reverse)
        turn_unit.sprite.moveToCell(move_col, move_row, animate_reverse, _ready_next_move)

        turn_unit.col = move_col
        turn_unit.row = move_row
