from tkinter import *
import graph
from Node import Node

class Edge():

    Drawing = None

    @staticmethod
    def init(Drawing):
        """ 
        :param Drawing:
        :type Drawing: graph.Drawing
        """
        Edge.Drawing = Drawing

    def __init__(self, n1, n2):
        """
        
        :param n1:
        :type n1: Node
        :param n2:
        :type n2: Node
        :param Drawing:
        :type Drawing: graph.Drawing
        """
        self.n1 = n1
        self.n2 = n2
        self.isDelted = False
        self.line = Edge.Drawing.line(n1.p, n2.p)

    def move(self):
        Edge.Drawing.canvas.coords( self.line, [self.n1.p[0], self.n1.p[1], self.n2.p[0], self.n2.p[1]] )

    def delete(self):
        self.isDelted = True
        Edge.Drawing.canvas.delete(self.line)