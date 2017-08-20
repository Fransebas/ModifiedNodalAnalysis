from tkinter import *
from graph import Drawing, Node

class Edge():

    def __init__(self, n1, n2):
        """
        
        :param n1:
        :type n1: Node
        :param n2:
        :type n2: Node
        """
        self.nodes = {}
        self.nodes[n1] = n1
        self.nodes[n2] = n2
        self.line = Drawing.line(n1.p, n2.p)

    def move(self):
        Drawing.canvas.coords( self.line, [self.n1.p[0], self.n1.p[1], self.n2.p[0], self.n2.p[1]] )