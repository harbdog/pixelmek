import cocos
import pyglet
import random
from cocos.batch import BatchNode
from cocos.rect import Rect
from cocos.sprite import Sprite
from PIL import Image

import floaters
import gl
from pixelmek.misc.resources import Resources


class UnitCard(cocos.layer.Layer):

    def __init__(self, battle_unit, is_friendly=True, reverse=False):
        super(UnitCard, self).__init__()
        from board import Board

        self.reverse = reverse
        self.width = 0
        self.height = 0

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
        mech_sprite.position = mech_sprite.width // 2, Board.TILE_SIZE // 2 + mech_sprite.height // 2

        self.unit_display.add(mech_sprite)
        self.add(self.unit_display)

        # Show unit name above the image
        if reverse:
            self.unit_name = floaters.TextFloater(battle_unit.getName(), font_name='TranscendsGames',
                                                  font_size=Board.TILE_SIZE // 2, anchor_x='right', anchor_y='bottom')
            name_rect = mech_sprite.get_rect().topright
            self.unit_name.position = name_rect[0], name_rect[1]
        else:
            self.unit_name = floaters.TextFloater(battle_unit.getName(), font_name='TranscendsGames',
                                                  font_size=Board.TILE_SIZE // 2, anchor_x='left', anchor_y='bottom')
            name_rect = mech_sprite.get_rect().topleft
            self.unit_name.position = name_rect[0], name_rect[1]

        self.add(self.unit_name)

        # Show unit variant below the image
        if reverse:
            self.unit_variant = floaters.TextFloater(battle_unit.getVariant().upper(), font_name='TranscendsGames',
                                                     font_size=Board.TILE_SIZE // 3, anchor_x='right', anchor_y='top')
            variant_rect = mech_sprite.get_rect().bottomright
            self.unit_variant.position = variant_rect[0], variant_rect[1] - 2
        else:
            self.unit_variant = floaters.TextFloater(battle_unit.getVariant().upper(), font_name='TranscendsGames',
                                                     font_size=Board.TILE_SIZE // 3, anchor_x='left', anchor_y='top')
            variant_rect = mech_sprite.get_rect().bottomleft
            self.unit_variant.position = variant_rect[0], variant_rect[1] - 2

        self.add(self.unit_variant)

        # Show armor, structure, heat stats next to the image (top)
        unit_stats = cocos.layer.Layer()
        stats_width = 0
        stats_height = 0

        # Show move and attack numbers next to the image (bottom)
        # values = "MV %i  ATK %i/%i/%i" % (battle_unit.getTurnMove(),
        #                                   battle_unit.short, battle_unit.medium, battle_unit.long)
        # self.unit_values = floaters.TextFloater(values, font_name='TranscendsGames',
        #                                         font_size=Board.TILE_SIZE // 4, anchor_x='left', anchor_y='bottom')
        # values_pos = mech_sprite.get_rect().bottomright
        # self.unit_values.position = 4 + values_pos[0], values_pos[1] - 2
        # self.add(self.unit_values)

        # create move icon and label of values
        move_icon = Sprite(Resources.move_icon_img)
        move_str = str(battle_unit.getTurnMove())

        if reverse:
            move_icon.position = -move_icon.width // 2, stats_height + move_icon.height // 2

            move_label = floaters.TextFloater(move_str, font_name='TranscendsGames',
                                              font_size=Board.TILE_SIZE // 3, anchor_x='right', anchor_y='bottom')
            move_label.position = move_icon.get_rect().bottomleft
            unit_stats.add(move_label, z=2)
        else:
            move_icon.position = move_icon.width // 2, stats_height + move_icon.height // 2

            move_label = floaters.TextFloater(move_str, font_name='TranscendsGames',
                                              font_size=Board.TILE_SIZE // 3, anchor_x='left', anchor_y='bottom')
            move_label.position = move_icon.get_rect().bottomright
            unit_stats.add(move_label, z=2)

        unit_stats.add(move_icon, z=2)

        stats_height += move_icon.height

        # create attack icon and label of values
        attack_icon = Sprite(Resources.weapon_icon_img)
        attack_str = "%i/%i/%i" % (battle_unit.short, battle_unit.medium, battle_unit.long)

        if reverse:
            attack_icon.position = -attack_icon.width // 2, stats_height + attack_icon.height // 2

            attack_label = floaters.TextFloater(attack_str, font_name='TranscendsGames',
                                                font_size=Board.TILE_SIZE // 3, anchor_x='right', anchor_y='bottom')
            attack_label.position = attack_icon.get_rect().bottomleft
            unit_stats.add(attack_label, z=2)
        else:
            attack_icon.position = attack_icon.width // 2, stats_height + attack_icon.height // 2

            attack_label = floaters.TextFloater(attack_str, font_name='TranscendsGames',
                                                font_size=Board.TILE_SIZE // 3, anchor_x='left', anchor_y='bottom')
            attack_label.position = attack_icon.get_rect().bottomright
            unit_stats.add(attack_label, z=2)

        unit_stats.add(attack_icon, z=2)

        stats_height += attack_icon.height

        # create heat icon and bars
        heat_icon = Sprite(Resources.heat_icon_img)
        if reverse:
            heat_icon.position = -heat_icon.width // 2, stats_height + heat_icon.height // 2
        else:
            heat_icon.position = heat_icon.width // 2, stats_height + heat_icon.height // 2

        unit_stats.add(heat_icon, z=2)

        # TESTING: Use actual heat!!!
        rand_heat = random.randint(0, 4)
        for i in range(rand_heat):
            pip = Sprite(Resources.heat_pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -heat_icon.width - (i * pip.width) - pip.width, stats_height + pip.height // 2
            else:
                pip.position = heat_icon.width + (i * pip.width) + pip.width // 2, stats_height + pip.height // 2

            unit_stats.add(pip, z=1)

            if pip.x + pip.width > stats_width:
                stats_width = pip.x + pip.width

        stats_height += heat_icon.height

        # create structure icon and bars
        structure_icon = Sprite(Resources.structure_icon_img)
        if reverse:
            structure_icon.position = -structure_icon.width // 2, stats_height + structure_icon.height // 2
        else:
            structure_icon.position = structure_icon.width // 2, stats_height + structure_icon.height // 2

        unit_stats.add(structure_icon, z=2)

        orig_structure = battle_unit.mech.structure
        for i in range(orig_structure):
            pip_img = Resources.structure_pip_img
            if i >= battle_unit.structure:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -structure_icon.width - (i * pip.width) - pip.width, stats_height + pip.height // 2
            else:
                pip.position = structure_icon.width + (i * pip.width) + pip.width // 2, stats_height + pip.height // 2

            unit_stats.add(pip, z=1)

            if pip.x + pip.width > stats_width:
                stats_width = pip.x + pip.width

        stats_height += structure_icon.height

        # create armor icon and bars
        armor_icon = Sprite(Resources.armor_icon_img)
        if reverse:
            armor_icon.position = -armor_icon.width // 2, stats_height + armor_icon.height // 2
        else:
            armor_icon.position = armor_icon.width // 2, stats_height + armor_icon.height // 2

        unit_stats.add(armor_icon, z=2)

        orig_armor = battle_unit.mech.armor
        for i in range(orig_armor):
            pip_img = Resources.armor_pip_img
            if i >= battle_unit.armor:
                pip_img = Resources.empty_pip_img

            pip = Sprite(pip_img)
            pip.scale = 2.0
            if reverse:
                pip.position = -armor_icon.width - (i * pip.width) - pip.width, stats_height + pip.height // 2
            else:
                pip.position = armor_icon.width + (i * pip.width) + pip.width // 2, stats_height + pip.height // 2

            unit_stats.add(pip, z=1)

            if pip.x + pip.width > stats_width:
                stats_width = pip.x + pip.width

        stats_height += armor_icon.height

        if reverse:
            stats_pos = mech_sprite.get_rect().topleft
            unit_stats.position = stats_pos[0] - 4, stats_pos[1] - stats_height

        else:
            stats_pos = mech_sprite.get_rect().topright
            unit_stats.position = 4 + stats_pos[0], stats_pos[1] - stats_height

        self.add(unit_stats)

        # calculate actual width and height of this element
        self.width = mech_sprite.width + stats_width
        self.height = mech_sprite.height + (3 * Board.TILE_SIZE // 2)


class Button(cocos.layer.ColorLayer):

    def __init__(self, icon, action, width, height,
                 border_width=2, border_color=(50, 50, 50), border_selected_color=(255, 255, 255),
                 color=(225, 225, 225), selected_color=(50, 150, 220)):
        super(Button, self).__init__(color[0], color[1], color[2], 255//2)

        self.border_width = border_width
        self.border_color = border_color
        self.border_selected_color = border_selected_color

        self.default_color = color
        self.selected_color = selected_color

        self.action = action
        self.selected = False
        self.disabled = False
        self.hidden = False

        self.width = width
        self.height = height

        # draw icon
        if icon is not None:
            self.icon = Sprite(icon)
            self.icon.position = self.icon.width // 2 + (width // 2 - self.icon.width // 2), \
                                 self.icon.height // 2 + (height // 2 - self.icon.height // 2)
            self.add(self.icon)

        self.borders = []
        self.draw_border()

    def draw_border(self):
        for border in self.borders:
            border.kill()

        border_color = self.border_color
        if self.selected:
            border_color = self.border_selected_color

        # draw border
        if self.border_width > 0:
            border_w = gl.SingleLine((0, 0), (0, self.height),
                                     width=self.border_width,
                                     color=(border_color[0], border_color[1], border_color[2], 255))
            border_e = gl.SingleLine((self.width, 0), (self.width, self.height),
                                     width=self.border_width,
                                     color=(border_color[0], border_color[1], border_color[2], 255))
            border_n = gl.SingleLine((0, self.height), (self.width, self.height),
                                     width=self.border_width,
                                     color=(border_color[0], border_color[1], border_color[2], 255))
            border_s = gl.SingleLine((0, 0), (self.width, 0),
                                     width=self.border_width,
                                     color=(border_color[0], border_color[1], border_color[2], 255))

            self.borders = [border_w, border_e, border_n, border_s]

            for border in self.borders:
                self.add(border)

    def is_at(self, x, y):
        p = Rect(x, y, 1, 1)
        r = Rect(self.x, self.y, self.width, self.height)

        return p.intersects(r)

    def set_selected(self, selected):
        if selected != self.selected:
            if selected:
                from interface import Interface
                Interface.UI.deselectAllButtons()

                self.color = self.selected_color

            else:
                self.color = self.default_color

            self.selected = selected
            self.draw_border()

    def do_action(self, **kwargs):
        if not self.selected:
            self.set_selected(True)

        kwargs['button'] = self
        return self.action(**kwargs)
