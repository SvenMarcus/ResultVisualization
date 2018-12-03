from typing import Generic, TypeVar

from ResultVisualization.Commands import UndoableCommand

T = TypeVar('T')

class Stack(Generic[T]):

    def __init__(self):
        self.__stack = list()

    def push(self, value: T) -> None:
        self.__stack.append(value)

    def pop(self) -> T:
        if not self.isEmpty():
            return self.__stack.pop()
        return None

    def clear(self) -> None:
        self.__stack.clear()

    def isEmpty(self) -> bool:
        return len(self.__stack) == 0


class CommandStack:

    def __init__(self):
        self.__undoStack: Stack[UndoableCommand] = Stack()
        self.__redoStack: Stack[UndoableCommand] = Stack()

    def addCommand(self, command: UndoableCommand) -> None:
        command.execute()
        self.__undoStack.push(command)
        self.__redoStack.clear()

    def canUndo(self) -> bool:
        return not self.__undoStack.isEmpty()

    def canRedo(self) -> bool:
        return not self.__redoStack.isEmpty()

    def undo(self) -> None:
        command: UndoableCommand = self.__undoStack.pop()
        command.undo()
        self.__redoStack.push(command)

    def redo(self) -> None:
        command: UndoableCommand = self.__redoStack.pop()
        command.execute()
        self.__undoStack.push(command)
