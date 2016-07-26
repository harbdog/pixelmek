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

    def __init__(self, name, short_name, _range):
        self.name = name
        self.short_name = short_name
        self.range = _range

    def __repr__(self):
        return "%s(name=%r)" % (
            self.__class__.__name__, self.name
        )


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
