from ResultVisualization.Filter import RowFilter

class TitledFilter(RowFilter):

    def __init__(self, rowFilter: RowFilter, title: str = ""):
        self.__filter: RowFilter = rowFilter
        self.__title = title

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    def appliesToRow(self, sourceSeries, row) -> bool:
        return self.__filter.appliesToRow(sourceSeries, row)
