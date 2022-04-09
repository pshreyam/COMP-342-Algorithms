from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def plot(x, y):
    x, y = round(x), round(y)
    print(x, y)
    glVertex2f(x, y)


def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    plot(x1, y1)

    if dx == 0 and dy == 0:
        # Same point and start and end points
        return
    else:
        x = x1
        y = y1

        if abs(dx) > abs(dy):
            stepsize = abs(dx)
        else:
            stepsize = abs(dy)

        x_inc = dx / stepsize
        y_inc = dy / stepsize

        for _ in range(stepsize):
            x = x + x_inc
            y = y + y_inc
            plot(x, y)


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-150.0, 150.0, -150.0, 150.0)


def plot_line():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.55, 0.19, 0.72)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    dda(10, 10, 70, 10)
    dda(10, 10, 10, 70)
    dda(70, 10, 70, 70)
    dda(10, 70, 70, 70)
    dda(10, 10, 70, 70)
    dda(10, 70, 70, 10)
    dda(10, 70, 40, 100)
    dda(70, 70, 40, 100)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("DDA Line Drawing")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_line)
    clearScreen()
    glutMainLoop()
