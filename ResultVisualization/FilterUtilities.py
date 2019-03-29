from ResultVisualization.Filter import ExactMetaDataMatchesInAllSeriesFilter, FilterVisitor, SeriesFilter, RowMetaDataContainsFilter, CompositeFilter


class FilterConnector(FilterVisitor):

    def connect(self, filter: SeriesFilter) -> None:
        filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.addFilter(listFilter)

    def visitCompositeFilter(self, seriesFilter: CompositeFilter):
        for subFilter in seriesFilter.getFilters():
            subFilter.accept(self)


class FilterDisconnector(FilterVisitor):

    def disconnect(self, filter: SeriesFilter) -> None:
        filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.removeFilter(listFilter)

    def visitCompositeFilter(self, seriesFilter):
        for subFilter in seriesFilter.getFilters():
            subFilter.accept(self)
