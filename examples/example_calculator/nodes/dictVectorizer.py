from sklearn.feature_extraction import DictVectorizer

# https://www.cnblogs.com/listenfwind/p/11310924.html
from examples.example_calculator.calc_conf import register_node, SKLEARN_NODE_DICTVECTORIZER
from examples.example_calculator.calc_node_base import CalcNode


@register_node(SKLEARN_NODE_DICTVECTORIZER)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = SKLEARN_NODE_DICTVECTORIZER
    op_title = "Sklearn_DictVectorizer"
    content_label = "+"
    content_label_objname = "Sklearn_DictVectorizer"
    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[1])
        self.vec=DictVectorizer(sparse=False)
    def evalImplementation(self,node):
        input_node1 = self.getInput(0)
        input_node2 = self.getInput(1)

        socket1 =self. getInputSocket(0)
        socket2 =self. getInputSocket(1)



        # val1=input_node1.eval({"a":socket1})
        # val2=input_node2.eval({"a":socket2})


        if input_node1 is None or input_node2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(input_node1.eval({"a":socket1}))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

    def evalOperation(self, *args, **kwargs):
        return self.vec.fit_transform(feature.to_dict(orient='record'))