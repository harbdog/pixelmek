class Modifiers(object):

    AUTO_MISS = 1000

    @staticmethod
    def getRangeModifier(distance):
        if distance > 42:
            return Modifiers.AUTO_MISS
        elif distance > 24:
            return 4
        elif distance > 6:
            return 2
        else:
            return 0

    @staticmethod
    def getTargetMovementModifier(battle_unit):
        if battle_unit is None:
            return Modifiers.AUTO_MISS

        if battle_unit.isShutdown():
            return -4

        # use the amount of move for the turn based on heat and critical effects
        current_move = battle_unit.getTurnMove()
        current_jump = battle_unit.getTurnJump()

        # TODO: for hardcore rules, use the actual amount of distance moved by the unit

        move_modifier = Modifiers._getMoveModifier(current_move)
        jump_modifier = 0
        if current_jump > 0:
            jump_modifier = 1 + Modifiers._getMoveModifier(current_jump)

        # basic alpha strike rules use the greater of move or jump modifier
        if jump_modifier > move_modifier:
            return jump_modifier

        return move_modifier

    @staticmethod
    def _getMoveModifier(distance):
        if distance >= 35:
            return 5
        elif distance >= 19:
            return 4
        elif distance >= 13:
            return 3
        elif distance >= 9:
            return 2
        elif distance >= 5:
            return 1

        return 0
