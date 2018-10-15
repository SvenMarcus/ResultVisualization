from abc import ABC, abstractmethod

class SeriesVisitor(ABC):

    @abstractmethod
    def visitLineSeries(series: 'LineSeries') -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitBoxSeries(series: 'BoxSeries') -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitFillAreaSeries(series: 'FillAreaSeries') -> None:
        raise NotImplementedError()
