from uimain import Ui_MainWindow, QtWidgets, QtGui
from pathlib import Path
from operator import itemgetter
from collections import OrderedDict
import subprocess, os
import json


class UiMain (Ui_MainWindow, QtWidgets.QWidget):
    __reportPath = ''
    __isChange = False
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(parent)
        self.ui.btnOpenFolder.clicked.connect(self.openFolder)
        self.ui.listReporte.itemSelectionChanged.connect(self.itemSeleccionado)
        self.ui.btnRemove.clicked.connect(self.removeItem)
        self.ui.listReporte.itemDoubleClicked.connect(self.openImage)
        self.ui.btnUnsSelect.clicked.connect(self.unSelectAll)
        self.ui.btnCloseFolder.clicked.connect(self.clearAll)
        self.ui.btnGrid.clicked.connect(self.setGrid)
        self.ui.btnList.clicked.connect(self.setList)

    def openFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Directorio del Reporte?')
        if folder:
            self.__reportPath = folder
            self.ui.lblOpenFolder.setText(str(self.__reportPath))
            self.addItems()

    def saveReport(self):
        pass

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
        self.ui.lblSelCount.setText('%d / %d'%(selCount, itemCount))

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
        imagePath = Path(item.toolTip())
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', imagePath))
        elif os.name == 'nt':
            os.startfile(imagePath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', imagePath))

    def loadReport(self, path):
        if(path):
            reporteFile = Path(path).joinpath('reporte.json')
            try:
                items = json.load(open(reporteFile))
                self.ui.lblSelCount.setText('%d / %d'%(0, len(items)))
                items = sorted(items, key=lambda item:item['score'])
                for item in items:
                    li = QtWidgets.QListWidgetItem()
                    li.setText(str(round((item['score'] * 100), 2)) + ' %')
                    icon1 = QtGui.QIcon()
                    iconFile = str(Path(self.__reportPath).joinpath(
                        'miniature', item['miniature']))
                    icon1.addPixmap(QtGui.QPixmap(iconFile),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    li.setIcon(icon1)
                    li.setToolTip(item['file_path'])
                    self.ui.listReporte.addItem(li)
                self.ui.btnCloseFolder.setEnabled(True)
            except(FileNotFoundError):
                QtWidgets.QMessageBox.warning(self, 'Reporte no encontrado!', "No se encontro el archivo [reporte.json] en el directorio!", QtWidgets.QMessageBox.Ok)        
                self.clearAll()

    def clearAll(self):
        if self.__isChange:
            pass
        self.__reportPath = ''
        self.ui.lblOpenFolder.setText(str(self.__reportPath))
        self.ui.lblSelCount.setText('0 / 0')
        self.ui.listReporte.clear()
        self.ui.btnCloseFolder.setEnabled(False)
        self.ui.btnSave.setEnabled(False)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMain(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
