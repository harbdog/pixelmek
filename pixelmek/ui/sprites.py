import math
import pygame
import pyglet
import random
import cocos

from cocos.actions import *
from cocos.batch import BatchNode
from cocos.euclid import Point2
from cocos.particle_systems import Meteor
from cocos.sprite import Sprite

from pixelmek.misc.resources import Resources
from pixelmek.model.battle import Battle
from pixelmek.model.map import Map
from board import Board
from settings import Settings


class MechSprite(cocos.layer.Layer):

    shadow_img = pyglet.resource.image("images/ui/shadows.png")
    shadow_img_grid = pyglet.image.ImageGrid(shadow_img, 1, 4)

    def __init__(self, battle_mech):
        super(MechSprite, self).__init__()

        self.battle_mech = battle_mech

        mech_img = pyglet.resource.image(self.battle_mech.getImagePath())
        mech_img_grid = pyglet.image.ImageGrid(mech_img, 1, 6)

        self.static = True

        img_static = Sprite(mech_img_grid[0])

        self.width = img_static.width
        self.height = img_static.height

        # TODO: setup the non square friendly/enemy indicators based on team of current player's turn
        if battle_mech.player.is_bot:
            indicator = Sprite(Resources.enemy_indicator_img)
        else:
            indicator = Sprite(Resources.friendly_indicator_img)

        indicator.visible = False
        indicator.position = 0, -img_static.height // 2 + indicator.height // 2 + 1
        self.indicator = indicator
        self.add(indicator, z=0)

        shadow = Sprite(MechSprite.shadow_img_grid[battle_mech.getSize() - 1])
        shadow_rect = shadow.get_rect()
        shadow_rect.bottomleft = (self.battle_mech.col * Board.TILE_SIZE), \
                                 (self.battle_mech.row * Board.TILE_SIZE)
        shadow.position = shadow_rect.center
        self.shadow = shadow

        rect = img_static.get_rect()
        rect.bottomleft = (self.battle_mech.col * Board.TILE_SIZE) - (img_static.width//2 - shadow.width//2), \
                          (self.battle_mech.row * Board.TILE_SIZE)
        self.position = rect.center

        self.node = BatchNode()
        self.add(self.node, z=2)

        img_static.y = Board.TILE_SIZE//4
        self.node.add(img_static)
        self.img_static = img_static

        img_ct = Sprite(mech_img_grid[1])
        img_ct.y = Board.TILE_SIZE//4
        self.img_ct = img_ct

        img_ll = Sprite(mech_img_grid[4])
        img_ll.y = Board.TILE_SIZE//4
        self.img_ll = img_ll

        img_rl = Sprite(mech_img_grid[5])
        img_rl.y = Board.TILE_SIZE//4
        self.img_rl = img_rl

        img_la = Sprite(mech_img_grid[2])
        img_la.y = Board.TILE_SIZE//4
        self.img_la = img_la

        img_ra = Sprite(mech_img_grid[3])
        img_ra.y = Board.TILE_SIZE//4
        self.img_ra = img_ra

        # testing the stats stuff
        self.stats = BatchNode()
        self.updateStatsIndicators()

    def get_width(self):
        return self.img_static.width

    def get_height(self):
        return self.img_static.height + int(self.img_static.y)

    def showIndicator(self, visible=True):
        self.indicator.visible = visible

    def showStats(self, visible=True):
        self.stats.visible = visible

    def timeBySize(self):
        times = {
            4: 0.25,
            3: 0.21,
            2: 0.17,
            1: 0.13
        }
        return times.get(self.battle_mech.getSize(), times[4])

    def destroy(self):
        # TODO: animate the destruction and show a wreckage
        self.node.kill()
        self.shadow.kill()
        self.indicator.kill()
        self.kill()

    def strut(self, reverse=False):
        self.reset()

        # make smaller mechs move faster
        time = self.timeBySize()

        shift = MoveBy((0, 3), duration=time)
        move = MoveBy((0, -4), duration=time)

        if reverse:
            # start with raising the left leg/right arm first
            self.img_ra.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
            self.img_la.do(Repeat(Reverse(shift) + shift + shift + Reverse(shift)))

            self.img_rl.do(Repeat(Delay(time * 2) + Reverse(move) + move))
            self.img_ll.do(Repeat(Reverse(move) + move + Delay(time * 2)))

        else:
            # start with raising the right leg/left arm first
            self.img_la.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
            self.img_ra.do(Repeat(Reverse(shift) + shift + shift + Reverse(shift)))

            self.img_ll.do(Repeat(Delay(time * 2) + Reverse(move) + move))
            self.img_rl.do(Repeat(Reverse(move) + move + Delay(time * 2)))

        rise = MoveBy((0, 2), duration=time)
        self.img_ct.do(Repeat(rise + Reverse(rise) + rise + Reverse(rise)))

    def sulk(self):
        if not self.static:
            self.stop()

        if self.static:
            self.static = False
            for section in self.node.get_children():
                section.kill()

            z = 1
            self.node.add(self.img_ct, z=z)
            z += 1
            self.node.add(self.img_ll, z=z)
            z += 1
            self.node.add(self.img_rl, z=z)
            z += 1
            self.node.add(self.img_la, z=z)
            z += 1
            self.node.add(self.img_ra, z=z)

        # TODO: adjust Z order only AFTER a Y position move
        # TODO: Z order should be based on the number of rows in the board
        new_z = (Map.numRows - self.battle_mech.row) * 10

        parent = self.parent

        parent.remove(self.shadow)
        parent.remove(self)

        parent.add(self.shadow, z=new_z)
        parent.add(self, z=new_z+2)

        # make smaller mechs move faster
        time = self.timeBySize()

        shift = MoveBy((0, 2), duration=time)
        self.img_la.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
        self.img_ra.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))

        sink = MoveBy((0, -2), duration=time)
        self.img_ct.do(Repeat(Delay(time * 2) + sink + Reverse(sink)))

    def shutdown(self):
        if not self.static:
            self.stop()

        if self.static:
            self.static = False
            for section in self.node.get_children():
                section.kill()

            z = 1
            self.node.add(self.img_ct, z=z)
            z += 1
            self.node.add(self.img_ll, z=z)
            z += 1
            self.node.add(self.img_rl, z=z)
            z += 1
            self.node.add(self.img_la, z=z)
            z += 1
            self.node.add(self.img_ra, z=z)

        # TODO: adjust Z order only AFTER a Y position move
        # TODO: Z order should be based on the number of rows in the board
        new_z = (Map.numRows - self.battle_mech.row) * 10

        parent = self.parent

        parent.remove(self.shadow)
        parent.remove(self)

        parent.add(self.shadow, z=new_z)
        parent.add(self, z=new_z+2)

        # make smaller mechs move faster
        time = 1.0

        shift = MoveBy((0, -8), duration=time)

        # lower the arms
        self.img_la.do(shift)
        self.img_ra.do(shift)

        # lower the torso
        lower = MoveBy((0, -4), duration=time/2)
        self.img_ct.do(lower)

    def reset(self):
        for section in self.node.get_children():
            section.stop()
            section.position = 0, Board.TILE_SIZE//4

        if self.battle_mech.isShutdown():
            # lower the arms
            self.img_la.y -= 8
            self.img_ra.y -= 8

            # lower the torso
            self.img_ct.y -= 4

    def stop(self):
        self.shadow.stop()

        for section in self.node.get_children():
            section.stop()
            section.position = 0, Board.TILE_SIZE//4

        if self.battle_mech.isShutdown():
            # lower the arms
            self.img_la.y -= 8
            self.img_ra.y -= 8

            # lower the torso
            self.img_ct.y -= 4

        elif not self.static:
            self.static = True
            for section in self.node.get_children():
                section.kill()

            self.node.add(self.img_static)

    def pause(self):
        self.shadow.pause()

        for section in self.node.get_children():
            section.pause()

    def resume(self):
        self.shadow.resume()

        for section in self.node.get_children():
            section.resume()

    def moveToCell(self, to_col, to_row, reverse=False, func=None):
        if to_col == self.battle_mech.col and to_row == self.battle_mech.row:
            return 0.5

        # determine the route and the points along the way
        to_cell = (to_col, to_row)
        cell_route = self._get_cell_move_route(to_cell)

        total_time = 0

        actions = Delay(0)
        shadow_actions = Delay(0)
        stomp_actions = Delay(0)

        for cell in cell_route:
            col = cell[0]
            row = cell[1]

            num_steps = 2
            time = self.timeBySize() * (num_steps * 2)

            shadow_rect = self.shadow.get_rect()
            shadow_rect.bottomleft = (col * 32), (row * 32)

            rect = self.img_static.get_rect()
            rect.bottomleft = (col * Board.TILE_SIZE) - (self.img_static.width // 2 - self.shadow.width // 2), \
                              (row * Board.TILE_SIZE)

            actions += MoveTo(rect.center, duration=time)
            shadow_actions += MoveTo(shadow_rect.center, duration=time)

            # play movement sounds
            sound_index = self.battle_mech.getSize() - 1
            stomp_sound = Resources.stomp_sounds[sound_index]
            for i in range(num_steps):
                # use channel 0 and 1 for alternating steps
                stomp_channel = pygame.mixer.Channel(i % 2)
                stomp_channel.set_volume(Settings.get_volume_fx())

                stomp_reverse = True
                if i % 2 == (1 if reverse else 0):
                    stomp_reverse = False

                stomp_actions += CallFunc(stomp_channel.play, stomp_sound) + Delay(time / num_steps) \
                    + CallFunc(self.spawnStompCloud, stomp_reverse)

            total_time += time

        if func is not None:
            actions += CallFunc(func)

        self.do(actions)
        self.shadow.do(shadow_actions)
        self.do(stomp_actions)

        return total_time

    def _get_cell_move_route(self, to_cell):
        battle = Battle.BATTLE
        cell_route = [to_cell]

        cells_in_range = battle.getCellsInRange(self.battle_mech.col, self.battle_mech.row, self.battle_mech.move)

        if to_cell not in cells_in_range:
            return cell_route

        # starting from the cell being moved to, find the connected cell paths that leads
        # back to the unit's current cell in as straight a path as possible
        cell_move_dist = cells_in_range[to_cell]

        self._recurse_cell_move_route(to_cell, cell_move_dist, cells_in_range, cell_route)

        return cell_route

    def _recurse_cell_move_route(self, recurse_cell, cell_move_dist, cells_in_range, cell_route):
        if cell_move_dist <= 1:
            return

        battle = Battle.BATTLE
        turn_unit = battle.getTurnUnit()
        turn_player = turn_unit.getPlayer()

        x = recurse_cell[0]
        y = recurse_cell[1]
        next_cell_dist = cell_move_dist - 1

        # get all adjacent cells in range with distance equal to the current cell_move_dist minus 1
        adjacent_cells = []
        for cell, dist in cells_in_range.items():
            if dist != next_cell_dist:
                # must be adjacent in the correct direction toward origin (0)
                continue

            cell_x = cell[0]
            cell_y = cell[1]

            if x != cell_x and y != cell_y:
                # must be either in same row or column as cell currently being looked at
                continue

            if abs(x - cell_x) != 1 and abs(y - cell_y) != 1:
                # and needs to be within one cell distance away in some direction
                continue

            # allow passing through friendly unit occupied cells
            cell_unit = battle.getUnitAt(cell_x, cell_y)
            is_friendly_occupied = False
            if cell_unit is not None:
                is_friendly_occupied = battle.isFriendlyUnit(turn_player, cell_unit)
            if battle.isCellAvailable(cell_x, cell_y) or \
                    (cell_unit is not None and is_friendly_occupied):
                adjacent_cells.append(cell)

        if len(adjacent_cells) == 0:
            # shouldn't happen...
            return

        # determine current course direction to prefer not turning if possible
        course_x = 0
        course_y = 0
        if len(cell_route) > 1:
            prev_cell = cell_route[1]
            course_x = prev_cell[0] - x
            course_y = prev_cell[1] - y

        next_cell = adjacent_cells[0]
        for cell in adjacent_cells:
            diff_x = x - cell[0]
            diff_y = y - cell[1]

            if course_x == diff_x and course_y == diff_y:
                next_cell = cell
                break

        cell_route.insert(0, next_cell)
        self._recurse_cell_move_route(next_cell, next_cell_dist, cells_in_range, cell_route)

    def spawnStompCloud(self, reverse):
        # show cloud particles from stomps
        stomp_cloud = Meteor()
        stomp_cloud.start_color = cocos.particle.Color(0.3, 0.3, 0.3, 1.0)
        stomp_cloud.end_color = cocos.particle.Color(0.5, 0.5, 0.5, 0.2)
        stomp_cloud.duration = 0.1
        stomp_cloud.blend_additive = False
        stomp_cloud.size = 10 + (10 * self.battle_mech.getSize() / 4)
        stomp_cloud.speed = 20
        stomp_cloud.gravity = Point2(0, 0)
        # TODO: offer decreased particle emission rate to improve performance
        stomp_cloud.emission_rate = 100
        stomp_cloud.life = 0.5
        stomp_cloud.life_var = 0.1

        if not reverse:
            stomp_cloud.position = self.indicator.position[0] + (self.img_static.width // 4), \
                self.indicator.position[1] - self.indicator.height // 5
        else:
            stomp_cloud.position = self.indicator.position[0] - (self.img_static.width // 4), \
                self.indicator.position[1] - self.indicator.height // 5

        self.add(stomp_cloud, z=1)

        stomp_action = Delay(stomp_cloud.duration + stomp_cloud.life + stomp_cloud.life_var) \
            + CallFunc(stomp_cloud.kill)

        self.do(stomp_action)

    def setStatsIndicatorsVisible(self, visible):
        for child in self.stats.get_children():
            child.visible = visible

    def updateStatsIndicators(self):
        # TODO: Just testing pips on the indicator, it should be put on a new UI layer on top of everything
        for child in self.stats.get_children():
            child.kill()

        pip_height = 6 - (self.indicator.height // 2)

        orig_armor = self.battle_mech.mech.armor
        for i in range(orig_armor):
            pip_img = Resources.armor_pip_img
            if i >= self.battle_mech.armor:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.position = (i * pip.width) - (orig_armor * pip.width) // 2, pip_height
            self.stats.add(pip, z=1)

        pip_height -= 4

        orig_structure = self.battle_mech.mech.structure
        for i in range(orig_structure):
            pip_img = Resources.structure_pip_img
            if i >= self.battle_mech.structure:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.position = (i * pip.width) - (orig_structure * pip.width) // 2, pip_height
            self.stats.add(pip, z=1)

        pip_height -= 4

        rand_heat = self.battle_mech.heat
        for i in range(rand_heat):
            pip = Sprite(Resources.heat_pip_img)
            pip.position = (i * pip.width) - (rand_heat * pip.width) // 2, pip_height
            self.stats.add(pip, z=1)

        self.stats.position = 0, -self.img_static.height // 2 + self.indicator.height // 2 + 1
        self.add(self.stats, z=1)
