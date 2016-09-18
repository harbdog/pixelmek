import cocos
import pyglet
import floaters

from cocos.batch import BatchNode
from cocos.director import director
from cocos.sprite import Sprite
from resources import Resources
from PIL import Image


class Interface(cocos.layer.Layer):

    UI = None

    def __init__(self):
        super(Interface, self).__init__()

        Interface.UI = self

        self.unit_stats = None
        self.unit_name = None

        self.target_stats = None
        self.target_name = None

        # size = director.get_window_size()
        # width = size[0]
        # height = size[1]
        #
        # test1 = Sprite(Resources.friendly_indicator_img)
        # test1.position = 0 + test1.width//2, 0 + test1.height//2
        #
        # test2 = Sprite(Resources.friendly_indicator_img)
        # test2.position = width - test1.width // 2, 0 + test1.height // 2
        #
        # test3 = Sprite(Resources.friendly_indicator_img)
        # test3.position = 0 + test1.width // 2, height - test1.height // 2
        #
        # test4 = Sprite(Resources.friendly_indicator_img)
        # test4.position = width - test1.width // 2, height - test1.height // 2
        #
        # self.add(test1)
        # self.add(test2)
        # self.add(test3)
        # self.add(test4)

    def updatePlayerUnitStats(self, battle_unit):
        if self.unit_stats is not None:
            self.unit_stats.kill()
            self.unit_name.kill()

        if battle_unit is None:
            # Hide player unit stats at bottom left
            self.unit_stats = None
            self.unit_name = None
            return

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.unit_stats = BatchNode()
        self.unit_stats.position = 0,0

        mech_img_grid = pyglet.image.ImageGrid(pyglet.resource.image(battle_unit.getImagePath()), 1, 6)
        mech_img_static = mech_img_grid[0]
        pitch = -(mech_img_static.width * len('RGBA'))
        img_data = mech_img_static.get_image_data()

        # testing with masking only a portion of the image
        damage_height = int(mech_img_static.height)  # int(mech_img_static.height * 0.67)
        data = img_data.get_region(0, 0, mech_img_static.width, damage_height).get_data('RGBA', pitch)

        mask = Image.frombytes('RGBA', (mech_img_static.width, damage_height), data)
        # the first image is the color that the stamp will be
        img1 = Image.new("RGBA", mask.size, color=(0, 0, 0, 255))
        # second image is the background
        img2 = Image.new("RGBA", mask.size, color=(225, 225, 225, 200))
        img1 = img1.convert("RGBA")

        # apply mask to background image
        img = Image.composite(img1, img2, mask)

        raw_image = img.tobytes()
        img_x = mask.size[0]
        img_y = mask.size[1]
        pyg_img = pyglet.image.ImageData(img_x, img_y, 'RGBA', raw_image, pitch=-img_x * len('RGBA'))

        mech_sprite = Sprite(pyg_img)
        mech_sprite.position = 0 + mech_sprite.width // 2, 0 + mech_sprite.height // 2  # width // 2, height // 2

        self.unit_stats.add(mech_sprite)
        self.add(self.unit_stats)

        # Show unit name above the image
        self.unit_name = floaters.TextFloater(battle_unit.getName(), anchor_x='left', anchor_y='bottom')
        self.unit_name.position = 0, 0 + mech_sprite.height

        self.add(self.unit_name)

    def updateTargetUnitStats(self, target_unit, is_friendly=False):
        if self.target_stats is not None:
            self.target_stats.kill()
            self.target_name.kill()

        if target_unit is None:
            # Hide player unit stats at bottom left
            self.target_stats = None
            self.target_name = None
            return

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.target_stats = BatchNode()
        self.target_stats.position = 0,0

        mech_img_grid = pyglet.image.ImageGrid(pyglet.resource.image(target_unit.getImagePath()), 1, 6)
        mech_img_static = mech_img_grid[0]
        pitch = -(mech_img_static.width * len('RGBA'))
        img_data = mech_img_static.get_image_data()

        # testing with masking only a portion of the image
        damage_height = int(mech_img_static.height)  # int(mech_img_static.height * 0.67)
        data = img_data.get_region(0, 0, mech_img_static.width, damage_height).get_data('RGBA', pitch)

        mask = Image.frombytes('RGBA', (mech_img_static.width, damage_height), data)
        # the first image is the color that the stamp will be
        img1 = Image.new("RGBA", mask.size, color=(0, 0, 0, 255))
        # second image is the background
        bg_color = (200, 75, 75, 200)
        if is_friendly:
            bg_color = (225, 225, 225, 200)
        img2 = Image.new("RGBA", mask.size, color=bg_color)
        img1 = img1.convert("RGBA")

        # apply mask to background image
        img = Image.composite(img1, img2, mask)

        raw_image = img.tobytes()
        img_x = mask.size[0]
        img_y = mask.size[1]
        pyg_img = pyglet.image.ImageData(img_x, img_y, 'RGBA', raw_image, pitch=-img_x * len('RGBA'))

        mech_sprite = Sprite(pyg_img)
        mech_sprite.position = width - mech_sprite.width // 2, 0 + mech_sprite.height // 2

        self.target_stats.add(mech_sprite)
        self.add(self.target_stats)

        # Show target name above the image
        self.target_name = floaters.TextFloater(target_unit.getName(), anchor_x='right', anchor_y='bottom')
        self.target_name.position = width, 0 + mech_sprite.height

        self.add(self.target_name)