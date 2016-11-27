import random


class CriticalHits(object):

    CRITICAL_AMMO = "CRIT AMMO"
    CRITICAL_ENGINE = "CRIT ENGINE"
    CRITICAL_FIRE_CTL = "CRIT FIRE CTL"
    CRITICAL_WEAPON = "CRIT WEAPON"
    CRITICAL_MOVE = "CRIT MOVE"
    CRITICAL_DESTROYED = "CRIT DESTRUCTION"

    CRITICAL_HITS_TABLE = {
        2: CRITICAL_AMMO,
        3: CRITICAL_ENGINE,
        4: CRITICAL_FIRE_CTL,
        5: None,
        6: CRITICAL_WEAPON,
        7: CRITICAL_MOVE,
        8: CRITICAL_WEAPON,
        9: None,
        10: CRITICAL_FIRE_CTL,
        11: CRITICAL_ENGINE,
        12: CRITICAL_DESTROYED
    }

    @staticmethod
    def rollCriticalHit(battle_unit):
        if battle_unit is None:
            return None

        roll = random.randint(2, 2)
        print("Rolled:", roll)

        critical_type = CriticalHits.CRITICAL_HITS_TABLE.get(roll)
        critical_type = CriticalHits.applyCriticalHitEffect(battle_unit, critical_type)

        return critical_type

    @staticmethod
    def applyCriticalHitEffect(battle_unit, critical_type):
        print("Critical Type:", str(critical_type))

        if critical_type is None:
            return None

        elif critical_type is CriticalHits.CRITICAL_AMMO:
            # Unless the unit has CASE(I/II) or Energy special, the unit is destroyed
            if battle_unit.hasSpecial('ENE') or battle_unit.hasSpecial('CASEII'):
                # If it has CASE(II) or Energy, treat as no critical
                critical_type = None
            elif battle_unit.hasSpecial('CASE'):
                # If it has CASE(I), unit takes an additional point of damage
                battle_unit.applyDamage(1)
            else:
                # Unit is destroyed
                battle_unit.structure = 0

        elif critical_type is CriticalHits.CRITICAL_ENGINE:
            # TODO: 1st hit: unit generates 1 heat from firing weapons
            # 2nd hit: unit is destroyed
            pass

        elif critical_type is CriticalHits.CRITICAL_FIRE_CTL:
            # TODO: Each hit adds +2 to weapon attack modifiers
            pass

        elif critical_type is CriticalHits.CRITICAL_WEAPON:
            # TODO: Each hit reduces all damage values by 1 (to minimum of 0)
            pass

        elif critical_type is CriticalHits.CRITICAL_MOVE:
            # TODO: Each hit halves the unit's current Move, rounding normally
            # If reduced to 0, unit is immobile
            pass

        elif critical_type is CriticalHits.CRITICAL_DESTROYED:
            # Unit is destroyed
            battle_unit.structure = 0

        return critical_type