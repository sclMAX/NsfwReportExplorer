from ui_nsfw_scann import Ui_dlgNsfwScanner
from PyQt5 import QtWidgets, QtGui
from pathlib import Path
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import model_from_json
import numpy as np
from time import time, sleep
import itertools
import threading

miniatureFolder = 'miniatures'
cNormal = QtGui.QColor('green')
cDanger = QtGui.QColor('red')
cWarning = QtGui.QColor('yellow')


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


class UiScanner(QtWidgets.QDialog, Ui_dlgNsfwScanner):
    # Model Settings
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    # Time Vars
    ti = time()
    tf = time()
    # Scann Vars
    scannFolder = ''
    saveFolder = ''
    isInScann = False
    totalFiles = 0
    currentFile = 0
    imageFiles = 0
    noImageFile = 0
    filesInReport = 0
    # Report Vars
    reporte = []
    score = 0.15
    isAnimateRun = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showDetalles(False)
        self.resize(self.groupBox.size())
        # Buttons Commands
        self.btnScannFolder.clicked.connect(self.selScannFolder)
        self.btnClose.clicked.connect(self.close)
        self.btnSaveFolder.clicked.connect(self.selSaveFolder)
        self.btnStart.clicked.connect(self.startScann)
        self.btnSave.clicked.connect(self.saveReport)
        # Filtro
        self.selScore.valueChanged.connect(self.progressBarScore.setValue)
        self.progressBarScore.valueChanged.connect(self.setScore)
        self.selScore.setValue((self.score * 100))

    def showDetalles(self, isShow):
        self.progressBar.setVisible(isShow)
        self.lblScannStatus.setVisible(isShow)
        self.lblProgressBar.setVisible(isShow)
        self.txtLog.setVisible(isShow)
        self.frame.setVisible(isShow)
        self.repaint()

    def updateScannStatus(self):
        while self.isInScann:
            ct = time()
            et = ct - self.ti
            strT = '%d:%d:%d'% (abs(et / 3600),abs(et / 60), et % 60)
            fs = self.currentFile / et
            eta = (self.totalFiles - self.currentFile) / (fs if fs else 1)
            strEta = '%d:%d:%d'% (abs(eta / 3600),abs(eta / 60), eta % 60)
            
            data = (self.currentFile, self.totalFiles,
                    self.filesInReport, self.imageFiles, self.noImageFile, strT, strEta, fs)
            txt = 'A: %d de %d | Img In: %d de %d | NoImg: %d | T: %s | ETA: %s @ %.2f A/seg'
            self.lblScannStatus.setText(txt % data)
            self.lblScannStatus.repaint()
            sleep(0.1)

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

    def startScann(self):
        try:
            self.btnStart.setEnabled(False)
            self.btnScannFolder.setEnabled(False)
            self.btnSaveFolder.setEnabled(False)
            self.txtLog.clear()
            self.ti = time()
            self.showDetalles(True)
            model = self.loadModel()
            self.setLog('Buscando archivos...', cNormal, True)
            fileList = searching_all_files(self.scannFolder)
            self.totalFiles = len(fileList)
            self.setLog('%d Archivos encontrados!' %
                        (self.totalFiles), cNormal)
            self.setLog('Iniciando Escaneo!', cNormal)
            self.isInScann = True
            updateState = threading.Thread(target=self.updateScannStatus)
            updateState.start()
            msg = ''
            color = cNormal
            self.progressBar.setMaximum(self.totalFiles)
            for f in fileList:
                file_path = f
                self.currentFile += 1
                self.progressBar.setValue(self.currentFile)
                try:
                    self.setState('Escaneando: %s' % (file_path))
                    resultado = self.isPorno(model, file_path)
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
                    msg = msg + ' - ' + str(file_path)
                    self.setLog(msg, color)
        except:
            self.btnScannFolder.setEnabled(True)
            self.btnSaveFolder.setEnabled(True)
            self.btnStart.setEnabled(True)

        finally:
            self.tf = time()
            self.isInScann = False
            self.setLog('Escaneo Completo!',cNormal) 
            tir = self.filesInReport
            self.setLog('%d Imagenes en el Reporte!'%(tir), cNormal if(tir > 0) else cDanger)
            self.btnSave.setEnabled(tir >0)

    def saveReport(self):
        self.accept()

    def isPorno(self, model, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        return preds[0][1]

    def setLog(self, state, color, isAnimate=False):
        self.isAnimateRun = isAnimate
        sleep(0.11)
        if(isAnimate):
            t = threading.Thread(target=self.__animate, args=(state,))
            t.start()
        else:
            self.setState(state)
            self.txtLog.setTextColor(color)
            self.txtLog.append(state)
            self.txtLog.repaint()

    def setState(self, state):
        self.lblProgressBar.setText(state)
        self.lblProgressBar.repaint()

    def __animate(self, state):
        for c in itertools.cycle([' |', ' /', ' -', ' \\']):
            if not self.isAnimateRun:
                break
            self.setState(state + c)
            sleep(0.1)

    def loadModel(self):
        try:
            self.setLog('Cargando Modelo...', cNormal, True)
            json_file = open(self.model_file, 'r')
            loaded_model_json = json_file.read()
        except(FileNotFoundError):
            QtWidgets.QMessageBox.warning(
                self, 'ERROR: Modelo no Disponible!', 'No se encontro le modelo en: ' + self.model_file + '!')
        finally:
            if json_file:
                json_file.close()
        self.setLog('Modelo Cargado!', cNormal)
        self.setLog('Configurando Modelo...', cNormal, True)
        model = model_from_json(loaded_model_json)
        model.load_weights(self.weight_file)
        self.setLog('Modelo Configurado!', cNormal)
        return model
