from graphics import *
from grapher import *
from tkinter import *
from tkpanel import *
import numpy as np
from collections import deque
import  Edge
from Node import Node

class Drawing():

    canvas = None

    @staticmethod
    def init(canvas):
        """
        
        :param canvas: the canvas where is the graph
        :type canvas: Canvas
        :return: 
        """
        Drawing.canvas = canvas


    @staticmethod
    def circle(p, r, color):
        return Drawing.canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill=color)

    @staticmethod
    def line(p1, p2, color = "#000000"):
        return Drawing.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)


class SubGraph():

    def __init__(self):
        self.nodes = []
        self.varCount = 0

    def addNode(self, n, outdegree):
        """
        
        :param n: a node in the subgraph
        :type n: Node
        :param outdegree: number of edeges coming out of the node
        :type outdegree: int
        :return: None
        """

        self.nodes.append(n)
        if outdegree > 0:
            self.varCount += outdegree - 1

    def __str__(self):
        return str(  [str(node) for node in self.nodes] )



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

        self.subGraphs = []


    def initTK(self,height, width):

        self.root = Tk()
        self.root.title = "Data"

        self.panel = Panel(self.root,
                           self.toLine,
                           self.toRes,
                           self.toVoltage,
                           self.toGround,
                           self.delete,
                           subGraphs=self.getSubGraphs)

        self.canvas = Canvas(self.root, width=width, height=height,relief='ridge',bd=1)
        self.canvas.grid(row=0,column=1)

        Drawing.init(self.canvas)
        Edge.Edge.init(Drawing)
        Node.init(Drawing)

        self.root.update()
        self.bindEvents()

    def setCurrents(self):

        for graph in self.subGraphs:
            pass

    def getSubGraphs(self):
        """ makes all the different graphs"""

        self.subGraphs = []
        visited = {}
        queue = deque()

        for s in self.nodes:

            if s not in visited:
                subGraph = SubGraph()
                self.subGraphs.append(subGraph)
            else:
                continue

            queue.append(s)

            while len (queue) > 0:
                outDegree = 0
                node = queue.popleft()
                if node in visited:
                    continue

                for u in node.adj:
                    if u not in visited:
                        outDegree += 1
                        queue.append(u)


                subGraph.addNode(node, outDegree)
                visited[node] = True

    def toLine(self):
        if self.activeNode:
            self.activeNode.setType("line")

    def toRes(self):
        if self.activeNode:

            self.activeNode.setType("res")
            inVal = self.panel.valueTB.get()

            if str.isnumeric(inVal):
                self.activeNode.value = int(inVal)

    def toVoltage(self):
        if self.activeNode:

            self.activeNode.setType("volt")
            inVal = self.panel.valueVoltTB.get()

            if str.isnumeric(inVal):
                self.activeNode.value = int(inVal)

    def toGround(self):
        if self.activeNode:
            self.activeNode.setType("ground")
            self._groundNode = self.activeNode

    def delete(self):
        if self.activeNode:
            self.activeNode.deleteMe()
            newList = []
            for node in self.nodes:
                if node == self.activeNode:
                    continue
                newList.append(node)

            self.nodes = newList

            if len(self.nodes) > 0:
                self.activeNode = self.nodes[-1]
                self.panel.update(self.activeNode)
            else:
                self.activeNode = None


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
            self.panel.update(self.activeNode)
            return True

        self.panel.update(self.activeNode)
        return False


    def add(self,pos):

        if not self.highlightNode:
            #self.searchHighlight(pos)
            self.addNode( pos )
        else:
            self.activeNode.add(self.highlightNode)
            self.activeNode.unselected()
            self.activeNode = self.highlightNode

    def gameLoop(self):

        while True:
            if self.activeNode:
                self.activeNode.selected("#00ff00")
            self.searchHighlight(self.pos)
            self.root.update_idletasks()
            self.root.update()

    def getNumVars(self):
        pass

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

        if self.adding_state == "r":
            n = Node(pos[0],pos[1], "res")
            self.nodes.append( n )

        elif self.adding_state == "l":
            n = Node(pos[0],pos[1], "line")
            self.nodes.append( n )

        if self.activeNode:
            self.activeNode.unselected()
            self.activeNode.add(n)

        self.activeNode = n

        self.panel.update(self.activeNode)

if __name__ == "__main__":
    graph = Graph(700,700)

    graph.gameLoop()