import cocos
from cocos.batch import BatchNode
from cocos.director import director
from cocos.sprite import Sprite

from pixelmek.misc.resources import Resources
from pixelmek.ui import actions
from pixelmek.ui.floaters import TextFloater
from pixelmek.ui.gl import SingleLine
from pixelmek.ui.widgets import Button, TextButton, UnitCard


class Interface(cocos.layer.Layer):

    UI = None

    ACTION = "ACTION"
    ACTION_MOVE = "MOVE"
    ACTION_EVADE = "EVADE"
    ACTION_SPRINT = "SPRINT"
    ACTION_FIRE = "FIRE"
    ACTION_OVR = "OVR"
    ACTION_END = "END"

    ACTION_LIST_MOVES = [ACTION_MOVE, ACTION_EVADE, ACTION_SPRINT]
    ACTION_LIST_ATTACKS = [ACTION_FIRE, ACTION_OVR]

    SUB_MOVE = "MV"
    SUB_EVADE = "EVA"
    SUB_SPRINT = "SPR"
    SUB_FIRE = "ATK"
    SUB_OVR = "OVR"
    SUB_END = "END TURN"

    def __init__(self):
        super(Interface, self).__init__()
        from board import Board
        Interface.UI = self

        self.action_btn = None

        self.action_btn_bg = BatchNode()
        action_bg = Sprite(Resources.action_buttons_bg_img)
        self.action_btn_bg.add(action_bg)
        self.action_btn_bg.width = action_bg.width
        self.action_btn_bg.height = action_bg.height
        self.action_btn_bg.visible = False
        self.add(self.action_btn_bg, z=-1)

        self.action_super_label = TextFloater("<super>", font_name='TranscendsGames',
                                          font_size=16, anchor_x='center', anchor_y='bottom')
        self.action_super_icon = Sprite(Resources.enemy_indicator_img)
        self.action_super_icon.scale = 0.75
        self.action_sub_label = TextFloater("<sub>", font_name='TranscendsGames',
                                          font_size=14, anchor_x='center', anchor_y='top')
        self.action_super_label.visible = False
        self.action_super_icon.visible = False
        self.action_sub_label.visible = False
        self.add(self.action_super_label)
        self.add(self.action_super_icon)
        self.add(self.action_sub_label)

        self.buttons = []
        self.button_action_labels = {}
        self.button_action = {}

        self.unit_display = None
        self.unit_display_bg = None

        self.target_display = None
        self.target_display_bg = None

        # used to retain the labels that show the to hit % over each enemy
        self.to_hit_labels = {}

        # used to retain the lines that show LOS to each enemy
        self.los_lines = []

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
        # self.addButton(self.evade_btn, actions.doEvadeAction)
        # self.addButton(self.sprint_btn, actions.doSprintAction)
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

            from board import Board
            battle = Board.BOARD.battle
            turn_unit = battle.getTurnUnit()
            sel_cell_pos = battle.getSelectedCellPosition()

            return button.do_action(**{'unit': turn_unit, 'cell_pos': sel_cell_pos})

        return button

    def getSelectedButton(self):
        for button in self.buttons:
            if button.selected:
                return button

        return None

    def deselectAllButtons(self, hide_action=True):
        if hide_action and self.action_btn is not None:
            self.action_btn.visible = False
            self.action_btn_bg.visible = False
            self.action_super_label.visible = False
            self.action_super_icon.visible = False
            self.action_sub_label.visible = False

        if self.action_btn is not None:
            self.action_btn.set_selected(False)

        for button in self.buttons:
            button.clearVars()
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
        action_label = selected_button.action_label
        action_call = self.button_action[action_label]
        action_text = self.button_action_labels[action_label]
        action_font_size = 2 * Board.TILE_SIZE // 3
        self.action_btn = TextButton(text=action_text, font_size=action_font_size,
                                     action_label=Interface.ACTION, icon=None, action=action_call,
                                     width=4 + len(action_text) * 3 * action_font_size // 4, height=4 + Board.TILE_SIZE)
        self.action_btn.visible = True
        self.action_btn_bg.visible = True
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
            total_width += button.width + button.border_width // 2

        button_x = (width // 2) - (total_width // 2)
        button_y = 0
        for button in self.buttons:
            button.x = button_x
            button.y = button_y + button.border_width // 2

            button_x += button.width + button.border_width

        self.action_btn_bg.x = (width // 2)
        self.action_btn_bg.y = self.action_btn_bg.height // 2

        if self.action_btn is not None:
            self.action_btn.x = (width // 2) - (self.action_btn.width // 2)
            self.action_btn.y = button_y + Board.TILE_SIZE * 2

            self.action_super_icon.x = (width // 2)
            self.action_super_icon.y = self.action_btn.y + self.action_btn.height \
                                       + self.action_super_icon.height // 2 + 2

            self.action_super_label.x = (width // 2)
            self.action_super_label.y = self.action_super_icon.y + self.action_super_icon.height // 2

            self.action_sub_label.x = (width // 2)
            self.action_sub_label.y = self.action_btn.y - 2

    def setButtonsVisible(self, visible):
        if self.action_btn is not None and self.getSelectedButton() is not None:
            self.action_super_label.visible = visible
            self.action_super_icon.visible = visible
            self.action_btn.visible = visible
            self.action_btn_bg.visible = visible
            self.action_sub_label.visible = visible

        for button in self.buttons:
            button.visible = visible

    def getButtonAt(self, x, y):
        if self.action_btn is not None and self.action_btn.is_at(x, y):
            return self.action_btn

        for button in self.buttons:
            if button.is_at(x, y):
                return button

        return None

    def setActionButtonEnabled(self, enabled):
        self.action_btn.set_enabled(enabled)

    def updateActionSubLabelText(self, text):
        if text is None:
            self.action_sub_label.visible = False

        else:
            size = director.get_window_size()
            width = size[0]
            height = size[1]

            self.action_sub_label.visible = True
            self.action_sub_label.set_text(text)

            self.action_sub_label.x = (width // 2)
            self.action_sub_label.y = self.action_btn.y - 2

    def updateActionSuperLabelText(self, text):
        if text is None:
            self.action_super_icon.visible = False
            self.action_super_label.visible = False

        else:
            size = director.get_window_size()
            width = size[0]
            height = size[1]

            self.action_super_icon.visible = True
            self.action_super_label.visible = True
            self.action_super_label.set_text(text)

            self.action_super_icon.x = (width // 2)
            self.action_super_icon.y = self.action_btn.y + self.action_btn.height \
                                       + self.action_super_icon.height // 2 + 2

            self.action_super_label.x = (width // 2)
            self.action_super_label.y = self.action_super_icon.y + self.action_super_icon.height // 2

    def setUnitStatsIndicatorsVisible(self, visible, except_units=None):
        from board import Board

        if except_units is None:
            except_units = []

        for battle_unit in Board.BOARD.battle.unit_list:
            if battle_unit.isDestroyed() or battle_unit in except_units:
                continue

            battle_unit.sprite.setStatsIndicatorsVisible(visible)

    def updatePlayerUnitStats(self, battle_unit):
        if self.unit_display is not None:
            self.unit_display.kill()
            self.unit_display_bg.kill()

        if battle_unit is None:
            # Hide player unit stats at bottom left
            self.unit_display = None
            self.unit_display_bg = None
            return

        from board import Board
        # size = director.get_window_size()
        # width = size[0]
        # height = size[1]

        self.unit_display = UnitCard(battle_unit)
        self.unit_display.position = Board.TILE_SIZE // 2, Board.TILE_SIZE
        self.add(self.unit_display)

        self.unit_display_bg = BatchNode()
        bg_sprite = Sprite(Resources.unit_card_bg_left_img)
        self.unit_display_bg.add(bg_sprite)
        bg_position = self.unit_display.sprite.get_rect().topleft
        self.unit_display_bg.position = bg_position[0] + bg_sprite.width // 2, bg_position[1]
        self.add(self.unit_display_bg, z=-1)

    def updateTargetUnitStats(self, target_unit, is_friendly=False):
        if self.target_display is not None:
            self.target_display.kill()
            self.target_display_bg.kill()

        if target_unit is None:
            # Hide target unit stats at top right
            self.target_display = None
            self.target_display_bg = None
            return

        from board import Board

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.target_display = UnitCard(target_unit, is_friendly=is_friendly, reverse=True)
        self.target_display.position = width - self.target_display.width - Board.TILE_SIZE // 2, \
                                       height - self.target_display.height - Board.TILE_SIZE // 2
        self.add(self.target_display)

        self.target_display_bg = BatchNode()
        bg_sprite = Sprite(Resources.unit_card_bg_right_img)
        self.target_display_bg.add(bg_sprite)
        self.target_display_bg.position = width - bg_sprite.width // 2, \
                                          height - bg_sprite.height // 2 - Board.TILE_SIZE // 2
        self.add(self.target_display_bg, z=-1)

    def clearToHitLabels(self):
        for battle_unit in self.to_hit_labels:
            self.to_hit_labels[battle_unit].kill()

        self.to_hit_labels.clear()

        # also clear LOS lines that tend to go with them
        self.clearLosLines()

    def updateToHitLabels(self):
        from board import Board
        board = Board.BOARD
        battle = board.battle

        self.clearToHitLabels()
        self.clearLosLines()

        if battle.isBotTurn():
            return

        turn_unit = battle.getTurnUnit()
        if turn_unit is None or turn_unit.isShutdown():
            return

        enemy_units = battle.getEnemyUnits(turn_unit)
        for enemy in enemy_units:
            if enemy.isDestroyed():
                continue

            to_hit = battle.getToHit(turn_unit, enemy)

            if to_hit > 0:
                to_hit_text = '{:>3}'.format(str(to_hit) + "%")
                to_hit_label = TextFloater(to_hit_text, font_name='TranscendsGames',
                                                 font_size=14, anchor_x='center', anchor_y='bottom')
                to_hit_label.x = enemy.sprite.x + Board.TILE_SIZE // 4
                to_hit_label.y = enemy.sprite.y + enemy.sprite.height // 2 + Board.TILE_SIZE // 2

                self.to_hit_labels[enemy] = to_hit_label
                board.add(to_hit_label, z=9000)

                # draw LOS line indicator to target
                self.drawLosLine(turn_unit.getPosition(), enemy.getPosition())

    def clearLosLines(self):
        for los_line in self.los_lines:
            los_line.kill()

        self.los_lines = []

    def drawLosLine(self, source_coords, target_coords, width=2, alpha=0.8):
        from board import Board
        board = Board.BOARD

        source_x, source_y = Board.board_to_layer(*source_coords)
        target_x, target_y = Board.board_to_layer(*target_coords)

        cell_offset = Board.TILE_SIZE // 2

        los_line = SingleLine((source_x + cell_offset, source_y + cell_offset),
                              (target_x + cell_offset, target_y + cell_offset),
                               width=width, color=(255, 50, 50, int(255 * alpha)))

        board.add(los_line, z=10000)
        self.los_lines.append(los_line)

    def generateLosLinesFrom(self, source_unit, source_coords=None):
        from board import Board
        board = Board.BOARD
        battle = board.battle

        self.clearLosLines()

        if source_unit is None:
            return

        if source_coords is None:
            source_coords = source_unit.getPosition()

        enemy_units = battle.getEnemyUnits(source_unit)
        for enemy in enemy_units:
            if enemy.isDestroyed():
                continue

            target_coords = enemy.getPosition()
            if battle.hasTargetLOS(source_coords, target_coords):
                # draw LOS line indicator to target
                self.drawLosLine(source_coords, target_coords)

    def generateTargetLosLine(self, source_unit, target_unit):
        from board import Board
        board = Board.BOARD
        battle = board.battle

        self.clearLosLines()

        if source_unit is None:
            return

        source_coords = source_unit.getPosition()

        enemy_units = battle.getEnemyUnits(source_unit)
        for enemy in enemy_units:
            if enemy.isDestroyed():
                continue

            target_coords = enemy.getPosition()
            if battle.hasTargetLOS(source_coords, target_coords):
                # draw LOS line indicator brightest to current target
                line_alpha = 1.0 if enemy is target_unit else 0.3
                line_width = 3 if enemy is target_unit else 2
                self.drawLosLine(source_coords, target_coords, width=line_width, alpha=line_alpha)
