import os
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
from typing import List

from Reader.CsvReader import readFile
from ResultVisualization.Dialogs import ChooseMultipleFilesDialog, Dialog, DialogResult
from ResultVisualization.GraphView import GraphView
from ResultVisualization.Plot import LineSeries
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.Templates import LineTemplate
from ResultVisualization.TemplateRepository import TemplateRepository
from ResultVisualization.util import isNumber, transposeList


class LoadFromTemplateDialog(Dialog, ABC):

    def __init__(self, templateRepository: TemplateRepository, graphView: GraphView, seriesRepo: SeriesRepository):
        self._result: DialogResult = DialogResult.Cancel
        self.__templates: List[LineTemplate] = list(templateRepository.getTemplates())
        self.__graphView: GraphView = graphView
        self.__seriesRepo: SeriesRepository = seriesRepo

        self.__files: List[str] = list()

        for template in self.__templates:
            self._addTemplateToComboBox(template.name)

    def _confirm(self) -> None:
        selectedTemplateIndex: int = self._getSelectedTemplateIndex()
        if selectedTemplateIndex == -1:
            self._showMessage("Error. No Template selected.")
            return
        if len(self.__files) == 0:
            self._showMessage("Error. No files selected.")
            return

        template: LineTemplate = self.__templates[selectedTemplateIndex]

        failedFileNames: List[str] = list()

        xValues = list()
        yValues = list()
        meta = list()

        columns = [template.xColumnTitle, template.yColumnTitle]
        if template.metaColumnTitle:
            columns.append(template.metaColumnTitle)

        index = -1
        for file in self.__files:
            index += 1
            series: LineSeries = LineSeries()

            dataFrame: pd.DataFrame = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
            dataFrame.sort_values(template.xColumnTitle, inplace=True)
            dataFrame.dropna(inplace=True)

            if template.xColumnTitle not in dataFrame.columns:
                failedFileNames.append(file)
                continue
            elif template.yColumnTitle not in dataFrame.columns:
                failedFileNames.append(file)
                continue

            xValues = list(dataFrame[template.xColumnTitle].values)
            yValues = list(dataFrame[template.yColumnTitle].values)
            
            meta = list()
            if template.metaColumnTitle and template.metaColumnTitle in dataFrame.columns:
                meta = list(dataFrame[template.metaColumnTitle])
            
            if len(xValues) != len(yValues):
                failedFileNames.append(file)
                continue

            series.title = os.path.basename(file)
            series.xValues = xValues
            series.yValues = yValues
            if template.metaColumnTitle:
                series.metaData = meta

            series.xLabel = template.xLabel
            series.yLabel = template.yLabel

            if index < len(template.styles):
                series.style = template.styles[index]

            self.__graphView.addSeries(series)
            self.__seriesRepo.addSeries(series)

        if len(failedFileNames) > 0:
            msg: str = "The following files could not be loaded:\n"
            for fileName in failedFileNames:
                msg += fileName + "\n"

            self._showMessage(msg)
            if len(failedFileNames) == len(self.__files):
                return

        self._result = DialogResult.Ok
        self._close()

    def _selectFiles(self) -> None:
        dialog: ChooseMultipleFilesDialog = self._makeChooseMultipleFilesDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            selectedFiles: List[str] = dialog.getSelectedFiles()
            self.__files.extend(selectedFiles)
            for file in selectedFiles:
                fileName: str = os.path.basename(file)
                self._addFileToListView(fileName)

    def _removeFiles(self) -> None:
        indexes: int = list(sorted(self._getSelectedFileIndexes(), reverse=True))
        for index in indexes:
            self.__files.pop(index)
            self._removeFileFromListView(index)

    @abstractmethod
    def _addFileToListView(self, template: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeFileFromListView(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getSelectedFileIndexes(self) -> List[int]:
        raise NotImplementedError()

    @abstractmethod
    def _addTemplateToComboBox(self, template: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeTemplateFromComboBox(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getSelectedTemplateIndex(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def _makeChooseMultipleFilesDialog(self) -> ChooseMultipleFilesDialog:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()