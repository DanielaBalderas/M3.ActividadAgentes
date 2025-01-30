import pygame
import agentpy as ap
import numpy as np
import random

# Configuración de Pygame
WIDTH, HEIGHT = 1000, 800  
BACKGROUND_COLOR = (30, 30, 30)

# Colores
CAR_COLOR = (0, 0, 255)  
STOPPED_CAR_COLOR = (255, 255, 0)  
LIGHT_GREEN = (0, 255, 0)  
LIGHT_YELLOW = (255, 255, 0)  
LIGHT_RED = (255, 0, 0)  
POST_COLOR = (50, 50, 50)  # Color del poste del semáforo

# Configuración de calles e intersecciones
VERTICAL_LANES = [WIDTH // 5 * (i + 1) for i in range(3)]  
HORIZONTAL_STREETS = [HEIGHT // 4 * (i + 1) for i in range(3)]  

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Tráfico - Semáforos Mejorados")

# Clase de los semáforos
class TrafficLight(ap.Agent):
    def __init__(self, model, x_position, y_position, group, orientation):
        super().__init__(model)
        self.state = "red"
        self.timer = 0
        self.group = group  
        self.orientation = orientation  # "vertical" o "horizontal"
        self.cycle_duration = {'red': 10, 'green': 10, 'yellow': 2}
        self.x = x_position
        self.y = y_position

    def update(self, current_cycle):
        """ Cambia el estado de los semáforos según el ciclo sincronizado. """
        if self.group == current_cycle:
            if self.state == "red":
                self.state = "green"
            elif self.state == "green":
                self.state = "yellow"
            elif self.state == "yellow":
                self.state = "red"
        self.timer = 0  

# Clase de los vehículos
class Vehicle(ap.Agent):
    def __init__(self, model, x_position, y_position):
        super().__init__(model)
        self.speed = random.randint(2, 4)
        self.sensor_range = 60
        self.stop_distance = 35
        self.stopped = False
        self.x = x_position
        self.y = y_position
        self.direction = "up"  

    def move(self):
        if not self.stopped:
            if self.direction == "up":
                self.y -= self.speed
            elif self.direction == "right":
                self.x += self.speed

    def brake(self):
        self.stopped = True

    def release_brake(self):
        self.stopped = False

    def detect_obstacle(self, vehicles):
        for other_vehicle in vehicles:
            if other_vehicle is not self and abs(other_vehicle.y - self.y) < self.stop_distance and other_vehicle.x == self.x:
                self.brake()
                return
        self.release_brake()

    def interact_with_traffic_light(self, traffic_light):
        if traffic_light.state == "red" and abs(traffic_light.y - self.y) < self.sensor_range and traffic_light.x == self.x:
            self.brake()
        elif traffic_light.state == "green":
            self.release_brake()

    def turn_at_intersection(self):
        """ Girar solo en intersecciones permitidas """
        if self.direction == "up" and self.y in HORIZONTAL_STREETS:
            if self.x in VERTICAL_LANES:  
                if random.random() < 0.5:  
                    self.direction = "right"

# Modelo de tráfico con semáforos bien ubicados
class TrafficModel(ap.Model):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.space = ap.Space(self, shape=(WIDTH, HEIGHT))
        self.t = 0
        self.current_cycle = 1  

        try:
            self.traffic_lights = []
            for x in VERTICAL_LANES:
                for y in HORIZONTAL_STREETS:
                    group = 1 if x in VERTICAL_LANES else 2
                    orientation = "vertical" if x in VERTICAL_LANES else "horizontal"
                    self.traffic_lights.append(TrafficLight(self, x, y, group, orientation))

            start_y = HEIGHT - 100
            separation = 100
            self.vehicles = [
                Vehicle(self, x_position=random.choice(VERTICAL_LANES), y_position=start_y - i * separation)
                for i in range(20)
            ]

        except Exception as e:
            print(f"❌ ERROR al crear agentes: {e}")
            raise

    def step(self):
        self.t += 1

        # Cambiar el ciclo de semáforos cada 12 pasos
        if self.t % 12 == 0:
            self.current_cycle = 2 if self.current_cycle == 1 else 1
            for light in self.traffic_lights:
                light.update(self.current_cycle)

        for vehicle in self.vehicles:
            vehicle.detect_obstacle(self.vehicles)
            for light in self.traffic_lights:
                vehicle.interact_with_traffic_light(light)
            vehicle.turn_at_intersection()
            vehicle.move()

# Dibujar la simulación en Pygame con postes de semáforo bien ubicados
def draw_simulation(model):
    screen.fill(BACKGROUND_COLOR)

    # Dibujar calles
    for lane in VERTICAL_LANES:
        pygame.draw.rect(screen, (50, 50, 50), (lane - 20, 0, 40, HEIGHT))
    for street in HORIZONTAL_STREETS:
        pygame.draw.rect(screen, (50, 50, 50), (0, street - 10, WIDTH, 20))

    # Dibujar semáforos con postes
    for light in model.traffic_lights:
        if light.state == "green":
            color = LIGHT_GREEN
        elif light.state == "yellow":
            color = LIGHT_YELLOW
        else:
            color = LIGHT_RED

        if light.orientation == "vertical":
            pygame.draw.line(screen, POST_COLOR, (light.x + 10, light.y - 15), (light.x + 10, light.y + 25), 5)
            pygame.draw.circle(screen, color, (light.x + 10, light.y), 15)
        else:
            pygame.draw.line(screen, POST_COLOR, (light.x - 15, light.y - 10), (light.x + 25, light.y - 10), 5)
            pygame.draw.circle(screen, color, (light.x, light.y - 10), 15)

    # Dibujar vehículos
    for vehicle in model.vehicles:
        car_color = STOPPED_CAR_COLOR if vehicle.stopped else CAR_COLOR
        pygame.draw.rect(screen, car_color, (vehicle.x - 20, vehicle.y, 40, 20))

    pygame.display.update()

# Configuración del modelo
parameters = {
    'steps': 150
}

print("🟢 Creando modelo de tráfico con semáforos bien ubicados...")
model = TrafficModel(parameters)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    model.step()
    draw_simulation(model)

    if model.t >= parameters['steps']:
        print("✅ Simulación finalizada.")
        running = False

    clock.tick(10)

pygame.quit()
