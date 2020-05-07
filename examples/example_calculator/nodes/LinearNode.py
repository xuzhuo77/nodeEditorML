from sklearn.linear_model import LinearRegression

from examples.example_calculator.calc_conf import LINEAR_NODE_FIT, LINEAR_NODE_PREDICT, register_node
from examples.example_calculator.sklearn_node_base import SkLearnNode

model = LinearRegression()
@register_node(LINEAR_NODE_FIT)
class LinearRegressionNode_Fit(SkLearnNode):
    icon = "icons/divide.png"
    op_code = LINEAR_NODE_FIT
    op_title = "LinearRegression_fit"
    content_label = "/"
    content_label_objname = "linear_node_fit"

    def evalOperation(self, data, target):
        model = LinearRegression()
        model.fit(data, target)
        return model

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
            val = self.evalOperation(input_node1.eval({"a":socket1}), input_node2.eval({"a":socket2}))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val
@register_node(LINEAR_NODE_PREDICT)
class LinearRegressionNode_Predict(SkLearnNode):
    icon = "icons/divide.png"
    op_code = LINEAR_NODE_PREDICT
    op_title = "LinearRegression_predict"
    content_label = "/"
    content_label_objname = "linear_node_predict"

    def evalOperation(self, model, X_test):
        y_pred = model.predict(X_test)
        return y_pred

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
            val = self.evalOperation(input_node1.eval({"a":socket1}), input_node2.eval({"a":socket2}))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val