import pygame

from cocos.director import director
from cocos.menu import *
from menuitem import UnitMenuItem
from pixelmek.misc.resources import Resources


class UnitSelectionMenu(Menu):

    def __init__(self):
        super(UnitSelectionMenu, self).__init__("Unit Selection")

        print("loading unit selection menu")

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        menus = []

        # TODO: sort units by tonnage and only show units that are the correct Clan/IS type as selected
        self.units = Resources.get_units()

        first_unit_select = UnitMenuItem(self.units, self.on_select_unit, default_unit=0)
        menus.append(first_unit_select)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_select_unit(self, unit_index):
        print('Selected unit: '+str(self.units[unit_index]))

    def on_quit(self):
        print("Back to the main menu...")
        director.pop()
