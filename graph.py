from graphics import *
from grapher import *
from tkinter import *
from tkpanel import *
import numpy as np
from collections import deque
import  Edge
from Node import Node
from GraphObjects import Power, Line, Resistance

from MNA import MNA

import States

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
        self.stateModule = States.State(self)

        self.initTK(height, width)

        self.state = "a"

        """
         state s - select and add lines
        """

        self.selectedObject = Power(self)
        self.selectedNode = None

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

        self.cableState = IntVar()
        self.panel = Panel(self,
                           self.root,
                           self.stateModule,
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

    def bindEvents(self):
        self.root.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.click) # click
        self.canvas.bind('<Motion>', self.getPos) # mouse move
        self.canvas.bind('<B1-Motion>', self.clickMove)
        self.canvas.bind('<ButtonRelease-1>', self.clickRelease)

    def clickMove(self,event):
        self.pos = (event.x, event.y)

        if self._selected:
            self.activeNode.move(self.pos)

    def getPos(self, event):
        self.pos = (event.x, event.y)

        if self.selectedObject:
            self.selectedObject.move(self.pos)


    def key(self,event):


        if event.char == "r":
            if self.selectedObject:
                self.selectedObject.rotate()

        #elif event.char == "s":

        return

    def clickRelease(self, event):
        pass

    def click(self,event):
        pos = (event.x, event.y)

        if self.state == "s": # select state
            self.select(pos)

        elif self.state == "a": # add state
            self.add()


    def select(self, pos):
        print("hi")
        if self.highlightNode:
            print("double hi")
            if self.highlightNode.type == Node.line:
                self.highlightNode.selected(self)
                return True

            else:
                self.panel.update(self.highlightNode)

        return False


    def add(self):
        if self.selectedObject:
             self.selectedObject.add()

        self.selectedObject = None

    def gameLoop(self):

        while True:
            #if self.activeNode:
            #    self.activeNode.selected("#00ff00")
            self.searchHighlight(self.pos)
            self.root.update_idletasks()
            self.root.update()

    def getNumVars(self):
        pass

    def searchHighlight(self, pos):

        if self.highlightNode:
            self.highlightNode.unhighlight()
            self.highlightNode = None

        for node in self.nodes:
            if  self.distSqrt(node.p, pos) < self._dist:
                node.highlight(self)
                return




    def distSqrt(self, p1, p2):
        return ((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2)

    def addNode(self):
        pass


    def solveGraph(self):
        MNAgraph = MNA(self)
        MNAgraph.solve()

if __name__ == "__main__":
    graph = Graph(700,700)

    graph.gameLoop()