from __future__ import division

import gl
import random
import cocos
import pyglet
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.particle import Color
from cocos.particle_systems import Meteor, Galaxy
from cocos.euclid import Point2
from pyglet.window import mouse

from math import atan2, degrees, pi


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
            self.battle.nextTurn()

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
        if buttons & mouse.RIGHT:
            for weaponMap in turn_unit.mech.weapons:
                for weapon in weaponMap.iterkeys():
                    weapon_data = weaponMap[weapon]

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

                        action = Delay(0.5) + MoveTo((real_x, real_y), duration=ppc_t) \
                            + CallFunc(impact_ppc, ppc) \
                            + Delay(0.5) + CallFunc(ppc.kill)

                        ppc.do(action)

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

                    elif weapon.isBallistic():
                        # fire test ballistic projectile
                        ballistic_img = pyglet.resource.image("images/weapons/ballistic.png")

                        num_ballistic = weapon.get_projectiles()

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

                            action = Delay(i * 0.1) + ToggleVisibility() + MoveTo((target_x, target_y), ballistic_t) \
                                + CallFunc(create_ballistic_impact, self.battle.board, target_pos) \
                                + CallFunc(ballistic.kill)
                            ballistic.do(action)

                            self.battle.board.add(ballistic, z=1000+i)

                    elif weapon.isMissile():
                        # fire test missile projectile
                        missile_img = pyglet.resource.image("images/weapons/missile.png")

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

                            action = Delay(i * 0.05) + ToggleVisibility() + MoveTo((target_x, target_y), missile_t) \
                                + CallFunc(create_missile_impact, self.battle.board, target_pos) \
                                + CallFunc(missile.kill)
                            missile.do(action)

                            self.battle.board.add(missile, z=1000 + i)

        elif buttons & mouse.LEFT:
            # test movement to the specific cell
            # chk_colnum = turn_unit.col
            # chk_rownum = turn_unit.row - 1
            chk_cell = self.battle.board.layer_to_board(real_x, real_y)
            chk_colnum = chk_cell[0]
            chk_rownum = chk_cell[1]

            if self.battle.isCellAvailable(chk_colnum, chk_rownum):
                turn_unit.col = chk_colnum
                turn_unit.row = chk_rownum

                turn_unit.sprite.strut()
                turn_unit.sprite.moveToCell(chk_colnum, chk_rownum, turn_unit.sprite.sulk)


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


def create_ballistic_impact(board, pos):
    # give ballistics an impact effect
    ballistic_impact = BallisticImpact(pos)
    ballistic_impact.scale = 0.25
    ballistic_impact.rotation = random.randint(0, 360)
    board.add(ballistic_impact, z=1000)


def random_offset(max_offset=12):
    return random.randint(-max_offset, max_offset)
