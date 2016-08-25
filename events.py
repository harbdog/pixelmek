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
from pyglet.window import mouse
from math import atan2, degrees, pi

from resources import Resources


class KeyboardEvents(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self, battle):
        super(KeyboardEvents, self).__init__()

        # keep track of battle objects being controlled by events
        self.battle = battle

        # To keep track of which keys are pressed:
        self.keys_pressed = set()

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """

        char = pyglet.window.key.symbol_string(key)
        self.keys_pressed.add(char)

        mech = self.battle.getTurnUnit()

        if char == "P":
            mech.sprite.pause()

        elif char == "SPACE":
            # skip to next unit for testing purposes
            prev_unit = self.battle.getTurnUnit()
            prev_unit.sprite.stop()
            prev_unit.sprite.indicator.visible = False

            self.battle.nextTurn()

            next_unit = self.battle.getTurnUnit()
            next_unit.sprite.sulk()
            next_unit.sprite.indicator.visible = True

        elif char == "W":
            mech.sprite.strut()

        elif char == "S":
            mech.sprite.sulk()

        elif char == "LEFT":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col - 1
            chk_rownum = turn_unit.row

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut(reverse=True)
                mech.sprite.moveBy(-32, 0, mech.sprite.sulk)

        elif char == "RIGHT":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col + 1
            chk_rownum = turn_unit.row

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut()
                mech.sprite.moveBy(32, 0, mech.sprite.sulk)

        elif char == "UP":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col
            chk_rownum = turn_unit.row + 1

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut(reverse=True)
                mech.sprite.moveBy(0, 32, mech.sprite.sulk)

        elif char == "DOWN":
            # check for legal move first
            turn_unit = self.battle.getTurnUnit()
            chk_colnum = turn_unit.col
            chk_rownum = turn_unit.row - 1

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                mech.sprite.strut()
                mech.sprite.moveBy(0, -32, mech.sprite.sulk)

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        char = pyglet.window.key.symbol_string(key)
        if char in self.keys_pressed:
            self.keys_pressed.remove(char)

        mech = self.battle.getTurnUnit()

        if char == "P":
            mech.sprite.resume()


class MouseEvents(cocos.layer.ScrollableLayer):

    is_event_handler = True     #: enable director.window events

    def __init__(self, battle):
        super(MouseEvents, self).__init__()

        self.battle = battle

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves over the app window with no button pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        """
        # self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        # self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        real_x, real_y = self.battle.scroller.screen_to_world(x, y)

        turn_unit = self.battle.getTurnUnit()
        src_cell = turn_unit.col, turn_unit.row

        dest_cell = Board.layer_to_board(real_x, real_y)
        target_unit = self.battle.getUnitAtCell(*dest_cell)

        if buttons & mouse.RIGHT:
            if target_unit is None:
                return

            # minimum travel time to target used to determine when to show the damage floater
            min_travel_time = None

            # cell distance used to determine which range of weapons will fire
            cell_distance = Battle.getCellDistance(src_cell, dest_cell)
            target_range = Battle.getDistanceRange(cell_distance)
            print(target_range + ": " + str(src_cell) + " -> " + str(dest_cell) + " = " + str(cell_distance))

            # determine actual target point based on the target unit sprite size
            target_sprite = target_unit.getSprite()
            real_x = (dest_cell[0] * Board.TILE_SIZE) + Board.TILE_SIZE//2
            real_y = (dest_cell[1] * Board.TILE_SIZE) + (2*target_sprite.get_height()//3)

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
                        self.battle.board.add(ppc, z=1000)

                        target_x = real_x + random_offset()
                        target_y = real_y + random_offset()
                        target_pos = target_x, target_y

                        # figure out the duration based on speed and distance
                        ppc_speed = weapon.get_speed()     # pixels per second
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
                        if min_travel_time is None or min_travel_time > travel_time:
                            min_travel_time = travel_time

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
                        self.battle.board.add(flamer, z=1000)

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
                        if min_travel_time is None or min_travel_time > travel_time:
                            min_travel_time = travel_time

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
                        self.battle.board.add(node, z=1000)

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
                        laser_charge.start_color = Color(weapon_color[0]/255, weapon_color[1]/255, weapon_color[2]/255, 1.0)
                        laser_charge.end_color = Color(weapon_color[0]/255, weapon_color[1]/255, weapon_color[2]/255, 1.0)
                        node.add(laser_charge, z=0)

                        laser_drift = random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)

                        las_action = Delay(0.5) + ToggleVisibility() \
                            + CallFunc(create_laser_impact, self.battle.board, target_pos, laser_drift, las_life) \
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
                        if min_travel_time is None or min_travel_time > travel_time:
                            min_travel_time = travel_time

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
                                + CallFunc(impact_func, weapon, self.battle.board, target_pos) \
                                + CallFunc(ballistic.kill)

                            if weapon.isGauss():
                                # give gauss sound a bit more time to stop
                                action += Delay(cannon_sound.get_length())

                            if i == num_ballistic - 1:
                                # stop the sound channel after the last projectile only
                                action += CallFunc(weapon_channel.stop)

                            ballistic.do(action)

                            self.battle.board.add(ballistic, z=1000+i)

                            travel_time = (i * 0.1) + ballistic_t
                            if min_travel_time is None or min_travel_time > travel_time:
                                min_travel_time = travel_time

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
                                + CallFunc(create_missile_impact, self.battle.board, target_pos) \
                                + CallFunc(missile.kill) \
                                + CallFunc(explosion_channel.play, explosion_sound) \
                                + Delay(0.5)

                            if i == num_missile - 1:
                                # stop the sound channels after the last missile only
                                action += CallFunc(weapon_channel.stop) + CallFunc(explosion_channel.stop)

                            missile.do(action)

                            self.battle.board.add(missile, z=1000 + i)

                            travel_time = (i * 0.05) + missile_t
                            if min_travel_time is None or min_travel_time > travel_time:
                                min_travel_time = travel_time

            if min_travel_time is not None:
                # scroll focus over to the target area halfway through the travel time
                target_area = Board.board_to_layer(target_unit.col, target_unit.row)

                # show damage floater after the travel time of the first projectile to hit
                floater = floaters.TextFloater("%s" % getattr(turn_unit, target_range))
                floater.visible = False
                floater.position = real_x, real_y + target_sprite.get_height()//3
                self.battle.board.add(floater, z=2000)

                action = Delay(min_travel_time/2) + CallFunc(self.battle.scroller.set_focus, *target_area) \
                    + Delay(min_travel_time/2) + ToggleVisibility() \
                    + Delay(0.25) + MoveBy((0, Board.TILE_SIZE), 1.0) \
                    + FadeOut(1.0) + CallFunc(floater.kill)
                floater.do(action)

        elif buttons & mouse.LEFT:
            # test movement to the specific cell
            chk_cell = self.battle.board.layer_to_board(real_x, real_y)
            chk_col = chk_cell[0]
            chk_row = chk_cell[1]

            if self.battle.isCellAvailable(chk_col, chk_row):
                animate_reverse = (turn_unit.col - chk_col > 0) or (turn_unit.row - chk_row > 0)

                turn_unit.sprite.strut(reverse=animate_reverse)
                turn_unit.sprite.moveToCell(chk_col, chk_row, animate_reverse, turn_unit.sprite.sulk)


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


def random_offset(max_offset=12):
    return random.randint(-max_offset, max_offset)
