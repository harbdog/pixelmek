import cocos
import pyglet
from cocos.director import director
from cocos.menu import *
from cocos.scenes import *

import actions
import settings
import battleselect
from interface import Interface


class MainMenu(Menu):
    BATTLE_SCENE = None
    SCROLLER = None

    def __init__(self, scroller):
        super(MainMenu, self).__init__("PixelMek")

        MainMenu.SCROLLER = scroller

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        menus = []

        battle_item = MenuItem('Battle', self.on_battle)
        menus.append(battle_item)

        settings_item = MenuItem('Settings', self.on_settings)
        menus.append(settings_item)

        exit_item = MenuItem('Exit', self.do_exit)
        menus.append(exit_item)

        self.create_menu(menus)

    @staticmethod
    def start_battle():
        starting = actions.initGame()
        if starting:
            MainMenu.BATTLE_SCENE = cocos.scene.Scene()
            MainMenu.BATTLE_SCENE.add(MainMenu.SCROLLER)
            MainMenu.BATTLE_SCENE.add(Interface.UI)
            director.replace(ZoomTransition(MainMenu.BATTLE_SCENE, duration=0.5))

            actions.nextTurn()
            actions.setActionReady(True)

        elif MainMenu.BATTLE_SCENE is not None:
            director.replace(ZoomTransition(MainMenu.BATTLE_SCENE, duration=0.5))

    def on_battle(self):
        if MainMenu.BATTLE_SCENE is not None:
            director.push(ZoomTransition(MainMenu.BATTLE_SCENE, duration=0.5))

        else:
            print("Battle Selection...")
            scene = cocos.scene.Scene()
            scene.add(battleselect.BattleSelectionMenu())
            director.push(FlipX3DTransition(scene, duration=0.5))

    def on_settings(self):
        print("Settings...")
        scene = cocos.scene.Scene()
        scene.add(settings.SettingsMenu())
        director.push(FlipX3DTransition(scene, duration=0.5))

    def do_exit(self):
        print("Quitter!")
        pyglet.app.exit()

    def on_quit(self):
        print("Back to the game if it's on...")
        if self.BATTLE_SCENE is not None:
            director.push(ZoomTransition(self.BATTLE_SCENE, duration=0.5))
