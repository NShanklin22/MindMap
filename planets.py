import pygame
import math

# Initialize pygame
pygame.init()

# Set the initial variables
WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (190,0,0)
DARK_GREY = (190,190,190)

FONT = pygame.font.SysFont('comicsans',16)

class Planet:
    AU = 149.6e6*1000
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100 px
    TIMESTEP = 3600*24 # 1 Day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    # Function that draws the object onto the screen
    def draw(self,win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 15:
            UpdatedPoints = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                UpdatedPoints.append((x,y))

            pygame.draw.lines(win, self.color, False, UpdatedPoints[int(len(UpdatedPoints)-len(UpdatedPoints)/2):], 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE)
            win.blit(distance_text,(x,y))

        pygame.draw.circle(win,self.color, (x,y), self.radius)

    # Calculate the force of attraction between two objects
    def attraction(self, other):
        other_x,other_y = other.x,other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta) *force
        force_y = math.sin(theta) * force
        return force_x,force_y

    # Update the position of the object
    def updatePosition(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y))


# Define the main function
def main():
    run = True
    # Set the maximum speed of the clock
    clock = pygame.time.Clock()

    # Create the sun
    sun = Planet(0,0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0,12,RED,6.39*10**23)
    mars.y_vel = 24.077 * 1000


    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 *10**23)
    mercury.y_vel = 47.4 * 1000


    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 3.30 *10**23)
    venus.y_vel = -35.02 * 1000


    planets = [sun,earth,mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        for planet in planets:
            planet.updatePosition(planets)
            planet.draw(WIN)


        pygame.display.update()


    pygame.quit()

main()