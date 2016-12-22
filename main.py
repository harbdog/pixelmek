import os
import pygame
import pyglet
from random import randint
from pixelmek.ai.bot import Bot
from pixelmek.misc import include
from pixelmek.misc import resources
from pixelmek.model.battle import *
from pixelmek.ui import events
from pixelmek.ui import menu
from pixelmek.ui import sprites
from pixelmek.ui.board import *

Settings.init()
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

mech_list = []

for root, dirs, f_names in os.walk(DATA_DIR+'/mechs/'):
    for f_name in f_names:
        mech = include.IncludeLoader(open(os.path.join(root, f_name), 'r')).get_data()
        print("Loaded %s:" % mech.full_name())
        print("  " + str(mech))
        mech_list.append(mech)

# sort list alphabetically by name
mech_list = sorted(mech_list, key=lambda x: x.name)

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

battle = Battle()
map_model = Map()
battle.setMap(map_model)

board = Board(battle)
key_events = events.KeyboardEvents(board)
mouse_events = events.MouseEvents(board)

# set up test players
player = Player("Human", team=0)
bot = Bot("Bot", team=1)

battle.addPlayer(player)
battle.addPlayer(bot)

# TODO: use menu system to determine which mechs the players get
player_mechs = 'Archer', 'Atlas', 'Awesome', 'Centurion', \
               'Commando', 'Firestarter', 'Hunchback', 'Jenner', \
               'King Crab', 'Marauder', 'Rifleman', 'Warhammer'

bot_mechs = 'Puma (Adder)', 'Hankyu (Arctic Cheetah)', 'Daishi (Dire Wolf)', 'Gladiator (Executioner)', \
            'Black Hawk (Nova)', 'Ryoken (Stormcrow)', 'Shadow Cat', 'Thor (Summoner)', 'Mad Cat (Timber Wolf)', \
            'Masakari (Warhawk)'


def get_mech_by_name(mech_name):
    for mech in mech_list:
        if mech.name == mech_name:
            return mech

    return None


def add_mech_for_player(mech, owner):
    # fill out the test board with mechs
    side_col = 1
    if owner is bot:
        side_col = battle.getNumCols() - 2

    rand_col = randint(-1, 1)
    col = side_col + rand_col
    row = randint(0, battle.getNumRows())

    while not battle.isCellAvailable(col, row):
        rand_col = randint(-1, 1)
        col = side_col + rand_col
        row = randint(0, battle.getNumRows() - 1)

    battle_mech = BattleMech(owner, mech, col, row)
    battle.addUnit(battle_mech)

    sprite = sprites.MechSprite(battle_mech)
    battle_mech.setSprite(sprite)
    # Z order is based on the number of rows in the board
    sprite_z = (battle.getNumRows() - row) * 10
    board.add(sprite.shadow, z=sprite_z)
    board.add(sprite, z=sprite_z + 1)


for mech_name in player_mechs:
    mech = get_mech_by_name(mech_name)

    if mech is not None:
        add_mech_for_player(mech, player)

for mech_name in bot_mechs:
    mech = get_mech_by_name(mech_name)

    if mech is not None:
        add_mech_for_player(mech, bot)

# mix up the turn order
battle.updateUnitsTurnOrder()

scroller = cocos.layer.ScrollingManager()
scroller.add(board, z=0)
scroller.add(key_events, z=-1)
scroller.add(mouse_events, z=1)

board.setScroller(scroller)

scene = cocos.scene.Scene(menu.MainMenu(scroller))

director.run(scene)
