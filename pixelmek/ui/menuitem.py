from cocos.menu import BaseMenuItem
from pyglet import gl
from pyglet.window import key
from pixelmek.model.battle import Battle, BattleMech
from widgets import UnitCard


class UnitMenuItem(BaseMenuItem):
    """ A menu item for selecting between multiple unit cards """
    def __init__(self, units, callback_func, default_unit=0, *args, **kwargs):
        super(UnitMenuItem, self).__init__(callback_func, *args, **kwargs)

        self.units = units
        self.idx = default_unit

        self.pos_x = 0
        self.pos_y = 0

    def generateWidgets(self, pos_x, pos_y, font_item, font_item_selected):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self._update_selected_unit()

    def _update_selected_unit(self):
        self.item = UnitCard(BattleMech(Battle.BATTLE.player_one, self.units[self.idx], col=0, row=0))
        self.item.x = self.pos_x
        self.item.y = self.pos_y

    def draw(self):
        gl.glPushMatrix()
        self.transform()

        if self.item not in self.get_children():
            self.add(self.item)

        gl.glPopMatrix()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.idx = max(0, self.idx - 1)
        elif symbol in (key.RIGHT, key.ENTER):
            self.idx = min(len(self.units) - 1, self.idx + 1)

        if symbol in (key.LEFT, key.RIGHT, key.ENTER):
            if self.item in self.get_children():
                self.remove(self.item)
            self._update_selected_unit()
            self.draw()
            self.callback_func(self.idx)
            return True
