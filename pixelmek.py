import os
import pygame
import pyglet
import sys

from pixelmek.ai.bot import Bot
from pixelmek.misc import resources
from pixelmek.model.battle import *
from pixelmek.ui import actions, events, menu
from pixelmek.ui.board import *


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)

        logfile = os.path.expanduser('~/.pixelmek.log')
        sys.stdout = sys.stderr = open(logfile, 'w')
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


DATA_DIR = find_data_file('data')
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

# randomize the starting units based on a target total PV
player_units = Resources.generate_random_unit_deck(12, 'is', target_pv=350, variance=0.05)

bot_units = Resources.generate_random_unit_deck(10, 'cl', target_pv=350, variance=0.05)

for unit in player_units:
    actions.add_unit_for_player(unit, player)

for unit in bot_units:
    actions.add_unit_for_player(unit, bot)

scroller = cocos.layer.ScrollingManager()
scroller.add(board, z=0)
scroller.add(key_events, z=-1)
scroller.add(mouse_events, z=1)

board.setScroller(scroller)

scene = cocos.scene.Scene(menu.MainMenu(scroller))

director.run(scene)
