from tkinter import *

import States

class Panel():

    def __init__(self, graph, root, states, subGraphs = None):
        """
        
        :param root: 
        :param states:
        :type states: States.State
        :param subGraphs: 
        """
        self.states = states
        self.states.panel = self

        ControlFrame = LabelFrame(root, text="Control Panel", relief=RIDGE)
        ControlFrame.grid(row=0, column=0)

        # Control Frame

        StateFrame = LabelFrame(ControlFrame, text="State Panel", relief=RIDGE)
        StateFrame.grid(row=0, column=0)

        # State Frame

        SateLabel = Label(StateFrame, text="State", relief=RIDGE)
        SateLabel.grid(row=0, column=0)

        self.changeStateLabel = Label(StateFrame, text="Add", relief=RIDGE)
        self.changeStateLabel.grid(row=0, column=1)


        cableButton = Button(StateFrame, text="add cable", command=states.toggleCableStateButton)
        cableButton.grid(row=1, column=0)

        self.cableState = IntVar()
        self.cableCheckBox =  Checkbutton(StateFrame, text="cable", variable=self.cableState, onvalue=1, offvalue=0)
        self.cableCheckBox.grid(row=1, column=1)



        # end

        NodeInfoFrame = LabelFrame(ControlFrame, text="Node", relief=RIDGE)
        NodeInfoFrame.grid(row=1, column=0)


        # Node info

        # row 0

        typeLabel = Label(NodeInfoFrame, text="type", relief=RIDGE)
        typeLabel.grid(row=0, column=0)

        self.nodeTypeLabel = Label(NodeInfoFrame, text="type text", relief=RIDGE)
        self.nodeTypeLabel.grid(row=0, column=1)

        # end

        # row 1
        lineButton = Button(NodeInfoFrame, text="Line", command=states.toLine)
        lineButton.grid(row=1, column=0)
        # end

        # row 2
        resButton = Button(NodeInfoFrame, text="Res", command=states.toRes)
        resButton.grid(row=2, column=0)

        self.valueTB = Entry(NodeInfoFrame)
        self.valueTB.grid(row=2, column=1)
        # end

        # row 3
        voltButton = Button(NodeInfoFrame, text="Voltage", command=states.toVoltage)
        voltButton.grid(row=3, column=0)

        self.valueVoltTB = Entry(NodeInfoFrame)
        self.valueVoltTB.grid(row=3, column=1)
        # end

        # row 4
        groundButton = Button(NodeInfoFrame, text="Ground", command=states.toGround)
        groundButton.grid(row=4, column=0)
        # end

        # row 5
        deleteButton = Button(NodeInfoFrame, text="Delete", command=states.delete)
        deleteButton.grid(row=5, column=0)
        # end

        # end node info

        MutltimeterFrame = LabelFrame(root, text="Multimeter", relief=RIDGE)
        MutltimeterFrame.grid(row=0, column=2)

        # Multimeter Frame

        groundButton = Button(MutltimeterFrame, text="Make SubGraphs", command=graph.solveGraph)
        groundButton.grid(row=0, column=0)

        # end Multimeter Frame

    def update(self, node):

        self.nodeTypeLabel['text'] = node.type

        self.valueTB.delete(0,END)
        self.valueVoltTB.delete(0, END)

        if node.value is not None:
            if node.type == "res":
                self.valueTB.insert(0, str(node.value) )
            elif node.type == "volt":
                self.valueVoltTB.insert(0, str(node.value) )


