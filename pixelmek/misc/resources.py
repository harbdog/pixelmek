import pyglet
from pygame.mixer import Sound


class Resources(object):

    @staticmethod
    def preload():
        from pixelmek.ui.board import Board

        # Preload images
        Resources.mouse_pointer = pyglet.resource.image("images/ui/mouse-pointer-0.png")

        buildings_img = pyglet.resource.image("images/board/colony-buildings-32.png")
        buildings_grid = pyglet.image.ImageGrid(buildings_img,
                                                columns=(buildings_img.width // Board.TILE_SIZE),
                                                rows=(buildings_img.height // Board.TILE_SIZE))

        Resources.buildings_tex = pyglet.image.TextureGrid(buildings_grid)
        Resources.ground_img = pyglet.resource.image("images/board/ground-dark.png")

        Resources.action_indicator_img = pyglet.resource.animation("images/ui/action-indicator.gif")

        Resources.player_indicator_img = pyglet.resource.image("images/ui/player-indicator.png")
        Resources.friendly_indicator_img = pyglet.resource.image("images/ui/friendly-indicator.png")
        Resources.enemy_indicator_img = pyglet.resource.image("images/ui/enemy-indicator.png")
        Resources.move_indicator_img = pyglet.resource.image("images/ui/move-indicator.png")

        Resources.armor_pip_img = pyglet.resource.image("images/ui/armor-pip.png")
        Resources.structure_pip_img = pyglet.resource.image("images/ui/structure-pip.png")
        Resources.empty_pip_img = pyglet.resource.image("images/ui/empty-pip.png")
        Resources.heat_pip_img = pyglet.resource.image("images/ui/heat-pip.png")

        Resources.armor_icon_img = pyglet.resource.image("images/ui/armor-icon.png")
        Resources.structure_icon_img = pyglet.resource.image("images/ui/structure-icon.png")
        Resources.heat_icon_img = pyglet.resource.image("images/ui/heat-icon.png")
        Resources.move_icon_img = pyglet.resource.image("images/ui/move-icon.png")
        Resources.weapon_icon_img = pyglet.resource.image("images/ui/weapon-icon.png")

        Resources.end_button_img = pyglet.resource.image("images/ui/end-button.png")
        Resources.evade_button_img = pyglet.resource.image("images/ui/evade-button.png")
        Resources.move_button_img = pyglet.resource.image("images/ui/move-button.png")
        Resources.overheat_button_img = pyglet.resource.image("images/ui/red-button.png")
        Resources.sprint_button_img = pyglet.resource.image("images/ui/sprint-button.png")
        Resources.weapon_button_img = pyglet.resource.image("images/ui/weapon-button.png")

        Resources.ballistic_img = pyglet.resource.image("images/weapons/ballistic.png")
        Resources.buckshot_img = pyglet.resource.image("images/weapons/buckshot.png")
        Resources.gauss_img = pyglet.resource.image("images/weapons/gauss.png")
        Resources.missile_img = pyglet.resource.image("images/weapons/missile.png")
        Resources.explosion01 = pyglet.resource.image('images/weapons/explosion_01.png')
        Resources.explosion07 = pyglet.resource.image('images/weapons/explosion_07.png')
        Resources.flash03 = pyglet.resource.image('images/weapons/flash_03.png')

        # Preload sound effects
        Resources.cannon_sound = Sound(pyglet.resource.file("sounds/autocannon-shot.ogg"))
        Resources.impact_sound = Sound(pyglet.resource.file("sounds/explosion-single.ogg"))

        Resources.flamer_sound = Sound(pyglet.resource.file("sounds/flamer-shot.ogg"))
        Resources.gauss_sound = Sound(pyglet.resource.file("sounds/gauss-shot.ogg"))
        Resources.las_sound = Sound(pyglet.resource.file("sounds/laser-blast-long.ogg"))
        Resources.machinegun_sound = Sound(pyglet.resource.file("sounds/machine-gun.ogg"))
        Resources.ppc_sound = Sound(pyglet.resource.file("sounds/ppc-shot.ogg"))

        Resources.missile_sounds = []
        for i in range(8):
            Resources.missile_sounds.append(Sound(pyglet.resource.file("sounds/missile-shot-%s.ogg" % i)))

        Resources.stomp_sounds = []
        for i in range(4):
            Resources.stomp_sounds.append(Sound(pyglet.resource.file("sounds/mech-stomp-%s.ogg" % i)))

        Resources.explosion_sounds = []
        for i in range(4):
            Resources.explosion_sounds.append(Sound(pyglet.resource.file("sounds/cannon-%s.ogg" % i)))

        for i in range(2):
            Resources.explosion_sounds.append(Sound(pyglet.resource.file("sounds/sparks-%s.ogg" % i)))

        # preload font
        pyglet.font.add_file(pyglet.resource.file('images/ui/Convoy.ttf'))
        pyglet.font.add_file(pyglet.resource.file('images/ui/TranscendsGames.otf'))
