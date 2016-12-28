import os
import pygame
import pyglet

from random import randint
from pixelmek.ai.bot import Bot
from pixelmek.misc import resources
from pixelmek.model.battle import *
from pixelmek.ui import actions, events, menu
from pixelmek.ui.board import *

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
Settings.init(DATA_DIR)

mech_list = Resources.get_units()

# director must be initialized before any cocos elements can be created
display_width = Settings.get_resolution_width()
display_height = Settings.get_resolution_height()
director.init(width=display_width, height=display_height, resizable=True, autoscale=False)
director.show_FPS = True

# initialize the audio mixer
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(32)

# preload all sound and image resources
resources.Resources.preload()


# setup custom mouse cursor
cursor = pyglet.window.ImageMouseCursor(resources.Resources.mouse_pointer, 1, 17)
director.window.set_mouse_cursor(cursor)

# set up test players
player = Player("Player", team=0)
bot = Bot("Enemy", team=1)

battle = Battle(player)
map_model = Map()
battle.setMap(map_model)

board = Board(battle)
key_events = events.KeyboardEvents(board)
mouse_events = events.MouseEvents(board)

battle.addPlayer(bot)

# TODO: use menu system to determine which mechs the players get
player_mechs = 'Commando', 'Firestarter', 'Jenner', 'Centurion', \
               'Hunchback', 'Archer', 'Rifleman', 'Warhammer', \
               'Marauder', 'Awesome', 'Atlas', 'King Crab'

bot_mechs = 'Hankyu (Arctic Cheetah)', 'Puma (Adder)', 'Shadow Cat', \
            'Black Hawk (Nova)', 'Ryoken (Stormcrow)', 'Thor (Summoner)', 'Mad Cat (Timber Wolf)', \
            'Masakari (Warhawk)', 'Gladiator (Executioner)', 'Daishi (Dire Wolf)',


def get_mech_by_name(mech_name):
    for mech in mech_list:
        if mech.name == mech_name:
            return mech

    return None


for mech_name in player_mechs:
    mech = get_mech_by_name(mech_name)

    if mech is not None:
        actions.add_unit_for_player(mech, player)

for mech_name in bot_mechs:
    mech = get_mech_by_name(mech_name)

    if mech is not None:
        actions.add_unit_for_player(mech, bot)

scroller = cocos.layer.ScrollingManager()
scroller.add(board, z=0)
scroller.add(key_events, z=-1)
scroller.add(mouse_events, z=1)

board.setScroller(scroller)

scene = cocos.scene.Scene(menu.MainMenu(scroller))

director.run(scene)
