from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class CarAgent:
    def __init__(self, x, y, width=40, height=20, color=(0.0, 0.0, 1.0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        glColor3f(*self.color)  # Color del coche
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def move(self, dx, dy):
        """Mueve el coche en la dirección indicada."""
        self.x += dx
        self.y += dy
