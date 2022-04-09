import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from mid_point import circle
from bresenham import bresenham


portions = []


def pie_chart(center, radius):
    angles = [2 * math.pi * (portion/sum(portions)) for portion in portions]
    cumulative_angles = []

    for i, angle in enumerate(angles):
        if i == 0:
            cumulative_angles.append(angle)
        else:
            cumulative_angles.append(angle + cumulative_angles[-1])

    circle(center, radius)

    x_c, y_c = center

    for angle in cumulative_angles:
        x = round(x_c + radius * math.cos(angle))
        y = round(y_c + radius * math.sin(angle))
        bresenham(x_c, y_c, x, y)


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-150.0, 150.0, -150.0, 150.0)


def plot_line():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    pie_chart((10, 10), 50)
    glEnd()
    glFlush()


if __name__ == "__main__":
    portions = list(map(int, input("Enter the value of portions separated by a space: ").split()))
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Pie Chart Drawing")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_line)
    clearScreen()
    glutMainLoop()
