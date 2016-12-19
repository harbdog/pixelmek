import pygame

from cocos.director import director
from cocos.menu import *
from pixelmek.misc.settings import Settings
from pixelmek.misc.resources import Resources


class SettingsMenu(Menu):

    RESOLUTIONS = ['640x480', '800x600', '1024x768', '1280x1024',
                   '1360x768', '1680x1050', '1920x1080', '2560x1440']

    VOLUMES = ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']

    def __init__(self):
        super(SettingsMenu, self).__init__("Settings")

        print("loading settings menu")

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        menus = []

        if Settings.get_resolution_string() not in self.RESOLUTIONS:
            self.RESOLUTIONS.insert(0, Settings.get_resolution_string())

        res_default = self.RESOLUTIONS.index(Settings.get_resolution_string())
        res_item = MultipleMenuItem('Resolution: ', self.on_res, self.RESOLUTIONS, default_item=res_default)
        menus.append(res_item)

        vol_default = int(Settings.get_volume_fx() * 10)
        vol_item = MultipleMenuItem('FX Volume: ', self.on_fx_volume, self.VOLUMES, default_item=vol_default)
        menus.append(vol_item)

        var_dmg_item = ToggleMenuItem('Variable Damage: ', self.on_var_dmg, value=Settings.get_variable_damage())
        menus.append(var_dmg_item)

        var_mod_item = ToggleMenuItem('Variable Modifiers: ', self.on_var_mod, value=Settings.get_variable_modifiers())
        menus.append(var_mod_item)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_res(self, index):
        # TODO: change resolution as it is selected, or make them restart the application?
        res_str = self.RESOLUTIONS[index]
        print("Change Resolution to %s" % res_str)
        Settings.set_resolution_string(res_str)
        Settings.save()

    def on_fx_volume(self, index):
        vol_val = float(index) / 10
        print("Change FX Volume to %s" % str(vol_val))

        # get sound channel to use just for this test sound
        fx_channel = pygame.mixer.find_channel()
        if fx_channel is None:
            fx_channel = pygame.mixer.Channel(0)
        fx_channel.set_volume(vol_val)
        fx_channel.play(Resources.gauss_sound)

        Settings.set_volume_fx(vol_val)
        Settings.save()

    def on_var_dmg(self, value):
        var_val = bool(value)
        print("Change Variable Damage to %s" % var_val)
        Settings.set_variable_damage(var_val)
        Settings.save()

    def on_var_mod(self, value):
        var_val = bool(value)
        print("Change Variable Modifiers to %s" % var_val)
        Settings.set_variable_modifiers(var_val)
        Settings.save()

    def on_quit(self):
        print("Back to the main menu...")
        director.pop()
