import cocos
import pygame
import pyglet
import battle

from board import Board
from cocos.actions import *
from cocos.batch import BatchNode
from cocos.sprite import Sprite
from resources import Resources


class MechSprite(cocos.layer.Layer):

    shadow_img = pyglet.resource.image("images/ui/shadows.png")
    shadow_img_grid = pyglet.image.ImageGrid(shadow_img, 1, 4)

    def __init__(self, battle_mech):
        super(MechSprite, self).__init__()

        self.battle_mech = battle_mech

        mech_img = pyglet.resource.image(self.battle_mech.getImagePath())
        mech_img_grid = pyglet.image.ImageGrid(mech_img, 1, 6)

        # TODO: add unit to model board by position, then keep updated as it moves
        # board[aws_col, aws_row] = self.batch

        self.static = True

        img_static = Sprite(mech_img_grid[0])

        indicator = cocos.layer.ColorLayer(0, 250, 0, 150, width=Board.TILE_SIZE, height=Board.TILE_SIZE)
        indicator.visible = False
        indicator.position = (self.battle_mech.col * Board.TILE_SIZE), (self.battle_mech.row * Board.TILE_SIZE)
        self.indicator = indicator

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

        # batches do not allow different positions within, so separate the shadow from the mech images
        self.node = BatchNode()
        self.add(self.node, z=1)

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

    def timeBySize(self):
        times = {
            4: 0.25,
            3: 0.22,
            2: 0.19,
            1: 0.16
        }
        return times.get(self.battle_mech.getSize(), times[4])

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
        new_z = (Board.numRows - self.battle_mech.row) * 10

        parent = self.parent
        parent.remove(self.indicator)
        parent.remove(self.shadow)
        parent.remove(self)
        parent.add(self.indicator, z=new_z)
        parent.add(self.shadow, z=new_z+1)
        parent.add(self, z=new_z+2)

        # make smaller mechs move faster
        time = self.timeBySize()

        shift = MoveBy((0, 2), duration=time)
        self.img_la.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
        self.img_ra.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))

        sink = MoveBy((0, -2), duration=time)
        self.img_ct.do(Repeat(Delay(time * 2) + sink + Reverse(sink)))

        # scroller.set_focus(self.x, self.y)

    def reset(self):
        for section in self.node.get_children():
            section.stop()
            section.position = 0, Board.TILE_SIZE//4

    def stop(self):
        self.shadow.stop()

        for section in self.node.get_children():
            section.stop()
            section.position = 0, Board.TILE_SIZE//4

        if not self.static:
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

    def moveBy(self, x, y, func):
        time = self.timeBySize() * 6

        actions = MoveBy((x, y), duration=time)
        if func is not None:
            actions += CallFunc(func)

        self.do(actions)
        self.shadow.do(actions)

    def moveToCell(self, col, row, func):
        time = self.timeBySize() * 6

        self.indicator.visible = False
        self.indicator.position = (col * 32), (row * 32)
        indicator_action = Delay(time) + ToggleVisibility()
        self.indicator.do(indicator_action)

        shadow_rect = self.shadow.get_rect()
        shadow_rect.bottomleft = (col * 32), (row * 32)

        rect = self.img_static.get_rect()
        rect.bottomleft = (col * Board.TILE_SIZE) - (self.img_static.width // 2 - self.shadow.width // 2), \
                          (row * Board.TILE_SIZE)

        actions = MoveTo(rect.center, duration=time)
        if func is not None:
            actions += CallFunc(func)

        self.do(actions)

        shadow_action = MoveTo(shadow_rect.center, duration=time)
        self.shadow.do(shadow_action)

        # play movement sounds
        sound_index = self.battle_mech.getSize() - 1

        stomp_sound = Resources.stomp_sounds[sound_index]
        sound_action = Delay(0)
        for i in range(3):
            # use channel 0 and 1 for alternating steps
            stomp_channel = pygame.mixer.Channel(i % 2)
            sound_action += CallFunc(stomp_channel.play, stomp_sound) + Delay(time / 3)

        self.do(sound_action)
