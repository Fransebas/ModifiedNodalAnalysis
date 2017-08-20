from graphics import *
from grapher import *
from tkinter import *
from tkpanel import *
import os

class Drawing():

    canvas = None

    @staticmethod
    def init(canvas):
        Drawing.canvas = canvas

    @staticmethod
    def circle(p, r, color):
        return Drawing.canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill=color)

    @staticmethod
    def line(p1, p2, color = "#000000"):
        return Drawing.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)


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

        self.inLineP = None # point of the line that enters
        self.outLineP = None # point of the line that goes out
        self.inLine = []
        self.outLine = []

        self.color = "#000000"

        self.value = None

        self.circle = Drawing.circle(self.p, self.r, self.color)

        self.setType(type)
        # elif self.type == "volt":
        #   pass

    """def draw(self):



        pygame.draw.circle(screen, self.color, self.p, self.r, 0)

        if self.highlight:
            pygame.draw.circle(screen, pygame.Color(0,255,0), self.p, self.r+2, 2)
            self.highlight = False # maybe move this


        for node in self.adj:
            pygame.draw.line(screen, pygame.Color(0,0,0), self.p, node.p)

            v = (node.p[0] - self.p[0], node.p[1] - self.p[1])
            rotated = pygame.transform.rotate(arrow, -math.degrees(math.atan2(v[1], v[0])) )
            #p = ( node.p[0] - arrow_rect.width/2 ,  node.p[0] - arrow_rect.height/2)
            screen.blit(rotated, node.p)"""

    def setType(self, type):

        self.color = "#00ff00"
        self.type = type
        self.value = None

        if self.type == "res":
            self.value = 0
            self.r = 10
            self.color = "#ff0000"

        elif self.type == "line":
            self.r = 3
            self.color = "#000000"

        elif self.type == "ground":
            self.r = 10
            self.color = "#00ffff"

        elif self.type == "volt":
            self.value = 0
            self.r = 10
            self.color = "#ffff00"

        Drawing.canvas.itemconfig(self.circle, fill=self.color, width=0)

    def selected(self, color="#ff00ff"):
        Drawing.canvas.itemconfig(self.circle, outline=color, width=4)

    def unselected(self):
        Drawing.canvas.itemconfig(self.circle, width=0)

    def add(self, n):

        if n not in self.nodes:
            self.adj.append(n)
            line = Drawing.line(self.p, n.p)
            self.outLine.append(line)
            n.inLine.append(line)
            self.nodes[n] = len(self.adj) -1

    def move(self, p2):
        Drawing.canvas.move(self.circle, p2[0] - self.p[0],  p2[1] - self.p[1])

        self.p = p2

        """ Check this method for the data tkinter uses"""
        for line in self.inLine:
            points = Drawing.canvas.coords(line)
            points[2], points[3] = self.p[0], self.p[1]
            Drawing.canvas.coords(line, points)

        for line in self.outLine:
            points = Drawing.canvas.coords(line)
            points[0], points[1] = self.p[0], self.p[1]
            Drawing.canvas.coords(line, points)

    def deleteMe(self):
        """ very very expensive """
        Drawing.canvas.delete(self.circle)

        for line in self.inLine:
            Drawing.canvas.delete(self.line)

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

        self._eventCountBuffer = 0

        self.pos = (0,0)


    def initTK(self,height, width):

        self.root = Tk()
        self.root.title = "Data"

        self.panel = Panel(self.root)

        self.canvas = Canvas(self.root, width=width, height=height,relief='ridge',bd=1)
        self.canvas.grid(row=0,column=2)

        Drawing.init(self.canvas)

        self.root.update()
        self.bindEvents()



    def updateNode(self):

        if self.activeNode:

            self.activeNode.setType(self.typeTB.get())

            if self.activeNode.type == "res":
                if str.isnumeric(self.valueTB.get()):
                    self.activeNode.value = int (self.valueTB.get())
                else:
                    self.activeNode.value = 0

    def updateNodeInfo(self):

        if self.activeNode:

            value = "0"
            if self.activeNode.value is not None:
                value = str( self.activeNode.value )

            type = self.activeNode.type

            self.nodeTypeLabel.config(text=type)
            self.typeTB.delete(0, END)
            self.typeTB.insert(0, type)

            self.valueTB.delete(0, END)
            self.valueTB.insert(0, value )

    def bindEvents(self):
        self.root.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.mouse)
        self.canvas.bind('<Motion>', self.getPos)
        self.canvas.bind('<B1-Motion>', self.clickMove)
        self.canvas.bind('<ButtonRelease-1>', self.clickRelease)

    def clickMove(self,event):
        self.pos = (event.x, event.y)
        if self._selected:
            self.activeNode.move(self.pos)

    def getPos(self, event):
        self.pos = (event.x, event.y)


    def key(self,event):
        print ( "pressed", repr(event.char) )

        if self.state == "s": # select state
            if event.char == "a":
                self.state = "a"
                return
            elif event.char == "G":
                pass

        elif self.state == "a": # add state

            if event.char == "s":
                self.state = "s"
                return
            elif event.char == "l":
                self.adding_state = "l"
            elif event.char == "r":
                self.adding_state = "r"

    def clickRelease(self, event):
        self._selected = False

    def mouse(self,event):
        pos = (event.x, event.y)

        if self.state == "s": # select state
            self._selected = self.select(pos)

        elif self.state == "a": # add state
            self.add(pos)


    def select(self, pos):

        if self.highlightNode:
            self.activeNode.unselected()
            self.activeNode = self.highlightNode
            self.updateNodeInfo()
            return True

        self.updateNodeInfo()
        return False


    def add(self,pos):

        if not self.highlightNode:
            #self.searchHighlight(pos)
            self.addNode( pos )
        else:
            self.activeNode.add(self.highlightNode)
            self.activeNode = self.highlightNode

    def gameLoop(self):

        while True:
            if self.activeNode:
                self.activeNode.selected("#00ff00")
            self.searchHighlight(self.pos)
            self.root.update_idletasks()
            self.root.update()

    def searchHighlight(self, pos):

        if not self._selected:
            for node in self.nodes:
                if self.distSqrt(node.p, pos) < self._dist:
                    self.highlightNode = node
                    self.highlightNode.highlight = True
                    self.highlightNode.selected()
                    return

            if self.highlightNode:
                self.highlightNode.highlight = False
                self.highlightNode.unselected()
                self.highlightNode = None


    def distSqrt(self, p1, p2):
        return ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2)

    def addNode(self, pos):

        n = None

        if self.activeNode:
            self.activeNode.unselected()

        if self.adding_state == "r":
            n = Node(pos[0],pos[1], "res")
            self.nodes.append( n )

        elif self.adding_state == "l":
            n = Node(pos[0],pos[1], "line")
            self.nodes.append( n )

        if self.activeNode:
            self.activeNode.add(n)

        self.activeNode = n

        self.updateNodeInfo()

if __name__ == "__main__":
    graph = Graph(700,700)

    graph.gameLoop()