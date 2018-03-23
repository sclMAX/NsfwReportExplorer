from ui_nsfw_scann import Ui_dlgNsfwScanner, QtCore, QtWidgets

class UiScanner(Ui_dlgNsfwScanner, QtWidgets.QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.dlg = Ui_dlgNsfwScanner()
        self.dlg.setupUi(parent)
        self.setWindowTitle('Open Nsfw Scanner v1.0 by MAX')

