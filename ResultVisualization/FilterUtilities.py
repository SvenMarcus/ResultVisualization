from ResultVisualization.Filter import ExactMetaDataMatchesInAllSeriesFilter, FilterVisitor, ListFilter, RowMetaDataContainsFilter, CompositeFilter


class FilterConnector(FilterVisitor):

    def connect(self, filter: ListFilter) -> None:
        filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.addFilter(listFilter)

    def visitCompositeFilter(self, filter: CompositeFilter):
        for subFilter in filter.getFilters():
            subFilter.accept(self)


class FilterDisconnector(FilterVisitor):

    def disconnect(self, filter: ListFilter) -> None:
        filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.removeFilter(listFilter)

    def visitCompositeFilter(self, filter):
        for subFilter in filter.getFilters():
            subFilter.accept(self)
