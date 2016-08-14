import pyglet
from pygame.mixer import Sound


class Resources(object):

    @staticmethod
    def preload():
        # Preload images
        Resources.ballistic_img = pyglet.resource.image("images/weapons/ballistic.png")
        Resources.buckshot_img = pyglet.resource.image("images/weapons/buckshot.png")
        Resources.gauss_img = pyglet.resource.image("images/weapons/gauss.png")
        Resources.missile_img = pyglet.resource.image("images/weapons/missile.png")
        Resources.explosion01 = pyglet.resource.image('images/weapons/explosion_01.png')
        Resources.explosion07 = pyglet.resource.image('images/weapons/explosion_07.png')
        Resources.flash03 = pyglet.resource.image('images/weapons/flash_03.png')

        # Preload sound effects
        Resources.cannon_sound = Sound(pyglet.resource.file("data/sounds/autocannon-shot.ogg"))
        Resources.explosion_sound = Sound(pyglet.resource.file("data/sounds/explosion-single.ogg"))
        Resources.flamer_sound = Sound(pyglet.resource.file("data/sounds/flamer-shot.ogg"))
        Resources.gauss_sound = Sound(pyglet.resource.file("data/sounds/gauss-shot.ogg"))
        Resources.las_sound = Sound(pyglet.resource.file("data/sounds/laser-blast-long.ogg"))
        Resources.machinegun_sound = Sound(pyglet.resource.file("data/sounds/machine-gun.ogg"))
        Resources.ppc_sound = Sound(pyglet.resource.file("data/sounds/ppc-shot.ogg"))

        Resources.missile_sounds = []
        for i in range(8):
            Resources.missile_sounds.append(Sound(pyglet.resource.file("data/sounds/missile-shot-%s.ogg" % i)))

        Resources.stomp_sounds = []
        for i in range(4):
            Resources.stomp_sounds.append(Sound(pyglet.resource.file("data/sounds/mech-stomp-%s.ogg" % i)))
