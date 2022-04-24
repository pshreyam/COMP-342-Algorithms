from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from transform2d import Transformation, plot_triangle


base = [[-50, -250], [50, -250], [0, 0]]
blades = [[0, 0], [70, 0], [70, -40]]

rotation_angle = 10


def run_when_idle():
    global blades, rotation_angle
    blades = Transformation(blades).rotation(rotation_angle)
    glutPostRedisplay()


def key_pressed(key, *args):
    global rotation_angle
    if key == b'i':
        """Increase the speed of the blades rotation!"""
        if rotation_angle <= 50:
            rotation_angle += 10
    if key == b'd':
        """Decrease the speed of the blades rotation!"""
        if rotation_angle >= 20:
            rotation_angle -= 10


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-500.0, 500.0, -500.0, 500.0)


def plot_transform():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.1, 0.1, 0.1)
    glPointSize(3.0)

    glBegin(GL_POLYGON)
    plot_triangle(base)
    glEnd()

    glColor3f(0.1, 0.7, 0.1)
    glBegin(GL_POLYGON)
    plot_triangle(blades)
    glEnd()

    transformed_coordinates = Transformation(blades)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.rotation(120))
    glEnd()

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.rotation(240))
    glEnd()

    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Windmill")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_transform)
    glutIdleFunc(run_when_idle)
    glutKeyboardFunc(key_pressed)
    clearScreen()
    glutMainLoop()
