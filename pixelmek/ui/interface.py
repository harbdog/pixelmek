import cocos
import actions
from cocos.director import director

from pixelmek.misc.resources import Resources
from widgets import UnitCard
from widgets import Button


class Interface(cocos.layer.Layer):

    UI = None

    def __init__(self):
        super(Interface, self).__init__()
        from board import Board
        Interface.UI = self

        self.buttons = []

        self.unit_display = None
        self.target_display = None

        # add clickable UI buttons
        size = director.get_window_size()
        width = size[0]
        height = size[1]
        self.move_btn = Button(icon=Resources.move_button_img, action=actions.selectMoveAction,
                        width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.evade_btn = Button(icon=Resources.evade_button_img, action=actions.selectEvadeAction,
                        width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.sprint_btn = Button(icon=Resources.sprint_button_img, action=actions.selectSprintAction,
                          width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.weapon_btn = Button(icon=Resources.weapon_button_img, action=actions.selectWeaponAction,
                          width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.overheat_btn = Button(icon=Resources.overheat_button_img, action=actions.selectOverheatAction,
                            width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.end_btn = Button(icon=Resources.end_button_img, action=actions.selectEndAction,
                       width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.addButton(self.move_btn)
        self.addButton(self.evade_btn)
        self.addButton(self.sprint_btn)
        self.addButton(self.weapon_btn)
        self.addButton(self.overheat_btn)
        self.addButton(self.end_btn)

        self.arrangeButtons()

    def clearButtons(self):
        for button in self.buttons:
            button.kill()

        self.buttons = []

    def addButton(self, button):
        if button is not None:
            self.buttons.append(button)
            self.add(button)

    def deselectAllButtons(self):
        for button in self.buttons:
            button.set_selected(False)
            button.draw_border()

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
        button_y = 0
        for button in self.buttons:
            button.x = button_x
            button.y = button_y + button.border_width // 2

            button_x += button.width + button.border_width

    def getButtonAt(self, x, y):
        for button in self.buttons:
            if button.is_at(x, y):
                return button

        return None

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
