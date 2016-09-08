import events
import include
import menu
import model
import os
import pygame
import sprites

from battle import *
from board import *
from cocos.director import director
from random import randint

from resources import Resources

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
director.init(width=1024, height=768, resizable=True, autoscale=False)
director.show_FPS = True

# initialize the audio mixer
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(32)

# preload all sound and image resources
Resources.preload()

board = Board()
battle = Battle()
battle.setBoard(board)
key_events = events.KeyboardEvents(battle)
mouse_events = events.MouseEvents(battle)

# set up test players
player = Player("Human", team=0)
bot = Player("Bot", team=1, is_bot=True)

battle.addPlayer(player)
battle.addPlayer(bot)

for mech in mech_list:
    owner = player
    if mech.isClan():
        # TODO: use menu system to determine which mechs the players get
        owner = bot

    # fill out the test board with mechs
    side_col = 1
    row = 0
    if owner is bot:
        side_col = battle.getNumCols() - 2

    rand_col = randint(-1, 1)
    col = side_col + rand_col
    row = randint(0, battle.getNumRows())

    while not battle.isCellAvailable(col, row):
        rand_col = randint(-1, 1)
        col = side_col + rand_col
        row = randint(0, battle.getNumRows()-1)

    battle_mech = BattleMech(owner, mech, col, row)
    battle.addUnit(battle_mech)

    sprite = sprites.MechSprite(battle_mech)
    battle_mech.setSprite(sprite)
    # Z order is based on the number of rows in the board
    sprite_z = (battle.getNumRows() - row) * 10
    board.add(sprite.shadow, z=sprite_z)
    board.add(sprite, z=sprite_z+1)

scroller = cocos.layer.ScrollingManager()
scroller.add(board, z=0)
scroller.add(key_events, z=-1)
scroller.add(mouse_events, z=1)

battle.setScroller(scroller)

scene = cocos.scene.Scene(menu.MainMenu(scroller))

director.run(scene)
