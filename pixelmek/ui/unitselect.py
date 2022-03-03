import cocos
from cocos.director import director
from cocos.menu import *
from cocos.scenes import *

from pixelmek.misc.resources import Resources
from pixelmek.model.battle import Battle
from pixelmek.ui import actions
from pixelmek.ui.menuitem import UnitMenuItem


class PlayerUnitsMenu(Menu):
    def __init__(self, player, tech=None):
        print("loading player units menu for %s" % str(player))

        self.player = player
        self.player_units = Battle.BATTLE.getPlayerUnits(player)

        num_units = 0
        total_pv = 0
        for battle_unit_index, battle_unit in enumerate(self.player_units):
            num_units += 1
            total_pv += battle_unit.getPointValue()

        super(PlayerUnitsMenu, self).__init__("%i %s Units [%ipv]" % (num_units, str(player), total_pv))

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        menus = []

        for battle_unit_index, battle_unit in enumerate(self.player_units):
            def on_select_unit(this_unit=None):
                print('Selected unit: %s' % str(this_unit))

                scene = cocos.scene.Scene()
                scene.add(UnitSelectionMenu(self.player, battle_unit=this_unit, tech=tech))
                director.push(FlipX3DTransition(scene, duration=0.5))

            on_select_unit.__name__ = "on_select_unit_%s" % battle_unit_index

            unit_str = "%it %s [%ipv]" % (battle_unit.getTonnage(),
                                                battle_unit.getName(), battle_unit.getPointValue())
            unit_change = MenuItem(unit_str, on_select_unit, this_unit=battle_unit)
            menus.append(unit_change)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_quit(self):
        print("Back to the previous menu...")
        director.pop()


class UnitSelectionMenu(Menu):

    def __init__(self, player, battle_unit, tech=None):
        super(UnitSelectionMenu, self).__init__("Use arrow keys to cycle left/right")

        print("loading unit selection menu for %s" % str(player))

        self.font_title['font_name'] = 'Convoy'
        self.font_title['font_size'] = 40
        self.font_item['font_name'] = 'Convoy'
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Convoy'
        self.font_item_selected['font_size'] = 40

        self.player = player
        self.tech = tech
        self.unit_changed = False

        menus = []

        # sort units by tonnage
        self.units = sorted(Resources.get_units(), key=lambda unit: unit.tonnage)

        if tech is not None:
            # only show units with the correct tech
            self.units = [unit for unit in self.units if unit.tech == tech]

        # find the index of the base unit of the battle unit
        default_idx = 0
        for unit_index, unit in enumerate(self.units):
            if battle_unit.mech is unit:
                default_idx = unit_index
                break

        def on_select_unit(index):
            new_unit = self.units[index]
            print('Updating unit: ' + str(new_unit))
            actions.update_battle_unit(battle_unit, new_unit)
            self.unit_changed = True

        unit_select = UnitMenuItem(player, self.units, on_select_unit, default_unit=default_idx)
        menus.append(unit_select)

        ret_item = MenuItem('Return', self.on_quit)
        menus.append(ret_item)

        self.create_menu(menus)

    def on_quit(self):
        print("Back to the previous menu...")
        director.pop()

        if self.unit_changed:
            # unit changed, so the player units menu needs to be reloaded
            scene = cocos.scene.Scene()
            scene.add(PlayerUnitsMenu(player=self.player, tech=self.tech))
            director.replace(FlipX3DTransition(scene, duration=0.5))
