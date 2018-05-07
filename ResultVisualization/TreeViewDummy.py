from ResultVisualization.TreeItem import TreeItem
from ResultVisualization.TreeView import TreeView, TreeIndex


class TreeViewDummy(TreeView):

    def __init__(self):
        super(TreeViewDummy, self).__init__()

    def insertItem(self, item: TreeItem, index: TreeIndex, childPos: int):
        pass

    def deleteItem(self, index: TreeIndex):
        pass

