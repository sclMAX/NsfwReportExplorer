from ui_main import Ui_MainWindow, QtWidgets, QtGui
from nsfw_scanner import UiScanner
from pathlib import Path
import webbrowser
import json

miniatureFolder = 'miniature'
reportFileName = 'reporte.json'


class UiMain (QtWidgets.QMainWindow, Ui_MainWindow):
    __reportPath = ''
    __isChange = False

    def __init__(self):
        super().__init__()
        # App init
        self.setupUi(self)
        self.progressBar.setVisible(False)
        # Toolbar Commands
        self.btnOpenFolder.clicked.connect(self.openFolder)
        self.btnRemove.clicked.connect(self.removeItem)
        self.btnUnsSelect.clicked.connect(self.unSelectAll)
        self.btnCloseFolder.clicked.connect(self.clearAll)
        self.btnGrid.clicked.connect(self.setGrid)
        self.btnList.clicked.connect(self.setList)
        self.btnSave.clicked.connect(self.saveReport)
        self.btnScannFolder.clicked.connect(self.scann)
        # Report comands
        self.listReporte.itemSelectionChanged.connect(self.itemSeleccionado)
        self.listReporte.itemDoubleClicked.connect(self.openImage)

    def openFolder(self):
        try:
            self.progressBar.setVisible(True)
            self.progressBar.setMaximum(0)
            folder = QtWidgets.QFileDialog.getExistingDirectory(
                caption='Directorio del Reporte?')
            if folder:
                self.__reportPath = folder
                self.lblOpenFolder.setText(str(self.__reportPath))
                self.addItems()
        finally:
            self.progressBar.setVisible(False)

    def saveReport(self):
        if(self.__isChange):
            try:
                self.progressBar.setVisible(True)
                self.progressBar.setMaximum(0)
                folder = QtWidgets.QFileDialog.getExistingDirectory(
                    caption='En que Directorio guardo el Reporte?')
                if folder:
                    self.__reportPath = folder
                    try:
                        newMiniatureFolder = Path(
                            Path(folder).joinpath(miniatureFolder)).mkdir()
                    except(FileExistsError):
                        newMiniatureFolder = Path(
                            folder).joinpath(miniatureFolder)

                else:
                    return

            finally:
                self.progressBar.setVisible(False)

    def setList(self):
        self.btnList.setEnabled(False)
        self.btnGrid.setEnabled(True)
        self.listReporte.setWrapping(False)

    def setGrid(self):
        self.btnList.setEnabled(True)
        self.btnGrid.setEnabled(False)
        self.listReporte.setWrapping(True)

    def itemSeleccionado(self):
        selCount = len(self.listReporte.selectedItems())
        itemCount = self.listReporte.count()
        isSel = (selCount > 0)
        self.btnRemove.setEnabled(isSel)
        self.btnUnsSelect.setEnabled(isSel)
        self.lblSelCount.setText('%d / %d' % (selCount, itemCount))

    def unSelectAll(self):
        self.listReporte.clearSelection()

    def addItems(self):
        if(self.__reportPath):
            reporteFile = Path(self.__reportPath)
            self.loadReport(reporteFile)

    def removeItem(self):
        if(len(self.listReporte.selectedItems())):
            for i in self.listReporte.selectedItems():
                self.listReporte.takeItem(self.listReporte.row(i))
            self.__isChange = True
            self.btnSave.setEnabled(True)

    def openImage(self, item):
        imagePath = str(Path(item.toolTip()))
        webbrowser.open_new_tab(imagePath)

    def loadReport(self, path):
        if(path):
            reporteFile = Path(path).joinpath(reportFileName)
            try:
                self.progressBar.setVisible(True)
                self.progressBar.setMaximum(0)
                items = json.load(open(reporteFile))
                self.lblSelCount.setText('%d / %d' % (0, len(items)))
                items = sorted(items, key=lambda item: item['score'])
                self.progressBar.setMaximum(len(items))
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
                    self.listReporte.addItem(li)
                    self.progressBar.setValue(pv)
                self.btnCloseFolder.setEnabled(True)
            except(FileNotFoundError):
                QtWidgets.QMessageBox.warning(
                    self, 'Reporte no encontrado!', "No se encontro el archivo [reporte.json] en el directorio!", QtWidgets.QMessageBox.Ok)
                self.clearAll()
            finally:
                self.progressBar.setVisible(False)

    def clearAll(self):
        if self.__isChange:
            pass
        self.__reportPath = ''
        self.lblOpenFolder.setText(str(self.__reportPath))
        self.lblSelCount.setText('0 / 0')
        self.listReporte.clear()
        self.btnCloseFolder.setEnabled(False)
        self.btnSave.setEnabled(False)

    def scann(self):
        self.scanner = UiScanner()
        resultado = self.scanner.exec_()
        print(resultado)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = UiMain()
    MainWindow.show()
    sys.exit(app.exec_())
