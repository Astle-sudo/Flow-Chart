import random
import pygame
from text import graph
from classes import Grid, Camera, Vector, textbox, Graph

BOX_COLOR = 'purple'
SCREEN_COLOR = 'white'
GRID_COLOR = (200, 200, 200)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CELL_SIZE = 25

def createTextBox (x, y, screen, node) :
    return textbox (x, y, "black", "white", "black", screen, 20, node['title'], node['description'])

def setGraph (graph, screen, camera) :
    # X = 0
    # Y = -500
    count = 0
    G = Graph(screen)
    for i in graph.keys() :
        # if count == int(len(graph.keys())/2) :
        #     X += 400
        #     Y = -500
        Node = createTextBox(random.randint(-1200,1200),random.randint(-700, 700), screen, graph[i])
        Node.set_dimensions()
        G.addNode(Node)
        # Y += (Node.height + 100)
        for j in graph[i]["connections"] :
            G.addConnection(i, j)
        count += 1
    return G

def Draw (objects) :
    for i in objects :
        i.draw()

def update (objects, camera) :
    for ob in objects :
        ob.update(camera)
    camera.position = Vector(0, 0, 1)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
drag = False

camera = Camera(0, 0, 1)
G = setGraph(graph, screen, camera)
grid = Grid(SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5, CELL_SIZE, screen, GRID_COLOR)
 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_MINUS:
                camera.add(Vector(0, 0, -0.1))
            if event.key == pygame.K_EQUALS:
                camera.add(Vector(0, 0, 0.1))
            if event.key == pygame.K_c:
                camera.position = Vector(600, 350, 1)
            if event.key == pygame.K_EQUALS:
                camera.add(Vector(0, 0, 0.1))
        if event.type == pygame.MOUSEBUTTONDOWN:
            initial = pygame.mouse.get_pos()
            drag = True
        if event.type == pygame.MOUSEMOTION :
            if drag:
                current = pygame.mouse.get_pos()
                dx = current[0] - initial[0]
                dy = current[1] - initial[1]
                camera.add(Vector(dx, dy, 0))
                initial = current 
        if event.type == pygame.MOUSEBUTTONUP :
            drag = False

    screen.fill(SCREEN_COLOR)

    Draw([G])
    update([G], camera)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()




