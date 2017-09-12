import Node
import tkpanel
from MultimeterView import MultimeterView

class Multimeter():

    poss = "poss"
    negg = "negg"
    none = "none"


    def __init__(self, Drawing, graph):


        self.negTerminal = None 
        """:type negTerminal: Node.Node"""
        self.possTerminal = None
        """:type possTerminal: Node.Node"""
        self.state = Multimeter.none

    def intView(self, Drawing, panel):
        self.view = MultimeterView(self, Drawing, panel)

    def setPoss(self, node):
        """
        
        :param node:
        :type node: Node.Node
        :return: 
        """

        self.possTerminal = node
        self.view.setPoss(node)

        self.state = "None"

    def setNegg(self, node):
        """

        :param node:
        :type node: Node.Node
        :return: 
        """

        self.negTerminal = node
        self.view.setNegg(node)

        self.state = "None"


    def move(self, p):

        if self.state == Multimeter.poss:
            self.view.movePoss(p)
        elif self.state == Multimeter.negg:
            self.view.moveNegg(p)

    def setStatePos(self):

        self.possTerminal = None

        if self.negTerminal is None:
            self.view.moveNegg((-10, -10))
        self.state = Multimeter.poss

    def setStateNegg(self):

        self.negTerminal= None

        if self.possTerminal is None:
            self.view.movePoss((-10, -10))
        self.state = Multimeter.negg

    def click(self, node):
        """
        
        :param node:
        :type node: Node.Node
        :return: 
        """

        if node:
            if self.state == Multimeter.poss:
                self.setPoss(node)
            elif self.state == Multimeter.negg:
                self.setNegg(node)

    def calculateVolt(self):
        if self.possTerminal and self.negTerminal:
            val = self.possTerminal.MNAnode.volt - self.negTerminal.MNAnode.volt
            self.view.displayVolt(val)



