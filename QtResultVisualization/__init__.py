import sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QGridLayout, QHBoxLayout

from QtResultVisualization.QTreeViewImp import QTreeViewImp
from QtResultVisualization.QViewTreeNodeImp import QViewTreeNodeImp
from ResultVisualization.Filter import Filter
from ResultVisualization.TreeNodes import CategoryNode
from ResultVisualization.ViewTreeNode import ViewTreeNode


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        filterButton = QPushButton()
        filterButton.setText("Filter TreeView")
        filterButton.clicked.connect(lambda: self.__treeView.filter(MyFilter()))

        resetButton = QPushButton()
        resetButton.setText("Reset Filter")
        resetButton.clicked.connect(lambda: self.__treeView.resetFilter())

        self.__treeView = QTreeViewImp()

        layout = QGridLayout(self)

        vBoxLayout = QVBoxLayout()
        vBoxLayout2 = QVBoxLayout()
        layout.addLayout(vBoxLayout, 0, 0)
        layout.addLayout(vBoxLayout2, 0, 1)

        vBoxLayout.addWidget(self.__treeView.getWidget())
        vBoxLayout2.addWidget(filterButton)
        vBoxLayout2.addWidget(resetButton)

        treeNode: CategoryNode = CategoryNode("A")
        subNode: CategoryNode = CategoryNode("A_Sub")
        subNode.add_child(CategoryNode("a_Sub_Sub_B"))
        treeNode.add_child(subNode)

        treeNode.add_child(CategoryNode("A_Sub"))
        treeNode.add_child(CategoryNode("A_Sub"))

        treeNode1: CategoryNode = CategoryNode("B")
        treeNode1.add_child(CategoryNode("B_Sub"))
        treeNode1.add_child(CategoryNode("B_Sub"))
        treeNode1.add_child(CategoryNode("B_Sub"))

        vtn: ViewTreeNode = QViewTreeNodeImp(treeNode)
        vtn2: ViewTreeNode = QViewTreeNodeImp(treeNode1)

        self.__treeView.addChild(vtn)
        self.__treeView.addChild(vtn2)


class MyFilter(Filter[ViewTreeNode]):
    def appliesTo(self, arg: ViewTreeNode) -> bool:
        return "A" in arg.getContent().get_text()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
