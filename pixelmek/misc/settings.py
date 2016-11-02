class Settings:
    def __init__(self):
        # TODO: load settings from file
        pass

    VOLUME_FX = 0.5
    VARIABLE_DAMAGE = True
    VARIABLE_MODIFIERS = True

    @staticmethod
    def set_volume_fx(volume):
        Settings.VOLUME_FX = volume

    @staticmethod
    def set_variable_damage(is_variable):
        Settings.VARIABLE_DAMAGE = is_variable

    @staticmethod
    def set_variable_modifiers(is_variable):
        Settings.VARIABLE_MODIFIERS = is_variable
