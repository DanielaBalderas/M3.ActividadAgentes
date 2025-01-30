import agentpy as ap
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def render_scene(model):
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glLoadIdentity()

  # Dibujar los carros
  for car in model.cars:
    glPushMatrix()
    glTranslatef(car.position[0], car.position[1], 0)  # Mover a la posición del carro
    glColor3f(0, 0, 1)  # Color azul
    glutSolidSphere(0.2, 20, 20)  # Dibujar una esfera
    glPopMatrix()

  # Dibujar el semáforo
  glPushMatrix()
  glTranslatef(model.traffic_light.position[0], model.traffic_light.position[1], 0)  # Mover a la posición del semáforo
  if model.traffic_light.state == 'green':
    glColor3f(0, 1, 0)  # Color verde
  else:
    glColor3f(1, 0, 0)  # Color rojo
  glutSolidCube(0.3)  # Dibujar un cubo
  glPopMatrix()

  glutSwapBuffers()

class CarAgent(ap.Agent):

    def setup(self):
        # Inicializa las propiedades del carro, como velocidad, posición, etc.
        self.speed = 0
        self.position = (0, 0)  # Tupla (x, y)
        # ... otras propiedades ...

    def step(self):
        # Define el comportamiento del carro en cada paso de tiempo
        # Por ejemplo, mover el carro, cambiar su velocidad, etc.
        self.position = (self.position[0] + self.speed, self.position[1])  # Mover en el eje x
        # ... otras acciones ...

class TrafficLightAgent(ap.Agent):

    def setup(self):
        self.state = 'green'  # Estado inicial: verde
        self.position = (0, 0) #posicion del semaforo
        self.timer = 0
    
    def step(self):
        self.timer +=1
        if self.state == 'green' and self.timer == 10 :
          self.state = 'red'
          self.timer = 0
          
        elif self.state == 'red' and self.timer == 5:
          self.state = 'green'
          self.timer = 0

class MyModel(ap.Model):

    def setup(self):
        # Crea una lista de CarAgent en lugar de ap.Agent
        self.cars = ap.AgentList(self, 10, CarAgent) 
        self.traffic_lights = TrafficLightAgent(self)
        self.traffic_light.position = (5, 0)

    def step(self):
      for car in self.cars:
        # Llama a la función step de cada CarAgent
        if car.position[0] == self.traffic_light.position[0] and self.traffic_light.state == 'red':
          car.speed = 0

        elif car.position[0] == self.traffic_light.position[0] and self.traffic_light.state == 'green':
          car.speed = 1
        
        car.step()
      self.traffic_light.step()