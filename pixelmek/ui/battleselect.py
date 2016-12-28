import cocos
import actions
import unitselect

from cocos.director import director
from cocos.menu import *
from cocos.scenes import *
from menuitem import LoopingMultipleMenuItem
from pixelmek.model.battle import Battle
from interface import Interface


class BattleSelectionMenu(Menu):

    TECH_MAP = {'Inner Sphere': 'is',
                'Clan': 'cl'}

    def __init__(self):
        super(BattleSelectionMenu, self).__init__("Battle Selection")

        print("loading battle selection menu")

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        menus = []

        self.teams = self.TECH_MAP.keys()

        # Select player team (IS/Clan)
        self.player = Battle.BATTLE.player_one
        self.player_tech = 'Inner Sphere'
        player_team = self.teams.index(self.player_tech)
        player_team_item = LoopingMultipleMenuItem('Player Tech: ', self.on_player_tech,
                                                   self.teams, default_item=player_team)
        menus.append(player_team_item)

        # Select player units
        unit_select_item = MenuItem('Player Units', self.on_player_unit_select)
        menus.append(unit_select_item)

        # Select enemy team (IS/Clan)
        self.enemy = Battle.BATTLE.player_list[1]
        self.enemy_tech = 'Clan'
        enemy_team = self.teams.index(self.enemy_tech)
        enemy_team_item = LoopingMultipleMenuItem('Enemy Tech: ', self.on_enemy_tech,
                                                  self.teams, default_item=enemy_team)
        menus.append(enemy_team_item)

        # Select enemy units
        unit_select_item = MenuItem('Enemy Units', self.on_enemy_unit_select)
        menus.append(unit_select_item)

        combat_item = MenuItem('Enter Combat', self.on_combat)
        menus.append(combat_item)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_player_tech(self, index):
        print('Player: ' + str(self.teams[index]))
        self.player_tech = self.teams[index]

    def on_player_unit_select(self):
        print("Player Unit Selection...")
        scene = cocos.scene.Scene()
        scene.add(unitselect.PlayerUnitsMenu(player=self.player, tech=self.TECH_MAP.get(self.player_tech)))
        director.push(FlipX3DTransition(scene, duration=0.5))

    def on_enemy_tech(self, index):
        print('Enemy: ' + str(self.teams[index]))
        self.enemy_tech = self.teams[index]

    def on_enemy_unit_select(self):
        print("Enemy Unit Selection...")
        scene = cocos.scene.Scene()
        scene.add(unitselect.PlayerUnitsMenu(player=self.enemy, tech=self.TECH_MAP.get(self.enemy_tech)))
        director.push(FlipX3DTransition(scene, duration=0.5))

    def on_combat(self):
        from menu import MainMenu

        MainMenu.start_battle()

    def on_quit(self):
        print("Back to the main menu...")
        director.pop()
