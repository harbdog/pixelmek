import cocos
import pyglet


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
            mech.sprite.stop()

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
