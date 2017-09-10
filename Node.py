import Edge
import graph
#import GraphObjects

class Node():

    Drawing = None
    count = 0

    res = "res"
    line = "line"
    ground = "gruond"
    volt = "volt"

    @staticmethod
    def init(Drawing):
        Node.Drawing = Drawing

    r = 10
    def __init__(self, x, y, graphObject ,type="line"):
        """
        
        :param x: x coordinate
        :type x: float
        :param y: y coordinate
        :type y: float
        :param type: node type
        :type type: str
        :param graphObject: object which the node belongs
        :type graphObject: GraphObjects.GraphObject
        """


        self.p = (x, y)
        self.type = type
        self.adj = []
        self.nodes = {}
        self.r = 10
        self.isHighlight = False

        self.isSelected = False

        self.edges = []
        self.color = "#000000"
        self.value = None
        self.circle = Node.Drawing.circle(self.p, self.r, self.color)
        self.setType(type)

        self.graphObject = graphObject

        self.id = Node.count
        Node.count += 1

        self.debugText = Node.Drawing.canvas.create_text(self.p[0], self.p[1] - 25, text=str(self.id))

        self.resVal = 0

        self.MNAnode = None

    def setType(self, type):

        self.color = "#00ff00"
        self.type = type
        self.value = None

        if self.type == Node.res:
            self.value = 0
            self.r = 10
            self.color = "#ff0000"

        elif self.type == Node.line:
            self.r = 3
            self.color = "#000000"

        elif self.type ==  Node.line:
            self.r = 10
            self.color = "#00ffff"

        elif self.type ==  Node.volt:
            self.value = 0
            self.r = 10
            self.color = "#ffff00"

        Node.Drawing.canvas.itemconfig(self.circle, fill=self.color, width=0)

    def selected(self, graph ,color="#00ff00"):
        """
        
        :param graph:
        :type graph: graph.Graph
        :param color: 
        :return: 
        """
        self.isSelected = True
        if graph.selectedNode:
            graph.selectedNode.unselected()


        Node.Drawing.canvas.itemconfig(self.circle, outline=color, width=4)
        graph.selectedNode = self

    def highlight(self, graph, color="#ff00ff"):
        """

        :param graph:
        :type graph: graph.Graph
        :param color: 
        :return: 
        """

        self.isHighlight = True
        if graph.highlightNode:
            graph.highlightNode.unhighlight()

        if not self.isSelected:
            Node.Drawing.canvas.itemconfig(self.circle, outline=color, width=4)
        graph.highlightNode = self

    def unselected(self):
        self.isSelected = False
        Node.Drawing.canvas.itemconfig(self.circle, width=0)

    def unhighlight(self):
        self.isHighlight = False
        if not self.isSelected:
            Node.Drawing.canvas.itemconfig(self.circle, width=0)

    def add(self, n):

        if n not in self.nodes:

            self.adj.append(n)
            n.adj.append(self)

            e = Edge.Edge(self, n)

            self.edges.append(e)
            n.edges.append(e)

            self.nodes[n] = len(self.adj) - 1

            if self not in n.nodes:
                n.adj.append(self)
                n.nodes[self] = len(n.adj) - 1

    def move(self, p2):
        Node.Drawing.canvas.move(self.circle, p2[0] - self.p[0], p2[1] - self.p[1])
        Node.Drawing.canvas.move(self.debugText, p2[0] - self.p[0], p2[1] - self.p[1])

        self.p = p2

        for edge in self.edges:
            edge.move()

    def deleteMe(self):
        """ very very expensive """
        Node.Drawing.canvas.delete(self.circle)
        Node.Drawing.canvas.delete(self.debugText)

        for edge in self.edges:
            edge.delete()

        for node in self.adj:
            node.delete(self)

    def delete(self, n):
        """
        :param n: node to delete from self
        :type n: Node
        :return: None
        """

        i = self.nodes[n]
        self.nodes[n] = None

        aux = []
        auxDict = {}
        j = 0
        for node in self.adj:
            if node == n: continue
            aux.append(node)
            auxDict[n] = j
            j += 1

        auxEdges = []
        for edge in self.edges:
            if not edge.isDelted:
                auxEdges.append(edge)

        self.edges = auxEdges

        self.adj = aux
        self.nodes = auxDict

    def __str__(self):
        return "<Node | id : "+ str(self.id) +" | type : "+ str(self.type) +">"

    """def __eq__(self, b):
        

        :param self: self node
        :param b: another node
        :type b: Node 
        :return: Boolean
        
        return self.p == b.p"""

