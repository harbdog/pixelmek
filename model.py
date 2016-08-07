import yaml


class Mech(yaml.YAMLObject):
    yaml_tag = u'!Mech'

    def __init__(self, name, variant, cost, pv, _type, size, tmm, move, jump, role, skill,
                 short, medium, _long, overheat, armor, structure, specials, weapons, image_path):
        self.name = name
        self.variant = variant
        self.cost = cost
        self.pv = pv
        self.type = _type
        self.size = size
        self.tmm = tmm
        self.move = move
        self.jump = jump
        self.role = role
        self.skill = skill
        self.short = short
        self.medium = medium
        self.long = _long
        self.overheat = overheat
        self.armor = armor
        self.structure = structure
        self.specials = specials
        self.weapons = weapons
        self.image_path = image_path

    def __repr__(self):
        return "%s(name='%s %s', pv=%r, specials=%r, weapons=%r)" % (
            self.__class__.__name__, self.name, self.variant, self.pv, self.specials, self.weapons
        )

    def full_name(self):
        return "%s %s" % (self.name, self.variant)

    def get_jump(self):
        try:
            self.jump
        except AttributeError:
            self.jump = 0

        return self.jump


class Weapon(yaml.YAMLObject):
    yaml_tag = u'!Weapon'

    FLAMR = 'FLAMR'  # flamer
    SLAS = 'SLAS'   # small laser
    MLAS = 'MLAS'   # medium laser
    LLAS = 'LLAS'   # large laser
    ERSL = 'ERSL'   # ER small laser
    ERML = 'ERML'   # ER medium laser
    ERLL = 'ERLL'   # ER large laser
    SPL = 'SPL'     # small pulse laser
    MPL = 'MPL'     # medium pulse laser
    LPL = 'LPL'     # large pulse laser
    PPC = 'PPC'     # particle projection cannon
    ERPPC = 'ERPPC'  # ER particle projection cannon
    SRM = 'SRM'     # short range missile
    MRM = 'MRM'     # medium range missile
    LRM = 'LRM'     # long range missile
    ATM = 'ATM'     # advanced tactical missile
    MG = 'MG'       # machine gun
    AC = 'AC'       # autocannon
    LBX = 'LBX'     # LB-X autocannon
    GAUSS = 'GAUSS'  # gauss rifle

    _laser = (SLAS, MLAS, LLAS, ERSL, ERML, ERLL, SPL, MPL, LPL)
    _ppc = (PPC, ERPPC)

    TYPE_ENERGY = 'energy'
    TYPE_MISSILE = 'missile'
    TYPE_BALLISTIC = 'ballistic'

    RANGE_SHORT = 'short'
    RANGE_MEDIUM = 'medium'
    RANGE_LONG = 'long'

    def __init__(self, name, short_name, _range, _type, color, speed, scale, projectiles):
        self.name = name
        self.short_name = short_name
        self.range = _range
        self.type = _type
        self.color = color
        self.speed = speed
        self.scale = scale
        self.projectiles = projectiles

    def __repr__(self):
        return "%s(name=%r)" % (
            self.__class__.__name__, self.name
        )

    def get_color(self):
        try:
            self.color
        except AttributeError:
            self.color = [0, 0, 0]

        return self.color

    def get_projectiles(self):
        try:
            self.projectiles
        except AttributeError:
            self.projectiles = 1

        return self.projectiles

    def get_scale(self):
        try:
            self.scale
        except AttributeError:
            self.scale = 1.0

        return self.scale

    def get_speed(self):
        try:
            self.speed
        except AttributeError:
            self.speed = 100

        return self.speed

    def isShort(self):
        return self.range == Weapon.RANGE_SHORT

    def isMedium(self):
        return self.range == Weapon.RANGE_MEDIUM

    def isLong(self):
        return self.range == Weapon.RANGE_LONG

    def isEnergy(self):
        return self.type == Weapon.TYPE_ENERGY

    def isMissile(self):
        return self.type == Weapon.TYPE_MISSILE

    def isBallistic(self):
        return self.type == Weapon.TYPE_BALLISTIC

    def isLaser(self):
        return self.short_name in Weapon._laser

    def isPPC(self):
        return self.short_name in Weapon._ppc

    def isLRM(self):
        return self.short_name == Weapon.LRM

    def isSRM(self):
        return self.short_name == Weapon.SRM

    def isMG(self):
        return self.short_name == Weapon.MG

    def isGauss(self):
        return self.short_name == Weapon.GAUSS


class Special(yaml.YAMLObject):
    yaml_tag = u'!Special'

    def __init__(self, name, short_name, description):
        self.name = name
        self.short_name = short_name
        self.description = description

    def __repr__(self):
        return "%s(name=%r [%s])" % (
            self.__class__.__name__, self.name, self.short_name
        )
