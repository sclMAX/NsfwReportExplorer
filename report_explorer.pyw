from ui_main import Ui_MainWindow, QtWidgets, QtGui
from pathlib import Path
from keras.preprocessing import image
import webbrowser
import json

miniatureFolder = 'miniature'
reportFileName = 'reporte.json'


class ReporteListItem(QtWidgets.QListWidgetItem):
    id: int
    file_path: str
    score: float
    miniature: str
    basePath: str

    def __init__(self, id: int, file_path: str, score: float, miniature: str, basePath: str):
        super().__init__()
        self.id = id
        self.file_path = file_path
        self.score = score
        self.miniature = miniature
        self.basePath = basePath
        self.setup()

    def setup(self):
        self.setText(str(round((self.score * 100), 2)) + ' %')
        self.icon1 = QtGui.QIcon()
        self.iconFile = str(Path(self.basePath).joinpath(
            miniatureFolder, self.miniature))
        self.icon1.addPixmap(QtGui.QPixmap(self.iconFile),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon1)
        self.setToolTip(self.file_path)


class UiMain (QtWidgets.QMainWindow, Ui_MainWindow):
    __reportPath = ''
    saveFolder = ''
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
        self.btnSave.clicked.connect(self.btnSave_Click)
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

    def btnSave_Click(self):
        if(self.listReporte.count()):
            reporte = []
            for i in range(self.listReporte.count()):
                reporte.append({
                    'id': self.listReporte.item(i).id,
                    'file_path': self.listReporte.item(i).file_path,
                    'score': self.listReporte.item(i).score,
                    'miniature': self.listReporte.item(i).miniature
                })
            if(self.saveReport(reporte, False)):
                self.__reportPath = self.saveFolder
                self.btnSave.setEnabled(False)
                self.__isChange = False
                self.addItems()
        else:
            self.btnSave.setEnabled(False)

    def saveReport(self, reporte, isNew=False):
        if(not isNew):
            self.saveFolder = QtWidgets.QFileDialog.getExistingDirectory(
                caption='En que Directorio guardo el Reporte?')
        if(not self.saveFolder):
            return False
        try:
            self.progressBar.setVisible(True)
            self.progressBar.repaint()
            self.progressBar.setMaximum(0)
            self.lblOpenFolder.setText('Guardando reporte...')
            self.lblOpenFolder.repaint()
            newMiniatureFolder = Path(
                self.saveFolder).joinpath(miniatureFolder)
            if(not Path(newMiniatureFolder).exists()):
                try:
                    newMiniatureFolder = Path(
                        Path(self.saveFolder).joinpath(miniatureFolder)).mkdir()
                except(FileExistsError):
                    return False
            if(len(reporte)):
                reporteFile = str(
                    Path(self.saveFolder).joinpath('reporte.json'))
                json.dump(reporte, open(reporteFile, 'w'))
                totalItems = len(reporte)
                currentItem = 0
                self.progressBar.setMaximum(totalItems)
                for i in reporte:
                    currentItem += 1
                    self.lblOpenFolder.setText(
                        'Creando miniatura %d de %d' % (currentItem, totalItems))
                    self.lblOpenFolder.repaint()
                    img = image.load_img(i['file_path'], target_size=(80, 80))
                    file = str(
                        Path(newMiniatureFolder).joinpath(i['miniature']))
                    img.save(open(file, 'w'))
                    self.progressBar.setValue(currentItem)
            return True
        finally:
            self.lblOpenFolder.setText(
                'Reporte guardado en: ' + self.saveFolder)
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
                reporte = json.load(open(reporteFile))
                self.lblSelCount.setText('%d / %d' % (0, len(reporte)))
                reporte = sorted(reporte, key=lambda item: item['score'])
                self.progressBar.setMaximum(len(reporte))
                pv = 0
                self.listReporte.clear()
                for item in reporte:
                    pv += 1
                    li = ReporteListItem(
                        id=int(item['id']),
                        file_path=str(item['file_path']),
                        score=float(item['score']),
                        miniature=str(item['miniature']),
                        basePath=str(path)
                    )
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
        from nsfw_scanner import UiScanner
        self.scanner = UiScanner()
        if(self.scanner.exec_()):
            self.saveFolder = self.scanner.saveFolder
            if(self.saveReport(self.scanner.reporte, True)):
                self.__reportPath = self.scanner.saveFolder
                self.addItems()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = UiMain()
    MainWindow.show()
    sys.exit(app.exec_())
