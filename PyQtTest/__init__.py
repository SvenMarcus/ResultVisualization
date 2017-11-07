import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget

from PyQtTest.TreeNodes import CategoryNode, FloatNode
from PyQtTest.TreeWidgetController import TreeWidgetController


class GraphWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__baseLayout = QtWidgets.QHBoxLayout(self)
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setLayout(self.__baseLayout)

        self.__tree = QTreeWidget()
        self.__tree.setColumnCount(1)
        self.__tree.setMinimumWidth(300)
        self.__tree.setMaximumWidth(300)

        self.__treeController = TreeWidgetController(self.__tree)
        self.__treeController.item_checked_event.append(self.__update_label)

        for i in range(1, 3):
            prisme: CategoryNode = CategoryNode("IRSN Prisme Door " + str(i))
            tg: CategoryNode = CategoryNode("TG")
            tg.add_child(FloatNode("PEAK", random.randint(1, 50)))
            tg.add_child(FloatNode("PEACOCK", random.randint(1, 50)))
            tg.add_child(FloatNode("Median_EXP", random.randint(1, 50)))
            prisme.add_child(tg)

            tp: CategoryNode = CategoryNode("TP")
            tp.add_child(FloatNode("PEAK", random.randint(1, 50)))
            tp.add_child(FloatNode("PEACOCK", random.randint(1, 50)))
            tp.add_child(FloatNode("Median_EXP", random.randint(1, 50)))
            prisme.add_child(tp)

            tca: CategoryNode = CategoryNode("TCA")
            tca.add_child(FloatNode("PEAK", random.randint(1, 50)))
            tca.add_child(FloatNode("PEACOCK", random.randint(1, 50)))
            tca.add_child(FloatNode("Median_EXP", random.randint(1, 50)))
            prisme.add_child(tca)

            self.__treeController.add_node(prisme)

        self.__baseLayout.addWidget(self.__tree)
        self.__label = QLabel("")
        self.__baseLayout.addWidget(self.__label)
        self.show()

    def __update_label(self, sender, args):
        checked_nodes = self.__treeController.get_checked_nodes()
        string = ""
        for node in checked_nodes:
            string += str(node)
            if type(node) is FloatNode:
                string += " Value: " + str(node.get_value())
            string += "\n"
        self.__label.setText(string)


app = QApplication(sys.argv)
window = GraphWindow()
sys.exit(app.exec_())
