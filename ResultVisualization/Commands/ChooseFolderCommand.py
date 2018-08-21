from ResultVisualization.TreeFileLoader.TreeViewFileLoader import TreeViewFileLoader


class ChooseFolderCommand:

    def __init__(self, treeViewLoader: TreeViewFileLoader):
        self.__treeViewFileLoader = treeViewLoader

    def execute(self):
