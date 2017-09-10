import graph
from GraphObjects import Line, Resistance, Power
import tkpanel
import Types

class State():

    def __init__(self, graph, panel = None):
        """
        
        :param graph:
        :type graph: graph.Graph
        :param panel:
        :type panel: tkpanel.Panel
        """
        self.graph = graph
        self.panel = panel

    def toLine(self):
        self.cleanState()
        self.graph.selectedObject = Line(self.graph, self.graph.selectedNode)

    def toRes(self):
        self.cleanState()
        self.graph.selectedObject = Resistance(self.graph)

        inVal = self.panel.valueTB.get()

        if str.isnumeric(inVal):
            self.graph.selectedObject.setVal(int(inVal))

    def toVoltage(self):
        self.cleanState()
        self.graph.selectedObject = Power(self.graph)

        inVal = self.panel.valueVoltTB.get()

        if str.isnumeric(inVal):
            self.graph.selectedObject.setVal(int(inVal))

    def toGround(self):
        self.cleanState()
        pass

    def delete(self):
        self.cleanState()
        pass


    def cleanState(self):

        if self.panel.cableState.get() == 1:
            self.toggleCableStateButton()

        if self.graph.selectedObject:
            self.graph.selectedObject.delete()
            del self.graph.selectedObject


    def toggleCableStateButton(self):

        print("state", self.panel.cableState.get())

        if self.panel.cableState.get() == 0:
            self.panel.cableState.set(1)
            self.graph.state = "s"
        else:
            self.panel.cableState.set(0)
            self.graph.state = "a"

        self.panel.cableCheckBox.toggle()

    def changeSelectedObject(self, type):



        if self.graph.selectedObject:
            self.graph.selectedObject.delete()

        if type == Types.res:
            self.toRes()
        elif type == Types.volt:
            self.toVoltage()
        elif type == Types.line:
            self.toLine()
        elif type == Types.ground:
            self.toGround()