from __future__ import division

import cocos
import pyglet
from pyglet import window
from pyglet.window import mouse

import actions
from board import Board
from interface import Interface


class KeyboardEvents(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self, board):
        super(KeyboardEvents, self).__init__()

        # keep track of battle objects being controlled by events
        self.board = board
        self.battle = board.battle

        # To keep track of which keys are pressed:
        self.keys_pressed = set()

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """

        char = pyglet.window.key.symbol_string(key)
        self.keys_pressed.add(char)

        mech = self.battle.getTurnUnit()

        if char == "P":
            mech.sprite.pause()

        elif char in ("SPACE", "RETURN"):
            cell_pos = self.battle.getSelectedCellPosition()
            if cell_pos is None:
                return

            actions.actOnCell(self.board, cell_pos[0], cell_pos[1])

        elif char in ("LEFT", "A"):
            if modifiers & window.key.MOD_SHIFT:
                # move view left
                self.board.cellInViewMoveBy(-3, 0, force_focus=True)
            else:
                # move selection left
                actions.moveSelectionBy(self.board, -1, 0)

        elif char in ("RIGHT", "D"):
            if modifiers & window.key.MOD_SHIFT:
                # move view right
                self.board.cellInViewMoveBy(3, 0, force_focus=True)
            else:
                # move selection right
                actions.moveSelectionBy(self.board, 1, 0)

        elif char in ("UP", "W"):
            if modifiers & window.key.MOD_SHIFT:
                # move view up
                self.board.cellInViewMoveBy(0, 3, force_focus=True)
            else:
                # move selection up
                actions.moveSelectionBy(self.board, 0, 1)

        elif char in ("DOWN", "S"):
            if modifiers & window.key.MOD_SHIFT:
                # move view down
                self.board.cellInViewMoveBy(0, -3, force_focus=True)
            else:
                # move selection down
                actions.moveSelectionBy(self.board, 0, -1)

        elif char in ("LSHIFT", "RSHIFT", "LCTRL", "RCTRL"):
            print("modifier pressed: " + char)

        else:
            print("unused binding: " + char)

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        char = pyglet.window.key.symbol_string(key)
        if char in self.keys_pressed:
            self.keys_pressed.remove(char)

        mech = self.battle.getTurnUnit()

        if char == "P":
            mech.sprite.resume()


class MouseEvents(cocos.layer.ScrollableLayer):

    is_event_handler = True     #: enable director.window events

    def __init__(self, board):
        super(MouseEvents, self).__init__()

        self.board = board
        self.battle = board.battle

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves over the app window with no button pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        """
        # self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        # self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """

        # first, check if there is a UI button where pressed before cascading down
        if actions.actOnUI(x, y) is not False:
            return

        real_x, real_y = self.board.scroller.screen_to_world(x, y)
        col, row = Board.layer_to_board(real_x, real_y)

        if buttons & mouse.RIGHT:
            # perform action on the cell
            actions.actOnCell(self.board, col, row)

        elif buttons & mouse.LEFT:
            if modifiers & window.key.MOD_SHIFT:
                # move view to the cell
                self.board.cellInView(col, row, force_focus=True)
            else:
                # select the specific cell
                if not self.board.cellInView(col, row, autofocus=True):
                    return

                actions.moveSelectionTo(self.board, col, row)
