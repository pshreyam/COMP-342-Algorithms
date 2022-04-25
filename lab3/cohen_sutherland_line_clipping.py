import itertools

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class ClippingWindow:
    def __init__(self, xw_min, xw_max, yw_min, yw_max):
        self.xw_min = xw_min
        self.xw_max = xw_max
        self.yw_min = yw_min
        self.yw_max = yw_max

    def get_endpoints(self):
        return [
            (self.xw_min, self.yw_min),
            (self.xw_max, self.yw_min),
            (self.xw_max, self.yw_max),
            (self.xw_min, self.yw_max),
        ]

    def get_region_code(self, point):
        x, y = point
        region_code = [y > self.yw_max, y < self.yw_min, x > self.xw_max, x < self.xw_min]
        region_code = list(map(lambda x: 1 if x else 0, region_code))
        return region_code

    def clip(self, start, end):
        x1, y1 = start
        x2, y2 = end

        rc_start = self.get_region_code(start)
        rc_end = self.get_region_code(end)

        rc_all_zero_start = all(x==0 for x in rc_start)
        rc_all_zero_end = all(x==0 for x in rc_end)

        if rc_all_zero_start and rc_all_zero_end:
            # The line is accepted!
            return start, end

        result_anding_codes = [x & y for x, y in zip(rc_start, rc_end)]

        if not all(x==0 for x in result_anding_codes):
            # The line is rejected!
            return False

        m = (y2 - y1) / (x2 - x1)

        if not rc_all_zero_start:
            rc_outside = rc_start
            other_point = end
        else:
            rc_outside = rc_end
            other_point = start

        if rc_outside[-1]:
            x = self.xw_min
            y = int(y1 + m * (x - x1))
            return self.clip([x, y], other_point)
        if rc_outside[-2]:
            x = self.xw_min
            y = int(y1 + m * (x - x1))
            return self.clip([x, y], other_point)
        if rc_outside[-3]:
            y = self.yw_min
            x = int(x1 + (y - y1) / m)
            return self.clip([x, y], other_point)
        if rc_outside[-4]:
            y = self.yw_max
            x = int(x1 + (y - y1) / m)
            return self.clip([x, y], other_point)


start_point, end_point = [0, 120], [130, 5]
clipper = ClippingWindow(10, 150, 10, 100)


def key_pressed(key, *args):
    global start_point, end_point
    if key == b'c':
        start_point , end_point = clipper.clip(start_point, end_point)


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-500.0, 500.0, -500.0, 500.0)


def plot_lines():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.1, 0.1, 0.1)

    glPointSize(2.0)

    # Drawing the axes
    glBegin(GL_LINES)
    glVertex2f(500, 0)
    glVertex2f(-500, 0)
    glVertex2f(0, 500)
    glVertex2f(0, -500)
    glEnd()

    glPointSize(5.0)

    glBegin(GL_LINES)
    clipping_window_endpoints = clipper.get_endpoints()
    for i in range(len(clipping_window_endpoints)):
        for point in (clipping_window_endpoints[i], clipping_window_endpoints[i-1]):
            glVertex2f(*point)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(*start_point)
    glVertex2f(*end_point)
    glEnd()
    glutPostRedisplay()
    glFlush()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Cohen Sutherland Line Clipping")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_lines)
    glutKeyboardFunc(key_pressed)
    clearScreen()
    glutMainLoop()
