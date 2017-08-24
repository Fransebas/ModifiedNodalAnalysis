import Edge

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
    def __init__(self, x, y, type="line"):
        self.p = (x, y)
        self.type = type
        self.adj = []
        self.nodes = {}
        self.r = 10
        self.highlight = False
        self.inLineP = None  # point of the line that enters
        self.outLineP = None  # point of the line that goes out
        self.inLine = []
        self.outLine = []

        self.edges = []

        self.color = "#000000"

        self.value = None

        self.circle = Node.Drawing.circle(self.p, self.r, self.color)

        self.setType(type)

        self.id = Node.count
        Node.count += 1

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

        Node.Drawing.canvas.itemconfig(self.circle, fill=self.color, width=0)

    def selected(self, color="#ff00ff"):
        Node.Drawing.canvas.itemconfig(self.circle, outline=color, width=4)

    def unselected(self):
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

        self.p = p2

        for edge in self.edges:
            edge.move()

    def deleteMe(self):
        """ very very expensive """
        Node.Drawing.canvas.delete(self.circle)

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
        return "<Node | id : "+ str(self.id) +">"

    """def __eq__(self, b):
        

        :param self: self node
        :param b: another node
        :type b: Node 
        :return: Boolean
        
        return self.p == b.p"""

