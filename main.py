import events
import include
import model
import os
import sprites

from battle import *
from board import *
from cocos.director import director
from random import randint

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
director.init(width=480, height=400, autoscale=False)
board = Board()
battle = Battle()
battle.setBoard(board)
key_events = events.KeyboardEvents(battle)
mouse_events = events.MouseEvents(battle)

for mech in mech_list:
    col = randint(0, 5)
    row = randint(0, 5)

    battle_mech = BattleMech(mech, col, row)
    battle.addUnit(battle_mech)

    sprite = sprites.MechSprite(battle_mech)
    battle_mech.setSprite(sprite)
    board.add(sprite.shadow, z=100)
    board.add(sprite, z=100)

    # TODO: only sulk during the unit's turn
    sprite.sulk()

scroller = cocos.layer.ScrollingManager()
scroller.add(board, z=0)
scroller.add(key_events, z=-1)
scroller.add(mouse_events, z=1)

battle.setScroller(scroller)

# TODO: focus on an actual unit
scroller.set_focus(150, 150)

scene = cocos.scene.Scene()
scene.add(scroller, z=1)

director.run(scene)
