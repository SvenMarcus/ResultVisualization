class Action:

    def __init__(self, parentMenu, icon: str, text: str, command: 'Command'):
        self.__parentMenu: str = parentMenu
        self.__command: 'Command' = command
        self.__text: str = text
        self.__icon: str = icon

    def trigger(self) -> None:
        self.__command.execute()

    @property
    def parentMenu(self) -> str:
        return self.__parentMenu

    @property
    def icon(self) -> str:
        return self.__icon

    @property
    def text(self) -> str:
        return self.__text
