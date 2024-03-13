import pygame
from functions import wrap_text

class Vector :

    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z
    
    def __add__ (self, other) :
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) :
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def Copy (self) :
        return Vector(self.x, self.y, self.z)
            
class Camera :

    def __init__(self, x, y, z) :
        self.position = Vector(x, y, z)
    
    def add (self, vector) :
        self.position += vector
    
    def transform (self, point) :
        return [(point[0] + self.position.x) * self.position.z, (point[1] + self.position.y) * self.position.z]
    
    # def deltaTransform (self, point) :
    #     return [(point[0] + self.delta.x), (point[1] + self.delta.y)]

class Grid :

    def __init__(self, width, height, cellSize, screen, color) :
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.color = color
        self.screen = screen
        self.points = []
        for x in range(0, int(self.width), self.cellSize):
            for y in range(0, int(self.height), self.cellSize):
                self.points.append([x - (self.width/2), y - (self.height/2)])

    def draw (self) :
        for point in self.points :
            pygame.draw.circle(self.screen, self.color, point, 2)
    
    def update (self, camera) :
        # if camera.position.z != 1 :
        #     stepSize = self.cellSize
        #     self.cellSize = self.cellSize * camera.position.z
        #     X = generate_list(math.ceil(self.width/self.cellSize), stepSize)
        #     Y = generate_list(math.ceil(self.height/self.cellSize), stepSize)
        #     self.points = [camera.deltaTransform([x, y]) for x in X for y in Y]
        #     camera.delta.x *= camera.delta.z
        #     camera.delta.y *= camera.delta.z
        #     camera.delta.z = 1
        # movedPoints = [camera.transform(point) for point in self.points]
        # self.points = bounds(movedPoints, self.width, self.height, self.boundaryX, self.boundaryY)
        self.points = [camera.transform(point) for point in self.points]

class textbox :

    def __init__(self, x: int, y: int, textColor: str, color: str, borderColor: str, screen: object, font: int, title="", text="") :
        self.x = x
        self.y = y
        self.textColor = textColor
        self.color = color
        self.borderColor = borderColor
        self.text = text
        self.fontSize = font
        self.screen = screen
        self.title = title
        self.width = 5 * 50
        self.height = 4 * 50
    
    def set_dimensions (self) :
        self.font = pygame.font.Font(None, self.fontSize)
        if self.font.size(self.text)[0] + 2 >= self.width :
            lines = wrap_text(self.text, self.font, self.width - 4)
            y = self.y + 2
            for line in lines:
                y += self.font.get_linesize()
            self.height = min(y - self.y, 4 * 50)
        else:
            lines = wrap_text(self.text, self.font, self.width - 2)
            y = self.y + 2
            for line in lines:
                y += self.font.get_linesize()
            self.height = min(y - self.y, 4 * 50)
        self.width = min(self.font.size(self.text)[0] + 2, 5 * 50)
    
    def draw (self) :
        self.set_dimensions()
        self.title_font = pygame.font.Font(None, self.fontSize)
        self.title_text = self.title_font.render(self.title, True, self.textColor)
        pygame.draw.rect(self.screen, self.borderColor, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.color, (self.x+1, self.y+1, self.width-2, self.height-2))
        if self.font.size(self.text)[0] + 2 >= self.width :
            lines = wrap_text(self.text, self.font, self.width - 4)
            y = self.y + 2
            for line in lines:
                text = self.font.render(line, True, self.textColor)
                self.screen.blit(text, (self.x+4, y))
                y += self.font.get_linesize()
        else:
            lines = wrap_text(self.text, self.font, self.width - 2)
            y = self.y + 2
            for line in lines:
                text = self.font.render(line, True, self.textColor)
                self.screen.blit(text, (self.x+2, y))
                y += self.font.get_linesize()
        self.screen.blit(self.title_text, (self.x + (self.width - self.title_font.size(self.title)[0]) / 2, self.y - self.title_font.get_linesize()))
    
    def update (self, camera) :
        (self.x, self.y) = camera.transform([self.x, self.y])
        self.width *= camera.position.z
        self.height *= camera.position.z
        # self.fontSize = int(self.fontSize * camera.possition.z)

class Edge :

    def __init__(self, source, target) :
        self.source = source
        self.target = target

class Graph :

    def __init__(self, screen) :
        self.nodes = {}
        self.connections = []
        self.screen = screen
    
    def addNode (self, node) :
        self.nodes[node.title] = node
    
    def addConnection (self, node1, node2) :
        self.connections.append(Edge(node1, node2))
     
    def draw (self) :
        for edge in self.connections :
            source = self.nodes[edge.source]
            target = self.nodes[edge.target]
            pygame.draw.line(
                self.screen, "red", 
                (source.x+(source.width/2), source.y), 
                (target.x+(target.width/2), target.y), 
                1
            )
        for i in self.nodes.keys() :
            self.nodes[i].draw()
    
    def update (self, camera) :
        for i in self.nodes.keys() :
            self.nodes[i].update(camera)
        