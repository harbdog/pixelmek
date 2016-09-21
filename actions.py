from __future__ import division

import gl
import random
import cocos
import floaters
import pyglet
import pygame
from battle import Battle
from board import Board
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.particle import Color
from cocos.particle_systems import Meteor, Galaxy, Fire
from cocos.euclid import Point2
from math import atan2, degrees, pi

from resources import Resources
from ui import Interface


class Actions(object):
    # indicator for when an action can be performed or waiting on animation
    action_ready = False


def isActionReady():
    return Actions.action_ready


def setActionReady(is_ready):
    Actions.action_ready = is_ready


def actOnCell(battle, col, row):
    if not isActionReady():
        return

    # perform an action based on the given cell and/or its occupants
    turn_unit = battle.getTurnUnit()
    turn_player = turn_unit.getPlayer()

    if turn_unit is None:
        # TODO: make sure it is a player unit's turn or do something else
        return

    cell = battle.getCellAt(col, row)
    if cell is None:
        return

    # if the cell is not already selected, select it instead
    sel_pos = battle.getSelectedCellPosition()
    if sel_pos is None or col != sel_pos[0] or row != sel_pos[1]:
        moveSelectionTo(battle, col, row)
        return

    cell_unit = battle.getUnitAtCell(col, row)

    if col == turn_unit.col and row == turn_unit.row:
        setActionReady(False)

        # TODO: ask confirmation to end the turn without firing
        print("Skipping remainder of the turn!")

        battle.nextTurn()

        setActionReady(True)

    elif battle.isCellAvailable(col, row) and cell.range_to_display > 0:
        setActionReady(False)

        turn_unit.move -= cell.range_to_display

        for cell in battle.board.cellMap.itervalues():
            cell.remove_indicators()

        animate_reverse = (turn_unit.col - col > 0) or (turn_unit.row - row > 0)

        def _ready_next_move():
            turn_unit.sprite.sulk()
            for chk_cell in battle.board.cellMap.itervalues():
                chk_cell.remove_indicators()

            battle.showRangeIndicators()
            battle.showUnitIndicators()

            battle.setSelectedCellPosition(turn_unit.col, turn_unit.row)

            turn_cell_pos = Board.board_to_layer(turn_unit.col, turn_unit.row)
            if turn_cell_pos is not None:
                turn_cell_pos = turn_cell_pos[0] + Board.TILE_SIZE//2, turn_cell_pos[1] + Board.TILE_SIZE//2

            battle.scroller.set_focus(*turn_cell_pos)

            setActionReady(True)

        turn_unit.sprite.strut(reverse=animate_reverse)
        turn_unit.sprite.moveToCell(col, row, animate_reverse, _ready_next_move)

    elif Battle.isFriendlyUnit(turn_player, cell_unit):
        # TODO: interact with friendly unit somehow, like swap cells with it if it has move remaining?
        print("Friendly: " + str(cell_unit))

    elif cell_unit is not None \
            and not cell_unit.isDestroyed() \
            and cell_unit is not turn_unit:
        setActionReady(False)

        print("Enemy: " + str(cell_unit))

        battle.showUnitIndicators(visible=False)
        for chk_cell in battle.board.cellMap.itervalues():
            chk_cell.remove_indicators()

        attack_time = performAttackOnUnit(battle, cell_unit)

        def _ready_next_turn():
            setActionReady(False)
            battle.nextTurn()
            setActionReady(True)

        # start the next turn when the attack is completed
        battle.board.do(Delay(attack_time) + CallFunc(_ready_next_turn))


def moveSelectionTo(battle, col, row):
    # move selection to the given cell
    battle.setSelectedCellPosition(col, row)


def moveSelectionBy(battle, col_amt, row_amt):
    # move selection cell by given amount
    cell_pos = battle.getSelectedCellPosition()
    if cell_pos is None:
        return

    battle.setSelectedCellPosition(cell_pos[0] + col_amt, cell_pos[1] + row_amt)


def performAttackOnUnit(battle, target_unit):
    # perform an attack on the given target BattleUnit
    turn_unit = battle.getTurnUnit()
    if turn_unit is None or target_unit is None\
            or turn_unit.isDestroyed() or target_unit.isDestroyed():
        # TODO: make sure it is a player unit's turn
        return 0

    src_cell = turn_unit.col, turn_unit.row
    dest_cell = target_unit.col, target_unit.row

    # minimum travel time to target used to determine when to show the damage floater
    min_travel_time = 0
    # maximum travel time to target used to determine when all animations are finished
    max_travel_time = 0

    # cell distance used to determine which range of weapons will fire
    cell_distance = Battle.getCellDistance(src_cell, dest_cell)
    target_range = Battle.getDistanceRange(cell_distance)
    print(target_range + ": " + str(src_cell) + " -> " + str(dest_cell) + " = " + str(cell_distance))

    # TODO: introduce dynamic damage (optional?)
    attack_damage = int(getattr(turn_unit, target_range))

    # apply damage to model before animating
    attack_remainder = target_unit.applyDamage(attack_damage)

    # determine actual target point based on the target unit sprite size
    target_sprite = target_unit.getSprite()
    real_x = (dest_cell[0] * Board.TILE_SIZE) + Board.TILE_SIZE // 2
    real_y = (dest_cell[1] * Board.TILE_SIZE) + (2 * target_sprite.get_height() // 3)

    for weaponMap in turn_unit.mech.weapons:
        for weapon in weaponMap.iterkeys():

            if not weapon.inRange(cell_distance):
                continue

            weapon_data = weaponMap[weapon]

            # get sound channel to use just for this weapon
            weapon_channel = pygame.mixer.find_channel()
            if weapon_channel is None:
                weapon_channel = pygame.mixer.Channel(0)

            weapon_offset = weapon_data.get('offset', [0, 0])
            weapon_x = turn_unit.sprite.position[0] + weapon_offset[0]
            weapon_y = turn_unit.sprite.position[1] + weapon_offset[1]

            weapon_color = weapon.get_color()

            if weapon.isPPC():
                # fire test ppcs
                ppc = Meteor()
                ppc.size = 10
                ppc.speed = 20
                ppc.gravity = Point2(0, 0)
                # TODO: offer decreased particle emission rate to improve performance
                ppc.emission_rate = 100
                ppc.life = 0.5
                ppc.life_var = 0.1

                ppc.position = weapon_x, weapon_y
                battle.board.add(ppc, z=1000)

                target_x = real_x + random_offset()
                target_y = real_y + random_offset()
                target_pos = target_x, target_y

                # figure out the duration based on speed and distance
                ppc_speed = weapon.get_speed()  # pixels per second
                distance = Point2(ppc.x, ppc.y).distance(Point2(target_x, target_y))
                ppc_t = distance / ppc_speed

                ppc_sound = Resources.ppc_sound
                weapon_channel.play(ppc_sound)

                action = Delay(0.5) + MoveTo((target_x, target_y), duration=ppc_t) \
                         + CallFunc(impact_ppc, ppc) \
                         + Delay(0.5) + CallFunc(ppc.kill) \
                         + Delay(ppc_sound.get_length()) \
                         + CallFunc(weapon_channel.stop)

                ppc.do(action)

                travel_time = 0.5 + ppc_t
                if min_travel_time == 0 or min_travel_time > travel_time:
                    min_travel_time = travel_time

                if travel_time > max_travel_time:
                    max_travel_time = travel_time

            elif weapon.isFlamer():
                # fire test flamer
                flamer = Fire()

                flamer.size = 25
                flamer.speed = 300
                flamer.gravity = Point2(0, 0)
                # TODO: offer decreased particle emission rate to improve performance
                flamer.emission_rate = 100

                dx = real_x - weapon_x
                dy = real_y - weapon_y
                rads = atan2(-dy, dx)
                rads %= 2 * pi
                angle = degrees(rads) + 90

                flamer.rotation = angle
                flamer.angle_var = 5
                flamer.pos_var = Point2(5, 5)

                flamer.position = weapon_x, weapon_y
                battle.board.add(flamer, z=1000)

                target_x = real_x + random_offset()
                target_y = real_y + random_offset()
                target_pos = target_x, target_y

                # figure out the duration based on speed and distance
                flamer_speed = weapon.get_speed()  # pixels per second
                distance = Point2(flamer.x, flamer.y).distance(Point2(target_x, target_y))
                flamer_t = 1

                flamer.life = distance / flamer_speed
                flamer.life_var = 0

                flamer_sound = Resources.flamer_sound
                weapon_channel.play(flamer_sound)

                action = Delay(flamer_t) \
                         + CallFunc(impact_flamer, flamer) \
                         + CallFunc(weapon_channel.fadeout, 750) \
                         + Delay(flamer_t) + CallFunc(flamer.kill) \
                         + CallFunc(weapon_channel.stop)

                flamer.do(action)

                travel_time = flamer_t
                if min_travel_time == 0 or min_travel_time > travel_time:
                    min_travel_time = travel_time

                if travel_time > max_travel_time:
                    max_travel_time = travel_time

            elif weapon.isLaser():
                # fire test laser
                las_life = 1.0
                las_size = (1, 1, 1)
                if weapon.isShort():
                    las_size = (2, 1, 0.5)
                    las_life = 0.5
                elif weapon.isMedium():
                    las_size = (3, 2, 1)
                    las_life = 0.75
                elif weapon.isLong():
                    las_size = (6, 4, 2)
                    las_life = 1.0

                target_x = real_x + random_offset()
                target_y = real_y + random_offset()
                target_pos = target_x, target_y

                las_outer = gl.SingleLine((weapon_x, weapon_y), (target_x, target_y),
                                          width=las_size[0],
                                          color=(weapon_color[0], weapon_color[1], weapon_color[2], 50))
                las_middle = gl.SingleLine((weapon_x, weapon_y), (target_x, target_y),
                                           width=las_size[1],
                                           color=(weapon_color[0], weapon_color[1], weapon_color[2], 125))
                las_inner = gl.SingleLine((weapon_x, weapon_y), (target_x, target_y),
                                          width=las_size[2],
                                          color=(weapon_color[0], weapon_color[1], weapon_color[2], 200))

                las_outer.visible = False
                las_middle.visible = False
                las_inner.visible = False

                node = cocos.layer.Layer()
                node.add(las_outer, z=1)
                node.add(las_middle, z=2)
                node.add(las_inner, z=3)
                battle.board.add(node, z=1000)

                # give lasers a small particle pre-fire effect
                laser_charge = Galaxy()
                laser_charge.angle = 270
                laser_charge.angle_var = 180
                laser_charge.position = weapon_x, weapon_y
                laser_charge.size = 10
                laser_charge.size_var = 5
                laser_charge.emission_rate = 15
                laser_charge.life = 0.5
                laser_charge.speed = 0
                laser_charge.speed_var = 0
                laser_charge.start_color = Color(weapon_color[0] / 255, weapon_color[1] / 255, weapon_color[2] / 255,
                                                 1.0)
                laser_charge.end_color = Color(weapon_color[0] / 255, weapon_color[1] / 255, weapon_color[2] / 255, 1.0)
                node.add(laser_charge, z=0)

                laser_drift = random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)

                las_action = Delay(0.5) + ToggleVisibility() \
                             + CallFunc(create_laser_impact, battle.board, target_pos, laser_drift, las_life) \
                             + gl.LineDriftBy(laser_drift, las_life) \
                             + CallFunc(laser_charge.stop_system) + CallFunc(node.kill)
                las_outer.do(las_action)
                las_middle.do(las_action)
                las_inner.do(las_action)

                las_sound = Resources.las_sound
                weapon_channel.play(las_sound)
                las_duration_ms = int(las_action.duration * 1000)
                weapon_channel.fadeout(las_duration_ms)

                travel_time = 0.5
                if min_travel_time == 0 or min_travel_time > travel_time:
                    min_travel_time = travel_time

                if travel_time > max_travel_time:
                    max_travel_time = travel_time

            elif weapon.isBallistic():
                # fire test ballistic projectile
                num_ballistic = weapon.get_projectiles()

                if weapon.isGauss():
                    ballistic_img = Resources.gauss_img
                elif weapon.isLBX():
                    # LBX fires only one projectile, but will appear to have multiple random impacts
                    num_ballistic = 1
                    ballistic_img = Resources.buckshot_img
                else:
                    ballistic_img = Resources.ballistic_img

                # machine gun sound only plays once instead of per projectile
                cannon_sound = None
                if weapon.isMG():
                    cannon_sound = Resources.machinegun_sound
                elif weapon.isGauss():
                    cannon_sound = Resources.gauss_sound

                for i in range(num_ballistic):
                    ballistic = Sprite(ballistic_img)
                    ballistic.visible = False
                    ballistic.position = weapon_x, weapon_y
                    ballistic.scale = weapon.get_scale()
                    ballistic.anchor = 0, 0

                    dx = real_x - weapon_x
                    dy = real_y - weapon_y
                    rads = atan2(-dy, dx)
                    rads %= 2 * pi
                    angle = degrees(rads)

                    ballistic.rotation = angle

                    target_x = real_x + random_offset()
                    target_y = real_y + random_offset()
                    target_pos = target_x, target_y

                    # figure out the duration based on speed and distance
                    ballistic_speed = weapon.get_speed()  # pixels per second
                    distance = Point2(weapon_x, weapon_y).distance(Point2(target_x, target_y))
                    ballistic_t = distance / ballistic_speed

                    # setup the firing sound
                    if cannon_sound is None:
                        cannon_sound = Resources.cannon_sound

                    impact_func = create_ballistic_impact
                    if weapon.isLBX():
                        impact_func = create_lbx_impact

                    action = Delay(i * 0.1) + ToggleVisibility() \
                             + CallFunc(weapon_channel.play, cannon_sound) \
                             + MoveTo((target_x, target_y), ballistic_t) \
                             + CallFunc(impact_func, weapon, battle.board, target_pos) \
                             + CallFunc(ballistic.kill)

                    if weapon.isGauss():
                        # give gauss sound a bit more time to stop
                        action += Delay(cannon_sound.get_length())

                    if i == num_ballistic - 1:
                        # stop the sound channel after the last projectile only
                        action += CallFunc(weapon_channel.stop)

                    ballistic.do(action)

                    battle.board.add(ballistic, z=1000 + i)

                    travel_time = (i * 0.1) + ballistic_t
                    if min_travel_time == 0 or min_travel_time > travel_time:
                        min_travel_time = travel_time

                    if travel_time > max_travel_time:
                        max_travel_time = travel_time

            elif weapon.isMissile():
                # get another sound channel to use just for the explosions
                explosion_channel = pygame.mixer.find_channel()
                if explosion_channel is None:
                    explosion_channel = pygame.mixer.Channel(1)

                # fire test missile projectile
                missile_img = Resources.missile_img

                num_missile = weapon_data.get('count', 1)

                num_per_row = 1
                if weapon.isLRM():
                    num_per_row = 5
                elif weapon.isSRM():
                    num_per_row = 2

                for i in range(num_missile):

                    tube_x = i % num_per_row
                    tube_y = i // num_per_row

                    missile = Sprite(missile_img)
                    missile.visible = False
                    missile.position = weapon_x + tube_x, weapon_y + tube_y
                    missile.scale = weapon.get_scale()
                    missile.anchor = 0, 0

                    dx = real_x - weapon_x
                    dy = real_y - weapon_y
                    rads = atan2(-dy, dx)
                    rads %= 2 * pi
                    angle = degrees(rads)

                    missile.rotation = angle

                    target_x = real_x + random_offset()
                    target_y = real_y + random_offset()
                    target_pos = target_x, target_y

                    # figure out the duration based on speed and distance
                    missile_speed = weapon.get_speed()  # pixels per second
                    distance = Point2(weapon_x, weapon_y).distance(Point2(target_x, target_y))
                    missile_t = distance / missile_speed

                    rand_missile_sound = random.randint(0, 7)
                    missile_sound = Resources.missile_sounds[rand_missile_sound]

                    explosion_sound = Resources.explosion_sound

                    action = Delay(i * 0.05) + ToggleVisibility() \
                             + CallFunc(weapon_channel.play, missile_sound) \
                             + MoveTo((target_x, target_y), missile_t) \
                             + CallFunc(create_missile_impact, battle.board, target_pos) \
                             + CallFunc(missile.kill) \
                             + CallFunc(explosion_channel.play, explosion_sound) \
                             + Delay(0.5)

                    if i == num_missile - 1:
                        # stop the sound channels after the last missile only
                        action += CallFunc(weapon_channel.stop) + CallFunc(explosion_channel.stop)

                    missile.do(action)

                    battle.board.add(missile, z=1000 + i)

                    travel_time = (i * 0.05) + missile_t
                    if min_travel_time == 0 or min_travel_time > travel_time:
                        min_travel_time = travel_time

                    if travel_time > max_travel_time:
                        max_travel_time = travel_time

    # scroll focus over to the target area halfway through the travel time
    target_area = Board.board_to_layer(target_unit.col, target_unit.row)

    # show damage floater after the travel time of the first projectile to hit
    floater = floaters.TextFloater("%i" % attack_damage)
    floater.visible = False
    floater.position = real_x, real_y + target_sprite.get_height() // 3
    battle.board.add(floater, z=2000)

    action = Delay(min_travel_time / 2) + CallFunc(battle.scroller.set_focus, *target_area) \
        + Delay(min_travel_time / 2) + ToggleVisibility() \
        + Delay(0.25) + MoveBy((0, Board.TILE_SIZE), 1.0) \
        + FadeOut(1.0) + CallFunc(floater.kill)
    floater.do(action)

    if action.duration > max_travel_time:
        max_travel_time = action.duration

    stats_action = Delay(min_travel_time) + CallFunc(target_sprite.updateStatsIndicators) \
                   + CallFunc(Interface.UI.updateTargetUnitStats, target_unit)
    target_sprite.do(stats_action)

    if attack_remainder > 0:
        print("Overkill by %i!" % attack_remainder)

    if target_unit.structure > 0:
        print("Remaining %i/%i" % (target_unit.armor, target_unit.structure))

    else:
        print("Target destroyed!")
        # show destroyed floater after the travel time of the first projectile to hit
        destroyed = floaters.TextFloater("DESTROYED")
        destroyed.visible = False
        destroyed.position = real_x, real_y + target_sprite.get_height() // 3
        battle.board.add(destroyed, z=5000)

        # get another sound channel to use just for the explosions
        explosion_channel = pygame.mixer.find_channel()
        if explosion_channel is None:
            explosion_channel = pygame.mixer.Channel(1)

        explosion_sound = Resources.explosion_multiple_sound

        action = Delay(max_travel_time) + ToggleVisibility() \
            + CallFunc(explosion_channel.play, explosion_sound) \
            + (MoveBy((0, Board.TILE_SIZE), 1.0) | CallFunc(create_destruction_explosions, battle.board, target_unit)) \
            + Delay(0.5) + CallFunc(target_sprite.destroy) + FadeOut(2.0) + CallFunc(destroyed.kill)
        destroyed.do(action)

        # give a bit of extra time to explode
        max_travel_time = action.duration

    return max_travel_time


class LaserImpact(cocos.sprite.Sprite):
    raw = pyglet.resource.image('images/weapons/explosion_01.png')
    seq = pyglet.image.ImageGrid(raw, 1, 24)
    explosion_img = pyglet.image.Animation.from_image_sequence(seq, 0.05, False)

    def __init__(self, pos):
        super(LaserImpact, self).__init__(LaserImpact.explosion_img, pos)
        self.do(Delay(0.05 * 24) + CallFunc(self.kill))


def create_laser_impact(board, pos, drift, duration):
    # give lasers an impact effect
    laser_impact = LaserImpact(pos)
    laser_impact.scale = 0.25
    board.add(laser_impact, z=1000)

    impact_action = MoveBy(drift, duration)
    laser_impact.do(impact_action)


def impact_ppc(ppc):
    ppc.speed = 50
    ppc.emission_rate *= 2
    ppc.do(Delay(0.25) + CallFunc(ppc.stop_system))


def impact_flamer(flamer):
    flamer.emission_rate *= 2
    flamer.do(Delay(0.25) + CallFunc(flamer.stop_system))


class MissileImpact(cocos.sprite.Sprite):
    raw = pyglet.resource.image('images/weapons/explosion_07.png')
    seq = pyglet.image.ImageGrid(raw, 1, 26)
    explosion_img = pyglet.image.Animation.from_image_sequence(seq, 0.05, False)

    def __init__(self, pos):
        super(MissileImpact, self).__init__(MissileImpact.explosion_img, pos)
        self.do(Delay(0.05 * 26) + CallFunc(self.kill))


def create_missile_impact(board, pos):
    # give missiles an impact effect
    missile_impact = MissileImpact(pos)
    missile_impact.scale = 0.5
    board.add(missile_impact, z=1000)


class BallisticImpact(cocos.sprite.Sprite):
    raw = pyglet.resource.image('images/weapons/flash_03.png')
    seq = pyglet.image.ImageGrid(raw, 1, 6)
    explosion_img = pyglet.image.Animation.from_image_sequence(seq, 0.07, False)

    def __init__(self, pos):
        super(BallisticImpact, self).__init__(BallisticImpact.explosion_img, pos)
        self.do(Delay(0.07 * 6) + CallFunc(self.kill))


def create_ballistic_impact(weapon, board, pos):
    # give ballistics an impact effect
    ballistic_impact = BallisticImpact(pos)
    ballistic_impact.scale = 0.5 * weapon.scale
    ballistic_impact.rotation = random.randint(0, 360)
    board.add(ballistic_impact, z=1000)


def create_lbx_impact(weapon, board, pos):
    # give lbx a special set of impact effects
    num_ballistic = weapon.get_projectiles()
    for i in range(num_ballistic):
        ballistic_impact = BallisticImpact(pos)
        ballistic_impact.x += random.randint(-8, 8)
        ballistic_impact.y += random.randint(-8, 8)
        ballistic_impact.scale = 0.5 * weapon.scale
        ballistic_impact.rotation = random.randint(0, 360)
        board.add(ballistic_impact, z=1000)


def create_destruction_explosions(board, battle_unit):
    unit_sprite = battle_unit.getSprite()
    pos = unit_sprite.position[0], unit_sprite.position[1] + (unit_sprite.height // 3)

    actions = Delay(0)

    def _add_random_explosion():
        offset_x = random.randint(-unit_sprite.width // 3, unit_sprite.width // 3)
        offset_y = random.randint(-unit_sprite.height // 4, unit_sprite.height // 4)

        rand_pos = pos[0] + offset_x, pos[1] + offset_y

        coin_flip = random.randint(0, 1)

        if coin_flip == 0:
            missile_impact = MissileImpact(rand_pos)
            missile_impact.rotation = random.randint(0, 360)
            board.add(missile_impact, z=1000)
        else:
            ballistic_impact = BallisticImpact(rand_pos)
            ballistic_impact.rotation = random.randint(0, 360)
            board.add(ballistic_impact, z=1000)

    for i in range(20):
        actions += CallFunc(_add_random_explosion) + Delay(0.1)

    board.do(actions)


def random_offset(max_offset=12):
    return random.randint(-max_offset, max_offset)
