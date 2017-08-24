from graph import Graph, Node, SubGraph
from collections import deque

class MNAEdge():

    def __init__(self, n1, n2):
        self.conductance = 0
        self.n1 = n1
        self.n2 = n2

    def addStart(self, node):

        self.n1 = node

    def addEnd(self, node):

        self.n2 = node

class MNANode():

    def __init__(self, node):
        """
        
        :param node:
        :type node: Node
        """
        self.conductance = 0
        self.edges = []

    def addEdge(self, edge):
        """
        
        :param edge:
        :type edge: MNAEdge
        :return: None
        """
        if edge:
            self.edges.append(edge)


class MNA():

    def __init__(self, graph):
        """
        
        :param graph:
        :type graph: SubGraph
        """
        self.NormalGraph = graph
        self.nodes = []
        self.start = None

    def makeGraph(self):

        self.findStart()

        queue = deque()

        edge = MNAEdge()
        edge.addStart(self.start)
        self.start.addEdge(edge)
        queue.append((self.start, edge))

        while len(queue) > 0:
            ( node, edge ) = queue.popleft()

            if node.type == Node.res:
                if Node.res == 0:
                    pass # implement this
                edge.conductance += 1/Node.res

                queue.append( (node.adj[0], edge) )
                continue

            elif node.type == Node.volt:
                edge.addEnd(node)
                #self.

            elif node.type == Node.ground:



            for u in node.adj:
                edge = MNAEdge()
                edge.addStart(node)
                queue.append((u,edge))


    def findStart(self):
        node = self.NormalGraph.nodes[0]

        queue = deque()
        queue.append(node)
        while len(queue) > 0:
            node = queue.popleft()

            if node.type == Node.ground or node.type == Node.volt:
                self.start = node
                return







