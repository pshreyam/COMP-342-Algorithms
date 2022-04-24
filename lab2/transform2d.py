from math import sin, cos, radians

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Transformation:
    def __init__(self, coordinates):
        # Convert to homogeneous coordinates
        homogeneous_coordinates = [row + [1] for row in coordinates]
        self.homogeneous_coordinates_matrix = [list(coordinate) for coordinate in zip(*homogeneous_coordinates)]

    def translation(self, t_x, t_y):
        self.transformation_matrix = [
            [1, 0, t_x],
            [0, 1, t_y],
            [0, 0, 1]
        ]
        return self.transform()

    def rotation(self, angle):
        self.transformation_matrix = [
            [cos(radians(angle)), -sin(radians(angle)), 0],
            [sin(radians(angle)), cos(radians(angle)), 0],
            [0, 0, 1]
        ]
        return self.transform()

    def scaling(self, s_x, s_y):
        self.transformation_matrix = [
            [s_x, 0, 0],
            [0, s_y, 0],
            [0, 0, 1]
        ]
        return self.transform()

    def reflection_x(self):
        self.transformation_matrix = [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
        return self.transform()

    def reflection_y(self):
        self.transformation_matrix = [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        return self.transform()

    def shearing_x(self, sh_x):
        self.transformation_matrix = [
            [1, sh_x, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        return self.transform()

    def shearing_y(self, sh_y):
        self.transformation_matrix = [
            [1, 0, 0],
            [sh_y, 1, 0],
            [0, 0, 1]
        ]
        return self.transform()

    def transform(self):
        # Multiply the homogeneous coordinates matrix with the transformation matrix
        transformed_homogeneous_matrix = [[sum(a*b for a,b in zip(X_row, Y_col)) for Y_col in zip(*self.homogeneous_coordinates_matrix)] for X_row in self.transformation_matrix]

        # Converting to regular coordinates
        transformed_coordinates = [list(row) for row in zip(*transformed_homogeneous_matrix[:-1])]
        return transformed_coordinates


def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-500.0, 500.0, -500.0, 500.0)


def plot_triangle(coordinates):
    for coordinate in coordinates:
        glVertex2f(coordinate[0], coordinate[1])


def plot_transform():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.1, 0.1, 0.1)
    glPointSize(3.0)

    # Drawing the axes
    glBegin(GL_LINES)
    glVertex2f(500, 0)
    glVertex2f(-500, 0)
    glVertex2f(0, 500)
    glVertex2f(0, -500)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glPointSize(2.0)

    # Drawing the triangle
    coordinates = [[60, 40], [-10, 300], [200, 20]]

    glBegin(GL_POLYGON)
    plot_triangle(coordinates)
    glEnd()

    transformed_coordinates = Transformation(coordinates)

    # Rotation
    glColor3f(0.6, 0.6, 0.1)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.rotation(90))
    glEnd()

    # Reflection
    glColor3f(0.3, 0.8, 0.3)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.reflection_x())
    glEnd()

    # Scaling
    glColor3f(0.6, 0.6, 0.6)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.scaling(1.5, 1.5))
    glEnd()

    # Translation
    glColor3f(0.6, 0.1, 0.6)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.translation(-200, -350))
    glEnd()

    # Shearing
    glColor3f(0.1, 0.6, 0.6)

    glBegin(GL_POLYGON)
    plot_triangle(transformed_coordinates.shearing_x(1.5))
    glEnd()

    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutCreateWindow("Transformation of 2D object")
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 50)
    glutDisplayFunc(plot_transform)
    clearScreen()
    glutMainLoop()
