from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def plot(point, center):
    x_c, y_c = center
    x, y = point

    points = [(x, y), (-x, y), (x, -y), (-x, -y)]

    for x, y in points:
         print(x+x_c, y+y_c)
         glVertex2f(x+x_c, y+y_c)


def ellipse(r_x, r_y, center):
    x_k, y_k = 0, r_y

    plot((x_k, y_k), center)

    p1k = (r_y ** 2) - ((r_x ** 2) * r_y) + ((1/4) * (r_x ** 2))
    p2k = (r_y ** 2) * ((x_k + 1/2) ** 2) + ((r_x ** 2) * ((y_k - 1) ** 2)) - (r_x ** 2) * (r_y ** 2)

    while 2 * (r_y ** 2) * x_k < 2 * (r_x ** 2) * y_k:
        x_k += 1

        if p1k < 0:
            plot((x_k, y_k), center)
            p1k += 2 * (r_y ** 2) * x_k + (r_y ** 2)
        else:
            y_k -= 1
            plot((x_k, y_k), center)
            p1k += 2 * (r_y ** 2) * x_k - 2 * (r_x ** 2) * y_k + (r_y ** 2)

    while y_k > 0:
        y_k -= 1

        if p2k < 0:
            x_k += 1
            plot((x_k, y_k), center)
            p2k += 2 * (r_y ** 2) * x_k - 2 * (r_x ** 2) * y_k + (r_x ** 2)
        else:
            plot((x_k, y_k), center)
            p2k += -2 * (r_x ** 2) * y_k + (r_x ** 2)


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-300.0, 300.0, -300.0, 300.0)


def plot_ellipse():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    ellipse(200, 100, (10, 10))
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Midpoint Ellipse Drawing")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_ellipse)
    clearScreen()
    glutMainLoop()
