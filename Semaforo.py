from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos

class TrafficLightAgent:
    def __init__(self, x, y, width=20, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = "red"  # Estado inicial del semáforo (rojo)

    def draw(self):
        # Fondo del semáforo (negro)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Luz del semáforo según el estado
        if self.state == "red":
            glColor3f(1.0, 0.0, 0.0)  # Rojo
        elif self.state == "green":
            glColor3f(0.0, 1.0, 0.0)  # Verde

        # Dibujar luz como un círculo
        glBegin(GL_POLYGON)
        for i in range(360):
            angle = i * 3.14159 / 180
            glVertex2f(
                self.x + self.width / 2 + (self.width / 4) * cos(angle),
                self.y + self.height / 2 + (self.width / 4) * sin(angle)
            )
        glEnd()

    def change_state(self, new_state):
        """Cambia el estado del semáforo (red, yellow, green)."""
        if new_state in ["red", "green"]:
            self.state = new_state
