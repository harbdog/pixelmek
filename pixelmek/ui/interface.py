import cocos
import actions
from cocos.director import director

from pixelmek.misc.resources import Resources
from widgets import UnitCard
from widgets import Button, TextButton


class Interface(cocos.layer.Layer):

    UI = None

    ACTION = "ACTION"
    ACTION_MOVE = "MOVE"
    ACTION_EVADE = "EVADE"
    ACTION_SPRINT = "SPRINT"
    ACTION_FIRE = "FIRE"
    ACTION_OVR = "OVR FIRE"
    ACTION_END = "END"

    ACTION_LIST_MOVES = [ACTION_MOVE, ACTION_EVADE, ACTION_SPRINT]
    ACTION_LIST_ATTACKS = [ACTION_FIRE, ACTION_OVR]

    def __init__(self):
        super(Interface, self).__init__()
        from board import Board
        Interface.UI = self

        self.action_btn = None
        self.buttons = []
        self.button_action_labels = {}
        self.button_action = {}

        self.unit_display = None
        self.target_display = None

        # add clickable UI button bar
        self.move_btn = Button(action_label=Interface.ACTION_MOVE,
                               icon=Resources.move_button_img, action=actions.selectMoveAction,
                               width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.evade_btn = Button(action_label=Interface.ACTION_EVADE,
                                icon=Resources.evade_button_img, action=actions.selectEvadeAction,
                                width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.sprint_btn = Button(action_label=Interface.ACTION_SPRINT,
                                 icon=Resources.sprint_button_img, action=actions.selectSprintAction,
                                 width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.weapon_btn = Button(action_label=Interface.ACTION_FIRE,
                                 icon=Resources.weapon_button_img, action=actions.selectWeaponAction,
                                 width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.overheat_btn = Button(action_label=Interface.ACTION_OVR,
                                   icon=Resources.overheat_button_img, action=actions.selectOverheatAction,
                                   width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.end_btn = Button(action_label=Interface.ACTION_END,
                              icon=Resources.end_button_img, action=actions.selectEndAction,
                              width=4 + Board.TILE_SIZE, height=4 + Board.TILE_SIZE)

        self.addButton(self.move_btn, actions.doMoveAction)
        self.addButton(self.evade_btn, actions.doEvadeAction)
        self.addButton(self.sprint_btn, actions.doSprintAction)
        self.addButton(self.weapon_btn, actions.doWeaponAction)
        self.addButton(self.overheat_btn, actions.doOverheatAction)
        self.addButton(self.end_btn, actions.doEndAction)

        self.arrangeButtons()

    def isActionButton(self, button):
        return button is self.action_btn

    def clearButtons(self):
        for button in self.buttons:
            button.kill()

        self.buttons = []

    def addButton(self, button, action_call):
        if button is not None:
            self.buttons.append(button)
            self.add(button)

            before_txt = "/// "
            after_txt = " \\\\\\"
            self.button_action_labels[button.action_label] = before_txt + button.action_label + after_txt
            self.button_action[button.action_label] = action_call

    def getButtonByActionLabel(self, action_label):
        for button in self.buttons:
            if button.action_label == action_label:
                return button

        return None

    def selectButtonByActionLabel(self, action_label):
        button = self.getButtonByActionLabel(action_label)
        if button is not None:
            button.set_selected(True)

        return button

    def getSelectedButton(self):
        for button in self.buttons:
            if button.selected:
                return button

        return None

    def deselectAllButtons(self, hide_action=True):
        if hide_action and self.action_btn is not None:
            self.action_btn.visible = False

        for button in self.buttons:
            button.set_selected(False)
            button.draw_border()

    def buttonSelected(self, selected_button):
        if selected_button is self.action_btn:
            selected_button.selected = True
            selected_button.update_selected()
            return

        from board import Board

        if self.action_btn is not None:
            self.action_btn.kill()

        # a button has been selected, add an action button with the appropriate text
        action_call = self.button_action[selected_button.action_label]
        action_text = self.button_action_labels[selected_button.action_label]
        action_font_size = 2 * Board.TILE_SIZE // 3
        self.action_btn = TextButton(text=action_text, font_size=action_font_size, action_label=Interface.ACTION,
                                     icon=None, action=action_call,
                                     width=4 + len(action_text) * 3 * action_font_size // 4, height=4 + Board.TILE_SIZE)
        self.action_btn.visible = True
        self.add(self.action_btn)

        self.arrangeButtons()

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

        if self.action_btn is not None:
            self.action_btn.x = (width // 2) - (self.action_btn.width // 2)
            self.action_btn.y = button_y + Board.TILE_SIZE * 2

    def getButtonAt(self, x, y):
        if self.action_btn is not None and self.action_btn.is_at(x, y):
            return self.action_btn

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
