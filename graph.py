from graphics import *
from grapher import *
import sys, pygame
from tkinter import *
import os

arrow = pygame.image.load("arrow.png")

class Node():
    r = 10
    def __init__(self, x, y, type = "line"):
        self.p = (x,y)
        self.type = type
        self.circle = None
        self.adj = []
        self.nodes = {}
        self.r = 10
        self.highlight = False

        self.setType(type)
        # elif self.type == "volt":
        #   pass

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.p, self.r, 0)

        if self.highlight:
            pygame.draw.circle(screen, pygame.Color(0,255,0), self.p, self.r+2, 2)
            self.highlight = False # maybe move this


        for node in self.adj:
            pygame.draw.line(screen, pygame.Color(0,0,0), self.p, node.p)

            v = (node.p[0] - self.p[0], node.p[1] - self.p[1])
            rotated = pygame.transform.rotate(arrow, -math.degrees(math.atan2(v[1], v[0])) )
            #p = ( node.p[0] - arrow_rect.width/2 ,  node.p[0] - arrow_rect.height/2)
            screen.blit(rotated, node.p)

    def setType(self, type):
        self.color = pygame.Color(0, 255, 0, 255)
        self.type = type

        if self.type == "res":
            self.r = 10
            self.color = pygame.Color(255, 0, 0, 255)

        elif self.type == "line":
            self.r = 3
            self.color = pygame.Color(0, 0, 0, 255)

        elif self.type == "ground":
            self.r = 10
            self.color = pygame.Color(0, 255, 255, 255)

        elif self.type == "volt":
            self.r = 10
            self.color = pygame.Color(255, 255, 0, 255)


    def add(self, n):
        if n not in self.nodes:
            self.adj.append(n)
            self.nodes[n] = len(self.adj) -1

    def deleteMe(self):
        """ very very expensive """
        for node in self.adj:
            node.delete(self)

    def delete(self, n):
        i = self.nodes[n]
        self.nodes[n] = None

        aux = []
        auxDict = {}
        j = 0
        for node in self.adj:
            if i == j: continue
            aux.append(node)
            auxDict[n] = len(aux) - 1
            j += 1

        self.adj = aux
        self.auxDict = auxDict



class Graph():

    def __init__(self, height, width):
        self.initTK(height, width)

        self.state = "a"
        self.adding_state = "l"
        """
            S - select nodes
                G - make node ground
                V - mke node voltage
            A - add nodes
                l - line nodes
                R - resistance
            C - check
        """
        self.nodes = []
        self.activeNode = None
        self.highlightNode = None
        self._dist = 15**2
        self._selected = False

        self._voltageNode = None
        self._groundNode = None


    def initTK(self,height, width):

        self.root = Tk()
        self.root.title = "Data"
        embed = Frame(self.root, width=640, height=480)
        embed.grid(row=0, column=2)
        playpausebutton = Button(self.root, text="Play/Pause")
        playpausebutton.grid(row=1, column=2)
        self.root.update()

        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        print (str(embed.winfo_id()))
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.screen = pygame.display.set_mode((height, width))
        pygame.display.flip()



    def gameLoop(self):
        white = pygame.Color(255,255,255)
        while True: # game loop
            #print(pygame.event.get())
            events = pygame.event.get()
            if len(events) > 0:
                print (events)

            self.screen.fill(white)
            self.drawActive()
            self.drawNodes()
            if self.state == "a":
                self.eventsAdd()
            elif self.state == "s":
                self.eventsSelect()

            pygame.display.flip()
            self.root.update()
            #tk.update()


    def eventsAdd(self):
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    self.state = 's'

                elif event.key == pygame.K_r:
                    self.adding_state = 'r'

                elif event.key == pygame.K_l:
                    self.adding_state = 'l'

                return

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.highlightNode:
                    self.activeNode.add(self.highlightNode)
                    self.activeNode = self.highlightNode
                    return
                else:
                    self._selected = False
                    self.addNode(pos)

                return


            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.searchHighlight(pos)


    def eventsSelect(self):
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.state = "a"

                elif event.key == pygame.K_z:
                    self.activeNode.deleteMe()
                    self.nodes.pop()
                    self.activeNode = self.nodes[-1]

                elif event.key == pygame.K_g:
                    if self._groundNode:
                        self._groundNode.setType( "line" )

                    self._groundNode = self.activeNode
                    self._groundNode.setType( "ground" )

                elif event.key == pygame.K_v:
                    if self._voltageNode:
                        self._voltageNode.setType( "line" )

                    self._voltageNode = self.activeNode
                    self._voltageNode.setType( "volt" )



            elif event.type == pygame.MOUSEBUTTONUP:
                self._selected = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.highlightNode:
                    self._selected = True
                    self.highlightNode.p = pygame.mouse.get_pos()
                    self.activeNode = self.highlightNode

            elif event.type == pygame.MOUSEMOTION:

                if self._selected:
                    self.highlightNode.p = pygame.mouse.get_pos()
                else:
                    pos = pygame.mouse.get_pos()
                    self.searchHighlight(pos)

    def checkEvent(self):
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    """ to state ressistance """
                    self.state = "r"

                if event.key == pygame.K_l:
                    self.state = "l"

                if event.key == pygame.K_z:
                    self.activeNode.deleteMe()
                    self.nodes.pop()
                    self.activeNode = self.nodes[-1]

            elif event.type == pygame.MOUSEBUTTONUP:
                self._selected = False
                pos = pygame.mouse.get_pos()
                if not self.highlightNode:
                    self.addNode(pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.highlightNode:
                    self._selected = True
                    self.highlightNode.p = pygame.mouse.get_pos()
                    self.activeNode = self.highlightNode

            elif event.type == pygame.MOUSEMOTION:

                if self._selected:
                    self.highlightNode.p = pygame.mouse.get_pos()
                else:
                    pos = pygame.mouse.get_pos()
                    self.searchHighlight(pos)




    def searchHighlight(self, pos):

        if not self._selected:
            for node in self.nodes:
                if self.distSqrt(node.p, pos) < self._dist:
                    self.highlightNode = node
                    self.highlightNode.highlight = True
                    return

            if self.highlightNode:
                self.highlightNode.highlight = False
                self.highlightNode = None


    def distSqrt(self, p1, p2):
        return ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2)

    def drawNodes(self):
        for n in self.nodes:
            n.draw(self.screen)


    def addNode(self, pos):

        n = None

        if self.adding_state == "r":
            n = Node(pos[0],pos[1], "res")
            self.nodes.append( n )

        elif self.adding_state == "l":
            n = Node(pos[0],pos[1], "line")
            self.nodes.append( n )

        if self.activeNode:
            self.activeNode.add(n)
        self.activeNode = n

    def drawActive(self):

        if self.activeNode:
            pygame.draw.circle(self.screen, pygame.Color(0,0,255,255), self.activeNode.p, 15)

if __name__ == "__main__":
    pygame.init()
    graph = Graph(700,700)
    arrow_rect = arrow.get_rect()

    graph.gameLoop()