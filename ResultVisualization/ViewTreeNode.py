from ResultVisualization.Event import Event
from ResultVisualization.TreeNodes import TreeNode, CategoryNode
from ResultVisualization.TreeView import TreeView


class ViewTreeNode(TreeView):
    nodeChecked = Event()

    def __init__(self, treeNode: TreeNode):
        super().__init__()
        self.__content: TreeNode = treeNode
        self.__isChecked: bool = False

    def isChecked(self) -> bool:
        return self.__isChecked

    def setChecked(self, state: bool):
        self.__isChecked = state
        self.nodeChecked(self, state)
        self._setCheckStateInView(state)

    def getContent(self) -> TreeNode:
        return self.__content

    def addTreeNodeChildren(self) -> None:
        if type(self.__content) is CategoryNode:
            treeNode: CategoryNode = self.__content
            for childNode in treeNode.get_children():
                self.addChild(self._makeViewTreeNode(childNode))

    def _makeViewTreeNode(self, content: TreeNode):
        raise NotImplementedError()

    def _setCheckStateInView(self, state: bool) -> None:
        raise NotImplementedError()
