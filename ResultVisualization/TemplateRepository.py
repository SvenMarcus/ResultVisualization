from typing import Iterable, Set

from ResultVisualization.Templates import LineTemplate


class TemplateRepository:

    def __init__(self):
        self.__templates: Set[LineTemplate] = set()

    def addTemplate(self, template: LineTemplate) -> None:
        self.__templates.add(template)

    def removeTemplate(self, template: LineTemplate) -> None:
        self.__templates.remove(template)

    def getTemplates(self) -> Iterable[LineTemplate]:
        return self.__templates
