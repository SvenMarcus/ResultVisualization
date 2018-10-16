from QtResultVisualization.QtBoxSeriesDialog import QtBoxSeriesDialog
from QtResultVisualization.QtFillAreaDialog import QtFillAreaDialog
from QtResultVisualization.QtLineSeriesDialog import QtLineSeriesDialog
from ResultVisualization.Dialogs import SeriesDialog, SeriesDialogFactory
from ResultVisualization.Plot import (BoxSeries, FillAreaSeries, LineSeries,
                                      Series)


class QtSeriesDialogFactory(SeriesDialogFactory):

    def makeSeriesDialog(self, kind: str = "", initialSeries: Series = None) -> SeriesDialog:
        dialog = None
        if kind:
            if kind == "linear":
                dialog = QtLineSeriesDialog()
                dialog.getWidget().setMinimumSize(1000, 800)
            elif kind == "box":
                dialog = QtBoxSeriesDialog()
                dialog.getWidget().setMinimumSize(1000, 800)
            elif kind == "area":
                dialog = QtFillAreaDialog()
                dialog.getWidget().setMinimumSize(500, 400)

            return dialog
        elif initialSeries is not None:
            if isinstance(initialSeries, LineSeries):
                dialog = QtLineSeriesDialog(initialSeries)
                dialog.getWidget().setMinimumSize(1000, 800)
            elif isinstance(initialSeries, BoxSeries):
                dialog = QtBoxSeriesDialog(initialSeries)
                dialog.getWidget().setMinimumSize(1000, 800)
            elif isinstance(initialSeries, FillAreaSeries):
                dialog = QtFillAreaDialog(initialSeries)
                dialog.getWidget().setMinimumSize(500, 400)

            return dialog
