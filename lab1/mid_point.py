from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def plot(point, center):
    x_c, y_c = center
    x, y = point

    points = [(x, y), (-x, y), (x, -y), (-x, -y), (y, x),
               (-y, x), (y, -x), (-y, -x)]

    for x, y in points:
         print(x+x_c, y+y_c)
         glVertex2f(x+x_c, y+y_c)


def circle(center, radius):
    p_k = 1 - radius

    x_k, y_k = 0, radius
    plot((x_k, y_k), center)

    while x_k < y_k:
        x_k = x_k + 1
        if p_k < 0:
            plot((x_k, y_k), center)
            p_k += 2*x_k + 1
        else:
            y_k = y_k - 1
            plot((x_k, y_k), center)
            p_k += 2*x_k - 2*y_k + 1


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-150.0, 150.0, -150.0, 150.0)


def plot_circle():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    circle((10, 0), 40)
    circle((10, 0), 30)
    circle((10, 0), 20)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Midpoint Circle Drawing")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_circle)
    clearScreen()
    glutMainLoop()
