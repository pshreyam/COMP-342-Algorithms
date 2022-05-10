from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from clippers import ClippingWindow


vertices = [(-40, 70), (50, 175), (175, 60), (60, -40)]
# vertices = [(0, 0), (160, 0), (160, 200), (0, 200)]
# vertices = [(0, 0), (160, 0), (160, 5), (0, 5)]
clipper = ClippingWindow(10, 150, 10, 100)


def key_pressed(key, *args):
    global vertices
    if key == b'c':
        result = clipper.sutherland_hodgeman_clip(vertices)
        if result:
            vertices = result
        else:
            print("The ploygon is rejected!")


def clear_screen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-500.0, 500.0, -500.0, 500.0)


def draw_polygon():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()


def draw_axes_and_clipping_window():
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


def plot():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_polygon()
    draw_axes_and_clipping_window()

    glutPostRedisplay()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Sutherland Hodgeman Polygon Clipping")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot)
    glutKeyboardFunc(key_pressed)
    clear_screen()
    glutMainLoop()
