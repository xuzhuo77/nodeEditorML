

# 不同比例布局
# https://blog.csdn.net/qq_20307987/article/details/77945024
from examples.example_calculator.calc_conf import *
from examples.example_calculator.calc_node_base import *
from examples.example_calculator.sklearn_node_base import SkLearnNode,SkLearnGraphicsNode
from sklearn.neighbors import KNeighborsClassifier
matrics = ["euclidean",  # （欧氏距离）,
           "minkowski",  # （明科夫斯基距离）,
           "maximum",  # （切比雪夫距离）,
           "manhattan",  # （绝对值距离）,
           "canberra",  # （兰式距离）,
           # "minkowski" # （马氏距离）
           ]


class SklearnKNNContent(QDMNodeContentWidget):
    def initUI(self):
        self.height_pp=0 #需要增加得高度
        self.inner_layout = QVBoxLayout()
        self.setLayout(self.inner_layout)

        self.lbl = QLabel(str(self.node.n_neighbors), self)

        self.cb = QComboBox()
        self.cb.addItems(matrics)  # 添加多个项目
        self.cb.setCurrentIndex(self.node.id_matric)
        self.cb.currentIndexChanged.connect(self.selectionchange)  # 发射currentIndexChanged信号，连接下面的selectionchange槽
        # self.cb.setObjectName(self.node.content_label_objname)
        self.cb.setMaximumHeight(30)

        self.xdatalbl = QLabel("X_data", self)
        self.ydatalbl = QLabel("Y_data", self)
        self.modellbl = QLabel("model", self)
        self.modellbl.setAlignment(Qt.AlignRight)


        self.configWidget(self.lbl)
        self.configWidget(self.cb)
        self.configWidget(self.xdatalbl)
        self.configWidget(self.ydatalbl)
        self.configWidget(self.modellbl)


    def configWidget(self,widget):
        # setcolor
        if self.inner_layout.count()%2==0:
            widget.setStyleSheet("background-color:#4B4B4B;")
        else:
            widget.setStyleSheet("background-color:#242424;")
        height=widget.geometry().height()
        self.height_pp +=height
        self.inner_layout.addWidget(widget)


    def selectionchange(self, i):
        self.node.id_matric=i


@register_node(KNEIGHBORSCLASSIFIER_NODE_FIT)
class KNeighborsClassifierNode_Fit(SkLearnNode):
    icon = "icons/divide.png"
    op_code = KNEIGHBORSCLASSIFIER_NODE_FIT
    op_title = "KNN_fit"
    content_label = "/"
    content_label_objname = "KNeighborsClassifier_node_fit"
    n_neighbors = 1
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    id_matric=1
    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1, 1], outputs=[2])


    def initInnerClasses(self):
        self.content = SklearnKNNContent(self)
        self.grNode = SkLearnGraphicsNode(self)

    def evalOperation(self, n_neighbors, x_data, y_data):
        if n_neighbors != self.n_neighbors:
            self.model = KNeighborsClassifier(n_neighbors=n_neighbors,matrics=matrics[self.id_matric])
            self.n_neighbors = n_neighbors
        self.model.fit(x_data, y_data)
        return self.model

    def evalImplementation(self, param):

        n_neighbors_Input = self.getInput(0)
        x_Input = self.getInput(1)
        y_Input = self.getInput(2)

        socket1 = self.getInputSocket(0)
        socket2 = self.getInputSocket(1)
        socket3 = self.getInputSocket(2)




        # val1=input_node1.eval({"a":socket1})
        # val2=input_node2.eval({"a":socket2})
        if n_neighbors_Input is not None:
            self.n_neighbors=n_neighbors_Input.eval({})
            self.content.lbl.setText(str(self.n_neighbors))


        if n_neighbors_Input is None or x_Input is None or y_Input is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(n_neighbors_Input.eval({}), x_Input.eval({"a": socket2}),
                                     y_Input.eval({"a": socket3}))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val


@register_node(KNEIGHBORSCLASSIFIER_NODE_PREDICT)
class KNeighborsClassifierNode_Predict(SkLearnNode):
    icon = "icons/divide.png"
    op_code = KNEIGHBORSCLASSIFIER_NODE_PREDICT
    op_title = "KNN_predict"
    content_label = "/"
    content_label_objname = "KNeighborsClassifier_node_predict"
    n_neighbors = 1

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[2])

    def evalOperation(self, model, x_data):
        y_ = model.predict(x_data)
        return y_

    def evalImplementation(self, param):

        model_Input = self.getInput(0)
        x_data = self.getInput(1)

        socket1 = self.getInputSocket(0)
        socket2 = self.getInputSocket(1)

        # val1=input_node1.eval({"a":socket1})
        # val2=input_node2.eval({"a":socket2})

        if model_Input is None or x_data is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(model_Input.eval({}), x_data.eval({"a": socket2}))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val


@register_node(KNEIGHBORSCLASSIFIER_NODE_SCORE)
class KNeighborsClassifierNode_Score(SkLearnNode):
    icon = "icons/divide.png"
    op_code = KNEIGHBORSCLASSIFIER_NODE_SCORE
    op_title = "KNN_score"
    content_label = "/"
    content_label_objname = "KNeighborsClassifier_node_score"
    n_neighbors = 1

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1, 1], outputs=[])

    def evalOperation(self, model, y_data1, y_data2):
        y_ = model.score(y_data1, y_data2)
        return y_

    def evalImplementation(self, param):
        model_Input = self.getInput(0)
        x_data = self.getInput(1)
        y_data = self.getInput(2)

        socket1 = self.getInputSocket(0)
        socket2 = self.getInputSocket(1)
        socket3 = self.getInputSocket(2)

        # val1=input_node1.eval({"a":socket1})
        # val2=input_node2.eval({"a":socket2})

        if model_Input is None or x_data is None or y_data is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(model_Input.eval({}), x_data.eval({"a": socket2}), y_data.eval({"a": socket3}))
            self.content.lbl.setText(str(val))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val
