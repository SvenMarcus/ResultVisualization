from ResultVisualization.TreeView import TreeView


class TreeViewImp(TreeView):

    def __init__(self):
        super().__init__()

    def _addToView(self, viewTreeNode) -> None:
        print("Add to View")

    def _removeFromView(self, index) -> None:
        print("Remove from View")
