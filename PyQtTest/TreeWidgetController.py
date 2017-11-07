from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from PyQtTest.Event import Event
from PyQtTest.TreeNodes import TreeNode, CategoryNode


class TreeWidgetController:

    item_checked_event = Event()

    __hierarchy: List[TreeNode] = []
    __checked_nodes: List[TreeNode] = []

    def __init__(self, widget: QTreeWidget = None):
        self.__widget: QTreeWidget = widget or QTreeWidget()
        self.__widget.itemChanged.connect(self.__trigger_item_changed_event)
        self.__changed_handler = ItemCheckHandler(self.__widget)

    def add_node(self, node: TreeNode) -> None:
        self.__hierarchy.append(node)
        widget_item = self.__make_tree_widget_item(node)
        self.__widget.addTopLevelItem(widget_item)
        self.__add_children(widget_item, node)

    def get_node_at(self, index) -> TreeNode:
        return self.__hierarchy[index]

    def get_checked_nodes(self) -> List[TreeNode]:
        checked_nodes: List[TreeNode] = []
        self.__append_checked_child_nodes(self.__widget, checked_nodes)
        return checked_nodes

    def __append_checked_child_nodes(self, widget_item, checked_nodes: List[TreeNode]) -> None:
        count = self.__get_child_count(widget_item)
        for i in range(0, count):
            child: QTreeWidgetItem = self.__get_child_at(widget_item, i)
            if child.checkState(0) == Qt.Checked:
                checked_nodes.append(child.data(0, Qt.UserRole))
            self.__append_checked_child_nodes(child, checked_nodes)

    def __get_child_count(self, widget) -> int:
        count = 0
        if type(widget) is QTreeWidget:
            count = widget.topLevelItemCount()
        elif type(widget) is QTreeWidgetItem:
            count = widget.childCount()
        return count

    def __get_child_at(self, widget, index) -> QTreeWidgetItem:
        if type(widget) is QTreeWidget:
            return widget.topLevelItem(index)
        elif type(widget) is QTreeWidgetItem:
            return widget.child(index)

    @staticmethod
    def __make_tree_widget_item(node) -> QTreeWidgetItem:
        widget_item = QTreeWidgetItem()
        widget_item.setCheckState(0, Qt.Unchecked)
        widget_item.setData(0, Qt.DisplayRole, node.get_text())
        widget_item.setData(0, Qt.UserRole, node)
        return widget_item

    def __add_children(self, parent_tree_widget, node) -> None:
        if type(node) is CategoryNode:
            category_node: CategoryNode = node
            for child in category_node.get_children():
                widget_item: QTreeWidgetItem = self.__make_tree_widget_item(child)
                parent_tree_widget.addChild(widget_item)
                self.__add_children(widget_item, child)

    def __trigger_item_changed_event(self, item: QTreeWidgetItem, col: int) -> None:
        data: TreeNode = item.data(0, Qt.UserRole)
        checked: bool = item.checkState(0) == Qt.Checked
        if checked:
            if data not in self.__checked_nodes:
                self.__checked_nodes.append(data)
        else:
            self.__checked_nodes.remove(data)
        self.item_checked_event(data, checked)


class ItemCheckHandler:

    def __init__(self, widget: QTreeWidget):
        self.__origin: QTreeWidgetItem = None
        self.__upAllowed: bool = False
        widget.itemChanged.connect(self.__item_changed_handler)

    def __item_changed_handler(self, item: QTreeWidgetItem, col: int) -> None:
        self.__set_origin(item)
        self.__check_children(item)
        self.__check_parents(item)
        self.__reset_check_helpers(item)

    def __set_origin(self, item) -> None:
        if self.__origin is None:
            self.__origin = item

    def __check_children(self, item) -> None:
        if not self.__upAllowed:
            for i in range(0, item.childCount()):
                child = item.child(i)
                child.setCheckState(0, item.checkState(0))

    def __check_parents(self, item) -> None:
        if self.__origin == item:
            self.__upAllowed = True

        if self.__upAllowed:
            parent = item.parent()
            if parent is not None:
                if self.__all_children_selected(parent):
                    parent.setCheckState(0, Qt.Checked)
                else:
                    parent.setCheckState(0, Qt.Unchecked)

    def __reset_check_helpers(self, item) -> None:
        if self.__origin == item:
            self.__origin = None
            self.__upAllowed = False

    @staticmethod
    def __all_children_selected(item: QTreeWidgetItem) -> bool:
        for i in range(0, item.childCount()):
            if item.child(i).checkState(0) == Qt.Unchecked:
                return False
        return True
