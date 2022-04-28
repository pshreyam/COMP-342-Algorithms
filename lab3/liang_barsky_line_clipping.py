from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from clippers import ClippingWindow


start_point, end_point = [0, 120], [130, 5]
# start_point, end_point = [200, 220], [230, 205]
clipper = ClippingWindow(10, 150, 10, 100)


def key_pressed(key, *args):
    global start_point, end_point
    if key == b'c':
        result = clipper.liam_barsky_clip(start_point, end_point)
        if result:
            start_point, end_point = result
        else:
            print("The line is rejected!")


def clear_screen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-500.0, 500.0, -500.0, 500.0)


def draw_lines():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(*start_point)
    glVertex2f(*end_point)
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

    draw_axes_and_clipping_window()
    draw_lines()

    glutPostRedisplay()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Liam Barsky Line Clipping")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot)
    glutKeyboardFunc(key_pressed)
    clear_screen()
    glutMainLoop()
