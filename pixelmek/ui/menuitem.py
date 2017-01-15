from cocos.menu import BaseMenuItem, MultipleMenuItem
from pyglet import gl
from pyglet.window import key
from pixelmek.model.battle import Battle, BattleMech
from widgets import UnitCard


class UnitMenuItem(BaseMenuItem):
    """ A menu item for selecting between multiple unit cards """
    def __init__(self, player, units, callback_func, default_unit=0, *args, **kwargs):
        super(UnitMenuItem, self).__init__(callback_func, *args, **kwargs)

        self.player = player
        self.units = units
        self.idx = default_unit

        self.pos_x = 0
        self.pos_y = 0

    def generateWidgets(self, pos_x, pos_y, font_item, font_item_selected):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self._update_selected_unit()

    def _update_selected_unit(self):
        battle_unit = BattleMech(self.player, self.units[self.idx], col=0, row=0)

        self.item = UnitCard(battle_unit, mask_image=False)
        self.item.x = self.pos_x - 25
        self.item.y = self.pos_y

        self.selected_item = UnitCard(battle_unit, mask_image=False, menu_selected=True)
        self.selected_item.x = self.pos_x - 25
        self.selected_item.y = self.pos_y

    def get_item_width(self):
        return self.item.width

    def get_item_height(self):
        return self.item.height

    def draw(self):
        gl.glPushMatrix()
        self.transform()

        children = self.get_children()

        if self.is_selected:
            if self.item in children:
                self.remove(self.item)
            if self.selected_item not in children:
                self.add(self.selected_item)
        else:
            if self.selected_item in children:
                self.remove(self.selected_item)

            if self.item not in children:
                self.add(self.item)

        gl.glPopMatrix()

    def on_key_press(self, symbol, modifiers):
        if symbol in (key.LEFT, key.BACKSPACE):
            self.idx -= 1
            if self.idx < 0:
                self.idx = len(self.units) - 1
        elif symbol in (key.RIGHT, key.ENTER):
            self.idx += 1
            if self.idx > len(self.units) - 1:
                self.idx = 0

        if symbol in (key.LEFT, key.RIGHT, key.ENTER, key.BACKSPACE):
            children = self.get_children()
            if self.item in children:
                self.remove(self.item)
            if self.selected_item in children:
                self.remove(self.selected_item)

            self._update_selected_unit()
            self.draw()
            self.callback_func(self.idx)
            return True


class LoopingMultipleMenuItem(MultipleMenuItem):
    """
    A menu item for switching between multiple values that loops around when it reaches list extents
    """

    def __init__(self, label, callback_func, items, default_item=0):
        super(LoopingMultipleMenuItem, self).__init__(label, callback_func, items, default_item)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.idx -= 1
            if self.idx < 0:
                self.idx = len(self.items)-1
        elif symbol in (key.RIGHT, key.ENTER):
            self.idx += 1
            if self.idx > len(self.items)-1:
                self.idx = 0

        if symbol in (key.LEFT, key.RIGHT, key.ENTER):
            self.item.text = self._get_label()
            self.item_selected.text = self._get_label()
            self.callback_func(self.idx)
            return True
