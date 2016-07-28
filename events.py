import cocos
import pyglet
from cocos.actions import *
from cocos.particle_systems import Meteor
from cocos.euclid import Point2
from pyglet.window import mouse


class KeyboardEvents(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self, battle):
        super(KeyboardEvents, self).__init__()

        # keep track of battle objects being controlled by events
        self.battle = battle

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

        elif char == "SPACE":
            # mech.sprite.stop()
            ppc = Meteor()
            ppc.size = 10
            ppc.speed = 0
            ppc.gravity = cocos.euclid.Point2(-200, -200)
            ppc.emission_rate = 100
            ppc.life = 0.5
            ppc.life_var = 0.1

            ppc.position = mech.sprite.position
            self.battle.board.add(ppc, z=1000)

            action = MoveTo((300, 300), duration=1) + CallFunc(ppc.stop_system)
            ppc.do(action)

        elif char == "W":
            mech.sprite.strut()

        elif char == "S":
            mech.sprite.sulk()

        elif char == "LEFT":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col - 1
            chk_rownum = turn_unit.row

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut(reverse=True)
                mech.sprite.moveBy(-32, 0, mech.sprite.sulk)

        elif char == "RIGHT":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col + 1
            chk_rownum = turn_unit.row

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut()
                mech.sprite.moveBy(32, 0, mech.sprite.sulk)

        elif char == "UP":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col
            chk_rownum = turn_unit.row + 1

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut(reverse=True)
                mech.sprite.moveBy(0, 32, mech.sprite.sulk)

        elif char == "DOWN":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col
            chk_rownum = turn_unit.row - 1

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut()
                mech.sprite.moveBy(0, -32, mech.sprite.sulk)

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

    def __init__(self, battle):
        super(MouseEvents, self).__init__()

        self.battle = battle

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
        real_x, real_y = self.battle.scroller.screen_to_world(x, y)

        turn_unit = self.battle.getTurnUnit()
        if buttons & mouse.RIGHT:
            # fire a test ppc
            ppc = Meteor()
            ppc.size = 10
            ppc.speed = 15
            ppc.gravity = Point2(0, 0)
            ppc.emission_rate = 100
            ppc.life = 0.5
            ppc.life_var = 0.1

            ppc.position = turn_unit.sprite.position
            self.battle.board.add(ppc, z=1000)

            # figure out the duration based on speed and distance
            ppc_speed = 400     # pixels per second
            distance = Point2(ppc.x, ppc.y).distance(Point2(real_x, real_y))
            ppc_t = distance / ppc_speed

            action = MoveTo((real_x, real_y), duration=ppc_t) + CallFunc(ppc.stop_system)
            ppc.do(action)

        elif buttons & mouse.LEFT:
            # test movement to the specific cell
            # chk_colnum = turn_unit.col
            # chk_rownum = turn_unit.row - 1
            chk_cell = self.battle.board.layer_to_board(real_x, real_y)
            chk_colnum = chk_cell[0]
            chk_rownum = chk_cell[1]

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                turn_unit.sprite.strut()
                turn_unit.sprite.moveToCell(chk_colnum, chk_rownum, turn_unit.sprite.sulk)
