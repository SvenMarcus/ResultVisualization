class Action:

    def __init__(self, category: str, icon: str, text: str, command: 'Command'):
        self.__command: 'Command' = command
        self.__category: str = category
        self.__text: str = text
        self.__icon: str = icon

    def trigger(self) -> None:
        self.__command.execute()

    @property
    def category(self) -> str:
        return self.__icon

    @property
    def icon(self) -> str:
        return self.__icon

    @property
    def text(self) -> str:
        return self.__text
