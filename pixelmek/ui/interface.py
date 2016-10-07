import cocos
from cocos.director import director

from widgets import Button
from widgets import UnitCard
from pixelmek.misc.resources import Resources


class Interface(cocos.layer.Layer):

    UI = None

    def __init__(self):
        super(Interface, self).__init__()
        from board import Board

        Interface.UI = self

        self.buttons = []

        self.unit_display = None
        self.target_display = None

        # TESTING: clickable UI buttons
        size = director.get_window_size()
        width = size[0]
        height = size[1]
        btn = Button(icon=Resources.move_button_img, action=self.doSomething,
                     width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        btn2 = Button(icon=Resources.evade_button_img, action=self.doSomethingElse,
                     width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        btn3 = Button(icon=Resources.sprint_button_img, action=self.doSomething,
                     width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        btn4 = Button(icon=Resources.weapon_button_img, action=self.doSomethingElse,
                      width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        btn5 = Button(icon=Resources.overheat_button_img, action=self.doSomething,
                     width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        btn6 = Button(icon=Resources.end_button_img, action=self.doSomethingElse,
                      width=4+Board.TILE_SIZE, height=4+Board.TILE_SIZE)

        self.addButton(btn)
        self.addButton(btn2)
        self.addButton(btn3)
        self.addButton(btn4)
        self.addButton(btn5)
        self.addButton(btn6)
        self.arrangeButtons()

    def clearButtons(self):
        for button in self.buttons:
            button.kill()

        self.buttons = []

    def addButton(self, button):
        if button is not None:
            self.buttons.append(button)
            self.add(button)

    def arrangeButtons(self):
        num_buttons = len(self.buttons)
        if num_buttons == 0:
            return

        from board import Board
        size = director.get_window_size()
        width = size[0]
        height = size[1]

        total_width = 0
        for button in self.buttons:
            total_width += button.width

        button_x = (width // 2) - (total_width // 2)
        button_y = Board.TILE_SIZE // 2
        for button in self.buttons:
            button.x = button_x
            button.y = button_y

            button_x += button.width

    def getButtonAt(self, x, y):
        for button in self.buttons:
            if button.is_at(x, y):
                return button

        return None

    def doSomething(self, unit=None, cell_pos=None):
        print(str(len(self.buttons)) + " do something with " + str(unit) + " to cell " + str(cell_pos))

    def doSomethingElse(self, unit=None, cell_pos=None):
        print(str(len(self.buttons)) + " do something else " + str(unit) + " to cell " + str(cell_pos))

    def updatePlayerUnitStats(self, battle_unit):
        if self.unit_display is not None:
            self.unit_display.kill()

        if battle_unit is None:
            # Hide player unit stats at bottom left
            self.unit_display = None
            return

        from board import Board
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

        from board import Board

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.target_display = UnitCard(target_unit, is_friendly=is_friendly, reverse=True)
        self.target_display.position = width - self.target_display.width - Board.TILE_SIZE // 2, \
                                       height - self.target_display.height - Board.TILE_SIZE // 2
        self.add(self.target_display)
