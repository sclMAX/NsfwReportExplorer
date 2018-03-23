# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_nsfw_scann.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgNsfwScanner(object):
    def setupUi(self, dlgNsfwScanner):
        dlgNsfwScanner.setObjectName("dlgNsfwScanner")
        dlgNsfwScanner.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgNsfwScanner.resize(992, 439)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgNsfwScanner.sizePolicy().hasHeightForWidth())
        dlgNsfwScanner.setSizePolicy(sizePolicy)
        dlgNsfwScanner.setMaximumSize(QtCore.QSize(1240, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon-wifi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgNsfwScanner.setWindowIcon(icon)
        dlgNsfwScanner.setToolTip("")
        dlgNsfwScanner.setLayoutDirection(QtCore.Qt.LeftToRight)
        dlgNsfwScanner.setSizeGripEnabled(False)
        dlgNsfwScanner.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dlgNsfwScanner)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(dlgNsfwScanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnScannFolder = QtWidgets.QToolButton(self.layoutWidget)
        self.btnScannFolder.setMinimumSize(QtCore.QSize(48, 48))
        self.btnScannFolder.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/icon-searchfolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnScannFolder.setIcon(icon1)
        self.btnScannFolder.setIconSize(QtCore.QSize(48, 48))
        self.btnScannFolder.setObjectName("btnScannFolder")
        self.horizontalLayout.addWidget(self.btnScannFolder)
        self.lblScannFolder = QtWidgets.QLabel(self.layoutWidget)
        self.lblScannFolder.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lblScannFolder.setWordWrap(False)
        self.lblScannFolder.setObjectName("lblScannFolder")
        self.horizontalLayout.addWidget(self.lblScannFolder)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSave = QtWidgets.QToolButton(self.layoutWidget1)
        self.btnSave.setEnabled(False)
        self.btnSave.setMinimumSize(QtCore.QSize(48, 48))
        self.btnSave.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/icon-save-floppy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setIconSize(QtCore.QSize(48, 48))
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.lblSaveFolder = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSaveFolder.sizePolicy().hasHeightForWidth())
        self.lblSaveFolder.setSizePolicy(sizePolicy)
        self.lblSaveFolder.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lblSaveFolder.setWordWrap(False)
        self.lblSaveFolder.setObjectName("lblSaveFolder")
        self.horizontalLayout_2.addWidget(self.lblSaveFolder)
        self.horizontalLayout_3.addWidget(self.splitter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnStart = QtWidgets.QToolButton(self.groupBox)
        self.btnStart.setEnabled(False)
        self.btnStart.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/icon-acsource.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon3)
        self.btnStart.setIconSize(QtCore.QSize(48, 48))
        self.btnStart.setObjectName("btnStart")
        self.verticalLayout.addWidget(self.btnStart)
        self.btnClose = QtWidgets.QToolButton(self.groupBox)
        self.btnClose.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/icon-circledelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon4)
        self.btnClose.setIconSize(QtCore.QSize(48, 48))
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.groupBox, 0, QtCore.Qt.AlignTop)
        self.lblProgressBar = QtWidgets.QLabel(dlgNsfwScanner)
        self.lblProgressBar.setText("")
        self.lblProgressBar.setWordWrap(False)
        self.lblProgressBar.setObjectName("lblProgressBar")
        self.verticalLayout_2.addWidget(self.lblProgressBar, 0, QtCore.Qt.AlignTop)
        self.progressBar = QtWidgets.QProgressBar(dlgNsfwScanner)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar, 0, QtCore.Qt.AlignTop)
        self.txtLog = QtWidgets.QTextEdit(dlgNsfwScanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtLog.sizePolicy().hasHeightForWidth())
        self.txtLog.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(78, 154, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(78, 154, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.txtLog.setPalette(palette)
        self.txtLog.setReadOnly(True)
        self.txtLog.setObjectName("txtLog")
        self.verticalLayout_2.addWidget(self.txtLog)
        self.lblResumen = QtWidgets.QLabel(dlgNsfwScanner)
        self.lblResumen.setMaximumSize(QtCore.QSize(1240, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblResumen.setFont(font)
        self.lblResumen.setTextFormat(QtCore.Qt.AutoText)
        self.lblResumen.setAlignment(QtCore.Qt.AlignCenter)
        self.lblResumen.setWordWrap(False)
        self.lblResumen.setObjectName("lblResumen")
        self.verticalLayout_2.addWidget(self.lblResumen)
        self.lblScannFolder.setBuddy(self.btnScannFolder)
        self.lblSaveFolder.setBuddy(self.btnScannFolder)

        self.retranslateUi(dlgNsfwScanner)
        QtCore.QMetaObject.connectSlotsByName(dlgNsfwScanner)

    def retranslateUi(self, dlgNsfwScanner):
        _translate = QtCore.QCoreApplication.translate
        dlgNsfwScanner.setWindowTitle(_translate("dlgNsfwScanner", "Open Nsfw Scann v1.0 by MAX"))
        self.btnScannFolder.setToolTip(_translate("dlgNsfwScanner", "Directorio a Escanear."))
        self.lblScannFolder.setText(_translate("dlgNsfwScanner", "Seleccione el directorio a escanear!"))
        self.btnSave.setStatusTip(_translate("dlgNsfwScanner", "Directorio para guardar reporte."))
        self.lblSaveFolder.setText(_translate("dlgNsfwScanner", "Seleccione el directorio para guaradar el Reporte!"))
        self.btnStart.setStatusTip(_translate("dlgNsfwScanner", "Iniciar Escaneo."))
        self.btnClose.setStatusTip(_translate("dlgNsfwScanner", "Cerrar."))
        self.txtLog.setHtml(_translate("dlgNsfwScanner", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">Cargando....</span></p></body></html>"))
        self.lblResumen.setText(_translate("dlgNsfwScanner", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">Archivos:</span> 20000 </p></body></html>"))

