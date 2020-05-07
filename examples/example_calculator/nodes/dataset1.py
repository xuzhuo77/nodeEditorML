from sklearn import datasets
from examples.example_calculator.calc_conf import *
from examples.example_calculator.calc_node_base import *

iris=datasets.load_iris()


class DatasetContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("data", self)
        self.lbl.setAlignment(Qt.AlignRight)
        self.lbl.setObjectName(self.node.content_label_objname)
        self.lbl2 = QLabel("target", self)
        self.lbl2.setAlignment(Qt.AlignRight)
        self.lbl2.setObjectName(self.node.content_label_objname)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.lbl)
        self.layout.addWidget(self.lbl2)



@register_node(OP_NODE_IRIS)
class DatasetNode_Iris(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_IRIS
    op_title = "DatasetNode_Iris"
    content_label_objname = "DatasetNode_Iris"


    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1,1])

    def initInnerClasses(self):
        self.content = DatasetContent(self)
        self.grNode = CalcGraphicsNode(self)

    def outputData(self):
        return iris.data

    def outputTarget(self):
        return iris.target

    def eval(self,node):

            # outputnode=self.getOutputs(0)
            val = self.evalImplementation(node)
            return val


    def evalImplementation(self,node):


        self.value={}

        index=self.outputs.index(node["a"])

        self.value[0]=iris.data
        self.value[1]=iris.target



        datashape=str(iris.data.shape)
        targetshape=str(iris.target.shape)
        val="data:{} \n target:{}".format(datashape, targetshape) 
        self.content.lbl.setText( val)
        # self.markInvalid(False)
        # self.markDirty(False)
        # self.grNode.setToolTip("")
        # self.evalChildren()
        val=self.value[index]
        return val

