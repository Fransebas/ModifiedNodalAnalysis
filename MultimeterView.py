import Multimeter
import Node
import tkpanel


class MultimeterView():

    Drawing = None

    @staticmethod
    def init(Drawing):
        MultimeterView.Drawing = Drawing

    def __init__(self, controller, Drawing, panel):
        """
        
        :param controller:
        :type controller: Multimeter.Multimeter
        """

        MultimeterView.init(Drawing)

        self.possSelector = MultimeterView.Drawing.circle((-10,-10), Node.Node.r + 5, color=None)
        MultimeterView.Drawing.canvas.itemconfig(self.possSelector ,outline="#ff0000", width=4)
        self.pPoss = (-10,-10)
        self.neggSelector = MultimeterView.Drawing.circle((-10,-10), Node.Node.r + 5, color=None)
        MultimeterView.Drawing.canvas.itemconfig(self.neggSelector, outline="#0000ff", width=4)
        self.pNegg = (-10, -10)
        self.controller = controller

        self.panel = panel
        """: type panel: tkpanel.Panel"""




    def setPoss(self, node):
        """
        
        :param node:
        :type node: Node.Node
        :return: 
        """

        self.movePoss(node.p)

    def setNegg(self, node):
        """

        :param node:
        :type node: Node.Node
        :return: 
        """

        self.moveNegg(node.p)


    def movePoss(self, p):
        MultimeterView.Drawing.canvas.move(self.possSelector, p[0] - self.pPoss[0], p[1] - self.pPoss[1])
        self.pPoss = p

    def moveNegg(self, p):
        MultimeterView.Drawing.canvas.move(self.neggSelector, p[0] - self.pNegg[0], p[1] - self.pNegg[1])
        self.pNegg = p

    def displayVolt(self, val) -> None:
        """

        :param val: 
        :type val: float
        """

        self.panel.mutimeterShowVolt(val)

