import graph as gph
from collections import deque
import numpy as np
import Types

class MNAEdge():

    voltCount = 0

    def __init__(self, n1, n2, type):
        self.res = 0
        self.voltIndex = 0
        self.n1 = n1
        self.n2 = n2
        self.type = type

        if type == Types.volt:
            self.voltIndex = MNAEdge.voltCount
            MNAEdge.voltCount += 1


    def addStart(self, node):

        self.n1 = node

    def addEnd(self, node):

        self.n2 = node

    def __str__(self):
        return str(self.n1.i) + " to " + str(self.n2.i) + " | type " + self.type


class MNANode():
    count = 0

    def __init__(self):
        """

        :param node:
        :type node: gph.Node
        """
        self.conductance = 0
        self.edges = []
        self.volt = None
        self.i = MNANode.count
        MNANode.count += 1

    def addEdge(self, node, type, res=None):
        """

        :param edge:
        :type edge: MNAEdge
        :return: None
        """

        edge = MNAEdge(self, node, type)

        if res:
            edge.res = res

        self.edges.append(edge)
        node.edges.append(edge)


    def __str__(self):
        return "<MNANode i = " + str(self.i) + ">"





class MNA():

    def __init__(self, graph):
        """
        
        :param graph:
        :type graph: gph.SubGraph
        """
        self.graph = graph
        self.nodes = []
        self.voltNodes = []
        self.start = None
        self.voltSources = 0

        self.nodePos = {}
        self.edges = {}

    def findFirstLine(self):
        for n in self.graph.nodes:
            if n.type == Types.line:
                return n

    def makeGraph(self):

        used = {}
        queue = deque()
        node = self.findFirstLine()
        gNode = MNANode()
        node.MNAnode = gNode
        self.nodePos[gNode] = 0

        self.nodes.append(gNode)
        queue.append( ( node , gNode) )

        while len( queue ) > 0:

            node, gNode  = queue.popleft()
            #node, gNode = queue.pop()

            print( "node=", node)

            #if node in used:
                #continue

            used[node] = gNode

            if node.type == Types.line:
                for n in node.adj:
                    print("adj n", n)
                    if n not in used:
                        used[n] = node
                        queue.append( (n , gNode) )
                        n.MNAnode = gNode

            elif node.type == Types.res:
                gNode.conductance += 1/node.resVal
                for n in node.adj:
                    if n.MNAnode:
                        self.addEdge(n1=node.MNAnode, n2=n.MNAnode, res=node.resVal ,type=Types.res)
                    print ("adj n", n)
                    if n not in used:
                        used[n] = node
                        newGNode = MNANode()
                        queue.append( (n, newGNode) )
                        self.nodes.append( newGNode )
                        #gNode.addEdge(node= newGNode, res= node.resVal, type= Types.res )
                        self.addEdge(n1=gNode, n2=newGNode, res=node.resVal, type=Types.res)
                        self.nodePos[newGNode] = newGNode.i
                        n.MNAnode = newGNode

            elif node.type == Types.volt:

                self.voltNodes.append(( node, self.voltSources ))
                self.voltSources += 1

                #gNode.volt += node.volt # check this

                for n in node.adj:
                    if n.MNAnode:
                        self.addEdge(n1=node.MNAnode, n2=n.MNAnode, type=Types.volt)
                    if n not in used:
                        used[n] = node
                        newGNode = MNANode()
                        queue.append( (n, newGNode) )
                        self.nodes.append(newGNode)
                        #gNode.addEdge(node=newGNode, type=Types.volt)
                        self.addEdge(n1=gNode, n2=newGNode, type=Types.volt)
                        self.nodePos[newGNode] = newGNode.i
                        n.MNAnode = newGNode

    def addEdge(self, n1, n2, type, res = None):
        """
        
        :param n1:
        :type n1: MNANode
        :param n2:
        :type n2: MNANode
        :return: 
        """
        if n1.i == n2.i:
            return
        t = (n1,n2)
        if t in self.edges:
            return
        self.edges[t] = True
        n1.addEdge(n2, type=type, res=res)


    def solve(self):

        """
            
        A = G  B
            BT D
        
        :return: 
        """

        self.makeGraph()

        print ("Number of nodes = ", len(self.nodes))



        ground = self.nodes.pop()
        ground.volt = 0
        print ("nodes = " , self.nodes)
        print ("Calculing G matrix")
        G = self.getGMatrix()
        print("G = ", G)
        print("Calculing B matrix")
        self.nodes.append(ground)
        B = self.getBMatrix()
        print("B = " , B)

        n = len( self.nodes ) + self.voltSources - 1

        A = np.array( [[0.0 for i in range(n)] for j in range(n) ]  )

        for i in range(len( self.nodes )-1):
            for j in range(len( self.nodes )-1):
                A[i][j] = G[i][j]
            A[i][len( self.nodes )-1] = B[i]
            A[len(self.nodes) - 1][i] = B[i]

        print("A = ", A)

        z = self.makeZ()

        print("z = ", z)

        r = np.linalg.solve(A,z)

        print("R = ", r)


        for node in self.nodes:
            node.volt = r[node.i - 1]


    def makeZ(self):

        #TODO: for now z has only zeroes
        z = np.array([ 0 for i in range(len(self.nodes) + self.voltSources - 1 ) ])

        for t in self.voltNodes:
            node, i = t
            z[len(self.nodes)- 1 + i] = node.volt

        return z





    def getGMatrix(self):
        #TODO: maybe is not to node length but rather node length -1

        size = len(self.nodes)

        M = np.array( [ [ 0.0 for j in range( size ) ] for i in range( size ) ] )


        for n in self.nodes:
            print("node = ", n)
            cond = 0
            for e in n.edges:
                print("    edge = ", e)
                if e.res != 0:
                    cond += 1/e.res
                    print ("        res = ", e.res)

                    if e.n1.i == size or e.n2.i == size:
                        continue

                    M[e.n1.i][e.n2.i] = -e.res # Solo funciona si tienen una sola coneccion
                    M[e.n2.i][e.n1.i] = -e.res

            #if n.i != size:
            M[n.i][n.i] = cond

        return M

    def getBMatrix(self):

        print ("Volt sources = ", self.voltSources)

        size = len(self.nodes) - 1

        M = np.array( [ [ 0 for j in range( len(self.nodes) -1 ) ] for i in range( self.voltSources ) ])

        print ("Empty M ", M)

        usedEdges = {}

        for n in self.nodes:
            for edge in n.edges:
                if edge in usedEdges:
                    continue
                usedEdges[edge] = n

                if edge.type == Types.volt:
                    n1 = edge.n1
                    n2 = edge.n2

                    print ("Volt index = ", edge.voltIndex)

                    if n1.i != size:
                        M[ edge.voltIndex][n1.i ] = 1
                    if n2.i != size:
                        M[ edge.voltIndex][n2.i ] = -1

        print(M.transpose())
        print(M)
        return M.transpose()





    def findStart(self):
        node = self.NormalGraph.nodes[0]

        queue = deque()
        queue.append(node)
        while len(queue) > 0:
            node = queue.popleft()

            if node.type == Node.ground or node.type == Node.volt:
                self.start = node
                return







