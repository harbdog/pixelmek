from __future__ import division

import cocos
import pyglet
from pyglet.window import mouse

import actions
from board import Board


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

        elif char == "SPACE" or char == "RETURN":
            cell_pos = self.battle.getSelectedCellPosition()
            if cell_pos is None:
                return

            actions.actOnCell(self.board, cell_pos[0], cell_pos[1])

        elif char == "W":
            mech.sprite.strut()

        elif char == "S":
            mech.sprite.sulk()

        elif char == "LEFT":
            # move selection left
            actions.moveSelectionBy(self.board, -1, 0)

        elif char == "RIGHT":
            # move selection right
            actions.moveSelectionBy(self.board, 1, 0)

        elif char == "UP":
            # move selection up
            actions.moveSelectionBy(self.board, 0, 1)

        elif char == "DOWN":
            # move selection down
            actions.moveSelectionBy(self.board, 0, -1)

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
        real_x, real_y = self.board.scroller.screen_to_world(x, y)
        dest_cell = Board.layer_to_board(real_x, real_y)

        if buttons & mouse.RIGHT:
            # perform action on the cell
            actions.actOnCell(self.board, dest_cell[0], dest_cell[1])

        elif buttons & mouse.LEFT:
            # select the specific cell
            actions.moveSelectionTo(self.board, dest_cell[0], dest_cell[1])
