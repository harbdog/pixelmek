import os
import yaml


class Settings:
    def __init__(self):
        # Settings is to be a static only set of variables and methods so they can be looked up anywhere
        pass

    FILE = os.path.expanduser('~/.pixelmek')
    RESOLUTION = 'RESOLUTION'
    VOLUME_FX = 'VOLUME_FX'
    VARIABLE_DAMAGE = 'VARIABLE_DAMAGE'
    VARIABLE_MODIFIERS = 'VARIABLE_MODIFIERS'

    SETTINGS = {
        RESOLUTION: '1024x768',
        VOLUME_FX: 0.5,
        VARIABLE_DAMAGE: True,
        VARIABLE_MODIFIERS: True
    }

    @staticmethod
    def init():
        # load settings from file

        print('Loading settings file %s' % Settings.FILE)
        if not os.path.exists(Settings.FILE):
            Settings.save()

        else:
            try:
                with open(Settings.FILE, 'r') as infile:
                    Settings.SETTINGS = (yaml.load(infile))
            except IOError:
                print('Error loading settings file %s!' % Settings.FILE)

    @staticmethod
    def save():
        # save settings to file
        print('Saving settings file %s' % Settings.FILE)
        try:
            with open(Settings.FILE, 'w') as outfile:
                yaml.dump(Settings.SETTINGS, outfile, default_flow_style=False)
        except IOError:
            print('Error writing settings file %s!' % Settings.FILE)

    @staticmethod
    def set_volume_fx(volume):
        Settings.SETTINGS[Settings.VOLUME_FX] = volume

    @staticmethod
    def get_volume_fx():
        return Settings.SETTINGS[Settings.VOLUME_FX]

    @staticmethod
    def set_variable_damage(is_variable):
        Settings.SETTINGS[Settings.VARIABLE_DAMAGE] = is_variable

    @staticmethod
    def get_variable_damage():
        return Settings.SETTINGS[Settings.VARIABLE_DAMAGE]

    @staticmethod
    def set_variable_modifiers(is_variable):
        Settings.SETTINGS[Settings.VARIABLE_MODIFIERS] = is_variable

    @staticmethod
    def get_variable_modifiers():
        return Settings.SETTINGS[Settings.VARIABLE_MODIFIERS]

    @staticmethod
    def set_resolution_string(resolution_str):
        Settings.SETTINGS[Settings.RESOLUTION] = resolution_str

    @staticmethod
    def get_resolution_string():
        return Settings.SETTINGS[Settings.RESOLUTION]

    @staticmethod
    def get_resolution_width():
        return int( Settings.SETTINGS[Settings.RESOLUTION].split('x')[0])

    @staticmethod
    def get_resolution_height():
        return int( Settings.SETTINGS[Settings.RESOLUTION].split('x')[1])
