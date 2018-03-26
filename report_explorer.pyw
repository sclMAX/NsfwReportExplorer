from ui_main import Ui_MainWindow, QtWidgets, QtGui, QtCore
from pathlib import Path
from keras.preprocessing import image
import webbrowser
import json

miniatureFolder = 'miniature'
reportFileName = 'reporte.json'


class SaveReporte(QtCore.QThread):
    reporte = []
    saveFolder = ''
    # Signals
    result = QtCore.pyqtSignal(bool)
    progressSetup = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    state = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, reporte=[], saveFolder=''):
        super().__init__(parent)
        self.reporte = reporte
        self.saveFolder = saveFolder

    def run(self):
        newMiniatureFolder = Path(self.saveFolder).joinpath(miniatureFolder)
        if(not Path(newMiniatureFolder).exists()):
            try:
                Path(newMiniatureFolder).mkdir()
            except(FileExistsError):
                self.state.emit('Error al crear el directorio de miniaturas!')
                self.result.emit(False)
                return
        if(len(self.reporte)):
            reporteFile = str(
                Path(self.saveFolder).joinpath('reporte.json'))
            self.state.emit('Guradando reporte...')
            json.dump(self.reporte, open(reporteFile, 'w'))
            totalItems = len(self.reporte)
            currentItem = 0
            self.progressSetup.emit(totalItems)
            for i in self.reporte:
                currentItem += 1
                self.state.emit('Creando miniatura %d de %d' %
                                (currentItem, totalItems))
                try:
                    img = image.load_img(i['file_path'], target_size=(80, 80))
                    file = str(
                        Path(newMiniatureFolder).joinpath(i['miniature']))
                    img.save(open(file, 'w'))
                except:
                    continue
                self.progress.emit(currentItem)
            self.result.emit(True)
            return


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
            self.saveReport(reporte, False)
        else:
            self.btnSave.setEnabled(False)

    def saveReportFinish(self, result):
        if(result):
            self.progressBar.setVisible(False)
            self.setState('Reporte guardado en: ' + self.saveFolder)
            self.__reportPath = self.saveFolder
            self.btnSave.setEnabled(False)
            self.__isChange = False
            self.addItems()

    def setState(self, msg):
        self.lblOpenFolder.setText(msg)
        self.lblOpenFolder.repaint()

    def saveReport(self, reporte, isNew=False):
        if(not isNew):
            self.saveFolder = QtWidgets.QFileDialog.getExistingDirectory(
                caption='En que Directorio guardo el Reporte?')
        if(not self.saveFolder):
            return False
        self.progressBar.setVisible(True)
        self.progressBar.repaint()
        self.progressBar.setMaximum(0)
        self.saveTask = SaveReporte(
            self, reporte=reporte, saveFolder=self.saveFolder)
        self.saveTask.state.connect(self.setState)
        self.saveTask.progressSetup.connect(self.progressBar.setMaximum)
        self.saveTask.progress.connect(self.progressBar.setValue)
        self.saveTask.result.connect(self.saveReportFinish)
        self.saveTask.start()

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
                self.__reportPath = self.saveFolder
                self.addItems()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = UiMain()
    MainWindow.show()
    sys.exit(app.exec_())
