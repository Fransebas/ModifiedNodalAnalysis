from Node import Node
import Edge
import graph

class GraphObject():

    def __init__(self, graph):
        """
        
        :param graph:
        :type graph: Graph
        """

        self.graph = graph
        self.a = 30
        self.b = 0

    def move(self, p):
        """
        
        :param p:
        :type p: tuple
        :return: 
        """
        pass

    def delete(self):
        pass

    def rotate(self):
        aux = self.a
        self.a = self.b
        self.b = aux;

class Resistance(GraphObject):

    def __init__(self, graph):
        super(Resistance, self).__init__(graph)

        self.resNode = Node(0,0,self,"res")
        self.connection1 = Node(0,0, self)
        self.connection2 = Node(0,0, self)

        self.resNode.add(self.connection1)
        self.resNode.add(self.connection2)

    def move(self, p):

        p1 = (p[0] + self.a , p[1] + self.b)
        p2 = (p[0] - self.a , p[1] - self.b)

        self.connection1.move(p1)
        self.resNode.move(p)
        self.connection2.move(p2)

    def setVal(self, value):
        self.resNode.resVal = value

    def add(self):
        self.graph.nodes.append(self.connection1)
        self.graph.nodes.append(self.resNode)
        self.graph.nodes.append(self.connection2)

    def delete(self):
        self.resNode.deleteMe()
        self.connection1.deleteMe()
        self.connection2.deleteMe()

        del self.resNode
        del self.connection1
        del self.connection2


class Power(GraphObject):

    def __init__(self, graph):
        super(Power, self).__init__(graph)
        self.voltNode = Node(0, 0, self, Node.volt)
        self.connection1 = Node(0, 0, self)
        self.connection2 = Node(0, 0, self)

        self.voltNode.add(self.connection1)
        self.voltNode.add(self.connection2)

    def setVal(self, value):
        self.voltNode.volt = value

    def move(self, p):
        p1 = (p[0] + self.a, p[1] + self.b)
        p2 = (p[0] - self.a, p[1] - self.b)

        self.connection1.move(p1)
        self.voltNode.move(p)
        self.connection2.move(p2)


    def add(self):
        self.graph.nodes.append(self.connection1)
        self.graph.nodes.append(self.voltNode)
        self.graph.nodes.append(self.connection2)

    def delete(self):
        self.voltNode.deleteMe()
        self.connection1.deleteMe()
        self.connection2.deleteMe()

        del self.voltNode
        del self.connection1
        del self.connection2

class Line(GraphObject):

    def __init__(self, graph, node):
        """
        
        :param graph:
        :type graph: Graph
        :param node: 
        :type node: Node
        """
        super(Line, self).__init__(graph)
        self.lineNode = Node(0,0, self)
        self.connectedNode = node



        if self.connectedNode:
            e = Edge.Edge(self.lineNode, self.connectedNode)
            self.lineNode.add(node)
            self.lineNode.edges.append(e)
            self.connectedNode.edges.append(e)


    def move(self, p):
        self.lineNode.move(p)


    def add(self):

        if self.graph.highlightNode and self.graph.selectedNode: # TODO: test if the nodes are equal
            self.graph.selectedNode.add(self.graph.highlightNode)
            self.delete()
        else:
            self.graph.nodes.append(self.lineNode)




    def delete(self):
        self.lineNode.deleteMe()
        del self.lineNode
