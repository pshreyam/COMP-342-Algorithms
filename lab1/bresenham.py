from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def plot(x, y):
    print(x, y)
    glVertex2f(x, y)


def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    x = x1
    y = y1

    plot(x, y)

    x_inc = -1 if dx < 0 else 1
    y_inc = -1 if dy < 0 else 1

    if dx < 0:
        dx = abs(dx)

    if dy < 0:
        dy = abs(dy)

    if dx > dy:
        p_k = 2*dy - dx

        for i in range(dx):
            x = x + x_inc
            if p_k < 0:
                plot(x, y)
                p_k += 2*dy
            else:
                y = y + y_inc
                plot(x, y)
                p_k += 2*dy - 2*dx
    else:
        p_k = 2*dx - dy

        for i in range(dy):
            y = y + y_inc
            if p_k < 0:
                plot(x, y)
                p_k += 2*dx
            else:
                x = x + x_inc
                plot(x, y)
                p_k += 2*dx - 2*dy


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-150.0, 150.0, -150.0, 150.0)


def plot_line():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.55, 0.19, 0.72)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    bresenham(10, 10, 10, 70)
    bresenham(10, 70, 70, 70)
    bresenham(70, 10, 70, 70)
    bresenham(10, 10, 70, 10)
    bresenham(10, 10, 70, 70)
    bresenham(10, 70, 70, 10)
    bresenham(10, 70, 40, 100)
    bresenham(70, 70, 40, 100)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Bresenham Line Drawing")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_line)
    clearScreen()
    glutMainLoop()

