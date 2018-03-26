from ui_nsfw_scann import Ui_dlgNsfwScanner
from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import model_from_json
from keras import backend as K
import numpy as np
from time import time, sleep
import itertools

miniatureFolder = 'miniatures'
cNormal = QtGui.QColor('green')
cDanger = QtGui.QColor('red')
cWarning = QtGui.QColor('silver')


def searching_all_files(path: Path):
    dirpath = Path(path)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(x))
    return file_list


class Loading(QtCore.QThread):
    loading = QtCore.pyqtSignal(str)
    isStop = False

    def __init__(self, parent=None, text='Loading...'):
        super().__init__(parent)
        self.msg = text

    @QtCore.pyqtSlot()
    def stop(self):
        self.isStop = True
        self.exit()

    def run(self):
        for c in itertools.cycle([' |', ' /', ' -', ' \\']):
            if not self.isStop:
                break
            self.loading.emit(self.msg + c)
            sleep(0.1)


class NsfwSacnner(QtCore.QThread):
    # Model Settings
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    model = None
    # Time Vars
    ti = time()
    tf = time()
    # Scann Vars
    scannFolder = str
    totalFiles = 0
    currentFile = 0
    imageFiles = 0
    noImageFile = 0
    filesInReport = 0
    # Reporte Vars
    reporte = []
    score = 0.15
    # Signals
    log = QtCore.pyqtSignal(str, QtGui.QColor)
    finish = QtCore.pyqtSignal(object)
    state = QtCore.pyqtSignal(str)
    status = QtCore.pyqtSignal(str)
    progressSetup = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    # Slots
    isCanceled = False

    def __init__(self, parent=None, scannFolder='', score=0.15):
        super().__init__(parent)
        self.thparent = parent
        self.scannFolder = scannFolder
        self.score = score

    def loadading(self, msg, idx):
        chars = [' |', ' /', ' -', ' \\']
        if not(idx < len(chars)):
            idx = 0
        self.state.emit(self.msg + chars[idx])
        return idx

    def loadModel(self):
        try:
            K.clear_session()
            msg = 'Cargando Modelo...'
            self.log.emit(msg, cNormal)
            json_file = open(self.model_file, 'r')
            loaded_model_json = json_file.read()
            msg = 'Configurando Modelo...'
            self.log.emit('Modelo Cargado!', cNormal)
            self.log.emit(msg, cNormal)
            model = model_from_json(loaded_model_json)
            model.load_weights(self.weight_file)
            self.log.emit('Modelo Configurado!', cNormal)
            return model
        except(FileNotFoundError):
            QtWidgets.QMessageBox.warning(
                self, 'ERROR: Modelo no Disponible!', 'No se encontro le modelo en: ' + self.model_file + '!')
            return None
        finally:
            if json_file:
                json_file.close()

    def isPorno(self, model, img_path):
        try:
            img = image.load_img(img_path, target_size=(224, 224))
        except(SyntaxError):
            raise ValueError()
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        return preds[0][1]

    def emitStatus(self):
        ct = time()
        et = ct - self.ti
        strT = '%d:%d:%d' % (abs(et / 3600), abs(et / 60), et % 60)
        fs = self.currentFile / et
        eta = (self.totalFiles - self.currentFile) / (fs if fs else 1)
        strEta = '%d:%d:%d' % (abs(eta / 3600), abs(eta / 60), eta % 60)
        data = (self.currentFile, self.totalFiles, self.filesInReport,
                self.imageFiles, self.noImageFile, strT, strEta, fs)
        txt = 'A: %d de %d | Img In: %d de %d | NoImg: %d | T: %s | ETA: %s @ %.2f A/seg' % data
        self.status.emit(txt)

    @QtCore.pyqtSlot()
    def cancel(self):
        self.isCanceled = True

    def run(self):
        self.ti = time()
        if(not self.model):
            self.model = self.loadModel()
        if self.model:
            self.log.emit('Buscando archivos...', cNormal)
            fileList = searching_all_files(self.scannFolder)
            self.totalFiles = len(fileList)
            self.log.emit('%d Archivos encontrados!' %
                          (self.totalFiles), cNormal)
            self.log.emit('Iniciando Escaneo!', cNormal)
            self.progressSetup.emit(self.totalFiles)
            msg = ''
            color = cNormal
            for f in fileList:
                if(self.isCanceled):
                    break
                file_path = f
                self.currentFile += 1
                self.progress.emit(self.currentFile)
                try:
                    self.state.emit('Escaneando: %s' % (file_path))
                    resultado = self.isPorno(self.model, file_path)
                    self.imageFiles += 1
                    if(resultado >= self.score):
                        self.filesInReport += 1
                        msg = 'SI: %3.2f %s' % (round(resultado * 100, 2), '%')
                        color = cNormal
                        minFile = ('P%3d_mini_%4d.jpg' % (
                            (resultado * 100), self.filesInReport)).replace(' ', '0')
                        self.reporte.append({
                            'id': self.filesInReport,
                            'file_path': str(file_path),
                            'score': float(round(resultado, 4)),
                            'miniature': minFile
                        })
                    else:
                        msg = 'NO: %3.2f %s' % (round(resultado * 100, 2), '%')
                        color = cWarning
                except(OSError, ValueError):
                    self.noImageFile += 1
                    msg = 'NO IMAGEN'
                    color = cDanger
                    continue
                finally:
                    self.emitStatus()
                    msg = msg + ' - ' + str(file_path)
                    self.log.emit(msg, color)
            self.tf = time()
            self.log.emit('Escaneo Completo!', cNormal)
            tir = self.filesInReport
            self.log.emit('%d Imagenes en el Reporte!' %
                          (tir), cNormal if(tir > 0) else cDanger)
            self.finish.emit(self.reporte if(tir > 9)else [])
            return
        else:
            self.finish.emit(None)
            return


class UiScanner(QtWidgets.QDialog, Ui_dlgNsfwScanner):

    # Scann Vars
    scannFolder = ''
    saveFolder = ''
    isScanning = False
    # Report Vars
    reporte = []
    score = 0.15

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showDetalles(False)
        self.resize(self.groupBox.size())
        # Buttons Commands
        self.btnScannFolder.clicked.connect(self.selScannFolder)
        self.btnClose.clicked.connect(self.btnClose_Click)
        self.btnSaveFolder.clicked.connect(self.selSaveFolder)
        self.btnStart.clicked.connect(self.btnStart_Click)
        self.btnSave.clicked.connect(self.saveReport)
        # Filtro
        self.selScore.valueChanged.connect(self.progressBarScore.setValue)
        self.progressBarScore.valueChanged.connect(self.setScore)
        self.selScore.setValue((self.score * 100))

    def btnClose_Click(self):
        if(self.isScanning):
            if(self.scann.isRunning):
                q = QtWidgets.QMessageBox.question(
                    self, 'Escaneo en Proceso!', 'Desa salir de todos modos?')
                if(q == QtWidgets.QMessageBox.No):
                    return
                self.scann.cancel()
                self.scann.wait()
        self.close()

    def showDetalles(self, isShow):
        self.progressBar.setVisible(isShow)
        self.lblScannStatus.setVisible(isShow)
        self.lblProgressBar.setVisible(isShow)
        self.txtLog.setVisible(isShow)
        self.frame.setVisible(isShow)
        self.repaint()

    def updateScannStatus(self, txt: str):
        self.lblScannStatus.setText(txt)
        self.lblScannStatus.repaint()

    def setScore(self, value):
        self.score = (value / 100)

    def selScannFolder(self):
        self.scannFolder = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Directorio a Escanear?')
        if self.scannFolder:
            self.lblScannFolder.setText(str(self.scannFolder))
            self.btnSaveFolder.setEnabled(True)
        else:
            self.lblScannFolder.setText('Seleccione el directorio a escanear!')
            self.btnSaveFolder.setEnabled(False)

    def selSaveFolder(self):
        self.saveFolder = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Donde guardo el Reporte?')
        if self.saveFolder:
            self.lblSaveFolder.setText(str(self.saveFolder))
            self.btnStart.setEnabled(True)
        else:
            self.lblSaveFolder.setText('Directorio para guardar reporte.')
            self.btnStart.setEnabled(False)

    def btnStart_Click(self):
        try:
            self.showDetalles(True)
            self.btnStart.setEnabled(False)
            self.btnScannFolder.setEnabled(False)
            self.btnSaveFolder.setEnabled(False)
            self.txtLog.clear()
            self.scann = NsfwSacnner(
                parent=self,
                scannFolder=self.scannFolder,
                score=self.score)
            self.scann.finish.connect(self.scannFinish)
            self.scann.log.connect(self.setLog)
            self.scann.state.connect(self.setState)
            self.scann.status.connect(self.updateScannStatus)
            self.scann.progressSetup.connect(self.progressBar.setMaximum)
            self.scann.progress.connect(self.progressBar.setValue)
            self.scann.start()
            self.isScanning = True
        except:
            self.btnScannFolder.setEnabled(True)
            self.btnSaveFolder.setEnabled(True)
            self.btnStart.setEnabled(True)

    def scannFinish(self, reporte):
        self.isScanning = False
        if(reporte):
            self.reporte = reporte
            self.btnSave.setEnabled(True)
        else:
            if(self.scann.isRunning):
                self.scann.exit()
                self.scann.wait()
            self.btnSave.setEnabled(False)

    def saveReport(self):
        logFile = Path(self.saveFolder).joinpath('log.txt')
        with open(logFile, 'w') as log:
             log.write(str(self.txtLog.toPlainText()))
        self.accept()

    def setLog(self, state, color, isAnimate=False):
        self.setState(state)
        self.txtLog.setTextColor(color)
        self.txtLog.append(state)
        self.txtLog.repaint()

    def setState(self, state):
        self.lblProgressBar.setText(state)
        self.lblProgressBar.repaint()
