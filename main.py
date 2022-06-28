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

FONT = pygame.font.SysFont('comicsans',25)
StandardRadius = 100
Center_x = WIDTH/2
Center_y = HEIGHT/2

class Cell:

    def __init__(self, x, y, radius, color, text, link = (Center_x,Center_y)):
        self.x = x
        self.y = y
        self.radius = StandardRadius
        self.color = color
        self.text = text
        self.link = link

    # Function that draws the object onto the screen
    def draw_cells(self, win):
        x = self.x
        y = self.y

        CellText = FONT.render(self.text, 15, (0,0,0))

        CellTextWidth = CellText.get_width()
        CellTextHeight = CellText.get_height()

        pygame.draw.circle(win,self.color, (x,y), self.radius)
        win.blit(CellText, (x - CellTextWidth/2 , y - CellTextHeight/2))

    def draw_links(self, win):
        x = self.x
        y = self.y

        links = []
        links.append((x , y ))
        links.append(self.link)

        pygame.draw.line(win, (0,0,0), links[0],links[1], 10)

    # Update the position of the object
    def updatePosition(self,planets):
        total_fx = total_fy = 0

# Define the main function
def main():
    global StandardRadius
    global Center_y
    global Center_x
    global WIDTH, HEIGHT

    run = True
    # Set the maximum speed of the clock
    clock = pygame.time.Clock()

    # Create the sun
    MainCell = Cell(Center_x,Center_y, StandardRadius, DARK_GREY, "Nate!")
    ProgrammingCell = Cell(WIDTH/2 - MainCell.radius*2,HEIGHT/2 - MainCell.radius*2, StandardRadius, RED  , "Programming", (MainCell.x,MainCell.y))

    cells = [MainCell, ProgrammingCell]

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        for cell in cells:
            cell.updatePosition(cells)
            cell.draw_links(WIN)

        for cell in cells:
            cell.updatePosition(cells)
            cell.draw_cells(WIN)

        pygame.display.update()


    pygame.quit()

main()