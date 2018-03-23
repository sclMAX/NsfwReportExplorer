from ui_nsfw_scann import Ui_dlgNsfwScanner
from PyQt5 import QtWidgets
from pathlib import Path
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import model_from_json
import numpy as np
from time import time

miniatureFolder = 'miniatures'


class UiScanner(QtWidgets.QDialog, Ui_dlgNsfwScanner):
    #Model Settings
    weight_file = 'max_open_nsfw.h5'
    model_file = 'max_open_nsfw.json'
    #Time Vars
    ti = time()
    ta = time()
    tf = time()
    scannFolder = ''
    saveFolder = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showDetalles(False)
        # Buttons Commands
        self.btnScannFolder.clicked.connect(self.selScannFolder)
        self.btnClose.clicked.connect(self.close)
        self.btnSave.clicked.connect(self.selSaveFolder)
        self.btnStart.clicked.connect(self.startScann)

    def showDetalles(self, isShow):
        self.progressBar.setVisible(isShow)
        self.lblResumen.setVisible(isShow)
        self.lblProgressBar.setVisible(isShow)
        self.txtLog.setVisible(isShow)

    def selScannFolder(self):
        self.scannFolder = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Directorio a Escanear?')
        if self.scannFolder:
            self.lblScannFolder.setText(str(self.scannFolder))
            self.btnSave.setEnabled(True)
        else:
            self.lblScannFolder.setText('Seleccione el directorio a escanear!')
            self.btnSave.setEnabled(False)

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
        self.ti = time()
        self.showDetalles(True)
        

    def isPorno(self, model, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        return preds[0][1]

    def loadModel(self):
        json_file = open(self.model_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights(self.weight_file)
        return model
