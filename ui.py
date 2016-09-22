import cocos
import pyglet
import floaters
import random

from board import Board
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

        self.unit_display = None
        self.unit_name = None
        self.unit_variant = None
        self.unit_stats = None
        self.unit_values = None

        self.target_display = None
        self.target_name = None
        self.target_variant = None
        self.target_stats = None
        self.target_values = None

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
        if self.unit_display is not None:
            self.unit_display.kill()
            self.unit_name.kill()
            self.unit_variant.kill()
            self.unit_stats.kill()
            self.unit_values.kill()

        if battle_unit is None:
            # Hide player unit stats at bottom left
            self.unit_display = None
            self.unit_name = None
            self.unit_variant = None
            self.unit_stats = None
            self.unit_values = None
            return

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        self.unit_display = BatchNode()
        self.unit_display.position = 0, 0

        mech_img_grid = pyglet.image.ImageGrid(pyglet.resource.image(battle_unit.getImagePath()), 1, 6)
        mech_img_static = mech_img_grid[0]
        pitch = -(mech_img_static.width * len('RGBA'))
        img_data = mech_img_static.get_image_data()

        # testing with masking only a portion of the image
        damage_height = int(mech_img_static.height)  # int(mech_img_static.height * 0.67)
        data = img_data.get_region(0, 0, mech_img_static.width, damage_height).get_data('RGBA', pitch)

        mask = Image.frombytes('RGBA', (mech_img_static.width, damage_height), data)
        # the first image is the color that the stamp will be
        img1 = Image.new('RGBA', mask.size, color=(0, 0, 0, 255))
        # second image is the background
        img2 = Image.new('RGBA', mask.size, color=(225, 225, 225, 200))
        img1 = img1.convert('RGBA')

        # apply mask to background image
        img = Image.composite(img1, img2, mask)

        raw_image = img.tobytes()
        img_x = mask.size[0]
        img_y = mask.size[1]
        pyg_img = pyglet.image.ImageData(img_x, img_y, 'RGBA', raw_image, pitch=-img_x * len('RGBA'))

        mech_sprite = Sprite(pyg_img)
        mech_sprite.position = Board.TILE_SIZE // 2 + mech_sprite.width // 2, \
                               Board.TILE_SIZE + mech_sprite.height // 2

        self.unit_display.add(mech_sprite)
        self.add(self.unit_display)

        # Show unit name above the image
        self.unit_name = floaters.TextFloater(battle_unit.getName(), font_name='TranscendsGames',
                                              font_size=Board.TILE_SIZE // 2, anchor_x='left', anchor_y='bottom')
        self.unit_name.position = Board.TILE_SIZE // 2, mech_sprite.get_rect().topleft[1]
        self.add(self.unit_name)

        # Show unit variant below the image
        self.unit_variant = floaters.TextFloater(battle_unit.getVariant().upper(), font_name='TranscendsGames',
                                                 font_size=Board.TILE_SIZE // 3, anchor_x='left', anchor_y='top')

        self.unit_variant.position = Board.TILE_SIZE // 2, Board.TILE_SIZE - 4
        self.add(self.unit_variant)

        # Show armor, structure, heat stats next to the image (top)
        self.unit_stats = UnitStats(battle_unit)
        stats_pos = mech_sprite.get_rect().topright
        self.unit_stats.position = 4 + stats_pos[0], stats_pos[1] - self.unit_stats.height
        self.add(self.unit_stats)

        # Show move and attack numbers next to the image (bottom)
        values = "MV %i  ATK %i/%i/%i" % (battle_unit.getTurnMove(),
                                          battle_unit.short, battle_unit.medium, battle_unit.long)
        self.unit_values = floaters.TextFloater(values, font_name='TranscendsGames',
                                                font_size=Board.TILE_SIZE // 4, anchor_x='left', anchor_y='bottom')
        values_pos = mech_sprite.get_rect().bottomright
        self.unit_values.position = 4 + values_pos[0], values_pos[1] - 2
        self.add(self.unit_values)

    def updateTargetUnitStats(self, target_unit, is_friendly=False):
        if self.target_display is not None:
            self.target_display.kill()
            self.target_name.kill()
            self.target_variant.kill()
            self.target_stats.kill()
            self.target_values.kill()

        if target_unit is None:
            # Hide player unit stats at bottom left
            self.target_display = None
            self.target_name = None
            self.target_variant = None
            self.target_stats = None
            self.target_values = None
            return

        size = director.get_window_size()
        width = size[0]
        height = size[1]

        # Show target name above the image
        self.target_name = floaters.TextFloater(target_unit.getName(), font_name='TranscendsGames',
                                                font_size=Board.TILE_SIZE // 2, anchor_x='right', anchor_y='bottom')
        self.target_name.position = width - Board.TILE_SIZE // 2, height - Board.TILE_SIZE

        self.add(self.target_name)

        self.target_display = BatchNode()
        self.target_display.position = 0, 0

        mech_img_grid = pyglet.image.ImageGrid(pyglet.resource.image(target_unit.getImagePath()), 1, 6)
        mech_img_static = mech_img_grid[0]
        pitch = -(mech_img_static.width * len('RGBA'))
        img_data = mech_img_static.get_image_data()

        # testing with masking only a portion of the image
        damage_height = int(mech_img_static.height)  # int(mech_img_static.height * 0.67)
        data = img_data.get_region(0, 0, mech_img_static.width, damage_height).get_data('RGBA', pitch)

        mask = Image.frombytes('RGBA', (mech_img_static.width, damage_height), data)
        # the first image is the color that the stamp will be
        img1 = Image.new('RGBA', mask.size, color=(0, 0, 0, 255))
        # second image is the background
        bg_color = (200, 75, 75, 200)
        if is_friendly:
            bg_color = (225, 225, 225, 200)
        img2 = Image.new('RGBA', mask.size, color=bg_color)
        img1 = img1.convert('RGBA')

        # apply mask to background image
        img = Image.composite(img1, img2, mask)

        raw_image = img.tobytes()
        img_x = mask.size[0]
        img_y = mask.size[1]
        pyg_img = pyglet.image.ImageData(img_x, img_y, 'RGBA', raw_image, pitch=-img_x * len('RGBA'))

        mech_sprite = Sprite(pyg_img)
        mech_sprite.position = width - mech_sprite.width // 2 - Board.TILE_SIZE // 2, \
                               height - mech_sprite.height // 2 - Board.TILE_SIZE

        self.target_display.add(mech_sprite)
        self.add(self.target_display)

        # Show target variant below the image
        self.target_variant = floaters.TextFloater(target_unit.getVariant().upper(), font_name='TranscendsGames',
                                                   font_size=Board.TILE_SIZE // 3, anchor_x='right', anchor_y='top')
        variant_rect = mech_sprite.get_rect().bottomright
        self.target_variant.position = variant_rect[0], variant_rect[1] - 4
        self.add(self.target_variant)

        # Show armor, structure, heat stats next to the image (top)
        self.target_stats = UnitStats(target_unit, reverse=True)
        stats_pos = mech_sprite.get_rect().topleft
        self.target_stats.position = stats_pos[0] - self.target_stats.width - 4, stats_pos[1] - self.target_stats.height
        self.add(self.target_stats)

        # Show move and attack numbers next to the image (bottom)
        values = "MV %i  ATK %i/%i/%i" % (target_unit.getTurnMove(),
                                          target_unit.short, target_unit.medium, target_unit.long)
        self.target_values = floaters.TextFloater(values, font_name='TranscendsGames',
                                                  font_size=Board.TILE_SIZE // 4, anchor_x='right', anchor_y='bottom')
        values_pos = mech_sprite.get_rect().bottomleft
        self.target_values.position = values_pos[0] - 4, values_pos[1]
        self.add(self.target_values)


class UnitStats(cocos.batch.BatchNode):

    def __init__(self, battle_unit, reverse=False):
        super(UnitStats, self).__init__()

        self.reverse = reverse
        self.width = 0
        self.height = 0

        # create heat icon and bars
        heat_icon = Sprite(Resources.heat_icon_img)
        if reverse:
            heat_icon.position = -heat_icon.width // 2, self.height + heat_icon.height // 2
        else:
            heat_icon.position = heat_icon.width // 2, self.height + heat_icon.height // 2
        self.add(heat_icon, z=2)

        # TESTING: Use actual heat!!!
        rand_heat = random.randint(0, 4)
        for i in range(rand_heat):
            pip = Sprite(Resources.heat_pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -heat_icon.width - (i * pip.width) - pip.width, self.height + pip.height // 2
            else:
                pip.position = heat_icon.width + (i * pip.width) + pip.width // 2, self.height + pip.height // 2
            self.add(pip, z=1)

            if pip.x + pip.width > self.width:
                self.width = pip.x + pip.width

        self.height += 8

        # create structure icon and bars
        structure_icon = Sprite(Resources.structure_icon_img)
        if reverse:
            structure_icon.position = -structure_icon.width // 2, self.height + structure_icon.height // 2
        else:
            structure_icon.position = structure_icon.width // 2, self.height + structure_icon.height // 2
        self.add(structure_icon, z=2)

        orig_structure = battle_unit.mech.structure
        for i in range(orig_structure):
            pip_img = Resources.structure_pip_img
            if i >= battle_unit.structure:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -structure_icon.width - (i * pip.width) - pip.width, self.height + pip.height // 2
            else:
                pip.position = structure_icon.width + (i * pip.width) + pip.width // 2, self.height + pip.height // 2
            self.add(pip, z=1)

            if pip.x + pip.width > self.width:
                self.width = pip.x + pip.width

        self.height += 8

        # create armor icon and bars
        armor_icon = Sprite(Resources.armor_icon_img)
        if reverse:
            armor_icon.position = -armor_icon.width // 2, self.height + armor_icon.height // 2
        else:
            armor_icon.position = armor_icon.width // 2, self.height + armor_icon.height // 2
        self.add(armor_icon, z=2)

        orig_armor = battle_unit.mech.armor
        for i in range(orig_armor):
            pip_img = Resources.armor_pip_img
            if i >= battle_unit.armor:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -armor_icon.width - (i * pip.width) - pip.width, self.height + pip.height // 2
            else:
                pip.position = armor_icon.width + (i * pip.width) + pip.width // 2, self.height + pip.height // 2
            self.add(pip, z=1)

            if pip.x + pip.width > self.width:
                self.width = pip.x + pip.width

        self.height += 8
