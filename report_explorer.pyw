from ui_main import Ui_MainWindow, QtWidgets, QtGui
from nsfw_scanner import UiScanner
from pathlib import Path
from operator import itemgetter
from collections import OrderedDict
import webbrowser
import subprocess
import os
import json

miniatureFolder = 'miniature'
reportFileName = 'reporte.json'


class UiMain (Ui_MainWindow, QtWidgets.QDialog):
    __reportPath = ''
    __isChange = False

    def __init__(self, parent=None):
        super().__init__()
        # App init
        self.ui = Ui_MainWindow()
        self.ui.setupUi(parent)
        self.ui.progressBar.setVisible(False)
        # Toolbar Commands
        self.ui.btnOpenFolder.clicked.connect(self.openFolder)
        self.ui.btnRemove.clicked.connect(self.removeItem)
        self.ui.btnUnsSelect.clicked.connect(self.unSelectAll)
        self.ui.btnCloseFolder.clicked.connect(self.clearAll)
        self.ui.btnGrid.clicked.connect(self.setGrid)
        self.ui.btnList.clicked.connect(self.setList)
        self.ui.btnSave.clicked.connect(self.saveReport)
        self.ui.btnScannFolder.clicked.connect(self.scann)
        # Report comands
        self.ui.listReporte.itemSelectionChanged.connect(self.itemSeleccionado)
        self.ui.listReporte.itemDoubleClicked.connect(self.openImage)

    def openFolder(self):
        try:
            self.ui.progressBar.setVisible(True)
            self.ui.progressBar.setMaximum(0)
            folder = QtWidgets.QFileDialog.getExistingDirectory(
                caption='Directorio del Reporte?')
            if folder:
                self.__reportPath = folder
                self.ui.lblOpenFolder.setText(str(self.__reportPath))
                self.addItems()
        finally:
            self.ui.progressBar.setVisible(False)

    def saveReport(self):
        if(self.__isChange):
            try:
                self.ui.progressBar.setVisible(True)
                self.ui.progressBar.setMaximum(0)
                folder = QtWidgets.QFileDialog.getExistingDirectory(
                    caption='En que Directorio guardo el Reporte?')
                if folder:
                    self.__reportPath = folder
                    try:
                        newMiniatureFolder = Path(Path(folder).joinpath(miniatureFolder)).mkdir()
                    except(FileExistsError):
                        newMiniatureFolder = Path(folder).joinpath(miniatureFolder)

                else:
                    return

            finally:
                self.ui.progressBar.setVisible(False)

    def setList(self):
        self.ui.btnList.setEnabled(False)
        self.ui.btnGrid.setEnabled(True)
        self.ui.listReporte.setWrapping(False)

    def setGrid(self):
        self.ui.btnList.setEnabled(True)
        self.ui.btnGrid.setEnabled(False)
        self.ui.listReporte.setWrapping(True)

    def itemSeleccionado(self):
        selCount = len(self.ui.listReporte.selectedItems())
        itemCount = self.ui.listReporte.count()
        isSel = (selCount > 0)
        self.ui.btnRemove.setEnabled(isSel)
        self.ui.btnUnsSelect.setEnabled(isSel)
        self.ui.lblSelCount.setText('%d / %d' % (selCount, itemCount))

    def unSelectAll(self):
        self.ui.listReporte.clearSelection()

    def addItems(self):
        if(self.__reportPath):
            reporteFile = Path(self.__reportPath)
            self.loadReport(reporteFile)

    def removeItem(self):
        if(len(self.ui.listReporte.selectedItems())):
            for i in self.ui.listReporte.selectedItems():
                self.ui.listReporte.takeItem(self.ui.listReporte.row(i))
            self.__isChange = True
            self.ui.btnSave.setEnabled(True)

    def openImage(self, item):
        imagePath = str(Path(item.toolTip()))
        webbrowser.open_new_tab(imagePath)

    def loadReport(self, path):
        if(path):
            reporteFile = Path(path).joinpath(reportFileName)
            try:
                self.ui.progressBar.setVisible(True)
                self.ui.progressBar.setMaximum(0)
                items = json.load(open(reporteFile))
                self.ui.lblSelCount.setText('%d / %d' % (0, len(items)))
                items = sorted(items, key=lambda item: item['score'])
                self.ui.progressBar.setMaximum(len(items))
                pv = 0
                for item in items:
                    pv += 1
                    li = QtWidgets.QListWidgetItem()
                    li.setText(str(round((item['score'] * 100), 2)) + ' %')
                    icon1 = QtGui.QIcon()
                    iconFile = str(Path(self.__reportPath).joinpath(
                        miniatureFolder, item['miniature']))
                    icon1.addPixmap(QtGui.QPixmap(iconFile),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    li.setIcon(icon1)
                    li.setToolTip(item['file_path'])
                    self.ui.listReporte.addItem(li)
                    self.ui.progressBar.setValue(pv)
                self.ui.btnCloseFolder.setEnabled(True)
            except(FileNotFoundError):
                QtWidgets.QMessageBox.warning(
                    self, 'Reporte no encontrado!', "No se encontro el archivo [reporte.json] en el directorio!", QtWidgets.QMessageBox.Ok)
                self.clearAll()
            finally:
                self.ui.progressBar.setVisible(False)

    def clearAll(self):
        if self.__isChange:
            pass
        self.__reportPath = ''
        self.ui.lblOpenFolder.setText(str(self.__reportPath))
        self.ui.lblSelCount.setText('0 / 0')
        self.ui.listReporte.clear()
        self.ui.btnCloseFolder.setEnabled(False)
        self.ui.btnSave.setEnabled(False)

    def scann(self):
        self.scanner = UiScanner(self)
        self.scanner.exec_()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMain(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
