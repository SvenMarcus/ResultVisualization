# from ResultVisualization.Event import Event
# from ResultVisualization.TreeNodes import TreeNode, CategoryNode
# from ResultVisualization.TreeView import TreeView
#
#
# class ViewTreeNode(TreeView):
#     nodeChecked = Event()
#
#     def __init__(self, treeNode: TreeNode):
#         super().__init__()
#         self.__parent = None
#         self.__content: TreeNode = treeNode
#         self.__isChecked: bool = False
#         self.__itemCheckedHandler = ItemCheckHandler(self)
#
#     @property
#     def parent(self):
#         return self.__parent
#
#     @parent.setter
#     def parent(self, value) -> None:
#         self.__parent = value
#
#     def addChild(self, viewTreeNode) -> None:
#         super().addChild(viewTreeNode)
#         viewTreeNode.parent = self
#
#     @property
#     def checked(self) -> bool:
#         return self.__isChecked
#
#     @checked.setter
#     def checked(self, value: bool) -> None:
#         self.__isChecked = value
#         self._setCheckStateInView(value)
#         self.nodeChecked(self, value)
#
#     def getContent(self) -> TreeNode:
#         return self.__content
#
#     def addTreeNodeChildren(self) -> None:
#         if type(self.__content) is CategoryNode:
#             treeNode: CategoryNode = self.__content
#             for childNode in treeNode.get_children():
#                 self.addChild(self._makeViewTreeNode(childNode))
#
#     def _makeViewTreeNode(self, content: TreeNode):
#         raise NotImplementedError()
#
#     def _setCheckStateInView(self, state: bool) -> None:
#         raise NotImplementedError()
#
#
# class ItemCheckHandler:
#
#     def __init__(self, viewTreeNode: ViewTreeNode):
#         self.__origin: ViewTreeNode = None
#         self.__upAllowed: bool = False
#         # viewTreeNode.nodeChecked.append(self.__item_changed_handler)
#
#     def __item_changed_handler(self, item: ViewTreeNode) -> None:
#         self.__set_origin(item)
#         self.__check_children(item)
#         self.__check_parents(item)
#         self.__reset_check_helpers(item)
#
#     def __set_origin(self, item) -> None:
#         if self.__origin is None:
#             self.__origin = item
#
#     def __check_children(self, item) -> None:
#         if not self.__upAllowed:
#             for child in item.getChildren():
#                 child.checked = item.checked
#
#     def __check_parents(self, item) -> None:
#         if self.__origin == item:
#             self.__upAllowed = True
#
#         if self.__upAllowed:
#             parent = item.parent
#             if parent is not None:
#                 parent.checked = self.__all_children_selected(parent)
#
#     def __reset_check_helpers(self, item) -> None:
#         if self.__origin == item:
#             self.__origin = None
#             self.__upAllowed = False
#
#     @staticmethod
#     def __all_children_selected(item: ViewTreeNode) -> bool:
#         for child in item.getChildren():
#             if not child.checked:
#                 return False
#         return True
