import cocos
from pyglet.gl import *


class SingleLine(cocos.cocosnode.CocosNode):
    # from https://groups.google.com/d/msg/cocos-discuss/-Zco79IW9Sw/cfH5z7BjQJwJ
    def __init__(self, p1, p2, width=1.5, color=None):
        super(SingleLine, self).__init__()
        self.vertexes = [point_float(*p1), point_float(*p2)]
        if color is None:
            color = (255, 255, 255, 255)
        elif len(color) == 3:
            color = tuple(list(color).append(255))
        self.color = color
        self.width = width

    def draw(self):
        glPushMatrix()
        self.transform()
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(float(self.width))
        glBegin(GL_LINES)
        glColor4ub(*self.color)
        for v in self.vertexes:
            glVertex2f(*v)

        glEnd()
        glPopMatrix()


class LineDriftTo(cocos.actions.base_actions.IntervalAction):

    def __init__(self, dst_coords, duration=5):
        super(LineDriftTo, self).__init__()
        self.end_position = point_float(*dst_coords)
        self.duration = duration

    def start(self):
        self.start_position = self.target.vertexes[1]
        self.delta_x = self.end_position[0] - self.start_position[0]
        self.delta_y = self.end_position[0] - self.start_position[0]

    def update(self, t):
        self.target.vertexes[1] = point_float(self.start_position[0] + self.delta_x * t,
                                              self.start_position[1] + self.delta_y * t)


class LineDriftBy(LineDriftTo):

    def __init__(self, delta, duration=5):
        super(LineDriftBy, self).__init__(delta, duration)
        delta = point_float(*delta)
        self.delta_x = delta[0]
        self.delta_y = delta[1]

    def start(self):
        self.start_position = self.target.vertexes[1]
        self.end_position = point_float(self.delta_x, self.delta_y)


def point_float(x, y):
    return float(x), float(y)
