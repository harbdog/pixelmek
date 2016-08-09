import cocos
import battle
import pyglet

from cocos.actions import *
from cocos.batch import BatchNode
from cocos.sprite import Sprite


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

        aws_static = Sprite(mech_img_grid[0])
        self.aws_static = aws_static

        shadow = Sprite(MechSprite.shadow_img_grid[battle_mech.getSize() - 1])
        indicator_rect = shadow.get_rect()
        indicator_rect.bottomleft = (self.battle_mech.col * 32), (self.battle_mech.row * 32) - shadow.height//4
        shadow.position = indicator_rect.center
        self.shadow = shadow

        rect = aws_static.get_rect()
        rect.bottomleft = (self.battle_mech.col * 32) - (aws_static.width//2 - shadow.width//2), (self.battle_mech.row * 32)
        self.position = rect.center

        # batches do not allow different positions within, so separate the shadow from the mech images
        self.node = BatchNode()
        self.add(self.node, z=1)

        z = 1

        aws_ct = Sprite(mech_img_grid[1])
        aws_ct.y = 4
        self.node.add(aws_ct, z=z)
        self.aws_ct = aws_ct
        z += 1

        aws_ll = Sprite(mech_img_grid[4])
        aws_ll.y = 4
        self.node.add(aws_ll, z=z)
        self.aws_ll = aws_ll
        z += 1

        aws_rl = Sprite(mech_img_grid[5])
        aws_rl.y = 4
        self.node.add(aws_rl, z=z)
        self.aws_rl = aws_rl
        z += 1

        aws_la = Sprite(mech_img_grid[2])
        aws_la.y = 4
        self.node.add(aws_la, z=z)
        self.aws_la = aws_la
        z += 1

        aws_ra = Sprite(mech_img_grid[3])
        aws_ra.y = 4
        self.node.add(aws_ra, z=z)
        self.aws_ra = aws_ra
        z += 1

    def timeBySize(self):
        times = {
            4: 0.25,
            3: 0.22,
            2: 0.19,
            1: 0.16
        }
        return times.get(self.battle_mech.getSize(), times[4])

    def strut(self, reverse=False):
        self.stop()

        # make smaller mechs move faster
        time = self.timeBySize()

        shift = MoveBy((0, 3), duration=time)
        move = MoveBy((0, -4), duration=time)

        if reverse:
            # start with raising the left leg/right arm first
            self.aws_ra.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
            self.aws_la.do(Repeat(Reverse(shift) + shift + shift + Reverse(shift)))

            self.aws_rl.do(Repeat(Delay(time * 2) + Reverse(move) + move))
            self.aws_ll.do(Repeat(Reverse(move) + move + Delay(time * 2)))

        else:
            # start with raising the right leg/left arm first
            self.aws_la.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
            self.aws_ra.do(Repeat(Reverse(shift) + shift + shift + Reverse(shift)))

            self.aws_ll.do(Repeat(Delay(time * 2) + Reverse(move) + move))
            self.aws_rl.do(Repeat(Reverse(move) + move + Delay(time * 2)))

        rise = MoveBy((0, 2), duration=time)
        self.aws_ct.do(Repeat(rise + Reverse(rise) + rise + Reverse(rise)))

    def sulk(self):
        self.stop()

        # TODO: adjust Z order only AFTER a Y position move
        # TODO: Z order should be based on the number of rows in the board
        new_z = 10 - self.battle_mech.row

        parent = self.parent
        parent.remove(self.shadow)
        parent.remove(self)
        parent.add(self.shadow, z=new_z)
        parent.add(self, z=new_z)

        # make smaller mechs move faster
        time = self.timeBySize()

        shift = MoveBy((0, 2), duration=time)
        self.aws_la.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))
        self.aws_ra.do(Repeat(shift + Reverse(shift) + Reverse(shift) + shift))

        sink = MoveBy((0, -2), duration=time)
        self.aws_ct.do(Repeat(Delay(time * 2) + sink + Reverse(sink)))

        # scroller.set_focus(self.x, self.y)

    def stop(self):
        self.shadow.stop()

        for section in self.node.get_children():
            section.stop()
            section.position = 0, 4

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

        shadow_rect = self.shadow.get_rect()
        shadow_rect.bottomleft = (col * 32), (row * 32) - self.shadow.height // 4

        rect = self.aws_static.get_rect()
        rect.bottomleft = (col * 32) - (self.aws_static.width // 2 - self.shadow.width // 2), (row * 32)

        actions = MoveTo(rect.center, duration=time)
        if func is not None:
            actions += CallFunc(func)

        self.do(actions)

        shadow_action = MoveTo(shadow_rect.center, duration=time)
        self.shadow.do(shadow_action)
