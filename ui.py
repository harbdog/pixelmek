import cocos
import pyglet
from cocos.euclid import Point2
from cocos.rect import Rect

import floaters

from board import Board
from cocos.batch import BatchNode
from cocos.director import director
from cocos.sprite import Sprite
from widgets import UnitCard


class Interface(cocos.layer.Layer):

    UI = None

    def __init__(self):
        super(Interface, self).__init__()

        Interface.UI = self

        self.unit_display = None

        self.target_display = None

        # TESTING: clickable UI buttons
        size = director.get_window_size()
        width = size[0]
        height = size[1]
        btn = Button()
        btn.position = width//2, Board.TILE_SIZE
        self.add(btn)

    def updatePlayerUnitStats(self, battle_unit):
        if self.unit_display is not None:
            self.unit_display.kill()

        if battle_unit is None:
            # Hide player unit stats at bottom left
            self.unit_display = None
            return

        # size = director.get_window_size()
        # width = size[0]
        # height = size[1]

        self.unit_display = UnitCard(battle_unit)
        self.unit_display.position = Board.TILE_SIZE // 2, Board.TILE_SIZE
        self.add(self.unit_display)

    def updateTargetUnitStats(self, target_unit, is_friendly=False):
        if self.target_display is not None:
            self.target_display.kill()

        if target_unit is None:
            # Hide target unit stats at top right
            self.target_display = None
            return

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.target_display = UnitCard(target_unit, is_friendly=is_friendly, reverse=True)
        self.target_display.position = width - self.target_display.width - Board.TILE_SIZE // 2, \
                                       height - self.target_display.height - Board.TILE_SIZE // 2
        self.add(self.target_display)


class Button(cocos.layer.ColorLayer):

    def __init__(self, r=225, g=225, b=225, a=255//2):
        super(Button, self).__init__(r, g, b, a)

        self.width = Board.TILE_SIZE
        self.height = Board.TILE_SIZE

        director.window.push_handlers(self.on_mouse_press)

    def on_mouse_press(self, x, y, button, modifiers):
        p = Rect(x, y, 0.1, 0.1)
        r = Rect(self.x, self.y, self.width, self.height)

        if p.intersect(r) is not None:
            print("Pressed Button!")
        else:
            print("Missed Button")
