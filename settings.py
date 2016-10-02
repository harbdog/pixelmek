from cocos.director import director
from cocos.menu import *


class Settings:

    VOLUME_FX = 0.5

    def __init__(self):
        pass

    @staticmethod
    def set_volume_fx(volume):
        Settings.VOLUME_FX = volume


class SettingsMenu(Menu):

    RESOLUTIONS = ['320x200', '640x480', '800x600', '1024x768', '1280x1024',
                   '1360x768', '1680x1050', '1920x1080', '2560x1440']

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

        res_item = MultipleMenuItem('Resolution: ', self.on_res, self.RESOLUTIONS)
        menus.append(res_item)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_res(self, index):
        print("Change Resolution to %s" % self.RESOLUTIONS[index])

    def on_quit(self):
        print("Back to the main menu...")
        director.pop()
