import cocos
import pyglet

from cocos.director import director
from cocos.sprite import Sprite
from resources import Resources

from PIL import Image


class Interface(cocos.layer.Layer):

    UI = None

    def __init__(self):
        super(Interface, self).__init__()

        Interface.UI = self

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        test1 = Sprite(Resources.friendly_indicator_img)
        test1.position = 0 + test1.width//2, 0 + test1.height//2

        test2 = Sprite(Resources.friendly_indicator_img)
        test2.position = width - test1.width // 2, 0 + test1.height // 2

        test3 = Sprite(Resources.friendly_indicator_img)
        test3.position = 0 + test1.width // 2, height - test1.height // 2

        test4 = Sprite(Resources.friendly_indicator_img)
        test4.position = width - test1.width // 2, height - test1.height // 2

        self.add(test1)
        self.add(test2)
        self.add(test3)
        self.add(test4)

        mech_img_grid = pyglet.image.ImageGrid(pyglet.resource.image("images/mechs/adder.png"), 1, 6)
        mech_img_static = mech_img_grid[0]
        pitch = -(mech_img_static.width * len('RGBA'))
        img_data = mech_img_static.get_image_data()

        # testing with masking only a portion of the image
        damage_height = int(mech_img_static.height * 0.67)
        data = img_data.get_region(0, 0, mech_img_static.width, damage_height).get_data('RGBA', pitch)

        mask = Image.frombytes('RGBA', (mech_img_static.width, damage_height), data)
        # the first image is the color that the stamp will be
        img1 = Image.new("RGBA", mask.size, color=(0, 0, 0, 255))
        # second image is the background
        img2 = Image.new("RGBA", mask.size, color=(255, 50, 50, 100))
        img1 = img1.convert("RGBA")

        # apply mask to background image
        img = Image.composite(img1, img2, mask)

        raw_image = img.tobytes()
        img_x = mask.size[0]
        img_y = mask.size[1]
        pyg_img = pyglet.image.ImageData(img_x, img_y, 'RGBA', raw_image, pitch=-img_x * len('RGBA'))

        test_m = Sprite(pyg_img)
        test_m.position = width // 2, height // 2

        self.add(test_m)
